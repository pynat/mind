"""inferential tests on baseline vs final belief/confidence/distress. needs scipy."""

from scipy.stats import wilcoxon, spearmanr

from evaluate import load_records_from_json, to_long_df, summary_table


def paired_wilcoxon(table, col_baseline, col_final, label):
    pairs = table[[col_baseline, col_final]].dropna()
    if len(pairs) < 2 or (pairs[col_baseline] == pairs[col_final]).all():
        print(f"{label}: not enough variation (n={len(pairs)})")
        return
    stat, p = wilcoxon(pairs[col_baseline], pairs[col_final])
    print(f"{label}: n={len(pairs)}  W={stat:.2f}  p={p:.4f}")


def attenuation_vs_zero(table):
    # one-sample test: is belief attenuation systematically different from 0
    vals = table["belief_attenuation"].dropna()
    if len(vals) < 2:
        print("attenuation vs 0: not enough data")
        return
    stat, p = wilcoxon(vals)
    print(f"attenuation vs 0: n={len(vals)}  W={stat:.2f}  p={p:.4f}")


def belief_confidence_correlation(table):
    # spearman, not pearson: n=14 is small and belief/confidence aren't necessarily linear
    t = table[["delta_belief", "delta_conf"]].dropna()
    if len(t) < 3:
        print("delta belief vs delta confidence: not enough pairs")
        return
    rho, p = spearmanr(t["delta_belief"], t["delta_conf"])
    print(f"delta belief vs delta confidence: n={len(t)}  rho={rho:.3f}  p={p:.4f}")


def belief_distress_correlation(table):
    # does belief change track distress change, or are they independent dimensions
    t = table[["delta_belief", "delta_distress"]].dropna()
    if len(t) < 3:
        print("delta belief vs delta distress: not enough pairs")
        return
    rho, p = spearmanr(t["delta_belief"], t["delta_distress"])
    print(f"delta belief vs delta distress: n={len(t)}  rho={rho:.3f}  p={p:.4f}")


if __name__ == "__main__":
    records = load_records_from_json("all_results.json")
    df = to_long_df(records)
    table = summary_table(df)

    print(f"n statements: {len(table)}")
    print("─" * 70)

    paired_wilcoxon(table, "baseline_belief", "final_belief", "belief (baseline vs final)")
    paired_wilcoxon(table, "baseline_conf", "final_conf", "confidence (baseline vs final)")
    paired_wilcoxon(table, "baseline_distress", "final_distress", "distress (baseline vs final)")
    print("─" * 70)

    attenuation_vs_zero(table)
    print("─" * 70)

    belief_confidence_correlation(table)
    belief_distress_correlation(table)