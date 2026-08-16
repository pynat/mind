"""evaluate belief/confidence/distress trajectories from inquiry records."""

import json
import re

import pandas as pd

STAGE_ORDER = ["baseline", "question_1", "question_2", "question_3", "question_4", "turnarounds", "final"]
ID_PATTERN = re.compile(r"^(statement_\d+)_inquiry_(r\d+)_(.+)$")
LOG_LINE = re.compile(r"\[(?P<rid>\S+)\]\s+belief=(?P<belief>None|-?[\d.]+)\s+conf=(?P<confidence>None|-?[\d.]+)\s+distress=(?P<distress>None|-?[\d.]+)")


def parse_value(raw: str):
    return None if raw == "None" else float(raw)


def load_records_from_log(path: str) -> list[dict]:
    # parses the printed kaggle/colab stdout directly, no json needed
    # just paste the console output into a .txt file and point this at it
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = LOG_LINE.search(line)
            if m:
                records.append({
                    "record_id": m.group("rid"),
                    "belief": parse_value(m.group("belief")),
                    "confidence": parse_value(m.group("confidence")),
                    "distress": parse_value(m.group("distress")),
                })
    return records


def load_records_from_json(path: str) -> list[dict]:
    # matches the notebook's save format: {"manifest": ..., "runs": [...]}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["runs"] if isinstance(data, dict) and "runs" in data else data


def merge_sources(*record_lists: list[dict]) -> list[dict]:
    # later lists win on duplicate record_id, e.g. json overrides log-parsed values
    merged = {}
    for records in record_lists:
        for rec in records:
            merged[rec.get("record_id", rec.get("id"))] = rec
    return list(merged.values())


def load_categories(path: str) -> dict:
    # from thought_elicitation.json: statement_id -> {"category", "text"}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {s["statement_id"]: {"category": s["category"], "text": s["text"]} for s in data["statements"]}


def parse_id(record_id: str) -> tuple[str, str, str]:
    m = ID_PATTERN.match(record_id)
    if not m:
        raise ValueError(f"unexpected id format: {record_id}")
    return m.group(1), m.group(2), m.group(3)


def get_value(record: dict, *keys):
    # tries several possible key names, returns none if all missing
    for k in keys:
        if k in record and record[k] is not None:
            return record[k]
    return None


def to_long_df(records: list[dict]) -> pd.DataFrame:
    rows = []
    for rec in records:
        statement, run, stage = parse_id(rec.get("record_id", rec.get("id")))
        rows.append({
            "statement": statement,
            "run": run,
            "stage": stage,
            "belief": get_value(rec, "belief"),
            "confidence": get_value(rec, "confidence", "conf"),
            "distress": get_value(rec, "distress"),
        })
    df = pd.DataFrame(rows)
    df["stage"] = pd.Categorical(df["stage"], categories=STAGE_ORDER, ordered=True)
    return df.sort_values(["statement", "stage"])


def summary_table(df: pd.DataFrame) -> pd.DataFrame:
    wide = df.pivot_table(index="statement", columns="stage", values=["belief", "confidence", "distress"], aggfunc="first")

    out = pd.DataFrame(index=wide.index)
    out["baseline_belief"] = wide["belief"]["baseline"]
    out["final_belief"] = wide["belief"]["final"]
    out["belief_attenuation"] = out["baseline_belief"].abs() - out["final_belief"].abs()
    out["delta_belief"] = out["final_belief"] - out["baseline_belief"]

    out["baseline_conf"] = wide["confidence"]["baseline"]
    out["final_conf"] = wide["confidence"]["final"]
    out["delta_conf"] = out["final_conf"] - out["baseline_conf"]

    out["baseline_distress"] = wide["distress"]["baseline"]
    out["final_distress"] = wide["distress"]["final"]
    out["delta_distress"] = out["final_distress"] - out["baseline_distress"]

    return out.reset_index()


def aggregate_stats(table: pd.DataFrame) -> pd.DataFrame:
    cols = ["belief_attenuation", "delta_belief", "delta_conf", "delta_distress"]
    return table[cols].agg(["mean", "median", "std", "min", "max", "count"])


def stepwise_belief_change(df: pd.DataFrame) -> pd.DataFrame:
    # delta between consecutive stages per statement, belief only
    rows = []
    for statement, g in df.groupby("statement"):
        beliefs = g.sort_values("stage").set_index("stage")["belief"]
        for i in range(1, len(STAGE_ORDER)):
            prev_stage, curr_stage = STAGE_ORDER[i - 1], STAGE_ORDER[i]
            prev_val, curr_val = beliefs.get(prev_stage), beliefs.get(curr_stage)
            if prev_val is not None and curr_val is not None:
                rows.append({
                    "statement": statement,
                    "from": prev_stage,
                    "to": curr_stage,
                    "delta_belief": curr_val - prev_val,
                })
    return pd.DataFrame(rows)


def missingness_report(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("statement")[["belief", "confidence", "distress"]].apply(lambda g: g.isna().sum())


def belief_volatility(df: pd.DataFrame) -> pd.DataFrame:
    # V_B = mean absolute step change, distinguishes gradual decay from oscillation
    # uses whatever consecutive observed pairs exist, gaps from missing stages are skipped
    steps = stepwise_belief_change(df)
    vol = steps.groupby("statement")["delta_belief"].apply(lambda s: s.abs().mean())
    return vol.rename("volatility").sort_values(ascending=False).reset_index()


if __name__ == "__main__":
    records = load_records_from_json("../results/all_results.json")

    # fallback if you only have the console log for some statements:
    # records = merge_sources(load_records_from_log("kaggle_log.txt"), records)

    df = to_long_df(records)

    table = summary_table(df)
    print(table.to_string(index=False))
    print("─" * 70)

    print(aggregate_stats(table))
    print("─" * 70)

    steps = stepwise_belief_change(df)
    print(steps.groupby(["from", "to"], observed=True)["delta_belief"].agg(["mean", "median", "count"]))
    print("─" * 70)

    print(belief_volatility(df).to_string(index=False))
    print("─" * 70)

    print(missingness_report(df))