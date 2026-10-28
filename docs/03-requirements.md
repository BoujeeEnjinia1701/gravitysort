---
doc_id: GVS-PRS-001
title: GravitySort product requirements and specifications
project: GravitySort
doc_type: Product requirements and specifications
version: "1.1"
status: Draft
date: '2026-10-25'
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
- version: "0.8"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from GVS-CAL-001 v0.6 with the table bump stop (GVS-DDR-003 A2); R9 $569 (USD 114 over the target); R11 met on paper at 96.5 kg
- version: "0.9"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R2 restated as 200 kg/h of feed time (GVS-DEC-001, 2026-10-02); status updated"
- version: "1.0"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Status from GVS-CAL-001 v0.8 with the 1.7 m braced tank post and the flush container (decisions of 2026-10-02): R9 $580 (USD 125 over the target), R11 99.3 kg, R12 lowest safety factor 16, R13 hasps on both containers; no status changed"
- version: "1.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.8 pipeline: becomes GVS-PRS-001 (replaces GVS-REQ-001); R1 to R14 migrated to PR-001 to PR-014 with the old number in Was, each traced to a user requirement in GVS-URS-001, with tolerance and units; PR-015 (tipping with a full tank) and PR-016 (containment of a liner fragment) added; status from GVS-CAL-001 v0.9 after the STEM fixes F1 to F5 (GVS-DEC-001): PR-009 $594 (USD 139 over the target), PR-011 99.6 kg"
---

# GravitySort product requirements and specifications

What the design must do, each requirement traced to a user need in GVS-URS-001. Targets are proposals for review with a co-design partner, not user-validated needs. Method: STANDARDS section 22; the links to evidence are generated in GVS-RTM-001 (`03b-traceability.md`).

At TRL 3 every requirement has been checked by calculation or design review in GVS-CAL-001 v0.9, for the constructable design of GVS-DDR-003 with the STEM fixes of 2026-10-25 (GVS-DEC-001 F1 to F5). None is unmet. Four are at risk (PR-005, PR-006, PR-011, PR-016), two cannot be verified before testing (PR-004, PR-014), PR-009 is reported against the value-engineering target (USD 139 over it), and the other nine are met on paper or by design review. Recovery, liner life and containment can only be verified by testing, which is TRL 4 work and on hold under the portfolio cap.

Table 1. Product requirements and specifications. Status from GVS-CAL-001 (`docs/04-calcs/results.csv`).

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Safety | No mercury | The flowsheet shall have no amalgamation step, no mercury-coated plates or traps and no step that needs mercury to recover gold from the concentrate | 0 | none | steps using mercury | Design review of the flowsheet, TRL 3 | Met (design review) | R1 |
| PR-002 | UR-002 | Performance | Throughput | The machine shall process ore milled below 2 mm as slurry of 25 to 35 % solids at the design feed rate, giving about 1.55 t in an eight-hour shift with three flush stops (restated by Amish on 2026-10-02, GVS-DEC-001) | 200 | min | kg/h of feed time | Analysis, bowl capacity and cycle (GVS-CAL-001 section 3), TRL 3; timed run at TRL 4 | Met on paper: 200 kg/h; 1.55 t per shift | R2 |
| PR-003 | UR-003, UR-014 | Performance | Bowl G and speed shown | Bowl acceleration at the 100 mm reference radius shall be adjustable over the range, with the bowl speed shown to the operator | 40 to 80 | about 600 to 850 rpm | G | Analysis, drive ratio (GVS-CAL-001 section 2), TRL 3; inspection of the display at TRL 4 | Met on paper: 40 to 81 G at a 50 to 71 rpm cadence; speed display (BOM line 19) | R3 |
| PR-004 | UR-003 | Performance | Fine-gold recovery | Of free gold in the screened feed, the bowl concentrate shall hold at least the target share of 75 to 1,000 um gold and 50 % of 38 to 75 um gold, and at least 60 % of all gold in the ore shall reach smelted gold | 80 | min (50 for 38 to 75 um; 60 overall) | % | Test with characterized or spiked ore, TRL 4 | **Not verifiable at TRL 3; at risk.** Settling check passes (STM S2); bed retention not calculable (STM S3) | R4 |
| PR-005 | UR-004 | Performance | Smeltable concentrate | The bowl mass pull shall be at most 0.5 % of the feed, and the shaking table shall reduce one shift's bowl concentrate (about 5.3 kg) to the target mass | 100 | max (pull 0.5 % max) | g | Analysis, mass balance (GVS-CAL-001 section 8), TRL 3; test at TRL 4 | **At risk:** pull 0.33 % met; 5.3 kg needs 53:1 on the table, likely two passes (STM S15) | R5 |
| PR-006 | UR-005 | Performance | Pedal power | Full throughput shall need no more than the target power at the pedals, at a cadence of 55 to 70 rpm | 60 | max | W | Analysis, power estimate (GVS-CAL-001 section 7), TRL 3; measured at TRL 4 | **At risk:** 48.2 W at 60 G met; 62.8 W at 80 G not; union seal drag assumed | R6 |
| PR-007 | UR-006 | Electrical | Motor option | The MotionCore 250 W reference drive on any 20 to 58 V pack that MotionCore accepts shall run full throughput with at least the target power margin | 3 | min | times the power needed | Analysis (GVS-CAL-001 section 7), TRL 3 | Met on paper: 5.2 times at 60 G, 4.0 times at 80 G; 0.55 kWh per shift | R7 |
| PR-008 | UR-007 | Performance | Water use and quality | Total water at 200 kg/h shall not exceed the target, and the fluidization supply shall tolerate recirculated water with fine silt (filtered to at most a third of the 1.0 mm hole size) | 1.5 | max | m3/h | Analysis, water balance and supply (GVS-CAL-001 sections 4 and 6), TRL 3 | Met on paper: 1.19 m3/h; 120 mesh screen filter on the fluidization hose (GVS-DEC-001 F2); with the 3/4 in valve and rotameter (F6), 12.6 kPa at the union and 10.0 kPa net at the lowest ring at 600 rpm at mid-tank | R8 |
| PR-009 | UR-008 | Physical architecture | Parts cost | Parts cost, excluding the MotionCore module and battery, shall be reported against the value-engineering target (a hypothetical control target, not a limit; Amish, 2026-10-01) | 455 | reported, not capped | USD | Analysis, priced BOM (GVS-CAL-001 section 12), TRL 3 | Estimated cost $594: **over the value-engineering target by USD 139** | R9 |
| PR-010 | UR-009 | Materials | Local workshop build | Every part shall be made with welding, drilling and hand tools, with no lathe; the bowl liner cast in a printed mold | 0 | none | parts needing a lathe | Design review of every part (GVS-BLD-001), TRL 3; build at TRL 4 | Met (design review); casting route unproven (STM S25) | R10 |
| PR-011 | UR-010 | Packaging and transport | Transport mass | The machine shall break into loads carried by two people and weigh no more than the target in all (restated by Amish on 2026-10-01, GVS-DDR-003 A1), assembled with hand tools in 30 min or less | 100 | max (each load 30 max) | kg | Analysis, mass estimate (GVS-CAL-001 section 11), TRL 3; weighed at TRL 4 | **At risk:** 99.6 kg in six loads, heaviest 27.3 kg, only 0.4 kg of margin on an estimate (independent review); assembly time not verified | R11 |
| PR-012 | UR-011 | Safety | Guards, speed and stopping | The bowl shall run only under its lid guard; belts, chains and the table head shall be guarded; with the motor, bowl speed shall be capped at 900 rpm by the ratio and the MotionCore limit; with the pedals, the bowl, jacket and rings shall keep a burst safety factor of at least 10 at 1,200 rpm with the speed shown; the bowl shall stop within 15 s of stopping the drive (restated per GVS-DDR-002) | 10 | min (stop 15 s max; motor 900 rpm max) | safety factor | Design review, burst calculation (GVS-CAL-001 section 10), TRL 3 | Met on paper: guards, lid interlock and disc brake (0.6 s stop); motor capped; lowest safety factor 16 at 1,200 rpm | R12 |
| PR-013 | UR-012 | Usability | Quick, secure clean-up | The bowl concentrate shall be flushed into a lockable container without tools within the target time, and the table concentrate shall drop into a lockable box | 5 | max | min | Design review, TRL 3; timed trial at TRL 4 | Met on paper: toolless lid clamps; flush container and concentrate box with padlock hasps (GVS-DEC-001); time not verified | R13 |
| PR-014 | UR-013 | Materials | Liner life and replacement | The bowl liner and riffles shall be replaceable in 30 min, with a liner life of at least the target | 500 | min (replace in 30 min max) | h | Wear data for cast polyurethane on quartz, TRL 4 | Not verifiable at TRL 3 (STM S29) | R14 |
| PR-015 | UR-011 | Safety | Stability with a full tank | The machine with a full header tank shall stand on a slope of at least the target in any direction without tipping (criterion decided by Amish on 2026-10-03, GVS-DEC-001), and the tank post and braces shall not yield at the side push that tips it | 10 | min | degrees | Analysis, tipping and post check (GVS-CAL-001 section 11), TRL 3 | Met on paper: 13.1 degrees with the 560 mm drum (GVS-DEC-001 F1); post safety factor 2.1 at a 185 N push; sway of the full tank near the table drive frequency to decide (GVS-DEC-001 O3) | none |
| PR-016 | UR-011 | Safety | Containment of a liner fragment | The tub and lid shall contain a quarter of the liner and shell thrown off at the highest reachable speed (decided by Amish on 2026-10-01: check by calculation before any spin test; steel band only if the check fails) | 1200 | min | rpm | Analysis (GVS-CAL-001 section 10), TRL 3; impact test before any spin test, TRL 4 | **At risk:** contained face first (57 J against 40 J); not shown edge first (14 J against 22 J at 900 rpm) or for a quarter of the whole bowl group (125 J); band option awaiting Amish (GVS-DEC-001 O2) | none |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- Ore is milled to below 2 mm by the user's existing mill and screened on the GravitySort hopper screen.
- Free, liberated gold in the 38 to 1,000 um range. Gold locked in sulfides or finer than about 20 um is lost to tailings by any gravity method, so PR-004 applies to free gold only.
- Reference ore for the daily balance: 5 g/t, 1.55 t per shift (7.75 g of gold). Real grades vary widely (about 1 to 20 g/t).
- Healthy adult pedalling at 60 W or less for sessions of about 1 h, with operators taking turns.
- Budget: the $455 in `project.yaml` is a value-engineering target, a hypothetical control target and not a limit (Amish, 2026-10-01); it was raised from $350 to $450 on 2026-09-25 and to $455 on 2026-09-26 (GVS-DDR-002). It covers GravitySort parts. The MotionCore kit and reference motor ($335: $265 kit plus $70 motor, per MTC-CAL-001) and a battery are shared lab components, budgeted with MotionCore.
- The pack for the motor option is left to the user (GVS-DDR-001 item 6).

## Changes to requirements decided by Amish

- 2026-09-25 (GVS-DDR-002): R9 target $350 to $450; R12 restated for the pedal drive (burst safety factor of 10 or more at 1,200 rpm plus the speed display); R11 target kept at 80 kg with the lighter frame tube.
- 2026-09-26: R9 target $450 to $455 (budget approved).
- 2026-10-01 (GVS-DDR-003, A1): R11 restated from 80 kg or less to 100 kg or less, every load 30 kg or less.
- 2026-10-02 (GVS-DEC-001): R2 restated as 200 kg/h of feed time, about 1.55 t per eight-hour shift with three flush stops.
- 2026-10-03 (GVS-DEC-001): the tipping criterion behind PR-015, a 10 degree slope in any direction with a full tank.

## Changes on 2026-10-25 (kit 1.8 pipeline; not decisions by Amish)

- The R numbers became PR numbers, traced to GVS-URS-001; no target changed.
- PR-015 and PR-016 written down from decisions Amish had already made (2026-10-03 and 2026-10-01).
- PR-008 now names water quality for the fluidization holes, because the STEM check found that the design had no filter (STM S24; filter added under the standing instruction of 2026-10-23, GVS-DEC-001 F2).
