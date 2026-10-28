---
doc_id: GVS-RSK-001
title: GravitySort risk register and hazard analysis
project: GravitySort
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First issue (kit 1.8 pipeline): project risk register, preliminary hazard analysis and first-pass design FMEA for the constructable design (option A) at P3"
---

# GravitySort risk register and hazard analysis

The top project risk is that the fluidized bowl does not hold fine gold from real feed as well as the paper case assumes, which only a test with characterized ore can settle; the top hazards are the spinning bowl (entanglement, a liner fragment at speed) and a full header tank tipping the machine. Method: STANDARDS section 23 and the risk assessment approach of ISO 12100 (GVS-REG-001 G4). Likelihood, impact, severity, occurrence and detection are scored 1 (low) to 5 (high).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Fine-gold recovery below PR-004 | Bed packs or washes out fine gold; feed rich in heavy minerals saturates the rings before the 2 h flush | Miners see no gain over sluices; adoption fails | 3 | 5 | Design lead | Spiked-ore test at TRL 4 before any field trial; adjustable fluidization flow and flush interval |
| P2 | Table cannot reach 100 g from 5.3 kg (PR-005) | Heavy-mineral concentrate, small table | More than 100 g to smelt; borax use and losses rise | 3 | 3 | Design lead | Two passes; tune stroke, tilt and bump stop setting at TRL 4 |
| P3 | Pedal effort too high at 80 G (PR-006) | Seal drag and slurry power rise with speed squared | Riders tire; motor becomes the default | 3 | 2 | Design lead | Run at 60 G; measure union drag; motor option |
| P4 | Over the value-engineering target | Constructable design and fixes add parts ($594 against $455) | Harder for a small group to afford | 4 | 3 | Project lead | Savings in GVS-DEC-001 (quarter-turn belt, used bearings, bushes); price check in Colombia |
| P5 | Mass over 100 kg (PR-011) | 0.4 kg margin on the estimate; the model's solid volume reads higher | Not carried by two people in six loads | 3 | 3 | Design lead | Weigh parts at TRL 4; savings of about 16 kg in GVS-DDR-003 A1 (b) |
| P6 | PU liner cannot be cast reliably or wears fast (PR-010, PR-014) | No local PU casting experience; abrasive quartz | Bowl down time; cost of liners | 3 | 4 | Workshop partner | Trial casting at TRL 4; bought liner as fallback |
| P7 | Bought parts not available locally | Rotary union, bevel gearbox, resin | Delay or redesign | 3 | 3 | Project lead | Items to confirm list in GVS-DEC-001; quarter-turn belt instead of the gearbox |
| P8 | Partner engagement does not happen | No agreement yet with the cooperative introduced through the Alliance for Responsible Mining | Requirements stay unvalidated | 3 | 4 | Project lead (Amish) | Outreach is Amish's action (GVS-DEC-001, 2026-10-02) |
| P9 | Equipment used on mercury-contaminated tailings | Old tailings reprocessed at legacy sites | Mercury spread through the bowl, water and table | 2 | 5 | Partner organization | Safety rule and training; test tailings before use |
| P10 | Concentrate theft | Valuable concentrate at remote sites | Loss to the group; conflict | 3 | 3 | Partner organization | Hasps on both containers; two-person rule proposed to the partner |

## Preliminary hazard analysis

Table 2. Hazards (option A, constructable design).

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Entanglement in belts, chains and pulleys | Unguarded drive, loose clothing or hair | Crushed fingers, scalping | 4 | 2 | Belt, chain and table guards fitted before running (PR-012); guard openings to check against ISO 13857 (REG G5) | Low to medium until G5 is checked |
| H2 | Contact with the spinning bowl | Lid opened while the bowl coasts (about 20 s) | Hand injury | 4 | 2 | Lid interlock pin on the brake cable; disc brake with parking latch stops it in 0.6 s | Low |
| H3 | Liner or shell fragment at speed | Debonded or cracked liner; over-speed by a sprinting rider | Impact injury | 5 | 1 | Burst safety factor 16 at 1,200 rpm; liner check before every run; speed display; containment shown face first only (PR-016) | Medium until the impact test or the band decision (GVS-DEC-001 O2) |
| H4 | Machine tips with a full tank | Uneven ground, side push on the tank, climbing on the frame | Crush injury | 4 | 2 | Tank on the centre line, braced post; stands on 13.1 degrees (PR-015); fill only standing level | Low |
| H5 | Table head and pitman | Hands near the eccentric or bump stop while running | Pinched fingers | 3 | 2 | Table belt guard; stop adjusted only with the belt slack | Low |
| H6 | Slips and drowning | Slurry underfoot; open settling ponds and pits | Falls; drowning | 5 | 2 | Boots with grip; fence ponds (site rule with the partner) | Medium (site dependent) |
| H7 | Mosquito breeding in ponds | Standing water in settling ponds and pits | Malaria and other vector-borne disease | 4 | 3 | Pond management with the partner (cover, drain, recirculate); STM S30 | Medium (site dependent) |
| H8 | Arsenic and lead in concentrate | Arsenopyrite and galena in heavy-mineral concentrate | Poisoning by ingestion | 4 | 2 | Gloves, hand washing, no eating at clean-up (STM S31) | Low to medium |
| H9 | Mercury cross-contamination | Processing old amalgamation tailings | Mercury exposure and spread | 5 | 2 | Never use with mercury or untested tailings (STM S28) | Low with the rule kept |
| H10 | Smelting heat and borax | Smelting outside the machine at about 1,065 C; borax is Repr. 1B (REG G10) | Burns; reproductive toxicity | 4 | 2 | Furnace, tongs, face shield, ventilation, outdoors; partner's smelting procedure | Medium (outside this design) |
| H11 | Battery and electrical (motor option) | Lithium pack, controller | Fire, shock | 4 | 1 | MotionCore safety section; hardwired e-stop; mechanical brake still used | Low |
| H13 | Full tank sways when the table runs | Post above the brace node about 3.5 Hz, table drive 4.0 to 5.0 Hz with impact harmonics (STEM S33) | Weld fatigue, tank falling, tipping | 4 | 2 | Interim rule: run the table with the drum drained; raise the brace node (GVS-DEC-001 O3) | Medium until O3 is decided |
| H12 | Manual handling | Loads up to 27.3 kg carried to site | Back injury | 3 | 3 | Two-person carries, loads 30 kg or less (PR-011) | Medium |

## Design FMEA (first pass, P3)

Table 3. Failure modes, option A. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Bowl liner (BOM 3) | Hold the bed in the riffle rings | Debonds from the shell or cracks | Fragment risk; bed lost | Poor casting, wear, impact | 5 | 3 | 3 | 45 | Visual and tap check before every run; impact test at TRL 4; band option (O2) |
| F2 | Fluidization holes (BOM 3) | Keep the bed loose | Holes block, or flow too low to loosen a coarse bed | Bed packs; recovery falls | Silt and sand in recirculated water; 2.7 mm/s upflow near the minimum fluidization of 75 um grains | 4 | 3 | 3 | 36 | Screen filter fitted (F2 fix); flush the filter when the rotameter drops; hole check at each flush |
| F3 | Rotary union (BOM 4) | Pass water into the turning spindle | Leaks or seal drag rises | Water loss, more pedal power | Silt in the seal, wear | 3 | 3 | 2 | 18 | Filter upstream; datasheet seal drag; spare seal kit |
| F4 | Header supply (BOM 13) | Give 8.1 kPa at the union | Tank runs low | Fluidization weak at the lower rings | Upstream supply interrupted | 3 | 3 | 2 | 18 | Keep the tank above half full; rotameter visible to the operator |
| F5 | Disc brake and interlock (BOM 18) | Stop the bowl; lock the lid | Cable stretches; pin misses | Lid opens while coasting | Wear, poor adjustment | 4 | 2 | 3 | 24 | Check the interlock at each flush; adjust the cable |
| F6 | V-belts (BOM 10) | Drive the bowl and table | Slip or break | Bowl slows; G falls | Wear, wet belts | 2 | 3 | 2 | 12 | Speed display shows it; spare belts |
| F7 | Spindle bearings (BOM 5) | Carry the spindle | Wear, seizing | Vibration, stop | Slurry ingress | 3 | 2 | 3 | 18 | Standpipe shields the upper bearing; grease interval at TRL 4 |
| F8 | Table bump stop (BOM 22) | Make the stroke asymmetric | Buffer tears or loosens | Gold stops walking | Fatigue at 270 strokes/min | 3 | 3 | 2 | 18 | Buffer rated 800 N (F3 fix); lock nuts; spare buffer |
| F9 | Tank post and braces (BOM 1) | Hold the full tank 1.7 m up | Weld cracks | Tank falls; tipping | Fatigue from sway near the table drive frequency (about 3.5 Hz against 4 to 5 Hz) and knocks | 4 | 3 | 3 | 36 | Raise the brace node (O3); drain the drum before running the table; weld inspection |
| F10 | Pedal drive (BOM 8, 9) | Turn the jackshaft | Chain off, freewheel slips | Stop; no harm | Wear, misalignment | 2 | 3 | 1 | 6 | Chain case; tension check |
| F11 | Frame members (BOM 1) | Carry bearings and loads | Bearing misalignment; first critical speed lowered by member compliance (1,274 to 1,976 rpm) | Vibration, belt wear; resonance near a sprint speed | Spindle member deflection 0.73 mm | 4 | 2 | 3 | 24 | Tap test and alignment check on the first frame (O4); never run above 900 rpm |
| F12 | Concentrate box and flush container hasps (BOM 16, 23) | Secure the concentrate | Forced open | Theft | Weak hasp | 3 | 2 | 2 | 12 | Two-person rule proposed to the partner |
