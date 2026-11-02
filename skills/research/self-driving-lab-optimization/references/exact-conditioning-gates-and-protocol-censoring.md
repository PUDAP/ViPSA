# Exact conditioning gates and protocol-level censoring

Use this note for staged memristor DOE campaigns in which forming and conditioning must pass before an assigned DC-IV or pulse recipe is executed.

## Full-precision acceptance

Apply numerical gates to the full-precision values stored in the run summary. Do not round a near miss into a pass. For a required run of `k` ratios and maximum spread `S`, evaluate:

```text
all(ratio_i >= minimum_ratio)
max(last_k_ratios) / min(last_k_ratios) <= S
no state read at compliance
```

For example, a computed spread of `2.521855×` fails a declared `<=2.5×` gate even if a short display rounds it to `2.52×`. Preserve the exact value and classify the downstream recipe as withheld/unevaluated.

## Read-compliance censoring

A post-SET or post-RESET read at compliance is censored evidence, not proof of a strong state:

- stop conditioning;
- preserve prior valid pairs and the clamped raw read;
- do not compute or approve ON/OFF from the clamped value;
- classify `state_read_compliance_saturation` separately from ordinary non-convergence;
- do not automatically raise compliance; review the shared SET/read compliance and read-bias design first; and
- keep the assigned recipe unevaluated.

If saturation recurs at the same conditioning position across independently formed devices, treat it as protocol-level censoring rather than repeated device success.

## Campaign-level decision rule

Track activation yield, clean-forming yield, conditioning yield, read-censoring rate, recipes actually executed, characterization pass, endurance pass, and retention pass separately.

When independent anchor replicates repeatedly form but fail conditioning before their recipes execute, freeze recipe ranking. The supported conclusion is that conditioning reproducibility is the dominant bottleneck. Redirect subsequent allocations toward replicated conditioning diagnostics or a prespecified campaign stop/review; never score withheld recipe assignments as recipe failures.

## Evidence-tier language

Rank outcomes as:

1. retention-qualified;
2. endurance-qualified;
3. fully characterized;
4. best-tested candidate with explicit failure point;
5. promising conditioning partial;
6. withheld/unevaluated assignment;
7. mechanistic recommendation not yet tested.

Large isolated ratios, five promising pairs followed by a clamped read, or two early valid characterization cycles do not establish an optimized protocol.
