---
doc_id: GVS-PRC-001
title: GravitySort design precis
project: GravitySort
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, components, first-order numbers, gold balance, safety, media)
---

# GravitySort design precis

## Summary

GravitySort is a two-stage, mercury-free gravity concentrator for small mining groups. A fluidized centrifugal bowl (220 mm across the lip, about 60 G at 730 rpm) catches fine gold from about 200 kg/h of milled ore, and a small shaking table (1,000 x 450 mm) cleans the day's bowl concentrate down to about 100 g, small enough to smelt directly with borax. One drive, either a pedal crank or a 250 W motor through the lab's MotionCore module, runs the bowl by day and the table at clean-up. The whole machine is a welded steel frame about 2.7 m long, about 75 kg, built from bicycle parts, bearings, V-belts, HDPE drums and a cast polyurethane bowl liner. First-order estimates suggest about 60 % overall gold recovery on free-gold ore, compared with about 30 % typical of whole-ore amalgamation in Colombian processing centers ([Veiga et al., 2018](https://doi.org/10.1016/j.jclepro.2018.09.039)), at about 45 W of input power. The parts cost is estimated at about $437, over the $350 budget. All figures are estimates for review, not measurements.

![Hero render](../media/hero.png)

*Figure 1. GravitySort with a 1.75 m person for scale. Pedal station on the left, centrifuge frame with hopper and water tank in the middle, shaking table on the right. Massing model.*

## Design approach

### How it works

1. **Feed.** Ore milled to below about 2 mm is shovelled or washed onto the 2 mm punched screen on top of the hopper. Oversize goes back to the mill. Water from the header tank carries the undersize down a feed pipe into the centre of the bowl as a slurry of about 30 % solids.
2. **Concentrate in the bowl.** The bowl spins at 600 to 850 rpm (40 to 80 G at 100 mm radius). Slurry climbs the conical wall and passes over four riffle rings. Dense particles (gold, about 19 g/cm3, and heavy minerals) settle in the rings; light gangue (quartz, about 2.7 g/cm3) spills over the lip into the splash tub and out through the tailings launder to a settling pond. Water injected through small holes in each ring from a rotating jacket keeps the bed loose (fluidized), so heavy particles can keep replacing light ones instead of the rings packing hard.
3. **Flush.** About every 2 h the operator stops feed, stops the drive and rinses the rings into a lockable container: about 1 to 1.5 kg of heavy concentrate per flush (estimate).
4. **Clean on the table.** At the end of the day the belt tension is moved from the bowl drive to the table drive, and the day's bowl concentrate (about 5 kg, estimate) is fed onto the shaking table. The table's asymmetric stroke and cross-flow of water spread particles by density: gold walks to the end of the riffles and drops into a lockable concentrate tray; lighter material washes off the front edge and is re-run.
5. **Smelt, outside this machine.** The final concentrate (about 100 g or less) is dried and smelted with borax in a small furnace, as in the Benguet method ([Appel and Na-Oy, 2012](https://www.journalhealthpollution.org/doi/full/10.5696/2156-9614-2.3.5)). No mercury is used at any step.

![Gold balance](../media/flow.png)

*Figure 2. Gold balance for one 8 h day at 200 kg/h on a reference ore of 5 g/t. All values are estimates: oversize loss 5 %, bowl recovery of screened gold about 71 %, table recovery about 93 %, smelting recovery about 96 %. Overall about 60 %.*

### Drive

The pedal crank (48-tooth chainring) drives a jackshaft through a 12-tooth freewheel (4:1). A right-angle bevel gearbox turns the drive to a vertical shaft carrying a 300 mm pulley, which belts to a 100 mm pulley on the bowl spindle (3:1). At a cadence of 61 rpm the bowl turns at about 730 rpm. The freewheel lets the bowl coast when the rider stops, and lets a MotionCore motor drive the jackshaft through its own chain without turning the pedals. For the table, a second pulley on the jackshaft drives the table's eccentric head through a V-belt that is slack (disengaged) unless its tensioner is set.

The optional motor follows the MotionCore README: a 250 W reference motor on a 24 to 48 V pack, with a hardwired emergency stop and an independent speed limit. The pack is not part of GravitySort. A SwapCell pack would fit through MotionCore, but whether to name it as the reference pack is proposed, awaiting Amish.

![Cutaway](../media/cutaway.png)

*Figure 3. Section through the centrifuge axis, looking from the front. Bowl (3) with riffle rings inside the fluidization jacket (4), spindle and bearings (5) below, splash tub (6) around, hopper (2) and feed pipe above.*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 4.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Base frame | 30 x 30 x 2 mm mild steel square tube, welded, 900 x 600 x 700 mm, with cross members for tub, spindle, jackshaft, motor and tank post | Painted; bolts to the pedal outrigger and table head |
| 2 | Feed hopper | Sheet steel or cut plastic cone, 2 mm punched stainless screen on top, 32 mm feed pipe to the bowl centre | Screen removable for cleaning |
| 3 | Centrifugal bowl | 220 mm lip, 130 mm base, 180 mm deep; four riffle rings with 0.8 to 1.2 mm fluidization holes; cast polyurethane liner (Shore 80 to 90A) in a 3D-printed mold on a fibreglass shell | No lathe needed; liner replaceable. Proposed, awaiting Amish |
| 4 | Fluidization jacket and rotary union | Sealed jacket around the bowl, fed through a 1/2 in rotary union at the spindle foot, 8 to 15 L/min | Proposed over a non-fluidized bowl, awaiting Amish |
| 5 | Spindle and bearings | 25 mm stainless shaft, two flanged ball-bearing units, 100 mm driven pulley | Upper bearing shielded under the tub floor |
| 6 | Splash tub and launder | Cut HDPE drum, 430 mm diameter, 75 mm tailings outlet and launder to the settling pond | |
| 7 | Bowl lid guard | 10 mm HDPE disc clamped to the tub, 60 mm feed hole | Keeps hands out of the bowl while running |
| 8 | Pedal station | Used bicycle bottom bracket, crank, 48T chainring, pedals and seat on a bolted outrigger | Adjustable seat |
| 9 | Jackshaft and gearbox | 20 mm shaft on two bearings, 12T freewheel, 1:1 right-angle bevel gearbox, 300 mm drive pulley, motor sprocket, table take-off pulley | Bevel box from a used agricultural or garden machine is an option |
| 10 | Drive belts | A-section V-belts: bowl (horizontal) and table (inclined, clutch by tensioner) | |
| 11 | Guards | Perforated sheet covers over belts, pulleys and chain | Must be fitted before running |
| 12 | MotionCore module and motor | MotionCore reference drive: 250 W geared motor, controller, e-stop, speed limit | Shared component; not in the GravitySort cost |
| 13 | Water header tank | 60 L HDPE drum on a post 1.25 m above ground, ball valve, 2 to 20 L/min rotameter, hoses | Filled by the user's pump from the settling pond |
| 14 | Shaking table deck | 1,000 x 450 mm, 18 mm marine plywood faced with HDPE, tapered riffles, feed box, 2 to 4 degrees cross tilt | Adjustable tilt |
| 15 | Table stand and head motion | Flexure legs (spring steel strip or plywood), eccentric head with pitman arm, 10 to 20 mm stroke at 240 to 300 strokes/min | Asymmetric stroke from a toggle or spring return |
| 16 | Concentrate tray | Launder along the table front, lockable concentrate tray at the gold end | Security for the operator |

Item 17 (hardware, hoses and sealant) is in the BOM but not modelled.

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with numbered callouts matching Table 1 and the BOM.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

Table 2. First-order numbers and assumptions.

| Quantity | Estimate | Assumption |
| --- | --- | --- |
| Bowl speed for 60 G at 100 mm radius | 730 rpm | a = ω²r; 40 G at 600 rpm, 80 G at 850 rpm |
| Drive ratio, pedal to bowl | 12:1 (4:1 chain, 1:1 bevel, 3:1 belt) | 61 rpm cadence gives 730 rpm |
| Feed rate | 200 kg/h solids, 1.6 t per 8 h day | Slurry 30 % solids by mass |
| Slurry water | about 0.47 m3/h | 200 kg/h solids at 30 % solids |
| Fluidization water | about 0.72 m3/h (12 L/min) | Mid-range for small fluidized bowls; to be tuned |
| Total water | about 1.2 m3/h, about 9.5 m3 per day | Mostly recirculated through a settling pond |
| Power to spin up slurry and water | about 27 W | 0.39 kg/s brought to the lip speed of 8.4 m/s (m·v², an upper bound for slip) |
| Bearing, seal and windage losses | about 10 W | Rotary union seal dominates; not yet from a datasheet |
| Input power at the pedals | about 45 W | Drivetrain efficiency about 85 % |
| Motor energy per 8 h day | about 0.5 kWh | 45 W at the bowl drive, motor and controller about 75 % efficient |
| Bowl concentrate per flush | about 1 to 1.5 kg | Riffle volume about 0.5 L at about 2.5 to 3 kg/L |
| Mass pull to bowl concentrate | about 0.3 % | 1.2 kg per 400 kg of feed (2 h cycle) |
| Table concentrate per day | about 100 g or less | Table reduces about 5 kg by about 50:1 |
| Overall gold recovery | about 60 % (4.8 of 8.0 g per day) | Free gold 38 to 1,000 µm; see Figure 2 |
| Kinetic energy of loaded bowl at 730 rpm | about 150 J | 5 kg at an effective radius of 100 mm |
| Size and mass | about 2.72 x 0.78 x 1.65 m; about 75 kg in four loads | Massing model; steel tube at 1.7 kg/m |
| Parts cost | about $437 | `bom/bom.csv`; MotionCore and battery excluded |

The daily motor energy of about 0.5 kWh is close to the energy of the SwapCell reference pack (about 468 Wh nominal) or one day of a 150 to 200 W solar panel. This is noted as an option, not a proposal to change scope.

## Key design choices

Each of these is proposed, awaiting Amish. Options and the recommendation are in `docs/REVIEW.md`.

1. **Two stages, centrifuge then table,** rather than a centrifuge alone (whose concentrate is too large to smelt) or a table alone (which loses fine gold at this throughput and needs more water).
2. **Fluidized bowl** with a rotary union, rather than a simpler non-fluidized bowl that packs hard and needs flushing every 15 to 30 min.
3. **Cast polyurethane liner** in a printed mold, rather than a turned HDPE bowl (needs a lathe) or a printed bowl (wears quickly on quartz).
4. **One drive, time-shared** between bowl and table, rather than two drives. Saves a motor or a second pedal station.
5. **Pedal drive as the baseline,** MotionCore motor as an option.
6. **Direct smelting with borax** as the recommended final step, outside this machine.

## Safety

> **Safety:** Rotating machinery. The bowl turns at up to 850 rpm with about 150 J of stored energy, and belts, chains and pulleys can trap fingers, hair and loose clothing. Never run without the lid guard and all belt and chain guards fitted. Stop the drive and wait for the bowl to stop before opening the lid or flushing. Keep children and animals away from the machine. The bowl liner must be checked for cracks before every run; a failed liner at speed can throw fragments. The motor option adds stored electrical energy and lithium cells; follow the MotionCore safety section, and never bridge its emergency stop.

> **Safety:** Mercury. GravitySort must never be used with mercury, and it must not process tailings or concentrates from sites that used mercury without testing, because mercury contamination would spread through the bowl, the water and the table. Legacy mercury at a site calls for specialist handling through the partner organization.

> **Safety:** Water and slurry. Settling ponds and pits are drowning hazards and must be fenced. Slurry is slippery; wear boots with grip. Wash hands after handling concentrate; heavy minerals can contain arsenic (arsenopyrite) and lead.

> **Safety:** Smelting (outside this machine). Direct smelting reaches about 1,065 °C or more. Use a proper furnace, tongs, a face shield and ventilation, and never smelt indoors.

## Open questions

- [ ] Does a fluidized bowl of this size hold gold of 38 to 75 µm at 60 G with local feed, or is a larger bowl or higher G needed?
- [ ] Is a low-cost rotary union reliable in silty recirculated water, and does its seal drag stay near 10 W?
- [ ] Can the cast polyurethane liner be made reliably in a small workshop, and how long does it last on quartz feed?
- [ ] Is a right-angle bevel gearbox easy to source, or should the bowl be driven by a quarter-turn belt?
- [ ] What bowl brake is simplest and safe (band brake on the spindle pulley, or a friction pad on the jackshaft)?
- [ ] How should concentrate security be handled in practice: padlock, sealed container or a two-person rule?
- [ ] Which partner and country for the first field trial?

## Key design decisions

Record each significant decision as a file in [decisions/](decisions/). No decision records exist yet; the choices above are proposals awaiting Amish.
