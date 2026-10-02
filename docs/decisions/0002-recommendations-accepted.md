---
doc_id: GVS-DDR-002
title: GravitySort recommendations accepted
project: GravitySort
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of the recommendations in GVS-DDR-001 and docs/REVIEW.md, what changed in the repo, and the items still open
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($455)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Items 8b, 11b, 12 and 13 decided by Amish as recommended (GVS-DEC-001)"
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item in GVS-DDR-001 and `docs/REVIEW.md` that carried a recommendation is decided by Amish, 2026-09-25: go with recommendation. Items 8b, 11b, 12 and 13, which had no recommendation, were decided by Amish on 2026-10-02 as later recommended: "i approve your recommendations for all 555 open decisions." (GVS-DEC-001).

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." GVS-DDR-001 (v0.1) had adopted most TRL 2 recommendations for TRL 3 work, open for his review, and listed the budget and six TRL 3 items as awaiting him. This record turns every item that had a recommendation into a decision, applies it at TRL 3 level inside this repo, and lists what is still open. Where a recommendation offered several options, the recommended option is the decision. TRL 4 work (building, testing, purchasing) stays on hold by Amish's instruction, and the project stays at TRL 3.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # (GVS-DDR-001) | Decision | What changed in the repo |
| --- | --- | --- |
| 1 | Budget raised from $350 to **$450** | `project.yaml` `budget_usd` 350 to 450; R9 target $450 (GVS-REQ-001 v0.4); README budget line; GVS-CAL-001 v0.2 section 12. The BOM is $455, so R9 is still not met, by $5 |
| 2 | Two stages: centrifugal bowl, then shaking table | Status wording only (GVS-PRC-001 v0.4, GVS-DDR-001 v0.2) |
| 3 | Fluidized bowl with a rotary union; non-fluidized bowl kept as a documented low-cost variant | Status wording only |
| 4 | Cast polyurethane liner in a 3D-printed mold on a GFRP shell | Status wording only |
| 5 | Pedal crank baseline, MotionCore 250 W option, one drive time-shared between bowl and table | Status wording only |
| 6 | Battery for the motor option left to the user; SwapCell not named | Status wording only |
| 7 | Direct smelting with borax as the downstream step, outside this hardware | Status wording in GVS-PRB-001 v0.4 |
| 8a | Partner screening criterion: a country with a mercury ban in force (Colombia) or a Minamata action plan with a planetGOLD programme | Status wording in GVS-PRB-001 v0.4 |
| 9 | R12 restated (option a): with the pedals, a burst safety factor of 10 or more at the highest reachable speed (1,200 rpm at a 100 rpm cadence) plus the speed display replaces the gearing cap; the motor stays capped at 900 rpm | GVS-REQ-001 v0.4 R12; GVS-CAL-001 v0.2 sections 10 and 14 and `sizing.py`. R12 moves from not met as written to **met on paper** (lowest factor 17) |
| 10 | Lighter frame (option b): 25 x 25 x 1.5 mm tube for the base frame, pedal outrigger, table stretchers and table head post, then re-estimate | `cad/src/model.py` (`tube` 30 to 25, new `tube_wall` 1.5; cross members and stand stretchers follow the tube size); STEP and STL re-exported; GVS-DWG-001 Rev P1 to P2; BOM items 1 ($40 to $32) and 15 ($30 to $28); GVS-CAL-001 v0.2 adds a frame member check (61 MPa, safety factor 3.9, 0.73 mm deflection). Mass 88.3 kg to **77.3 kg**, heaviest load 25.8 to 18.1 kg: R11 **met on paper** |
| 11a | Fluidization supply: 3/4 in hose and about 89 holes of 1.0 mm graded toward the lower rings | Already in the model notes and BOM; status wording in GVS-PRC-001 v0.4 and GVS-CAL-001 v0.2 section 6 |
| 14 | Engineering proposals: disc brake with parking latch and lid interlock pin (BOM item 18); bicycle computer speed display (item 19); 1.2:1 motor chain step-up; MotionCore lid switch on a brake input | Already in the model, BOM and calculation; status wording in GVS-PRC-001 v0.4. The MotionCore assumptions are listed as cross-repo actions in `docs/REVIEW.md` |

No pitch or problem rewording was recommended, so the `project.yaml` pitch and problem are unchanged.

### Items left open on 2026-09-25

*Table 2. Items with no recommendation on 2026-09-25, and their status since.*

| # (GVS-DDR-001) | Item | Why it was open | Status |
| --- | --- | --- | --- |
| 1 (part) | Cost-down options to close the $5 gap: quarter-turn belt instead of the bevel gearbox (about $25), non-fluidized variant (about $45), table later (about $70 deferred) | Listed as options with no recommendation | Carried as savings worth trying in the Value engineering section of GVS-DEC-001, not as an open decision |
| 8b | The first co-design partner itself | No partner was recommended; only the screening criterion | Decided by Amish, 2026-10-02, as recommended: Colombia, with a miners' cooperative introduced through the Alliance for Responsible Mining in Medellin as the first candidate (GVS-DEC-001) |
| 11b | Head for the fluidization supply: a 1.7 m post or a small pump, for 10 kPa net at every ring | No preference was stated between the two | Decided by Amish, 2026-10-02, as recommended: a 1.7 m post, braced (GVS-DEC-001) |
| 12 | Water pumping from the settling pond at pedal-only sites (about 1.19 m3/h, 5.5 W hydraulic) | No recommendation yet | Decided by Amish, 2026-10-02, as recommended: gravity supply from upstream as the site rule; otherwise a treadle or hand pump, or a 12 V pump with the MotionCore battery (GVS-DEC-001) |
| 13 | R2 and R5 margins: raise the design feed to about 210 kg/h, or restate R2 as 200 kg/h of feed time | Two options, no recommendation | Decided by Amish, 2026-10-02, as recommended: R2 restated as 200 kg/h of feed time; design feed kept at 200 kg/h (GVS-DEC-001) |

### On hold (TRL 4)

Nothing decided here needs TRL 4 work to be recorded. The checks the decisions point at, such as bearing alignment on the first 25 mm frame, spin-up with the tub and lid as containment, and brake stop time, are TRL 4 work and stay on hold by Amish's instruction.

## Consequences

- GVS-PRB-001, GVS-PRC-001 and GVS-REQ-001 move to v0.4, GVS-CAL-001 to v0.2 and GVS-DDR-001 to v0.2, each with a revision entry for this record.
- Requirements then stood at one not met (R9, $455 against $450), three at risk (R2, R5, R6), two not verifiable before testing (R4, R14) and eight met on paper (R1, R3, R7, R8, R10, R11, R12, R13).
- The pedal drive is still not speed-capped; the restated R12 makes the structural margin and the speed display carry that risk, and the tub and lid are not yet shown to contain a liner fragment.
- `trl` and `trl_target` stay at 3.

## Budget approved, 2026-09-26

On 2026-09-26 Amish wrote, in chat: "i approve all the budget items."

- Budget set to $455 to cover the priced BOM: decided by Amish, 2026-09-26. This closes the $5 gap left by item 1. The BOM is $455 (MotionCore and battery excluded), so R9 moves from not met to met on paper, with no margin. The cost-down options in GVS-DDR-001 item 1 stay on record but are no longer needed.
- Requirements now stand at none not met, three at risk (R2, R5, R6), two not verifiable before testing (R4, R14) and nine met on paper (R1, R3, R7, R8, R9, R10, R11, R12, R13).
- Files changed: `project.yaml` (`budget_usd` 450 to 455); GVS-REQ-001 v0.5; GVS-CAL-001 v0.3, `docs/04-calcs/sizing.py` (hard-coded budget 450 to 455) and `results.csv`; GVS-PRB-001 v0.5 and GVS-PRC-001 v0.5 (budget figure); `README.md`; `bom/bom-notes.md`; `docs/REVIEW.md`.
