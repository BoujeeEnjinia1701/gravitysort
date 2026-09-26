---
doc_id: GVS-REQ-001
title: GravitySort requirements
project: GravitySort
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from GVS-CAL-001; R7 pack range aligned with MotionCore and GVS-DDR-001 item 6; MotionCore cost $335; proposed changes to R11 and R12 listed, awaiting Amish
---

# GravitySort requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be revised after co-design sessions. At TRL 3 each has been checked by calculation or design review in GVS-CAL-001: six are met on paper, three are not met (R9, R11, R12), three are at risk (R2, R5, R6) and two cannot be verified before testing (R4, R14). Recovery can only be verified by testing with real or spiked ore, which is TRL 4 work and on hold by Amish's instruction.

Table 1. Requirements. Status is from GVS-CAL-001 (`docs/04-calcs/results.csv`).

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (GVS-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Use no mercury | No amalgamation step, no mercury-coated plates or traps, no step that needs mercury to recover gold from the concentrate | Design review of the flowsheet | Met (design review) |
| R2 | Process a small group's daily ore | 200 kg/h or more of ore milled to below 2 mm, as slurry of 25 to 35 % solids, for 8 h (1.6 t per day) | Bowl capacity and cycle calculation | **At risk:** 1.55 t per shift after three 5 min flush stops; 1.6 t needs 206 kg/h |
| R3 | Hold fine gold in the bowl | Bowl acceleration adjustable from 40 to 80 G at the riffle rings (about 600 to 850 rpm at 100 mm radius), with speed shown to the operator | Drive ratio and speed calculation | Met on paper: 598 to 846 rpm at a 50 to 71 rpm cadence; speed display (BOM item 19) |
| R4 | Recover fine gold | Of free gold in the screened feed: 80 % or more of 75 to 1,000 µm gold and 50 % or more of 38 to 75 µm gold in the bowl concentrate; 60 % or more of all gold in the ore to smelted gold overall | Test with spiked or characterized ore (TRL 4) | **Not verifiable at TRL 3; at risk.** Settling check passes; bed behaviour needs testing |
| R5 | Make a concentrate that can be smelted without mercury | Bowl mass pull 0.5 % or less of feed; shaking table reduces one day's bowl concentrate (about 5 kg) to 100 g or less | Mass balance calculation; later test | **At risk:** bowl pull 0.33 % is met; 5.3 kg per day needs 53:1 on the table, likely two passes |
| R6 | Run on pedal power | Full throughput at 60 W or less at the pedals, at a cadence of 55 to 70 rpm | Power estimate from slurry, fluidization water and bearing losses | **At risk:** 48.2 W at 60 G is met; 62.8 W at 80 G is not; union seal drag assumed |
| R7 | Run on a small motor | Full throughput from the MotionCore 250 W reference drive on any 20 to 58 V pack that MotionCore accepts, with at least 3 times power margin | Power estimate | Met on paper: 5.2 times at 60 G, 4.0 times at 80 G; 0.55 kWh per shift |
| R8 | Use little water | 1.5 m3/h or less at 200 kg/h, and tolerate recirculated water with fine silt | Water balance calculation | Met on paper: 1.19 m3/h; a 3/4 in fluidization hose is needed (GVS-CAL-001 section 6) |
| R9 | Stay within the concept budget | Parts $350 or less, excluding the MotionCore module and battery | Priced BOM | **Not met:** $465, over $350 and over the $450 recommended at TRL 2 (awaiting Amish) |
| R10 | Be built in a local workshop | Welding, drilling and hand tools only; no lathe; bowl liner cast in a printed mold | Design review of every part | Met (design review): set-screw bearing inserts and a taper bush avoid the lathe; bowl casting route unproven |
| R11 | Travel to site | Breaks into loads of 30 kg or less, carried by two people; total 80 kg or less; assembled with hand tools in 30 min or less | Mass estimate from the model | **Not met:** 88.3 kg in six loads (heaviest 25.8 kg); assembly time not verified |
| R12 | Guard every moving part | Bowl covered by a lid guard during running; belts, chains and the table head fully guarded; bowl speed limited to 900 rpm or less by gearing (pedal) or by the MotionCore speed limit (motor); bowl stops within 15 s of stopping the drive | Design review and safety checklist | **Not met as written:** guards, lid interlock and a disc brake (0.6 s stop; about 20 s coasting) are designed, and the motor is capped by its 1.2:1 step-up and the MotionCore limit, but gearing cannot cap the pedal drive (900 rpm at a 75 rpm cadence) |
| R13 | Clean up quickly and securely | Bowl concentrate flushed into a lockable container in 5 min or less without tools; table concentrate drops into a lockable tray | Design review; later timed trial | Met on paper: toolless lid clamps; time not verified |
| R14 | Last in abrasive service | Bowl liner and riffles replaceable in 30 min; liner life 500 h or more (estimate to be checked) | Wear data for cast polyurethane; later test | Not verifiable at TRL 3 |

## Assumptions

- Ore is milled to below 2 mm by the user's existing mill and screened on the GravitySort hopper screen.
- Free, liberated gold in the 38 to 1,000 µm range. Gold locked in sulfides or finer than about 20 µm is lost to tailings by any gravity method, so R4 applies to free gold only.
- Reference ore for the daily balance: 5 g/t, 1.6 t per day. Real grades vary widely (about 1 to 20 g/t).
- Healthy adult pedalling at 60 W or less for sessions of about 1 h, with operators taking turns.
- Budget: the $350 in `project.yaml` covers GravitySort parts. The MotionCore kit and reference motor ($335: $265 kit plus $70 motor, per MTC-CAL-001) and a battery are shared lab components, budgeted with MotionCore. The TRL 2 review recommended raising `budget_usd` to $450; that figure is recorded in GVS-DDR-001 as awaiting Amish and `budget_usd` is unchanged.
- The pack for the motor option is left to the user (GVS-DDR-001 item 6).

## Proposed changes, awaiting Amish

Apart from aligning R7's pack range with MotionCore (GVS-DDR-001 item 6), no target has been changed at TRL 3. GVS-DDR-001 proposes, for Amish's decision:

- **R12:** for the pedal drive, replace "limited to 900 rpm or less by gearing" with a structural margin at the highest reachable speed (1,200 rpm at a 100 rpm cadence) plus the speed display (item 9).
- **R11:** relax the total to 90 kg, or lighten the frame and table stand and re-estimate (item 10).
- **R2:** restate the target as 200 kg/h of feed time, or raise the design feed to about 210 kg/h (item 13).
