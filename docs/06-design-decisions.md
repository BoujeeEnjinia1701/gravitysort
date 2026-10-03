---
doc_id: GVS-DEC-001
title: GravitySort design decisions register
project: GravitySort
doc_type: Design decisions register
version: "0.7"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; open decisions from the review notes, the decision records and the design for construction
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Amish accepted the recommendations of open items 1 to 4, 9, 10 and 12 (GVS-DDR-003 accepted; R11 restated); moved to decisions made; open items renumbered 1 to 5
  - version: "0.3"
    date: '2026-10-01'
    author: Amish Chadha
    change: Table bump stop now in the model and build plan (follow-up note removed); buffer added to the items to confirm; Value engineering updated to USD 569
  - version: "0.4"
    date: '2026-10-01'
    author: Amish Chadha
    change: Amish accepted the change made while adding the bump stop (slotted pitman pin, leaning legs; GVS-DDR-003 Table 2); added to decisions made; no open item changed
  - version: "0.5"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for open decisions 1 to 5; moved to decisions made"
  - version: "0.6"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Decisions of 2026-10-02 carried into the model, BOM, calculations and build plan; one open decision added (tank on the centre line and the tipping criterion, made to carry out decision 1); Value engineering updated to USD 580"
  - version: "0.7"
    date: '2026-10-03'
    author: Amish Chadha
    change: "Open item 1 decided by Amish on 2026-10-03 (option a: tank post on the centre line, braced, 10 degree any-direction tip criterion); moved to decisions made"
---

# GravitySort design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, GVS-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

None. Open item 1 (tank post position and tip criterion) was decided on 2026-10-03.

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
| 11 | The bump stop's rubber buffer: 40 mm across, 30 mm long, about 55 Shore A, M8 female thread, rated 800 N or more in compression | The stop's force, squeeze and setting range are sized for this buffer (GVS-CAL-001 section 9) | GVS-DDR-003, A2 |

## Value engineering

Value-engineering target: USD 455 (a hypothetical control target, not a limit; Amish, 2026-10-01). Estimated cost of the constructable design: USD 580 (USD 125 over the target), excluding the MotionCore kit, reference motor and battery. Main cost drivers and savings worth trying:

- **Main cost drivers.** The jackshaft, gearbox, chains and pulleys ($60); the jacket, hub and rotary union ($55); the table stand and head ($52); the frame ($47); the bowl ($46); the water supply ($41). Making the design buildable added $103, mostly the table head and tensioner, more frame tube and plate, and the tub fittings (GVS-DDR-003); the table bump stop adds $11 more (bracket and striker $6, buffer and fixings $5); the decisions of 2026-10-02 add $11 (the braced 1.7 m tank post $4, the flush container with its hasp $7).
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
| 2026-09-30 | Make the design physically buildable while drawing the build plan; the changes are recorded in GVS-DDR-003 and were accepted on 2026-10-01 (below) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | GVS-DDR-003 |
| 2026-09-30 | Open decisions are kept out of the build plan, in this register | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | `.kit/STANDARDS.md` section 18 |
| 2026-10-01 | The budget is a value-engineering target, not a limit; cost is reported against it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | `.kit/STANDARDS.md` section 18 |
| 2026-10-01 | Design for construction accepted: the changes P1 to P15 and their knock-on changes, as made | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | GVS-DDR-003, Tables 1 and 2 |
| 2026-10-01 | R11 restated: total 100 kg or less, every load 30 kg or less (was 80 kg in all); the 95.7 kg design meets it on paper. Follow-up: try the savings of about 16 kg (option b) at TRL 4 | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | GVS-DDR-003, A1; GVS-REQ-001 v0.7 |
| 2026-10-01 | Asymmetric table stroke: an adjustable rubber bump stop at the return end of the stroke for the prototype. Follow-up: a toggle head (option b) only if the first test shows the stop is not enough | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | GVS-DDR-003, A2 |
| 2026-10-01 | Pedal position: keep the bicycle-style seat, about 910 to 960 mm up, seat post adjustable. Follow-up: check with two riders at TRL 4 | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | GVS-DDR-003, A3 |
| 2026-10-01 | Containment of a liner fragment: check by calculation before any spin test; add a steel band round the tub at the bowl lip height only if the check fails | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | GVS-CAL-001 section 10; review note 2026-09-25 |
| 2026-10-01 | Lid: keep the plain 10 mm HDPE lid, no sight window | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | Review note 2026-09-26, item 4 |
| 2026-10-01 | Renders: the cranks turned 100 degrees from top dead centre is a render pose only; the model keeps its crank angle | Amish: "i agree with your recommendations for both GrowRider and GravitySort" | Review note 2026-09-26, item 1 |
| 2026-10-01 | Table bump stop, change made to let the deck strike the stop: the pitman pin works in a 12 x 20 mm slot in the deck cheeks (8 mm of free play), and the plywood legs are set leaning about 5 mm so they press the deck on the buffer with about 200 N. Accepted as made; no design change | Amish: "I approve of your recommendations for PicoFlow and GravitySort" | GVS-DDR-003, Table 2 (v0.4) |
| 2026-10-02 | Head for the fluidization supply: raise the header tank post to 1.7 m (option a), braced so a full 60 L tank cannot tip it; no pump on the fluidization line. Carried into the model, drawings, build plan, BOM and GVS-CAL-001 v0.8 on 2026-10-02 (8.6 kPa at the union at mid-tank) | Amish: "i approve your recommendations for all 555 open decisions." | GVS-DDR-001, item 11b |
| 2026-10-02 | Water at pedal-only sites: gravity supply from upstream is the site rule for the first field trial; where that is impossible, a bought treadle or hand pump worked in turns by the crew, or a small 12 V pump at sites with the MotionCore battery | Amish: "i approve your recommendations for all 555 open decisions." | GVS-DDR-001, item 12 |
| 2026-10-02 | R2 restated as 200 kg/h of feed time, about 1.55 t in an eight-hour shift with three flush stops; the design feed stays at 200 kg/h | Amish: "i approve your recommendations for all 555 open decisions." | GVS-DDR-001, item 13 |
| 2026-10-02 | First co-design partner and country: Colombia, where the mercury ban is in force, with a miners' cooperative introduced through the Alliance for Responsible Mining in Medellin as the first candidate to approach | Amish: "i approve your recommendations for all 555 open decisions." | GVS-DDR-001, item 8b |
| 2026-10-02 | Concentrate security: padlock hasps on both the concentrate box and the flush container as the baseline, and a two-person rule for opening them proposed to the partner; both to be confirmed with the partner. Flush container with hasp added to the model and BOM (item 23) on 2026-10-02 | Amish: "i approve your recommendations for all 555 open decisions." | GVS-PRC-001, open questions |
| 2026-10-03 | Open item 1, option (a): the 1.7 m tank post stands on the centre line and is braced; "a full tank cannot tip it" means a 10 degree slope in any direction with a full tank (tips at 13.5 degrees, 193 N side push at the tank, better than the earlier 1.25 m layout at 11.6 degrees); no wider feet or outriggers | Amish: "GravitySort - i accept your recommendation" | GVS-CAL-001 v0.8 section 11; [REVIEW.md](REVIEW.md), session 2026-10-03 |
