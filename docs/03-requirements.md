---
doc_id: GVS-REQ-001
title: GravitySort requirements
project: GravitySort
doc_type: Requirements
version: "0.2"
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
---

# GravitySort requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs. They will be checked by calculation at TRL 3 and revised after co-design sessions. Recovery can only be verified by testing with real or spiked ore, which is TRL 4 work.

Table 1. Requirements. Status compares the concept estimates in GVS-PRC-001 with each target.

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status |
| --- | --- | --- | --- | --- |
| R1 | Use no mercury | No amalgamation step, no mercury-coated plates or traps, no step that needs mercury to recover gold from the concentrate | Design review of the flowsheet | Met by design |
| R2 | Process a small group's daily ore | 200 kg/h or more of ore milled to below 2 mm, as slurry of 25 to 35 % solids, for 8 h (1.6 t per day) | Bowl capacity and cycle calculation | Met on paper (estimate) |
| R3 | Hold fine gold in the bowl | Bowl acceleration adjustable from 40 to 80 G at the riffle rings (about 600 to 850 rpm at 100 mm radius), with speed shown to the operator | Drive ratio and speed calculation | Met on paper |
| R4 | Recover fine gold | Of free gold in the screened feed: 80 % or more of 75 to 1,000 µm gold and 50 % or more of 38 to 75 µm gold in the bowl concentrate; 60 % or more of all gold in the ore to smelted gold overall | Test with spiked or characterized ore (TRL 4) | **Not verifiable at TRL 2 or 3; at risk** |
| R5 | Make a concentrate that can be smelted without mercury | Bowl mass pull 0.5 % or less of feed; shaking table reduces one day's bowl concentrate (about 5 kg) to 100 g or less | Mass balance calculation; later test | Met on paper (estimate) |
| R6 | Run on pedal power | Full throughput at 60 W or less at the pedals, at a cadence of 55 to 70 rpm | Power estimate from slurry, fluidization water and bearing losses | Met on paper (about 45 W estimated); **at risk** until losses are measured |
| R7 | Run on a small motor | Full throughput from the MotionCore 250 W reference drive on a 24 to 48 V pack, with at least 3 times power margin | Power estimate | Met on paper |
| R8 | Use little water | 1.5 m3/h or less at 200 kg/h, and tolerate recirculated water with fine silt | Water balance calculation | Met on paper (about 1.2 m3/h estimated) |
| R9 | Stay within the concept budget | Parts $350 or less, excluding the MotionCore module and battery | Priced BOM | **Not met** (about $437 estimated) |
| R10 | Be built in a local workshop | Welding, drilling and hand tools only; no lathe; bowl liner cast in a printed mold | Design review of every part | Met on paper; bowl casting route unproven |
| R11 | Travel to site | Breaks into loads of 30 kg or less, carried by two people; total 80 kg or less; assembled with hand tools in 30 min or less | Mass estimate from the model | Met on paper (about 75 kg in four loads, estimate) |
| R12 | Guard every moving part | Bowl covered by a lid guard during running; belts, chains and the table head fully guarded; bowl speed limited to 900 rpm or less by gearing (pedal) or by the MotionCore speed limit (motor); bowl stops within 15 s of stopping the drive | Design review and safety checklist | Partly met; bowl brake not yet designed |
| R13 | Clean up quickly and securely | Bowl concentrate flushed into a lockable container in 5 min or less without tools; table concentrate drops into a lockable tray | Design review; later timed trial | Met on paper |
| R14 | Last in abrasive service | Bowl liner and riffles replaceable in 30 min; liner life 500 h or more (estimate to be checked) | Wear data for cast polyurethane; later test | Not verifiable at TRL 2 |

## Assumptions

- Ore is milled to below 2 mm by the user's existing mill and screened on the GravitySort hopper screen.
- Free, liberated gold in the 38 to 1,000 µm range. Gold locked in sulfides or finer than about 20 µm is lost to tailings by any gravity method, so R4 applies to free gold only.
- Reference ore for the daily balance: 5 g/t, 1.6 t per day. Real grades vary widely (about 1 to 20 g/t).
- Healthy adult pedalling at 60 W or less for sessions of about 1 h, with operators taking turns.
- Budget: the $350 in `project.yaml` covers GravitySort parts. The MotionCore module (about $325 for its reference kit, per the MotionCore README) and a battery are shared lab components, budgeted with MotionCore. Whether GravitySort's budget should change is proposed, awaiting Amish (see `docs/REVIEW.md`).
