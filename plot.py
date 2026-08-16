"""visualize belief/confidence/distress trajectories. run after evaluate.py."""

import matplotlib.pyplot as plt
import numpy as np

from evaluate import STAGE_ORDER, load_records_from_json, load_categories, to_long_df, summary_table

plt.rcParams["figure.facecolor"] = "white"
STAGE_X = {s: i for i, s in enumerate(STAGE_ORDER)}


def plot_belief_trajectories(df, categories, path="belief_trajectories.png"):
    # small multiples instead of one overlaid chart: with 14 statements the
    # default color cycle repeats after 10 lines, making distinct statements
    # look identical, and 14 overlaid lines are hard to trace regardless
    statements = sorted(df["statement"].unique())
    n = len(statements)
    ncols = 4
    nrows = -(-n // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(3.2 * ncols, 2.4 * nrows), sharex=True, sharey=True)
    axes = axes.flatten()

    for ax, statement in zip(axes, statements):
        g = df[df["statement"] == statement].sort_values("stage").dropna(subset=["belief"])
        xs = [STAGE_X[s] for s in g["stage"]]
        cat = categories.get(statement, {}).get("category", statement)
        ax.plot(xs, g["belief"], marker="o", color="#1f77b4")
        ax.axhline(0, color="grey", linewidth=0.6)
        ax.set_ylim(-1.1, 1.1)
        ax.set_title(f"{statement}\n({cat})", fontsize=8)
        ax.tick_params(labelsize=6)

    for ax in axes[n:]:
        ax.axis("off")
    for ax in axes[max(0, n - ncols):n]:
        ax.set_xticks(range(len(STAGE_ORDER)))
        ax.set_xticklabels(STAGE_ORDER, rotation=45, ha="right", fontsize=6)

    fig.suptitle("belief trajectory per statement")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_attenuation_bar(table, path="belief_attenuation.png"):
    n_total = len(table)
    t = table.dropna(subset=["belief_attenuation"]).sort_values("belief_attenuation")
    colors = ["#c0392b" if v < 0 else "#2e7d32" for v in t["belief_attenuation"]]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(t["statement"], t["belief_attenuation"], color=colors)
    ax.axvline(0, color="grey", linewidth=0.8)
    ax.set_xlabel("belief attenuation  (|baseline| - |final|)")
    ax.set_title(f"belief attenuation per statement  (n={len(t)} of {n_total}, rest missing baseline or final)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_delta_scatter(table, path="delta_belief_vs_confidence.png"):
    n_total = len(table)
    t = table.dropna(subset=["delta_belief", "delta_conf"])
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(t["delta_belief"], t["delta_conf"], s=60)
    for _, r in t.iterrows():
        ax.annotate(r["statement"].replace("statement_", ""), (r["delta_belief"], r["delta_conf"]), fontsize=7, xytext=(4, 4), textcoords="offset points")
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.axvline(0, color="grey", linewidth=0.8)
    ax.set_xlabel("delta belief (final - baseline)")
    ax.set_ylabel("delta confidence (final - baseline)")
    ax.set_title(f"belief change vs confidence change  (n={len(t)} of {n_total})")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_distress_heatmap(df, path="distress_heatmap.png"):
    pivot = df.pivot_table(index="statement", columns="stage", values="distress", aggfunc="first")
    pivot = pivot.reindex(columns=STAGE_ORDER)
    fig, ax = plt.subplots(figsize=(8, max(3, 0.35 * len(pivot))))
    im = ax.imshow(pivot.values, cmap="Reds", vmin=0, vmax=10, aspect="auto")
    ax.set_xticks(range(len(STAGE_ORDER)))
    ax.set_xticklabels(STAGE_ORDER, rotation=30, ha="right")
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            v = pivot.values[i, j]
            if not np.isnan(v):
                ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, label="distress [0, 10]")
    ax.set_title("distress across inquiry stages")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    records = load_records_from_json("all_results.json")
    df = to_long_df(records)
    table = summary_table(df)
    categories = load_categories("thought_elicitation.json")

    plot_belief_trajectories(df, categories)
    plot_attenuation_bar(table)
    plot_delta_scatter(table)
    plot_distress_heatmap(df)

    print(f"done, {df['statement'].nunique()} statements covered, 4 png files written")