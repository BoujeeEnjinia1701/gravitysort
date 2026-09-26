# BOM notes

Prices are indicative TRL 3 estimates with a supplier or supplier type on every line; none is a quotation. Row numbers match the exploded view (`media/exploded.png`) and Table 1 of the design precis. Items 18 and 19 are new at TRL 3. The total is checked by `docs/04-calcs/sizing.py` (GVS-CAL-001 section 12).

**The MotionCore kit and reference motor (item 12) are not included in the GravitySort total.** They are shared lab components with their own budget: $265 for the kit plus $70 for the reference hub motor, $335 in all (MTC-CAL-001). The pedal drive is the baseline. The battery for the motor option is the user's choice and is not included either.

| Group | Items | Cost |
| --- | --- | --- |
| Centrifuge stage and frame | 1 to 7 | $205 |
| Pedal drive and transmission | 8 to 11 | $110 |
| Water supply | 13 | $35 |
| Shaking table | 14 to 16 | $72 |
| Hardware | 17 | $15 |
| Bowl brake, lid interlock and speed display | 18 and 19 | $28 |
| **GravitySort total, MotionCore excluded** | 1 to 11, 13 to 19 | **$465** |
| Motor option (MotionCore kit and reference motor, battery excluded) | 12 | $335 |

The total of $465 is $115 (33 %) over the $350 in `project.yaml` and requirement R9, and $15 (3.3 %) over the $450 recommended at TRL 2, which is awaiting Amish (GVS-DDR-001 item 1). `budget_usd` is unchanged. Cost-down options, all awaiting Amish: a quarter-turn belt instead of the bevel gearbox (about $25 less), the non-fluidized bowl variant (about $45 less, lower fine-gold recovery), or building the table later (about $72 deferred).

A water pump from the settling pond to the header tank is needed on site (GVS-CAL-001 section 4) and is not in this BOM.
