---
doc_id: GVS-FEA-001
title: GravitySort feasibility assessment
project: GravitySort
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "First issue (kit 1.8 pipeline), closed at TRL 3 against the STEM check, GVS-CAL-001 v0.9, the build plan and the BOM"
---

# GravitySort feasibility assessment

GravitySort is feasible on paper as a workshop-built, pedal-driven concentrator: every physical claim in the STEM check sits within known science or is plausible pending a test, the constructable design closes with welding, drilling and bought parts, and the main open questions are performance (fine-gold retention, table ratio) and two safety and mass margins that only testing or Amish's decisions can close. Method: STANDARDS section 23. Evidence: GVS-STM-001, GVS-CAL-001, GVS-BLD-001, `bom/bom.csv`, `cad/fidelity.json`.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design (physics) | Bowl speed, G, settling, fluidization head, power, burst, critical speed, braking and tipping all check by first-order calculation; five details failed and were fixed under the standing instruction of 2026-10-23 (drum height, filter, buffer rating, gold balance, the climb to the rings found by the independent review) and one by the detailed CAD (head gussets) | High | Fine-gold retention in the bed (STM S3; upflow near minimum fluidization of 75 um grains) and table ratio (S15) need tests; critical speed on the real frame 1,274 to 1,976 rpm (S8); full-tank sway near the table frequency (S33, O3); pedal power at 80 G exceeds 60 W (PR-006) | GVS-STM-001; GVS-CAL-001 sections 2 to 11 |
| Safety | Guards, lid interlock, disc brake with parking latch, speed display and a burst safety factor of 16 at sprint speed; stands on 13.1 degrees with a full tank | Medium | Containment of a liner fragment is shown face first but not edge first (PR-016 at risk; steel band option to Amish, GVS-DEC-001 O2); guard openings against ISO 13857 not yet checked (REG G5) | GVS-CAL-001 section 10; GVS-RSK-001 |
| Materials | Mild steel tube and plate, HDPE drums, PU liner on GFRP, bought bearings and bicycle parts | Medium | PU liner life on quartz unknown (PR-014); hand-laid GFRP quality decides the burst margin; painted steel in a wet splash zone needs upkeep | GVS-STM-001 S7, S29 |
| Manufacturing and assembly | Every part has a making sketch and an assembly step; no lathe; D3 model with every fastener and weld passes the fidelity check for all three options | High | Casting the liner on a six-segment printed core is untried (STM S25); used bevel gearbox hard to source (quarter-turn belt option in DEC) | GVS-BLD-001; `cad/fidelity.json` |
| Power and controls | Pedal baseline (48 W at 60 G) with the MotionCore 250 W option (5.2 times margin); no electronics of its own beyond a bicycle computer | High | Rider effort at 80 G; motor pack energy 0.55 kWh per shift is the user's choice | GVS-CAL-001 section 7 |
| Water | 1.19 m3/h, gravity-fed from a 1.7 m post, just meeting the proposed 10 kPa net at every ring at mid-tank with 3/4 in valve and rotameter (F6); filter protects the 1.0 mm holes; flow at the low end of commercial practice (O5) | Medium | Sites without an upstream source need a pump (site rule decided 2026-10-02); filter must be flushed when the rotameter flow drops | GVS-CAL-001 sections 4 and 6 |
| Supply of parts | Steel, bicycle parts, V-belts, bearings, HDPE drums and irrigation fittings are sold in mining towns; the liner resin and rotary union are specialist | Medium | Union seal drag and price unconfirmed; resin supply for PU casting to check in Colombia | `bom/bom.csv`; GVS-DEC-001 items to confirm |
| Cost | $594 in parts against the $455 value-engineering target | Medium | USD 139 over the target; savings listed in GVS-DEC-001 (quarter-turn belt, used bearings, bushes) | GVS-CAL-001 section 12; GVS-MKT-001 |
| Mass and transport | 99.6 kg in six loads, heaviest 27.3 kg (estimate) | Low | 0.4 kg under the 100 kg of PR-011; the model's solid volume gives more (see GVS-CAL-001 section 11 note), so R11 is effectively at risk until parts are weighed | GVS-CAL-001 section 11; `cad/fidelity.json` |

Ratings: High, Medium, Low.

## Verdict

Feasible to build and test as a TRL 4 prototype once Amish decides the open items in GVS-DEC-001 (concept selection O1, containment band O2). No aspect is rated infeasible.
