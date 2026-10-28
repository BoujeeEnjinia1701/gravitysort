---
doc_id: GVS-DDR-004
title: GravitySort concept selection
project: GravitySort
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First issue (kit 1.8 pipeline): three concept options scored against GVS-URS-001; all within 10 %, so the choice goes to Amish without a pick (Proposed, awaiting Amish)"
---

# 0004: Concept selection

- **Date:** 2026-10-25
- **Status:** proposed (Proposed, awaiting Amish; GVS-DEC-001 O1)

## Context

GravitySort was designed before kit 1.8, as a fluidized centrifugal bowl and a small shaking table on one pedal drive, and has been at TRL 3 since 2026-09-25. Kit 1.8 asks every repo for at least two concept options with different working principles, scored against the user requirements (STANDARDS section 21), and kit 1.9 asks for every option to be modelled to the repo's detail level (Amish, 2026-10-24: "Detail every option"). In a repo designed before kit 1.8 the current design is option A, and it is not redesigned without Amish's go. The options, their STEM rows, first-order numbers and the full scoring are in GVS-OPT-001.

## Options considered

| Option | Working principle | Weighted score (of 230) | Main strength | Main weakness |
| --- | --- | --- | --- | --- |
| A. Fluidized bowl and shaking table (current design) | Enhanced gravity: a fluidized bed at about 60 G holds fine gold; the table cleans the concentrate to about 100 g | 165 | Catches fine gold (UR-003) and makes a smeltable concentrate | Dearest ($594, USD 139 over the target), most complex, spinning bowl and open containment item |
| B. Diaphragm jig and shaking table | Pulsed water through a ragging bed stratifies by density; same table for clean-up | 157 | Slow, simple, safe mechanism; cheaper (about $400, estimate) | Loses much of the gold finer than 0.1 mm; more water; more concentrate to clean |
| C. Carpeted sluice and gold pans | Flowing film over expanded metal riffles and matting; hand panning | 172 | Cheapest (about $195, estimate), no power, no moving parts | Under 20 % recovery of gold finer than 100 um; tens of kilograms to pan by hand, the material miners amalgamate today |

All three are within 10 % of the top score (A is 4.1 % and B 8.7 % below C).

## Decision

Proposed, awaiting Amish. Under STANDARDS section 21 two options within 10 % go to Amish without a pick, so no option is recommended. Two observations for the decision:

1. The weighted table treats no requirement as a gate. C scores highest because cost, buildability and safety are counted twice (as user requirements and as the section 21 criteria), while it scores 1 of 5 on UR-003, the fine-gold need the project exists for. If Amish treats UR-003 as a gate (a score of 3 or more), only option A passes.
2. Under section 21 the current design, option A, stays in the repo (model, drawings, BOM and build plan) unless Amish decides otherwise; `concept_chosen` stays unset.

## Consequences

- If A is confirmed: no change to the repo; the open items are the TRL 4 tests (PR-004, PR-005, PR-016) and the decisions in GVS-DEC-001.
- If B or C is chosen: the repo would be redesigned around that option at TRL 2 (its D3 model in `cad/src/gvs_option_b.py` or `gvs_option_c.py` is the starting point), with new calculations, drawings, BOM and build plan; the pitch would change for C (no fine-gold capture), which is Amish's decision in any case.
- Ideas worth grafting whatever is chosen: a short carpeted sluice from C under the bowl's tailings outlet as a no-power scavenger for coarse gold and for upsets; B's slow, low-energy drive is a reminder that the table clean-up costs only about 15 W.
