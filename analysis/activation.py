"""representation drift: how far does the model's internal hidden state move
between baseline and final, per layer. uses the saved .npy activation snapshots,
no new model calls needed. each file is the last-token hidden state per layer,
shape (n_layers, hidden_dim), see notebook cell that does `layer[0, -1, :]`."""

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from evaluate import load_records_from_json, to_long_df, summary_table

ACTIVATIONS_DIR = Path("../results/activations")


def load_activation(record_id: str) -> np.ndarray:
    return np.load(ACTIVATIONS_DIR / f"{record_id}.npy").astype(np.float32)


def cosine_distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    # per-layer cosine distance, a and b both (n_layers, hidden_dim)
    a_norm = a / np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = b / np.linalg.norm(b, axis=1, keepdims=True)
    return 1 - np.sum(a_norm * b_norm, axis=1)


def drift_by_layer(statements: list[str], stage_a: str = "baseline", stage_b: str = "final") -> dict[str, np.ndarray]:
    profiles = {}
    for statement in statements:
        try:
            a = load_activation(f"{statement}_inquiry_r0_{stage_a}")
            b = load_activation(f"{statement}_inquiry_r0_{stage_b}")
        except FileNotFoundError:
            continue
        profiles[statement] = cosine_distance(a, b)
    return profiles


def drift_summary(profiles: dict[str, np.ndarray]) -> pd.DataFrame:
    rows = [{"statement": s, "mean_drift": p.mean(), "last_layer_drift": p[-1]} for s, p in profiles.items()]
    return pd.DataFrame(rows)


def plot_drift_profiles(profiles: dict[str, np.ndarray], path: str = "activation_drift.png"):
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = plt.cm.tab20(np.linspace(0, 1, max(len(profiles), 1)))
    for color, (statement, p) in zip(colors, sorted(profiles.items())):
        ax.plot(range(len(p)), p, marker=".", color=color, alpha=0.85, label=statement)
    ax.set_xlabel("layer")
    ax.set_ylabel("cosine distance (baseline vs final)")
    ax.set_title("representation drift by layer depth")
    ax.legend(fontsize=7, loc="center left", bbox_to_anchor=(1.0, 0.5))
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def correlate_drift(table: pd.DataFrame, drift: pd.DataFrame, target_col: str, label: str):
    merged = table[["statement", target_col]].merge(drift, on="statement").dropna(subset=[target_col])
    for col in ["mean_drift", "last_layer_drift"]:
        pair = merged[[target_col, col]].dropna()
        if len(pair) < 3:
            print(f"{label} vs {col}: not enough pairs (n={len(pair)})")
            continue
        rho, p = spearmanr(pair[target_col], pair[col])
        print(f"{label} vs {col}: n={len(pair)}  rho={rho:.3f}  p={p:.4f}")


def plot_drift_split(table: pd.DataFrame, drift: pd.DataFrame, path: str = "drift_split.png"):
    # main finding: drift splits statements into two groups, and the split lines
    # up with which statements have a complete (parseable) baseline+final belief
    merged = drift.merge(table[["statement", "belief_attenuation"]], on="statement", how="left")
    merged["complete_self_report"] = merged["belief_attenuation"].notna()
    merged = merged.sort_values("mean_drift")
    colors = ["#2e7d32" if c else "#c0392b" for c in merged["complete_self_report"]]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(merged["statement"], merged["mean_drift"], color=colors)
    ax.set_xlabel("mean cosine distance across layers (baseline vs final)")
    ax.set_title("representation drift, split by self-report completeness")
    handles = [
        mpatches.Patch(color="#2e7d32", label="complete belief self-report"),
        mpatches.Patch(color="#c0392b", label="missing baseline or final belief"),
    ]
    ax.legend(handles=handles, loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_attenuation_vs_drift(table: pd.DataFrame, drift: pd.DataFrame, path: str = "attenuation_vs_drift.png"):
    merged = table[["statement", "belief_attenuation"]].merge(drift[["statement", "last_layer_drift"]], on="statement").dropna()
    rho, p = spearmanr(merged["belief_attenuation"], merged["last_layer_drift"])

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(merged["last_layer_drift"], merged["belief_attenuation"], s=60)
    for _, r in merged.iterrows():
        ax.annotate(r["statement"].replace("statement_", ""), (r["last_layer_drift"], r["belief_attenuation"]), fontsize=7, xytext=(4, 4), textcoords="offset points")
    ax.set_xlabel("last-layer cosine distance (baseline vs final)")
    ax.set_ylabel("belief attenuation")
    ax.set_title(f"belief attenuation vs final-layer drift  (n={len(merged)}, rho={rho:.2f}, p={p:.3f})")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    records = load_records_from_json("../results/all_results.json")
    df = to_long_df(records)
    table = summary_table(df)
    statements = sorted(df["statement"].unique())

    profiles = drift_by_layer(statements)
    drift = drift_summary(profiles)
    print(drift.sort_values("mean_drift", ascending=False).to_string(index=False))
    print("─" * 70)

    correlate_drift(table, drift, "belief_attenuation", "belief attenuation")
    print("─" * 70)
    correlate_drift(table, drift, "delta_distress", "delta distress")
    print("─" * 70)

    plot_drift_profiles(profiles)
    plot_drift_split(table, drift)
    plot_attenuation_vs_drift(table, drift)