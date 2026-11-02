# Legacy campaign audit and manuscript use

Use this workflow when historical ViPSA folders are being used to support publication-scale counts, throughput, contact, or electrical-performance claims.

## Audit hierarchy

Treat the following as different populations:

1. planned input/design rows;
2. raw substrate/slot folders;
3. saved device sweep files;
4. saved resistance files;
5. devices represented in compiled metrics;
6. compiled cycle rows.

Reconcile each count programmatically using stable keys such as `(batch, molarity, slot, device_id)`. Never silently equate a raw sweep with an attempted device, a saved sweep with successful contact, or a design row with a unique processing condition.

## Provenance and inventory

- Perform a read-only recursive inventory by extension, path class, size, and modification time.
- Hash the authoritative compiled tables and input-design files with SHA-256.
- Record raw schema signatures, row-count distributions, missing sweep/resistance pairs, extra raw files, missing metadata, and extra/missing design links.
- Retain anomaly lists and generated analysis code outside the source archive.

## Defensible campaign claims

Compiled tables can support exact device/cycle totals only after:

- every compiled device key is matched to a raw sweep;
- cycle rows are counted directly;
- cycles-per-device distribution is reported;
- raw sweeps excluded from compiled metrics are listed;
- approximate language is removed when exact reconciled totals are available.

Use wording such as `raw device-sweep records`, `devices represented in compiled analysis`, and `compiled DCIV cycles`. Do not call all of these `attempted devices`.

## Timing

Parse start/end metadata per substrate or slot and report:

- number of timing-bearing runs;
- summed recorded duration;
- number of raw runs missing timing metadata;
- median and IQR of run duration divided by saved device records.

When metadata coverage is incomplete, the duration is a **lower bound**. If only run-level timestamps exist, label the result `total elapsed time per saved device`, not `hardware overhead`; phase-resolved motion, imaging, approach, measurement, retraction, and recovery require event-level logs.

## Contact-current fields

A stored contact-current value in every accepted sweep supports only that the accepted electrical precondition was retained. It does not reconstruct:

- rejected approach attempts;
- contact success or false-contact rate;
- approach success;
- Z-increment distribution;
- contact-resistance repeatability;
- electrode damage or probe wear.

State this limitation explicitly and use a prospective conductive-coupon benchmark for those claims. See `conductive-contact-coupon-validation.md`.

## Compiled electrical-metric quality control

Before using derived `R_on`, `R_off`, ON/OFF, Vset, Vreset, or yield fields:

1. check finite values and missingness;
2. count sub-ohm, near-zero, inverted-ratio, and extreme values;
3. inspect whether resistance was computed at zero/near-zero voltage;
4. verify branch and cycle definitions;
5. regenerate scientific distributions from raw ordered sweeps when compiled outputs contain non-physical values.

A compiled table may remain authoritative for exact campaign counts while being unsuitable for materials-science metrics. Make that distinction in the manuscript.

## Manuscript integration

Prefer replacing unverifiable TODO rows with a table of defensible archive metrics. Mark unavailable legacy failure/intervention fields as `not recorded` rather than estimating them. After editing:

- compile the manuscript;
- extract PDF text to verify values rendered correctly;
- render and visually inspect affected pages for clipped tables or broken flow;
- rebuild and integrity-test the source bundle;
- report remaining TODO categories separately.
