---
doc_id: GVS-REQ-001
title: GravitySort requirements
project: GravitySort
doc_type: Requirements
version: "0.7"
status: Draft
date: '2026-10-01'
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
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R9 target $450; R12 restated for the pedal drive; R11 met with the lighter frame tube; status from GVS-CAL-001 v0.2
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from GVS-CAL-001 v0.4 for the constructable design (GVS-DDR-003); R11 not met (95.7 kg, every load under 30 kg); R9 reported against the value-engineering target
- version: "0.7"
  date: '2026-10-01'
  author: Amish Chadha
  change: R11 restated by Amish (total 100 kg or less, loads 30 kg or less; GVS-DDR-003, A1); R11 met on paper
---

# GravitySort requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be revised after co-design sessions. At TRL 3 each has been checked by calculation or design review in GVS-CAL-001 v0.5, for the constructable design of GVS-DDR-003 (every part can be made and fixed to the next): none is unmet, three are at risk (R2, R5, R6), two cannot be verified before testing (R4, R14) and eight are met on paper or by design review. R9 is reported against the value-engineering target: the constructable design is USD 103 over it. Recovery can only be verified by testing with real or spiked ore, which is TRL 4 work and on hold by Amish's instruction.

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
| R9 | Keep parts cost near the value-engineering target | Value-engineering target $455 for parts, excluding the MotionCore module and battery: a hypothetical control target, not a limit (Amish, 2026-10-01; was $350, then $450; GVS-DDR-002) | Priced BOM | Estimated cost of the constructable design $558: **over the value-engineering target by USD 103** |
| R10 | Be built in a local workshop | Welding, drilling and hand tools only; no lathe; bowl liner cast in a printed mold | Design review of every part | Met (design review): set-screw bearing inserts, a taper bush and a welded nipple on a tube spindle avoid the lathe; liner cast on a six-segment printed core (GVS-DDR-003); casting route unproven |
| R11 | Travel to site | Breaks into loads of 30 kg or less, carried by two people; total 100 kg or less (restated from 80 kg by Amish, 2026-10-01; GVS-DDR-003, A1); assembled with hand tools in 30 min or less | Mass estimate from the model | Met on paper: 95.7 kg in six loads for the constructable design (GVS-DDR-003), every load under 30 kg (heaviest 25.2 kg); assembly time not verified |
| R12 | Guard every moving part | Bowl covered by a lid guard during running; belts, chains and the table head fully guarded; with the motor, bowl speed limited to 900 rpm or less by the drive ratio and the MotionCore speed limit; with the pedals, which gearing cannot cap, a burst safety factor of 10 or more for the bowl, jacket and rings at the highest reachable speed (1,200 rpm at a 100 rpm cadence) and the bowl speed shown to the rider; bowl stops within 15 s of stopping the drive (restated per GVS-DDR-002) | Design review, burst calculation and safety checklist | Met on paper: guards, lid interlock and a disc brake (0.6 s stop; about 20 s coasting); motor capped by its 1.2:1 step-up and the MotionCore limit; lowest pedal-case safety factor 17 at 1,200 rpm; speed display item 19. Containment of a liner fragment not verified |
| R13 | Clean up quickly and securely | Bowl concentrate flushed into a lockable container in 5 min or less without tools; table concentrate drops into a lockable tray | Design review; later timed trial | Met on paper: toolless lid clamps, lid lifts clear of the feed pipe; lockable concentrate box under the table's far end; time not verified |
| R14 | Last in abrasive service | Bowl liner and riffles replaceable in 30 min; liner life 500 h or more (estimate to be checked) | Wear data for cast polyurethane; later test | Not verifiable at TRL 3 |

## Assumptions

- Ore is milled to below 2 mm by the user's existing mill and screened on the GravitySort hopper screen.
- Free, liberated gold in the 38 to 1,000 µm range. Gold locked in sulfides or finer than about 20 µm is lost to tailings by any gravity method, so R4 applies to free gold only.
- Reference ore for the daily balance: 5 g/t, 1.6 t per day. Real grades vary widely (about 1 to 20 g/t).
- Healthy adult pedalling at 60 W or less for sessions of about 1 h, with operators taking turns.
- Budget: the $455 in `project.yaml` is a value-engineering target, a hypothetical control target and not a limit (Amish, 2026-10-01) (raised from $350 to $450 by Amish's decision of 2026-09-25 and to $455 on 2026-09-26, GVS-DDR-002) covers GravitySort parts. The MotionCore kit and reference motor ($335: $265 kit plus $70 motor, per MTC-CAL-001) and a battery are shared lab components, budgeted with MotionCore.
- The pack for the motor option is left to the user (GVS-DDR-001 item 6).

## Changes decided on 2026-09-25

Amish accepted the recommendations on 2026-09-25 (GVS-DDR-002):

- **R9:** target raised from $350 to $450 (item 1).
- **R12:** for the pedal drive, "limited to 900 rpm or less by gearing" is replaced by a burst safety factor of 10 or more at the highest reachable speed (1,200 rpm at a 100 rpm cadence) plus the speed display (item 9).
- **R11:** target unchanged at 80 kg; the frame, pedal outrigger and table stand move to 25 x 25 x 1.5 mm tube and the mass is re-estimated at 77.3 kg (item 10).

## Change decided on 2026-09-26

- **R9:** target raised from $450 to $455 to cover the priced BOM (budget approved by Amish, GVS-DDR-002). Not met to met on paper.

## Change decided on 2026-10-01

Amish, 2026-10-01: "i agree with your recommendations for both GrowRider and GravitySort" (GVS-DDR-003, A1; GVS-DEC-001):

- **R11:** total restated from 80 kg or less to 100 kg or less, keeping every load at 30 kg or less, because the per-load limit decides whether two people can carry the machine to site. Not met to met on paper (95.7 kg). The savings of about 16 kg are to be tried at TRL 4.

## Still proposed, awaiting Amish

These are tracked in the design decisions register, GVS-DEC-001 (`docs/06-design-decisions.md`).

- **R2:** restate the target as 200 kg/h of feed time, or raise the design feed to about 210 kg/h (GVS-DDR-001 item 13). No option was recommended.
