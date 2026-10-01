---
doc_id: GVS-DEC-001
title: GravitySort design decisions register
project: GravitySort
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; open decisions from the review notes, the decision records and the design for construction
---

# GravitySort design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, GVS-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction | Accept the changes P1 to P15 as made; accept with changes; return to the concept layout | Accept: every change keeps what the machine does and all 102 model checks pass | The whole build plan | GVS-DDR-003, Table 1 |
| 2 | R11 total mass: the constructable design is 95.7 kg against 80 kg, with every load under 30 kg (heaviest 25.2 kg) | (a) restate R11's total as 100 kg or less, keeping loads of 30 kg or less; (b) look for about 16 kg of savings, then re-estimate; (c) keep 80 kg, R11 not met | (a), because the per-load limit decides whether two people can carry it; try the savings in (b) at TRL 4 | None now; (b) would change plates, hopper, guards and table base | GVS-DDR-003, A1; GVS-CAL-001 v0.4 section 11 |
| 3 | How the table gets its asymmetric stroke | (a) adjustable rubber bump stop at the return end; (b) toggle head; (c) spring return with a cam | (a) for the prototype; (b) if the first test shows it is not enough | Table head and the frame's table end (section 3.16 and step 16 of the plan) | GVS-DDR-003, A2; GVS-PRC-001 item 15 |
| 4 | Pedal position for riders of different sizes | (a) keep the bicycle-style seat, about 910 to 960 mm up, seat post adjustable; (b) a recumbent seat further back | (a); check with two riders at TRL 4 | Pedal outrigger (section 3.2) | GVS-DDR-003, A3 |
| 5 | Head for the fluidization supply | (a) a 1.7 m tank post (8.1 kPa at the union); (b) keep the 1.25 m post and add a small pump | None yet | Tank post height or a pump on the water line | GVS-DDR-001, item 11b |
| 6 | Water from the settling pond at pedal-only sites (about 1.19 m3/h, 5.5 W hydraulic) | Hand pump; a second rider on a pump; gravity supply from upstream | None yet | Not part of the machine; the header tank is filled by it | GVS-DDR-001, item 12 |
| 7 | R2 throughput margin (1.55 t per shift after flush stops) | Raise the design feed to about 210 kg/h; restate R2 as 200 kg/h of feed time | None yet | None (operating figure) | GVS-DDR-001, item 13 |
| 8 | First co-design partner and country | A partner in a country with a mercury ban in force (Colombia) or with a Minamata action plan and a planetGOLD programme | None yet (the screening criterion is decided) | None until a field trial | GVS-DDR-001, item 8b |
| 9 | Containment of a liner fragment by the tub and lid (61 J at 1,200 rpm) | (a) check by calculation before any spin test; (b) add a steel band round the tub at the bowl lip height | (a), then (b) only if the check fails | Splash tub and lid | GVS-CAL-001 section 10; review note 2026-09-25 |
| 10 | A sight window in the lid | (a) keep the plain 10 mm HDPE lid; (b) a window of 6 mm polycarbonate or more after the containment check | (a) | Lid guard (section 3.11) | Review note 2026-09-26, item 4 |
| 11 | Concentrate security in practice | Padlock on the box and container; sealed container; a two-person rule | Decide with the partner | Concentrate box and flush container | GVS-PRC-001, open questions |
| 12 | Renders: the cranks turned 100 degrees from top dead centre so the seated figure reads as pedalling | Accept as a render pose only; render with the model's crank angle | Accept as a render pose only | Renders only | Review note 2026-09-26, item 1 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The two flanged bearing units (UCF205 class): 95 mm square flange, bolts 70 mm apart, 25 mm bore with set screws | They set the holes in the two bearing plates | GVS-DDR-003, P2 |
| 2 | The shaft flange hub: 25 mm bore, 80 mm flange, four holes on a 60 mm circle, room for a 6 mm cross pin | It joins the bowl and jacket to the spindle | GVS-DDR-003, P4 |
| 3 | The rotary union: 1/2 in BSP on the shaft side, side water port, seal drag near 0.10 N m | Pedal power (R6) assumes this drag; the nipple welded into the spindle must match its thread | GVS-CAL-001 sections 7 and 10 |
| 4 | The right-angle 1:1 gearbox: through input shaft about 33 mm above its feet, feet about 100 x 80 mm, output shaft long enough for the drive pulley 85 mm below the feet | It sets the jackshaft height and the member spacing | GVS-DDR-003, P9; GVS-PRC-001 open questions |
| 5 | The four 20 mm pillow blocks (UCP204 class, centre height 33.3 mm, bolts 95 mm apart) | Two set the jackshaft height on the gearbox members; two carry the table head shaft | GVS-DDR-003, P8 and P14 |
| 6 | The two rubber pipe grommets for 63 mm and 75 mm pipe that seal in a 6 mm curved wall | They seal the standpipe and tailings pipe without welding | GVS-DDR-003, P6 |
| 7 | The 430 mm HDPE drum: flat floor, 6 mm wall, food-grade or clean | It is the splash tub | GVS-DDR-003, P6 |
| 8 | The used bicycle parts: a bottom bracket shell that can be cut from a scrap frame and welded, crank axle length, a 27.2 mm seat post | They set the outrigger's pedal post and seat tube | GVS-DDR-003, P8 |
| 9 | The disc caliper's mount (post mount or the older standard) and the disc's 6-bolt pattern | They set the caliper bracket holes and the brake flange | GVS-DDR-003, P15 |
| 10 | MotionCore: the reference hub motor's no-load speed (assumed 250 rpm), a sprocket on its disc mount, axle length for dropouts 76 mm apart inside, a speed limit that maps to 900 rpm at the spindle, a brake input for the lid switch | They set the 1.2:1 step-up, the cradle and the motor speed cap | GVS-DDR-002, item 14; review note 2026-09-25 |

## Value engineering

Value-engineering target: USD 455 (a hypothetical control target, not a limit; Amish, 2026-10-01). Estimated cost of the constructable design: USD 558 (USD 103 over the target), excluding the MotionCore kit, reference motor and battery. Main cost drivers and savings worth trying:

- **Main cost drivers.** The jackshaft, gearbox, chains and pulleys ($60); the jacket, hub and rotary union ($55); the table stand and head ($52); the bowl ($46); the frame ($43); the water supply ($41). Making the design buildable added $103, mostly the table head and tensioner, more frame tube and plate, and the tub fittings (GVS-DDR-003).
- **A quarter-turn belt instead of the bevel gearbox,** about $25 less (GVS-DDR-001, item 1). Worth a test, since a used gearbox is also the hardest part to find.
- **Used bearing units and pillow blocks** from scrap farm or factory machinery, about $10 to $15 less across the six bearings.
- **Run the table head shaft in two plain bronze bushes** in the head plate instead of two pillow blocks, about $8 less; the shaft turns slowly (about 300 rpm).
- **Take the table wash water from the main hose** with a tee at the rotameter instead of a separate branch and valve, about $4 less.
- **Buy steel as offcuts** and use one plate thickness (5 mm) throughout, a few dollars and a little mass.
- Not recommended: the non-fluidized bowl (about $45 less) or building the table later (about $100 deferred), because both change what the machine does.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items: two stages, fluidized bowl with rotary union, cast PU liner, pedal baseline with the MotionCore option and one time-shared drive, battery left to the user, borax smelting outside the machine, partner screening criterion | Amish: "i accept all your recommendations, go with them across all repos." | GVS-DDR-001, GVS-DDR-002 |
| 2026-09-25 | Budget from $350 to $450; R12 restated for the pedal drive; frame in 25 x 25 x 1.5 mm tube; 3/4 in fluidization hose and graded holes; disc brake with parking latch and lid interlock pin, speed display, 1.2:1 motor step-up, MotionCore lid switch | Amish, same instruction | GVS-DDR-002, items 1, 9, 10, 11a and 14 |
| 2026-09-26 | Budget set to $455 to cover the priced BOM | Amish: "i approve all the budget items." | GVS-DDR-002 v0.2 |
| 2026-09-26 | GravitySort chosen for the first batch of product renders | Amish | `docs/REVIEW.md`, session of 2026-09-26 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; the changes are recorded in GVS-DDR-003 and are open for review (open decision 1) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | GVS-DDR-003 |
| 2026-09-30 | Open decisions are kept out of the build plan, in this register | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | `.kit/STANDARDS.md` section 18 |
| 2026-10-01 | The budget is a value-engineering target, not a limit; cost is reported against it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | `.kit/STANDARDS.md` section 18 |
