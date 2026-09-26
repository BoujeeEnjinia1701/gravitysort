# BOM notes

Prices are indicative TRL 3 estimates with a supplier or supplier type on every line; none is a quotation. Row numbers match the exploded view (`media/exploded.png`) and Table 1 of the design precis. Items 18 and 19 are new at TRL 3. Items 1 and 15 use 25 x 25 x 1.5 mm tube under GVS-DDR-002 (Amish's decision of 2026-09-25). The total is checked by `docs/04-calcs/sizing.py` (GVS-CAL-001 section 12).

**The MotionCore kit and reference motor (item 12) are not included in the GravitySort total.** They are shared lab components with their own budget: $265 for the kit plus $70 for the reference hub motor, $335 in all (MTC-CAL-001). The pedal drive is the baseline. The battery for the motor option is the user's choice and is not included either.

| Group | Items | Cost |
| --- | --- | --- |
| Centrifuge stage and frame | 1 to 7 | $197 |
| Pedal drive and transmission | 8 to 11 | $110 |
| Water supply | 13 | $35 |
| Shaking table | 14 to 16 | $70 |
| Hardware | 17 | $15 |
| Bowl brake, lid interlock and speed display | 18 and 19 | $28 |
| **GravitySort total, MotionCore excluded** | 1 to 11, 13 to 19 | **$455** |
| Motor option (MotionCore kit and reference motor, battery excluded) | 12 | $335 |

The total of $455 is $5 (1.1 %) over the $450 in `project.yaml` and requirement R9, set by Amish on 2026-09-25 (GVS-DDR-002; it was $350). The lighter tube saved $10 against the v0.1 total of $465. Cost-down options, none recommended and all still awaiting Amish: a quarter-turn belt instead of the bevel gearbox (about $25 less), the non-fluidized bowl variant (about $45 less, lower fine-gold recovery), or building the table later (about $70 deferred).

A water pump from the settling pond to the header tank is needed on site (GVS-CAL-001 section 4) and is not in this BOM.
