# Review note: GravitySort

## Session 2026-10-01: table bump stop in the model, drawings and build plan

Amish asked: "gravitysort - update the documentation, CAD work and picture renderings", to carry out the bump stop he accepted earlier the same day (GVS-DDR-003, A2; register, Decisions made).

### What was done

- **Design.** The stop sits at the return end, the far end of the forward stroke where the deck turns back toward the head, because gold walks toward the concentrate box only if the deck stops sharply while moving that way. Parts: a stop bracket (25 x 25 x 1.5 mm tube arm 244 long, 40 x 66 x 6 mm foot bolted on top of the frame's table-end top rail 205 mm behind the centre line with two M8, 40 x 61 x 6 mm upright); a bought rubber buffer 40 mm across and 30 mm long, about 55 Shore A, M8 female thread, rated 800 N or more, on an M8 stud 45 long with a lock nut each side of the upright; a 6 mm steel striker angle (40 wide, legs 40 and 70) screwed under the deck's head end at its back edge. Setting: zero where the buffer just touches at full forward travel, 3 mm in to start, 2 to 6 mm useful, 0 to 8 mm available. The nuts are reached with a 13 mm spanner from behind the machine.
- **Knock-on change needed to make the stop work.** A rigid pitman drags the deck through the whole circle of the eccentric, so it can never strike anything. The pitman pin now works in a 12 x 20 mm slot in the deck cheeks (8 mm of free play toward the far end), and the plywood legs are set leaning about 5 mm so they press the deck on the buffer with about 200 N. The pin pulls the deck toward the head; the legs push it forward into the stop. This keeps the accepted option (a) and the concept's "spring return"; it is recorded in GVS-DDR-003 Table 2. Amish may want to note it, since it is a second part of the table changed for the stop.
- `cad/src/model.py`: stop bracket, buffer with stud and nuts, striker, and the cheek slot; 13 new checks (contacts, 15 mm clearance at the head end of the stroke, clear of the legs, deck, head and pitman, spanner room); **115 of 115 pass**. STEP and STL re-exported.
- `docs/04-calcs/sizing.py`, `results.csv`, `docs/04-calcs/01-sizing.md` (GVS-CAL-001 v0.6): section 9 sizes the stop (Table 4); mass and cost updated.
- `bom/bom.csv`: line 21 (bracket and striker, make, $6) and line 22 (buffer, stud and fixings, buy, $5); `bom/bom-notes.md` updated.
- `cad/src/build_plan_media.py`: new making sketch GVS-DWG-121 (bracket and striker), new joint 15 (the stop), step 16 redrawn with the stop, steps 17 and 18 and the overview redrawn (the stop is in group 22); sketches GVS-DWG-114 (cheek slot), 116 and 117 to Rev P2; joint 10 subtitle.
- `cad/src/sheets.py`: general arrangement GVS-DWG-001 to Rev P4. `cad/src/concept_media.py`: concept media regenerated (blueprint GVS-DWG-010 Rev P3; the stop is item 21 in the exploded view).
- `docs/05-build-plan.md` (GVS-BLD-001 v0.3): section 2 row, section 3.15 (slot), section 3.16 (making, fitting and setting the stop, with Figures 29 and 30), 3.17 check, bought buffer, step 14 and step 16, a first check for the stop, safety stop S7 (before the table runs); figures renumbered.
- `docs/02-concept.md` (GVS-PRC-001 v0.8): component 15 and new row 21, 22; mass and cost. `docs/03-requirements.md` (GVS-REQ-001 v0.8): R9 and R11 values. `docs/decisions/0003-design-for-construction.md` (GVS-DDR-003 v0.3): A2 carried out. `docs/06-design-decisions.md` (GVS-DEC-001 v0.3): follow-up note removed, buffer added to the items to confirm, Value engineering updated. `README.md`: mass and cost.
- `cad/src/product_model.py`: the bump stop added (bracket, buffer, stud and nuts, striker) at the model's positions; the file builds (97 parts).

### Key results

- Bump stop at 270 strokes/min, 17 kg moving, set 3 mm in: stroke 12 mm, strike at 0.17 m/s, **0.24 J per stroke** (1.1 W), buffer squeezed 3.2 mm (11 %, limit 20 %), 539 N peak, **2.1 G at the stop against 0.6 G at the head end (3.4 times)**. Across 2 to 6 mm: 0.18 to 0.37 J, 3.1 to 3.9 times, peak force under 600 N, pin pull at most 593 N.
- Mass **96.5 kg** (was 95.7), heaviest load 25.2 kg: R11 still met on paper.
- Value-engineering target: USD 455. Estimated cost of the constructable design: USD 569 (USD 114 over the target).
- Requirements unchanged otherwise: none unmet; R2, R5, R6 at risk; R4, R14 not verifiable at TRL 3.

### Stale, to update on Amish's Mac (Blender)

- `media/render-*.png` photoreal renders, `media/card.png` and `media/social-preview.png` do not show the bump stop (and still show the concept table stand, as noted before). `cad/src/product_model.py` now includes the stop, so a re-render with `/render-product` will show it; the rest of that model's table end is still the concept stand and head.

### Decisions proposed and awaiting Amish

- None new. The cheek slot and the leaning legs are how the accepted stop is made to work, not a new choice; if Amish prefers, the toggle head (A2, option b) remains the fallback.

### Safety

- The striker and buffer close with up to about 600 N at every stroke: a pinch point. The plan says to set the stop only with the table belt slack and the head turned by hand (section 3.16, safety stop S7). The stop is outside the table belt guard, under the deck's back edge.

### Recommended next step

- Re-render the photoreal set and cards on the Mac. The stop setting (2 to 6 mm), leg stiffness and buffer rate are estimates to be tuned in the first table test, which is TRL 4 work and on hold under the TRL 3 cap.

## Session 2026-10-01: recommendations accepted

Amish, 2026-10-01: "i agree with your recommendations for both GrowRider and GravitySort". This answers the recommendations in the design decisions register (GVS-DEC-001 v0.1), including GVS-DDR-003. Items whose recommendation was "None yet" or "Decide with the partner" were not decided and stay open. trl stays 3; no build or test work was done.

### Accepted, as recommended

| Register item (v0.1) | Decision |
| --- | --- |
| 1 | GVS-DDR-003 accepted: design-for-construction changes P1 to P15 and their knock-on changes |
| 2 | R11 restated: total 100 kg or less, every load 30 kg or less (was 80 kg in all); try the savings of about 16 kg at TRL 4 |
| 3 | Asymmetric table stroke: adjustable rubber bump stop at the return end for the prototype; a toggle head only if the first test shows it is not enough |
| 4 | Pedal position: keep the bicycle-style seat, seat post adjustable; check with two riders at TRL 4 |
| 9 | Liner fragment containment: check by calculation before any spin test; add a steel band round the tub only if the check fails |
| 10 | Lid: keep the plain 10 mm HDPE lid, no sight window |
| 12 | Cranks at 100 degrees from top dead centre is a render pose only |

### What changed

- `docs/06-design-decisions.md` (GVS-DEC-001 v0.2): the seven items moved to Decisions made, dated 2026-10-01, with Amish's words and the record; open items renumbered 1 to 5.
- `docs/decisions/0003-design-for-construction.md` (GVS-DDR-003 v0.2, status Draft as for the pilot repos): status line now "accepted" with Amish's words; Table 3 marked as accepted as recommended; a consequence added for A1 to A3.
- `docs/03-requirements.md` (GVS-REQ-001 v0.7): R11 restated to 100 kg or less in all, loads 30 kg or less; status not met to **met on paper** (95.7 kg, heaviest load 25.2 kg); a "Change decided on 2026-10-01" section added; R11 removed from "Still proposed".
- `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: the R11 check uses 100 kg; re-run, and only the R11 row changed.
- `docs/04-calcs/01-sizing.md` (GVS-CAL-001 v0.5): summary, section 11 and Table 6 show R11 met on paper against the restated total.
- `docs/02-concept.md` (GVS-PRC-001 v0.7): summary and the size and mass row show R11 met on paper; component 15 records the bump stop decision; the decision records paragraph names GVS-DDR-003 and the register.
- `docs/05-build-plan.md` (GVS-BLD-001 v0.2): section 2 says GVS-DDR-003 is accepted. No open decisions were added.
- PDFs regenerated for GVS-DEC-001 v0.2, GVS-DDR-003 v0.2, GVS-REQ-001 v0.7, GVS-CAL-001 v0.5, GVS-PRC-001 v0.7 and GVS-BLD-001 v0.2; the superseded PDFs removed.

Requirements (GVS-CAL-001 v0.5): none unmet, three at risk (R2, R5, R6), two not verifiable at TRL 3 (R4, R14), eight met on paper or by design review; R9 is USD 103 over the value-engineering target.

### Still to do for the accepted decisions

- The rubber bump stop is not yet in the model, the making sketches or the build plan (section 3.16 and step 16 would carry it). Adding it needs a model change, a regenerated picture set and a first check for the stroke; it is left for the next design session.
- The containment calculation (decided item 9) is still to be done; safety stop S4 of the build plan already requires it before any spin above hand speed.

### Still open (GVS-DEC-001)

1. Head for the fluidization supply (1.7 m tank post or a small pump).
2. Water from the settling pond at pedal-only sites.
3. R2 throughput margin.
4. First co-design partner and country.
5. Concentrate security in practice.

The 10 items to confirm when parts are bought are unchanged.

### Recommended next step

Add the rubber bump stop to the model and the build plan, and do the containment calculation, once Amish asks for that session. Regenerate the product renders on the Mac. TRL 4 remains on hold by Amish's instruction.

## Session 2026-10-01: prototype build plan and design for construction (kit 1.7.0)

Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, root `CLAUDE.md` from `.kit/CLAUDE.md`). The design was made constructable under Amish's 2026-09-30 instruction ("If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations."), and the illustrated build plan and the design decisions register were written. Every change is in `docs/decisions/0003-design-for-construction.md` (GVS-DDR-003, Draft, open for Amish's review).

### Design changes made for construction

1. Frame: the low stretchers become lower side rails (255 mm up); the gearbox and spindle members lie in pairs on top of them, either side of each vertical shaft (the concept's members floated, and two were crossed by the spindle and the gearbox shaft); tub members hang on four drop posts; end post, low end member and head member added. 14.5 m of tube (was 11.75 m).
2. Bearings: 150 x 130 x 6 mm plates welded under the spindle pair and the tub pair; the flanged bearings hang under them (centres 255 and 420 mm, 165 mm apart).
3. Spindle: 25 x 2 mm stainless tube carrying the fluidization water, with a 1/2 in BSP nipple welded in its foot (was a solid shaft); first critical speed 2,710 rpm (2.3 times the sprint speed).
4. Bowl fixing: pinned 25 mm bore flange hub, four M6 bolts with 12 mm spacers into nuts cast in the liner; bonded closing ring at the jacket top (the jacket was open).
5. Liner core printed in six segments round a key (the riffle rings are undercuts).
6. Tub: 63 mm standpipe in a rubber grommet over the upper bearing; 75 mm tailings pipe through a rubber grommet in the back wall (the launder box ran through an uncut wall and into the frame); four M8 floor bolts.
7. Feed pipe stops 15 mm above the lid, so the lid lifts off; hopper bottom opened; hopper sits in a ring on a support post bolted to the front top rail.
8. Pedal drive: bottom bracket at 438 mm, 100 mm above the jackshaft (338 mm, on pillow blocks on the gearbox pair), so the chain clears the frame; outrigger detailed and bolted to the frame end by two plates; saddle about 910 to 960 mm.
9. Gearbox stands across the gearbox pair; its output shaft goes down between them.
10. Table belt plane moved outside the frame front (the take-off pulley hit the members and the belt looped round a frame rail).
11. Motor option on a bolt-on cradle behind the frame (the hub motor enclosed its chain).
12. Guards: bowl belt guard on hangers, chain case seated on the gearbox member, table belt guard added (safety note of 2026-09-26).
13. Water: tank post and cradle drawn; valve on the back of the drum; rotameter on a bracket on the back top rail; hose down the back of the frame to the union (it ran through the drive pulley).
14. Table: plywood flexure legs on a welded base; head plate and shelf bolted to the frame end with pillow blocks, eccentric (15 mm stroke) and pitman; latched belt tensioner as the clutch; tailings launder under the front edge; lockable concentrate box under the far end; wash water pipe.
15. Speed display and brake lever moved to the pedal-end top rail facing the rider; caliper on an L bracket on the spindle member; disc on a flange welded to a shaft collar.

`cad/src/model.py` now models every component and runs 102 constructability checks (`python cad/src/model.py --check`); all pass.

### Files

- `cad/src/model.py` (rewritten: `build_components()`, `checks()`), `cad/src/build_plan_media.py` (new), `cad/src/sheets.py` (GVS-DWG-001 Rev P2 to **P3**), `cad/src/concept_media.py` (key figures, blueprint GVS-DWG-010 P2); STEP and STL re-exported; `media/` concept media regenerated.
- `docs/05-build-plan.md` (GVS-BLD-001 v0.1) with pictures in `docs/05-build-plan/` (overview, frame cut list, 14 joints, 19 steps) and making sketches `cad/drawings/GVS-DWG-101` to `120` (20 sheets).
- `docs/06-design-decisions.md` (GVS-DEC-001 v0.1): 12 open decisions, 10 items to confirm when parts are bought, a Value engineering section, 7 decisions made.
- `docs/decisions/0003-design-for-construction.md` (GVS-DDR-003 v0.1, Draft).
- GVS-CAL-001 v0.4 and `docs/04-calcs/sizing.py` (hollow spindle, new masses, cost against the value-engineering target; `results.csv` regenerated); GVS-REQ-001 v0.6; GVS-PRC-001 v0.6; GVS-PRB-001 v0.6 (budget wording); `bom/bom.csv` (lines 1 to 4, 6, 8, 10, 11, 13 to 19 updated, line 20 added) and `bom/bom-notes.md`; `project.yaml` (`design_state: constructable`, three documents added to `trl_evidence`; `budget_usd` unchanged); `README.md` (links line, budget line, concept figures, "Building the prototype" section).

### Key results

- **R11 not met:** 95.7 kg in six loads against 80 kg (16 kg over); every load is under 30 kg, heaviest 25.2 kg. The concept's 77.3 kg left out several parts and joints.
- **Cost:** Value-engineering target: USD 455. Estimated cost of the constructable design: USD 558 (USD 103 over the target).
- Requirements (GVS-CAL-001 v0.4): one not met (R11), three at risk (R2, R5, R6), two not verifiable at TRL 3 (R4, R14), seven met on paper or by design review; R9 reported against the value-engineering target.
- Unchanged: bowl speed and G, drive ratio, power, water, settling, fluidization supply, burst factors, brake stop time, gold balance.

### Proposed, awaiting Amish

All open items are in the design decisions register (GVS-DEC-001). New this session: accept GVS-DDR-003 (open decision 1); R11 total mass (2: recommend restating the total as 100 kg, keeping loads of 30 kg or less); how to make the table stroke asymmetric (3: recommend an adjustable bump stop); pedal position for different riders (4). Carried over: fluidization head, water pumping, R2 margin, first partner, liner fragment containment, lid window, concentrate security, render crank pose.

### Safety

- The table belt now has a guard; every belt, chain and pulley is guarded in the model.
- The standpipe keeps spilt slurry off the upper bearing.
- Containment of a liner fragment by the tub and lid is still not checked (register item 9); the build plan's safety stop S4 requires it before any spin above hand speed.
- The pedal drive is still not speed-capped; the speed display and the burst margin carry that risk (R12 as restated).

### Stale media (made on Amish's Mac; not regenerated here)

The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept: the old frame and outrigger, the table head on a post, the hose route, the motor inside the frame and the display on the front rail. The design changed visibly, so all of them are stale and need regenerating on the Mac.

### Recommended next step

Amish to review GVS-DDR-003 and the open decisions in GVS-DEC-001, in particular R11 (2) and the table stroke (3). Then regenerate the product renders on the Mac. TRL 4 (building to the plan) stays on hold.

## Session 2026-09-26: budget approved

Amish wrote, in chat on 2026-09-26: "i approve all the budget items." The open budget item (the $5 gap on R9) is decided: budget set to $455 to cover the priced BOM (GVS-DDR-002 v0.2).

- `project.yaml` `budget_usd` $450 to $455; README budget and cost lines updated.
- R9 target $450 to $455; status **not met to met on paper**, with no margin ($455 BOM, MotionCore and battery excluded).
- Requirement counts (GVS-CAL-001 v0.3): none not met, three at risk, two not verifiable, nine met on paper.
- Documents: GVS-PRB-001 v0.5, GVS-PRC-001 v0.5, GVS-REQ-001 v0.5, GVS-CAL-001 v0.3 (`sizing.py` budget constant 450 to 455, script re-run, `results.csv` regenerated), GVS-DDR-002 v0.2; `bom/bom-notes.md`; PDFs rebuilt. No media shows the budget, so none was regenerated.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (GVS-DDR-002 v0.1). GVS-DDR-001 moves to v0.2 with its statuses updated.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| 1 | Budget | `budget_usd` $350 | `budget_usd` $450; R9 target $450; BOM $465 to $455 |
| 9 | R12 restated for the pedal drive: burst safety factor 10 or more at 1,200 rpm plus the speed display, instead of a gearing cap | R12 not met as written | R12 met on paper (lowest factor 17) |
| 10 | Frame, pedal outrigger, table stretchers and head post in 25 x 25 x 1.5 mm tube, then re-estimate | 30 x 30 x 2 mm; 88.3 kg, heaviest load 25.8 kg | 77.3 kg, heaviest load 18.1 kg; R11 met on paper. New frame member check: 61 MPa, safety factor 3.9, 0.73 mm deflection |
| 11a | 3/4 in fluidization hose and about 89 graded 1.0 mm holes | Engineering proposal | Decided; no geometry change |
| 14 | Disc brake with parking latch and lid pin, bicycle computer display, 1.2:1 motor step-up, MotionCore lid switch | Engineering proposals | Decided; no geometry change |
| 2 to 7, 8a | Two stages; fluidized bowl; cast PU liner; pedal baseline with MotionCore option; battery left to the user; borax smelting; partner screening criterion | Adopted for TRL 3, open for review | Decided; wording only |

Files changed: `project.yaml` (budget, DDR-002 in the evidence list); `README.md` (budget, concept numbers, DDR-002 link, safety line, new "What sparked the idea"); `cad/src/model.py` (`tube` 25, `tube_wall` 1.5; cross members and table stretchers follow the tube size) with STEP and STL re-exported; `cad/src/sheets.py` and GVS-DWG-001 Rev P1 to **P2**; `cad/src/concept_media.py` key figure (77 kg) and all of `media/` regenerated; `bom/bom.csv` items 1 ($40 to $32) and 15 ($30 to $28); `bom/bom-notes.md`; `docs/04-calcs/sizing.py` and `results.csv`; GVS-CAL-001 v0.1 to v0.2; GVS-REQ-001, GVS-PRC-001 and GVS-PRB-001 v0.3 to v0.4; GVS-DDR-001 v0.1 to v0.2. The pitch and problem in `project.yaml` are unchanged (no rewording was recommended). `docs/01-problem.md` did not attribute the idea to any ideation session.

The README "What sparked the idea" section now traces the design to the Minamata Convention's call to eliminate whole-ore amalgamation (NRDC summary cited). All drawings, media and PDFs were regenerated with designmolecule.com; superseded PDFs in `docs/pdf/` were removed where they still carried the old domain.

### Requirement status (GVS-CAL-001 v0.2)

| ID | Status | Value |
| --- | --- | --- |
| R9 | **Not met** | $455 against $450 ($5, 1.1 % over) |
| R2 | At risk | 1.55 t per shift after three flush stops; 1.6 t needs 206 kg/h |
| R5 | At risk | Bowl pull 0.33 % met; 5.3 kg per day needs 53:1 on the table, likely two passes |
| R6 | At risk | 48.2 W at 60 G met; 62.8 W at 80 G not met |
| R4 | Not verifiable at TRL 3 | Settling ratio 36 or more for 20 µm flakes; bed behaviour needs testing |
| R14 | Not verifiable at TRL 3 | No wear data |
| R11 | Met (paper) | 77.3 kg in six loads, heaviest 18.1 kg; assembly time not verified |
| R12 | Met (paper) | Brake stop 0.6 s; motor capped; pedal-case burst factor 17 at 1,200 rpm with display; containment not verified |
| R1, R3, R7, R8, R10, R13 | Met (paper or design review) | Unchanged from v0.1 |

Summary: one not met, three at risk, two not verifiable, eight met on paper (was three not met and six met).

### Still awaiting Amish (no recommendation was made)

1. Cost-down options to close the $5 gap on R9: quarter-turn belt instead of the bevel gearbox (about $25), non-fluidized variant (about $45), table later (about $70 deferred). **Decided by Amish, 2026-09-26: budget set to $455 to cover the priced BOM, which closes the gap; see "Session 2026-09-26: budget approved".**
2. The first co-design partner (item 8b).
3. Head for the fluidization supply: a 1.7 m post or a small pump (item 11b).
4. Water pumping from the settling pond at pedal-only sites (item 12).
5. R2 and R5 margins: raise the design feed to about 210 kg/h, or restate R2 as 200 kg/h of feed time (item 13).

### Cross-repo actions (not changed in other repos)

- **MotionCore** (item 14 decided): raise with MotionCore (a) the reference hub motor's no-load speed, assumed 250 rpm at full pack voltage, which sets GravitySort's 1.2:1 step-up; (b) mounting a sprocket on the hub motor's disc mount for a stationary chain drive; (c) a speed-limit setting that maps to 900 rpm at the GravitySort spindle, since MotionCore sets its limit in wheel-speed terms; (d) use of a MotionCore brake input for the GravitySort lid switch.

### TRL 4

TRL 4 remains on hold by Amish's instruction. No build, test, purchasing, PCB or firmware work was done. The checks these decisions point at (bearing alignment on a 25 mm frame, spin-up with the tub and lid as containment, brake stop time) are TRL 4 work and are listed for later only. `trl: 3`, `trl_target: 3`.

## Session 2026-09-25: TRL 3

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (GVS-DDR-001 v0.1): TRL 2 items 2 to 7 and the partner screening criterion (item 8a) adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review; the budget, the partner itself and six new TRL 3 items listed as open.
- `docs/04-calcs/01-sizing.md` (GVS-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `results.csv`: speed and G, throughput with flush stops, water, settling in the bowl, fluidization jacket pressure and supply, power, mass balance, table drive, rotor inertia, burst, spindle, coast-down and brake, transport mass, cost and the gold balance. The script reads `cad/src/model.py` and `bom/bom.csv` and prints every quoted number.
- `cad/src/model.py`: parametric build123d model (frame, hopper, bowl with liner, shell and riffle rings, rotating jacket and rotary union, spindle with bearing units, brake disc and caliper, tub, lid, pedal station, jackshaft and gearbox, belts, guards, MotionCore module and hub motor, tank, table deck, stand and head, tray, speed display). Exports `cad/step/` and `cad/stl/` `gravitysort-assembly`, `gravitysort-bowl` and `gravitysort-table-deck`.
- `cad/src/sheets.py` and `cad/drawings/GVS-DWG-001.svg`, `.pdf`, `.png`: general arrangement, Rev P1, "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION" (the concept sheet keeps GVS-DWG-010).
- `bom/bom.csv`: 19 lines, all priced with suppliers or supplier types; new items 18 (brake and lid interlock) and 19 (speed display); `bom/bom-notes.md` totals against $350 and $450.
- `cad/src/concept_media.py` now builds from the model; every image in `media/` regenerated and checked by eye; temporary `media/_views*` folders deleted.
- Docs updated to v0.3 with revision entries dated 2026-09-25: GVS-PRB-001, GVS-PRC-001, GVS-REQ-001. `project.yaml`: `trl: 3`, `trl_target: 3`, evidence listed; pitch and problem unchanged (no rewording was recommended). `README.md`: TRL 3, concept numbers from GVS-CAL-001, links to the drawing, sizing note and DDR, brake in the components and safety text.

### Requirements (GVS-CAL-001)

Six of fourteen met on paper; three not met; three at risk; two not verifiable at TRL 3.

| ID | Status | Value |
| --- | --- | --- |
| R9 | **Not met** | $465 against $350, and against the $450 recommended at TRL 2 (awaiting Amish) |
| R11 | **Not met** | 88.3 kg in six loads against 80 kg; every load under 30 kg (heaviest 25.8 kg) |
| R12 | **Not met as written** | Gearing cannot cap the pedal drive (900 rpm at a 75 rpm cadence); guards, lid interlock and brake (0.6 s stop, about 20 s coasting) are designed; motor capped by a 1.2:1 step-up and the MotionCore limit |
| R2 | At risk | 1.55 t per shift after three flush stops; 1.6 t needs 206 kg/h |
| R5 | At risk | Bowl pull 0.33 % is met; 5.3 kg per day needs 53:1 on the table, likely two passes |
| R6 | At risk | 48.2 W at 60 G is met; 62.8 W at 80 G is not; union seal drag assumed |
| R4 | Not verifiable at TRL 3 | Settling check passes (ratio 36 or more for 20 µm flakes); bed behaviour needs testing |
| R14 | Not verifiable at TRL 3 | No wear data |
| R1, R10 | Met (design review) | No mercury; no lathe (set-screw inserts, taper bush, printed mold) |
| R3, R7, R8, R13 | Met (paper) | 40 to 81 G over 600 to 850 rpm with a speed display; motor margin 5.2 times; 1.19 m3/h; toolless clamps |

Other key numbers: 165 J stored at 730 rpm (447 J at 1,200 rpm); burst safety factors at 1,200 rpm of 17 (jacket), 30 (shell) and 51 (ring lips); spindle first critical speed about 4,820 rpm; about 89 fluidization holes of 1.0 mm; 3.7 kPa at the rotary union with a 3/4 in hose; 0.55 kWh per shift on the motor.

TRL 2 numbers corrected: pedal power 45 to 48.2 W; stored energy 150 to 165 J; mass 75 to 88 kg; cost $437 to $465; motor energy 0.5 to 0.55 kWh; MotionCore $325 to $335; 1.6 to 1.55 t per shift.

### Decisions recorded (GVS-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: two stages (item 2); fluidized bowl with rotary union, non-fluidized variant documented (3); cast PU liner in a printed mold (4); pedal baseline with the MotionCore option and one time-shared drive (5); battery left to the user (6); direct smelting with borax as the downstream step (7); partner screening criterion (8a). The budget recommendation ($450) was not applied; `budget_usd` stays at $350.

### Still awaiting Amish

1. **Budget (item 1).** Recommended $450 at TRL 2; the BOM is now $465, over both. Cost-down options: quarter-turn belt instead of the bevel gearbox (about $25), non-fluidized variant (about $45), table later (about $72 deferred).
2. **First co-design partner (item 8b).** Not named.
3. **R12 pedal speed cap (item 9).** Recommendation: reword R12 for the pedal case to rely on the structural margin at 1,200 rpm plus the speed display; alternative is a slip clutch.
4. **R11 mass (item 10).** Recommendation: 25 x 25 x 1.5 mm frame tube (about 7.7 kg less) and a lighter table stand, then re-estimate; alternative is relaxing R11 to 90 kg.
5. **Fluidization supply (item 11).** 3/4 in hose (in the BOM), graded holes, and a 1.7 m post or a small pump for an even 10 kPa at every ring.
6. **Water pumping without power (item 12).** No recommendation yet.
7. **R2 and R5 margins (item 13).** Raise the design feed to about 210 kg/h or restate R2.
8. **Engineering proposals (item 14).** Disc brake with parking latch and lid pin; bicycle computer display; 1.2:1 motor step-up; MotionCore lid switch on a brake input.

### Cross-repo notes (not changed in other repos)

- **MotionCore:** consistent with MTC-DDR-001 and MTC-CAL-001: $265 kit plus $70 reference motor ($335, excluded from the GravitySort total), 20 to 58 V packs, stop category 0 (GravitySort therefore keeps its own mechanical brake), brake inputs used for the lid switch, speed sensor on the spindle. Two assumptions MotionCore does not state: the reference hub motor's no-load speed (assumed 250 rpm at full pack voltage) and mounting a sprocket on its disc mount for a stationary chain drive. The MotionCore speed limit is set in wheel-speed terms, so a GravitySort setting that maps to 900 rpm at the spindle is needed. No conflict found; these are questions for MotionCore, not changes.
- No other shared component (FieldNode, CellGuard, ThermaCart, TwinKit, CalRig) is used. SwapCell is not named (item 6).

### Safety concerns

- The bowl coasts for about 20 s after the drive stops; the brake and lid interlock are paper designs, and the lid pin must not be removable in normal use.
- A rider can reach about 1,200 rpm (447 J). Burst margins are large on paper but assume sound lamination and a bonded liner; containment of a 61 J liner fragment by the 6 mm HDPE tub and 10 mm lid is not verified.
- Mercury cross-contamination, arsenic and lead in concentrates, drowning risk at settling ponds and smelting heat are unchanged from TRL 2.
- The motor option brings a lithium pack to a wet, dusty site; MotionCore's stop does not brake.
- Concentrate theft and operator security remain a social risk for the partner.

### Other notes

- No TRL 4 material exists in the repo: no test plans or reports, build procedures, cut lists or purchasing lists. `build-log/README.md` is the scaffold stub and was not touched.
- Citations: the TRL 2 note lists no unchecked citations, so none were fetched; WebSearch was not used.
- The kit's cutaway cuts at the mean Y of the parts, which passes through the bowl axis; the model is not shifted. The water tank, water line, guards and speed display are left out of the section.
- build123d gives a shape only one parent compound, so `assemblies()` copies the parts for the bowl and deck sub-assemblies; without the copies the bowl and deck dropped out of the assembly STEP and the drawing views.
- `render.py --check` and `render.py` pass; PDFs are in `docs/pdf/`.

### Recommended next step

Review GVS-DDR-001, in particular the budget (item 1), R12 (item 9) and R11 (item 10), and decide how water is pumped at pedal-only sites (item 12). TRL 4 is on hold by Amish's instruction. For reference only, TRL 4 would need: a bench build of the bowl, jacket, spindle and brake; a lab test report (TST, `environment: lab`) covering liner casting and bond, spin-up with the lid and tub as containment, coast-down and brake stop time, union seal drag and pedal power, fluidization flow per ring, and recovery with tungsten or magnetite tracers; and build-log entries. None of this has been started.

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (GVS-PRB-001 v0.2): the problem with cited figures, users and operating environment, constraints, out of scope, prior work with sources (commercial centrifuges and tables, the CICAN project in Colombia, the Benguet borax method, planetGOLD), open questions; co-design checklist kept.
- `docs/03-requirements.md` (GVS-REQ-001 v0.2): 14 measurable requirements (R1 to R14) with targets, planned verification and concept status.
- `docs/02-concept.md` (GVS-PRC-001 v0.2): how it works, drive train, components table numbered to the BOM and exploded view, first-order numbers with assumptions, gold balance, key design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model (frame, hopper and screen, bowl with riffle rings, fluidization jacket and rotary union, spindle, splash tub and launder, lid guard, pedal station, jackshaft and gearbox, belts, guards, MotionCore module and motor, water tank, shaking table deck, table stand and head motion, concentrate tray) with the 1.75 m scale figure.
- `media/`: hero, blueprint sheet (PNG, PDF, SVG), cutaway, exploded view with BOM callouts, gold balance flow diagram (estimates marked), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 17 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md` with group totals.
- `README.md`: hero image and links line; Concept rationale, Burning platform, Where it could be used (6 industries, 5 countries or regions), What sparked the idea, Problem, Concept, Key components and Safety expanded with cited sources.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem still match the sources found.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Bowl speed and force | 730 rpm for 60 G at 100 mm; 600 to 850 rpm for 40 to 80 G | R3 met on paper |
| Throughput | 200 kg/h, 1.6 t per 8 h day | R2 met on paper |
| Input power | about 45 W (27 W slurry and water, 10 W losses, 85 % drivetrain) | R6 met on paper, at risk; R7 met |
| Motor energy | about 0.5 kWh per day | Information |
| Water | about 1.2 m3/h (0.47 slurry, 0.72 fluidization) | R8 met on paper |
| Mass pull | about 0.3 % to the bowl; about 5 kg per day to about 100 g on the table | R5 met on paper |
| Overall gold recovery | about 60 % on free-gold ore (reference 5 g/t: 4.8 of 8.0 g per day) | R4 not verifiable before testing, at risk |
| Size and mass | about 2.72 x 0.78 x 1.65 m; about 75 kg in four loads | R11 met on paper |
| Parts cost | about $437, MotionCore and battery excluded | **R9 not met**, about 25 % over $350 |

Requirements not met or at risk: **R9** (budget) is not met. **R4** (recovery) cannot be verified on paper and is the main technical risk. **R6** (pedal power) depends on the rotary union seal and bearing drag, which are guesses. **R12** is only partly met because the bowl brake is not yet designed. **R14** (liner life) is not verifiable at TRL 2.

### Proposed, awaiting Amish

1. **Budget.** Options: (a) raise `budget_usd` to $450; (b) keep $350 and phase the build, centrifuge stage and pedal drive first (items 1 to 11, 13 and 17, about $365) with the table later (about $72); (c) keep $350 and drop fluidization (saves about $45, lower fine-gold recovery). Recommendation: (a), because the table is what makes mercury-free smelting practical. `project.yaml` is unchanged at $350.
2. **Two stages (centrifuge then table)** over a centrifuge alone or a table alone. Recommendation: two stages.
3. **Fluidized bowl with a rotary union** over a non-fluidized bowl. Recommendation: fluidized, with the non-fluidized bowl kept as a documented low-cost variant.
4. **Bowl liner:** (a) cast polyurethane in a 3D-printed mold; (b) turned HDPE (needs a lathe); (c) printed bowl (low wear life). Recommendation: (a).
5. **Drive:** pedal crank as baseline with MotionCore 250 W as the option, one drive time-shared between bowl and table. Recommendation: as proposed.
6. **Reference battery for the motor option:** (a) leave it to the user (any 24 to 48 V pack MotionCore accepts); (b) name the SwapCell pack, whose about 468 Wh matches about one day of motor running. Recommendation: (a) for now; revisit after co-design shows whether users want the motor.
7. **Final step:** document direct smelting with borax as the recommended downstream method, outside the scope of this hardware. Recommendation: yes.
8. **First co-design partner:** options include a planetGOLD country programme, a university mining department in Ghana, Peru or Colombia, or a cooperative using the Benguet method in the Philippines. Recommendation: a partner in a country with a mercury ban already in force (Colombia) or a Minamata action plan with a planetGOLD programme.

### Dependencies

- **MotionCore:** GravitySort uses the MotionCore reference drive (250 W, 24 to 48 V, hardwired e-stop and independent speed limit) as its motor option, consistent with the MotionCore README. The MotionCore cost (about $325) is not in the GravitySort total.

### Safety concerns

- Rotating bowl at up to 850 rpm with about 150 J of stored energy, plus belts, chains and a moving table head: guards and a lid guard are in the model, but there is no interlock and no brake yet. A bowl brake and a guard interlock should be designed at TRL 3.
- Liner failure at speed could throw fragments; a burst check of the liner and shell belongs in the TRL 3 calculation note.
- Mercury cross-contamination: the machine must never be used with mercury or on untested legacy tailings. This must be stated in any user guide.
- Arsenic and lead minerals in concentrates; drowning risk at settling ponds; smelting heat (outside the machine).
- The motor option brings lithium cells to a wet, dusty site; MotionCore's safety section applies.
- Concentrate theft and the personal security of operators: the lockable tray and container help, but this is a social risk the partner must address.

### Suggestions (not in scope for this session)

- A simple recovery test protocol with tungsten or magnetite tracers would be the first TRL 4 activity, after Amish approves.

### Recommended next step

Review this note and the media. If approved, run `/advance-trl3` to size the bowl, fluidization flow and drive by calculation, check the liner and bowl for burst at 1.2 times maximum speed, design the bowl brake and guard interlock, settle the gearbox source, price the BOM with named suppliers, and produce the parametric model and drawing sheet.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was added

`cad/src/product_model.py` exposes `product_parts()` (94 parts: 60 shell, 24 internal, 7 accessory, 3 context), `TITLE` and `RENDER_VIEWS` (hero with the operator, exploded, and a detail view of the bowl, spindle and drive without the frame, guards, tub or operator). It imports PARAMS and riffle_rings() from `cad/src/model.py`; every main dimension and interface is as model.py. It adds:

- Frame, pedal outrigger and table stand in 25 mm tube with rounded edges, rubber feet and outrigger bolts; the tank post with a cradle plate and gussets.
- Galvanized feed hopper with a rolled rim, spigot collar, support arm and clamp band; the screen frame with a mesh texture.
- Bowl split into the amber cast PU liner with its four riffle rings and the GFRP shell with a lip flange, hub and bolts; the fluidization jacket; a brass rotary union with its side port.
- Spindle with two UCF205-style flanged bearing units and bolts, a grooved driven pulley, the speed sensor and magnet; a drilled 160 mm brake rotor, caliper, bracket and cable.
- Blue HDPE splash tub with rolling hoops and a teal band; galvanized tailings launder.
- White HDPE lid guard with a clear polycarbonate sight window over the bowl, window screws, a handle, two teal over-centre clamps and the red interlock pin.
- Pedal station with a padded seat, crank arms, treaded pedals and a toothed 48T chainring.
- Jackshaft with two pillow block bearings, 12T freewheel, motor sprocket, filleted bevel gearbox with cover screws, a 300 mm drive pulley with lightening holes, the table take-off pulley, closed chain and V-belt loops.
- Perforated teal belt and chain guards, with the name raised on the belt guard.
- MotionCore module with a label, glands and a lit status light; the reference hub motor with face grooves and its torque plate.
- Water header tank (natural HDPE drum with hoops, teal bung caps, label), ball valve with a red lever, clear rotameter with float and scale, the 3/4 in hose and clips.
- Shaking table: plywood deck with an HDPE face, tapered riffles, teal feed box and a wash water trough; flexure strips, eccentric head housing, pitman arm, eccentric shaft and head pulley; galvanized concentrate launder with a teal box lid, hasp and brass padlock.
- Bicycle speed display with screen and readout.
- Context: a compact patch of compacted earth, the tailings hose, and the shared clay mannequin (1.70 m, sit pose) on the seat with its feet solved onto the pedals and hands on its thighs.

`README.md` now shows `media/render-hero.png` and links `media/render-exploded.png`; the orchestrator produces both files. Matplotlib self-check previews (clear parts left out) are in `/tmp/gravitysort-prod/`.

### Differences from model.py (Proposed, awaiting Amish)

1. **Crank angle.** model.py draws the cranks vertical. The appearance model turns them to 100 degrees from top dead centre so the seated operator reads as pedalling. No dimension changes. Proposed, awaiting Amish. Recommendation: accept as a render pose only.
2. **Water hose route.** In model.py the water line drops straight down at x = -330 mm, y = -10 mm, which passes through the bowl belt guard, the 300 mm drive pulley and the tank post member. The appearance model runs the hose from the rotameter forward to y = -215 mm, down outside the guard, then under the guard to a side port on the rotary union. Proposed, awaiting Amish. Recommendation: adopt this route in model.py and GVS-DWG-001 at the next revision.
3. **Tank post and cradle.** `frame_members()` counts a 550 mm tank post, but `build_parts()` does not draw it, so the tank appears to sit on the water line. The appearance model draws the post plus a 240 mm cradle plate and two gussets. Proposed, awaiting Amish. Recommendation: add the post and cradle to model.py; the cradle is a small addition to BOM line 1 whose cost was not estimated.
4. **Lid sight window.** BOM line 7 is a plain 10 mm HDPE disc. The appearance model cuts a sector from the lid and bolts a 3 mm clear polycarbonate pane over it so the bowl and riffle rings show. The lid is a guard over a bowl storing about 165 J, so a window must not weaken containment. Proposed, awaiting Amish. Options: (a) keep the plain lid and treat the window as render only; (b) adopt a window of at least 6 mm polycarbonate after a containment check. Recommendation: (a) for now, (b) only after the check.
5. **Hub motor and motor chain.** In model.py the hub motor body (y = 190 to 250 mm) encloses the motor chain plane (y = 216 to 224 mm), so the chain runs into the motor. The appearance model keeps the model.py positions. Proposed, awaiting Amish. Recommendation: at the next model revision, move the motor along Y so its disc-mount sprocket lies in the jackshaft sprocket plane.
6. **Details not in model.py.** The lid handle, wash water trough along the back edge of the table, concentrate box lid, hasp and padlock, pillow block bearings (BOM line 9 already has "two bearings"), rubber feet, clips and bolts (BOM line 17) are appearance detail. The lid handle and wash water trough are not in any BOM line. Proposed, awaiting Amish. Recommendation: add the trough to BOM line 14 if the table's cross-flow of water needs a distributor; treat the rest as covered by lines 7, 16 and 17.
7. **Mannequin fit.** The mannequin's feet land about 27 mm inboard of the pedal centres (its hip width is fixed); the 830 mm seat of model.py is kept. No change proposed.

### Safety note

The inclined table belt and its take-off and head pulleys have no guard in model.py, and the renders show them exposed. Proposed, awaiting Amish: add a table belt guard to BOM line 11 at the next revision. Recommendation: yes.

### Status

This is an appearance model only: no tolerances, no fabrication detail, nothing past TRL 3. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold. model.py, the BOM and the other documents were not edited.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.
