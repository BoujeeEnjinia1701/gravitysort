# Review note: GravitySort

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
