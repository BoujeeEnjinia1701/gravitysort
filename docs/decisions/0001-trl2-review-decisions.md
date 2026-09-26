---
doc_id: GVS-DDR-001
title: GravitySort TRL 2 review decisions
project: GravitySort
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. Items 2 to 7 and the screening criterion in item 8 are adopted as recommended for TRL 3 work, pending Amish's review. Item 1 (budget), the choice of partner in item 8 and items 9 to 14 remain proposed, awaiting Amish.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25, /populate) listed eight items as "Proposed, awaiting Amish", each with a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the GravitySort items one by one. Under that instruction, each item that has a recommendation is adopted as recommended so that the TRL 3 work can proceed, and stays open for his review. A recommended change to `budget_usd` is not applied; the figure is recorded here as awaiting Amish. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for items 1 to 8 are in `docs/REVIEW.md` (TRL 2 section) and GVS-PRC-001. Items 9 to 14 are new at TRL 3 and come from GVS-CAL-001; their options are given in Table 2.

## Decision

*Table 1. Items adopted for TRL 3.*

| # | Item | Status | Where it now lives |
| --- | --- | --- | --- |
| 2 | Two stages: centrifugal bowl, then shaking table | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | GVS-PRC-001 v0.3, `cad/src/model.py` |
| 3 | Fluidized bowl with a rotary union; the non-fluidized bowl kept as a documented low-cost variant | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | GVS-PRC-001 v0.3, GVS-CAL-001 section 6, BOM item 4 |
| 4 | Bowl liner: cast polyurethane in a 3D-printed mold, on a GFRP shell | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | GVS-PRC-001 v0.3, GVS-REQ-001 R10, BOM item 3 |
| 5 | Drive: pedal crank as the baseline, MotionCore 250 W as the option, one drive time-shared between bowl and table | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | GVS-PRC-001 v0.3, GVS-CAL-001 sections 7 and 9 |
| 6 | Reference battery for the motor option: left to the user (any pack MotionCore accepts, 20 to 58 V); SwapCell not named | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | GVS-PRC-001 v0.3, GVS-REQ-001 R7 |
| 7 | Final step: direct smelting with borax documented as the recommended downstream method, outside this hardware | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | GVS-PRB-001 v0.3, GVS-PRC-001 v0.3 |
| 8a | Screening criterion for the first co-design partner: a country with a mercury ban in force (Colombia) or a Minamata action plan with a planetGOLD programme | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review | GVS-PRB-001 v0.3 open questions |

No pitch or problem rewording was recommended at TRL 2, so `project.yaml` and `README.md` keep the TRL 2 wording.

### Items that remain open

*Table 2. Open items, all Proposed, awaiting Amish.*

| # | Item | Options and recommendation | Status |
| --- | --- | --- | --- |
| 1 | Budget | The TRL 2 review recommended raising `budget_usd` from $350 to **$450**. At TRL 3 the BOM is **$465** (GVS-CAL-001 section 12), over both figures. `budget_usd` stays at $350. Cost-down options: replace the bevel gearbox with a quarter-turn belt (about $25 less, lower belt life), build the non-fluidized variant (about $45 less, lower fine-gold recovery), or phase the build with the table later (about $72 deferred) | Proposed, awaiting Amish |
| 8b | The first co-design partner itself | No partner is named; the criterion in 8a is only a screen | Proposed, awaiting Amish |
| 9 | R12 speed limit on the pedal drive | Gearing cannot cap a pedal drive: 900 rpm needs only a 75 rpm cadence. Options: (a) reword R12 so the pedal case relies on a structural margin at the highest reachable speed (100 rpm cadence, 1,200 rpm; safety factor 17 or more in GVS-CAL-001) plus the speed display; (b) add a centrifugal slip clutch on the jackshaft. Recommendation: (a) | Proposed, awaiting Amish |
| 10 | R11 transport mass | Estimated 88 kg against 80 kg. Options: (a) relax R11 to 90 kg; (b) frame in 25 x 25 x 1.5 mm tube (about 7.7 kg less, still about 81 kg) with a lighter table stand; (c) both. Recommendation: (b), then re-estimate | Proposed, awaiting Amish |
| 11 | Fluidization supply | The 1.25 m header post gives 3.7 kPa at the union with a 3/4 in hose and a negative pressure with a 1/2 in hose. Proposal: 3/4 in hose (in the BOM now), about 90 holes of 1.0 mm graded toward the lower rings, and either a 1.7 m post or a small pump for an even 10 kPa net at every ring | Engineering proposal, awaiting Amish |
| 12 | Water supply without power | 1.19 m3/h needs a pump from the settling pond to the header tank (about 5.5 W hydraulic); the tank holds only 3 min. The pump is not in the BOM or the pedal drive | Proposed, awaiting Amish; no recommendation yet |
| 13 | R2 and R5 margins | Flush stops cut a shift to 1.55 t at 200 kg/h; the table needs about 53:1, likely two passes. Options: raise the design feed to 210 kg/h, or restate R2 as 200 kg/h of feed time | Proposed, awaiting Amish |
| 14 | Engineering proposals from GVS-CAL-001 | Disc brake with parking latch and a lid interlock pin on the brake cable (item 18); bicycle computer as the speed display (item 19); motor chain step-up of 1.2:1 so the reference hub motor's no-load speed gives at most 900 rpm at the bowl; MotionCore lid switch on a brake input | Engineering proposals, awaiting Amish |

## Consequences

- GVS-PRC-001, GVS-REQ-001 and GVS-PRB-001 move to v0.3; the design choices in Table 1 are no longer described as proposals, but each stays open for Amish's review.
- `budget_usd` is unchanged at $350; R9 is not met against it or against the recommended $450.
- The MotionCore cost is now quoted as $335 ($265 kit plus $70 reference motor, MTC-CAL-001), still outside the GravitySort total.
- Requirements R9, R11 and R12 are not met on paper; R2, R5 and R6 are at risk; R4 and R14 cannot be verified before testing, which is TRL 4 work and on hold.
