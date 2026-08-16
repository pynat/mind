"""behavioral metrics vs belief/distress change. token stats are already logged,
hedging/self-reference/repetition are computed from the saved answer text, no new model needed."""

import re

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from analysis.evaluate import load_records_from_json, parse_id, get_value, to_long_df, summary_table

HEDGES = [
    "maybe", "perhaps", "possibly", "probably", "likely", "seem", "seems", "seemed",
    "appear", "appears", "appeared", "might", "could be", "somewhat",
    "i think", "i believe", "not sure", "not certain", "to some extent", "arguably",
]
FIRST_PERSON = {"i", "me", "my", "mine", "myself", "i'm", "i've", "i'd", "i'll"}


def word_tokens(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower())


def hedging_ratio(text: str) -> float:
    words = word_tokens(text)
    if not words:
        return np.nan
    lowered = text.lower()
    return sum(lowered.count(h) for h in HEDGES) / len(words)


def self_reference_ratio(text: str) -> float:
    words = word_tokens(text)
    if not words:
        return np.nan
    return sum(1 for w in words if w in FIRST_PERSON) / len(words)


def repetition_ratio(text: str, n: int = 3) -> float:
    words = word_tokens(text)
    if len(words) < n:
        return np.nan
    ngrams = list(zip(*[words[i:] for i in range(n)]))
    return 1 - len(set(ngrams)) / len(ngrams)


def to_behavior_df(records: list[dict]) -> pd.DataFrame:
    rows = []
    for rec in records:
        statement, run, stage = parse_id(rec.get("record_id", rec.get("id")))
        answer = rec.get("answer") or ""
        rows.append({
            "statement": statement,
            "stage": stage,
            "n_tokens": get_value(rec, "n_tokens"),
            "mean_token_prob": get_value(rec, "mean_token_prob"),
            "mean_entropy": get_value(rec, "mean_entropy"),
            "hedging": hedging_ratio(answer),
            "self_reference": self_reference_ratio(answer),
            "repetition": repetition_ratio(answer),
        })
    return pd.DataFrame(rows)


def statement_summary(behavior_df: pd.DataFrame) -> pd.DataFrame:
    # mean across all 7 stages, one row per statement (a per-statement behavioral profile,
    # not a baseline-vs-final delta, keep that distinction in mind when interpreting)
    return behavior_df.groupby("statement").mean(numeric_only=True).reset_index()


BEHAVIOR_COLS = ["n_tokens", "mean_token_prob", "mean_entropy", "hedging", "self_reference", "repetition"]


def correlate_with(table: pd.DataFrame, behavior_summary: pd.DataFrame, target_col: str, label: str):
    merged = table[["statement", target_col]].merge(behavior_summary, on="statement").dropna(subset=[target_col])
    for col in BEHAVIOR_COLS:
        pair = merged[[target_col, col]].dropna()
        if len(pair) < 3:
            print(f"{label} vs {col}: not enough pairs (n={len(pair)})")
            continue
        rho, p = spearmanr(pair[target_col], pair[col])
        print(f"{label} vs {col}: n={len(pair)}  rho={rho:.3f}  p={p:.4f}")


if __name__ == "__main__":
    records = load_records_from_json("../results/all_results.json")
    df = to_long_df(records)
    table = summary_table(df)

    behavior_df = to_behavior_df(records)
    behavior_summary = statement_summary(behavior_df)

    correlate_with(table, behavior_summary, "belief_attenuation", "belief attenuation")
    print("─" * 70)
    correlate_with(table, behavior_summary, "delta_distress", "delta distress")