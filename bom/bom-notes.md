# BOM notes

Prices are indicative TRL 3 estimates with a supplier or supplier type on every line; none is a quotation. Row numbers match the exploded view (`media/exploded.png`) and Table 1 of the design precis. Items 18 and 19 are new at TRL 3; item 23 (the flush container) was added on 2026-10-02. Items 1 and 15 use 25 x 25 x 1.5 mm tube under GVS-DDR-002 (Amish's decision of 2026-09-25). On 2026-10-01 the lines were updated for the constructable design (GVS-DDR-003): every part the build plan (GVS-BLD-001) needs is now in a line, and item 20 (the motor cradle) is new. The total is checked by `docs/04-calcs/sizing.py` (GVS-CAL-001 section 12).

**The MotionCore kit and reference motor (item 12) are not included in the GravitySort total.** They are shared lab components with their own budget: $265 for the kit plus $70 for the reference hub motor, $335 in all (MTC-CAL-001). The pedal drive is the baseline. The battery for the motor option is the user's choice and is not included either. The motor cradle (item 20) is specific to GravitySort and is included.

| Group | Items | Cost |
| --- | --- | --- |
| Centrifuge stage and frame | 1 to 7 | $243 |
| Pedal drive and transmission | 8 to 11 | $120 |
| Water supply | 13 | $41 |
| Shaking table | 14 to 16 | $100 |
| Table bump stop | 21 and 22 | $11 |
| Hardware | 17 | $22 |
| Bowl brake, lid interlock and speed display | 18 and 19 | $28 |
| Motor cradle (motor option) | 20 | $8 |
| Flush container with padlock hasp | 23 | $7 |
| **GravitySort total, MotionCore excluded** | 1 to 11, 13 to 23 | **$580** |
| Motor option (MotionCore kit and reference motor, battery excluded) | 12 | $335 |

Value-engineering target: USD 455. Estimated cost of the constructable design: USD 580 (USD 125 over the target). The target, `budget_usd` in `project.yaml`, is a hypothetical control target that keeps the design on a value-engineering lens, not a spending limit (Amish, 2026-10-01). The concept BOM was $455; making every part buildable added $103, mostly in the table stand and head (+$24), the frame (+$11), the tub fittings (+$14) and the bowl hub and fixings (+$10). Lines 21 and 22 (the table bump stop decided by Amish on 2026-10-01, GVS-DDR-003 A2) add $11. The decisions of 2026-10-02 (GVS-DEC-001) add $11 more: the 1.7 m braced tank post adds about 1.9 m of tube and its welding to line 1 ($43 to $47), and line 23 is the flush container with its padlock hasp ($7). The main cost drivers and the savings worth trying are listed in the Value engineering section of the design decisions register (`docs/06-design-decisions.md`).

Water reaches the header tank by gravity from upstream as the site rule for the first field trial; where that is impossible, a bought treadle or hand pump, or a small 12 V pump at sites with the MotionCore battery, is used (Amish, 2026-10-02, GVS-DEC-001). No pump is in this BOM. The header tank post rises to 1.7 m with two braces (line 1), and the flush container carries a padlock hasp like the concentrate box (line 23); both decided 2026-10-02. Padlocks are left to the partner, two per hasp if the two-person rule is adopted.
