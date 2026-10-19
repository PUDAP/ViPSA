# Conductive contact-coupon validation

Use conductive coupons to separate contact mechanics from fragile-device physics.

## Recommended validation ladder

1. **Bare ITO on glass plus a known series resistor** for first-stage approach/contact repeatability.
2. **Patterned ITO with device-sized isolated pads** for vision, pad-edge, and landing validation.
3. **Representative metal electrodes/device structures** for transferability, surface damage, high-HRS signatures, and probe wear.

Bare continuous ITO is useful because it is uniform, conductive, inexpensive, and sacrificial. It does not validate high-HRS/open discrimination, device switching, small-pad alignment, or contact on fragile top electrodes.

## Electrical fixture

Use a stable return connection at the ITO edge (for example a clip or characterized conductive attachment) and include a precision series resistor when necessary:

`probe -> ITO sheet -> edge return -> series resistor -> SMU`

A 100 kΩ series resistor gives approximately 100 nA at 10 mV, placing the expected current inside a 50–500 nA contact window while preventing low-resistance ITO from immediately reaching read compliance. Without a resistor, choose a coupon-specific low-voltage/current gate; do not reuse a high-resistance-device contact threshold blindly.

Independently measure the resistor and coupon geometry baseline. Two-terminal results include sheet, lead, edge-contact, series-resistor, and probe-contact contributions.

## Protocol

- Use a sacrificial coupon and fixed probe condition.
- Predefine at least 30–50 distributed landings, randomized or balanced across locations.
- Fully retract between landings.
- Record every attempt, including failed approaches and rejected contact gates.
- Save cumulative commanded Z, number of increments, contact current, measured resistance, settling time, retries, and cleanup.
- Capture before/after surface images and inspect for scratches, cracking, delamination, or probe wear.
- Include lifted-probe/open and fixed short/reference-resistor baselines.

## Metrics

Report contact success rate, false-contact rate, Z-travel/increment distribution, landing-to-landing resistance/current repeatability, spatial dependence, drift across repeats, damage rate, and probe-wear observations. Distinguish commanded Z, tracked readback, and independent physical/contact evidence.
