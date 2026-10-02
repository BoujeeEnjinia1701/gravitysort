---
doc_id: GVS-DDR-001
title: GravitySort TRL 2 review decisions
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
  change: Record the TRL 2 review items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Items 8b, 11b, 12 and 13 decided by Amish as recommended (GVS-DEC-001)"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted in part. On 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos". Items 1 to 7, 8a, 9, 10, 11a and 14 are decided by Amish, 2026-09-25: go with recommendation (GVS-DDR-002). Items 8b, 11b, 12 and 13 carried no recommendation at TRL 2; recommendations were written for them later, and Amish approved them on 2026-10-02: "i approve your recommendations for all 555 open decisions." (GVS-DEC-001).

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25, /populate) listed eight items as "Proposed, awaiting Amish", each with a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the GravitySort items one by one. Under that instruction, each item that has a recommendation is adopted as recommended so that the TRL 3 work can proceed, and stays open for his review. A recommended change to `budget_usd` is not applied; the figure is recorded here as awaiting Amish. TRL 4 is on hold by Amish's instruction. At v0.2 of this record, Amish's acceptance of the recommendations on 2026-09-25 is applied; the details are in GVS-DDR-002 (`0002-recommendations-accepted.md`).

## Options considered

The options for items 1 to 8 are in `docs/REVIEW.md` (TRL 2 section) and GVS-PRC-001. Items 9 to 14 are new at TRL 3 and come from GVS-CAL-001; their options are given in Table 2.

## Decision

*Table 1. Items adopted for TRL 3, now decided (GVS-DDR-002).*

| # | Item | Status | Where it now lives |
| --- | --- | --- | --- |
| 2 | Two stages: centrifugal bowl, then shaking table | Decided by Amish, 2026-09-25: go with recommendation | GVS-PRC-001 v0.3, `cad/src/model.py` |
| 3 | Fluidized bowl with a rotary union; the non-fluidized bowl kept as a documented low-cost variant | Decided by Amish, 2026-09-25: go with recommendation | GVS-PRC-001 v0.3, GVS-CAL-001 section 6, BOM item 4 |
| 4 | Bowl liner: cast polyurethane in a 3D-printed mold, on a GFRP shell | Decided by Amish, 2026-09-25: go with recommendation | GVS-PRC-001 v0.3, GVS-REQ-001 R10, BOM item 3 |
| 5 | Drive: pedal crank as the baseline, MotionCore 250 W as the option, one drive time-shared between bowl and table | Decided by Amish, 2026-09-25: go with recommendation | GVS-PRC-001 v0.3, GVS-CAL-001 sections 7 and 9 |
| 6 | Reference battery for the motor option: left to the user (any pack MotionCore accepts, 20 to 58 V); SwapCell not named | Decided by Amish, 2026-09-25: go with recommendation | GVS-PRC-001 v0.3, GVS-REQ-001 R7 |
| 7 | Final step: direct smelting with borax documented as the recommended downstream method, outside this hardware | Decided by Amish, 2026-09-25: go with recommendation | GVS-PRB-001 v0.3, GVS-PRC-001 v0.3 |
| 8a | Screening criterion for the first co-design partner: a country with a mercury ban in force (Colombia) or a Minamata action plan with a planetGOLD programme | Decided by Amish, 2026-09-25: go with recommendation | GVS-PRB-001 v0.3 open questions |

No pitch or problem rewording was recommended at TRL 2, so `project.yaml` and `README.md` keep the TRL 2 wording.

### Items that remain open

*Table 2. Items open at v0.1. Status updated at v0.2 under GVS-DDR-002.*

| # | Item | Options and recommendation | Status |
| --- | --- | --- | --- |
| 1 | Budget | The TRL 2 review recommended raising `budget_usd` from $350 to **$450**. At TRL 3 the BOM is **$465** (GVS-CAL-001 section 12), over both figures. `budget_usd` stays at $350. Cost-down options: replace the bevel gearbox with a quarter-turn belt (about $25 less, lower belt life), build the non-fluidized variant (about $45 less, lower fine-gold recovery), or phase the build with the table later (about $72 deferred) | Decided by Amish, 2026-09-25: go with recommendation: `budget_usd` $450. The cost-down options carry no recommendation and remain proposed, awaiting Amish |
| 8b | The first co-design partner itself | No partner is named; the criterion in 8a is only a screen | Decided by Amish, 2026-10-02, as recommended: Colombia, with a miners' cooperative introduced through the Alliance for Responsible Mining in Medellin as the first candidate to approach (GVS-DEC-001) |
| 9 | R12 speed limit on the pedal drive | Gearing cannot cap a pedal drive: 900 rpm needs only a 75 rpm cadence. Options: (a) reword R12 so the pedal case relies on a structural margin at the highest reachable speed (100 rpm cadence, 1,200 rpm; safety factor 17 or more in GVS-CAL-001) plus the speed display; (b) add a centrifugal slip clutch on the jackshaft. Recommendation: (a) | Decided by Amish, 2026-09-25: go with recommendation (a): R12 restated |
| 10 | R11 transport mass | Estimated 88 kg against 80 kg. Options: (a) relax R11 to 90 kg; (b) frame in 25 x 25 x 1.5 mm tube (about 7.7 kg less, still about 81 kg) with a lighter table stand; (c) both. Recommendation: (b), then re-estimate | Decided by Amish, 2026-09-25: go with recommendation (b): 25 x 25 x 1.5 mm tube, re-estimated at 77.3 kg |
| 11 | Fluidization supply | The 1.25 m header post gives 3.7 kPa at the union with a 3/4 in hose and a negative pressure with a 1/2 in hose. Proposal: 3/4 in hose (in the BOM now), about 90 holes of 1.0 mm graded toward the lower rings, and either a 1.7 m post or a small pump for an even 10 kPa net at every ring | 11a, 3/4 in hose and about 89 graded holes of 1.0 mm: Decided by Amish, 2026-09-25: go with recommendation. 11b, post or pump for the head: decided by Amish, 2026-10-02, as recommended: a 1.7 m post, braced so a full 60 L tank cannot tip it (GVS-DEC-001) |
| 12 | Water supply without power | 1.19 m3/h needs a pump from the settling pond to the header tank (about 5.5 W hydraulic); the tank holds only 3 min. The pump is not in the BOM or the pedal drive | Decided by Amish, 2026-10-02, as recommended: gravity supply from upstream is the site rule for the first field trial; otherwise a bought treadle or hand pump worked in turns, or a small 12 V pump at sites with the MotionCore battery (GVS-DEC-001) |
| 13 | R2 and R5 margins | Flush stops cut a shift to 1.55 t at 200 kg/h; the table needs about 53:1, likely two passes. Options: raise the design feed to 210 kg/h, or restate R2 as 200 kg/h of feed time | Decided by Amish, 2026-10-02, as recommended: R2 restated as 200 kg/h of feed time, about 1.55 t per eight-hour shift with three flush stops; design feed kept at 200 kg/h (GVS-DEC-001) |
| 14 | Engineering proposals from GVS-CAL-001 | Disc brake with parking latch and a lid interlock pin on the brake cable (item 18); bicycle computer as the speed display (item 19); motor chain step-up of 1.2:1 so the reference hub motor's no-load speed gives at most 900 rpm at the bowl; MotionCore lid switch on a brake input | Decided by Amish, 2026-09-25: go with recommendation |

## Consequences

- GVS-PRC-001, GVS-REQ-001 and GVS-PRB-001 move to v0.3; the design choices in Table 1 are no longer described as proposals. At v0.2 of this record they are decided by Amish (GVS-DDR-002), and the documents move to v0.4.
- `budget_usd` was unchanged at $350 at v0.1; it is $450 under GVS-DDR-002, and R9 is not met by $5 ($455).
- The MotionCore cost is now quoted as $335 ($265 kit plus $70 reference motor, MTC-CAL-001), still outside the GravitySort total.
- At v0.1, requirements R9, R11 and R12 were not met on paper (after GVS-DDR-002 only R9 is not met); R2, R5 and R6 are at risk; R4 and R14 cannot be verified before testing, which is TRL 4 work and on hold.
