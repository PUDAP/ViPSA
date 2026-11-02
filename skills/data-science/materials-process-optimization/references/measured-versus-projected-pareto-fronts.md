# Reporting observed and proxy Pareto fronts

Use for multi-objective device/recipe optimization reports where endurance may be capped or extrapolated.

1. Freeze the experimental population and objectives. Keep initial sampling, each BO round, new-substrate repeats and differently prepared controls distinct. Repeated cycles are not independent recipes.
2. Preserve objective provenance per point: measured completed cycles, right-censored cap, model-projected failure coordinate, or operator-assigned coordinate. A results-only table can still contain predictions.
3. Compute dominance programmatically: another point must be at least as good on every objective and strictly better on at least one. Retain the full objective table and source hashes; verify counts and device identities.
4. Show separate views when needed: observed completed-count versus measured contrast, and archived projected-objective space. Do not call projected thousands of cycles demonstrated endurance. Exclude arbitrary operator-assigned coordinates from an evidence-based front, or label a separate policy-defined front explicitly.
5. A measured-count front under unequal cycle caps is descriptive, not a definitive lifetime front: a 200-cycle survivor was not shown worse than a 300-cycle survivor. Explain censoring rather than inventing a precise lifetime ordering.
6. Label contrast as the actual extraction metric. Within-sweep forward/backward branch ratios are not independent retention or retained-state ON/OFF measurements. Use matching metric definitions for comparisons.
7. Plot fresh-substrate transfer repeats with distinct symbols and do not pool them silently with historical optimization data. Exclude forming-only and differently stressed yield controls from candidate performance comparisons.
8. Explain the high-contrast/short-run trade-off: a high aggregate contrast can coexist with early terminal failure. A Pareto label is not proof of a robust operating recipe or a transferable optimum.
9. Deliver a legible PNG and objective/front CSVs. Inspect labels, axes, legend overlap and model/measured distinctions before delivery. Provide parameter vectors at full precision in accompanying recipe data when recommending a point.
