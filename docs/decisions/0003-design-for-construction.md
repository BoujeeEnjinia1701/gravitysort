---
doc_id: GVS-DDR-003
title: GravitySort design for construction
project: GravitySort
doc_type: Design decision record
version: "0.4"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Accepted by Amish, including the recommendations for A1 to A3
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: A2 carried out; the table bump stop is now in the model, BOM, calculations, making sketch GVS-DWG-121 and build plan (section 3.16, step 16); the pitman pin works in a slot so the deck can strike the stop
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Accepted by Amish, the change made while adding the bump stop (slotted pitman pin with 8 mm free play in the deck cheeks; plywood legs set leaning about 5 mm to press the deck on the buffer with about 200 N), Table 2; no design change
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-01: "i agree with your recommendations for both GrowRider and GravitySort". This covers every change in Tables 1 and 2 and the recommendations in Table 3 (A1 to A3), which are now decided as recommended and recorded in the design decisions register (GVS-DEC-001). The change made while carrying out A2 (the slotted pitman pin and the leaning legs, Table 2, "Table bump stop"), which was open for his review, was accepted the same day. Amish, 2026-10-01: "I approve of your recommendations for PicoFlow and GravitySort".

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of GVS-DDR-002 showed what GravitySort does, but it was a massing model: several cross members floated in mid-air, two shafts passed straight through the members meant to carry them, the bearings had nothing to bolt to, the spindle had no way to carry water to the jacket, the lid could not be lifted off past the feed pipe, the table belt looped round a frame rail, and the hose to the rotary union ran through the drive pulley. Checking the model with build123d (intersections, contacts and clearances between every pair of parts) found each of these.

The changes below keep what GravitySort does: the same two stages, the same bowl, riffle rings, jacket and 12:1 drive, the same brake and lid interlock, the same table, tank and motor option, at the same main positions. `cad/src/model.py` now models every component as it is made or bought and runs 102 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must run clear are clear by at least the stated gap. All 102 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The tub cross members, the spindle bearing member, the jackshaft member and the motor member sat at heights where no rail joined them, so they floated. The spindle passed through its own bearing member and the gearbox output shaft through the jackshaft member. | The low stretchers move up to become lower side rails (255 to 280 mm). Four 600 mm members lie across on top of them in two pairs, one pair either side of the gearbox output shaft and one pair either side of the spindle. The two tub members (445 to 470 mm) hang from the top side rails on four 205 mm drop posts. A low end member (90 mm), an end post and a head member close the ends. 14.5 m of tube in all (was 11.75 m). | Every member now butts onto two others and can be welded; a member pair leaves a gap for each vertical shaft; the drop posts are lighter than a third pair of side rails. |
| P2 | The two flanged bearing units (95 mm square flanges) had only a 25 mm tube, or nothing, to bolt to. | A 150 x 130 x 6 mm plate is welded under each pair (spindle pair and tub pair) with a 40 mm centre hole and four bolt holes; each bearing hangs under its plate. Bearing centres are now 255 and 420 mm above the ground, 165 mm apart (were 300 and 450 mm, 150 apart). The driven pulley drops 10 mm, to 180 to 220 mm. | Bolting under the plate keeps both plates welded in one setting, so the two bores line up with a plumb line; the wider span helps the spindle. |
| P3 | The spindle was a solid 25 mm shaft, yet the rotary union at its foot has to feed water to the jacket at its top. | The spindle is a 25 x 2 mm stainless 316 tube, 372 mm long; water runs up its bore. A 1/2 in BSP stainless nipple is welded into its foot to take the union. | No lathe or deep drilling is needed (R10). The thinner section lowers the first critical speed from about 4,820 to 2,710 rpm, still 2.3 times the 1,200 rpm sprint speed; bending stress 21 MPa (GVS-CAL-001 v0.4). |
| P4 | The bowl hub was a plain cylinder that passed through the jacket floor and had no fixing; the jacket was open at its top, so the fluidization water would run out of the 12 mm gap there. | A bought 25 mm bore shaft flange hub (80 mm flange) is pinned to the spindle top and bolted by four M6 bolts through the jacket floor and four 12 mm spacer bushes into four M6 nuts cast into the liner floor. A 4 mm GFRP closing ring is bonded between the shell and the jacket top. | The spacers set the 12 mm gap at the floor; the closing ring seals it at the top, so water can only leave through the ring holes. The bowl, jacket and hub come off the spindle as one unit by pulling one pin. |
| P5 | The riffle rings stand inward from the liner wall, so a one-piece printed core could not be pulled out of the cast liner. | The printed core is made in six segments round a central key: the key comes out first, then each segment moves inward past the rings. The GFRP shell is the outer mould. | Keeps the cast PU liner of GVS-DDR-001 item 4 with no lathe. |
| P6 | The tub's centre hole opened onto the upper bearing, so spilt slurry would run into it; the tailings launder was a box through an uncut tub wall that also ran into the frame. | A 63 mm standpipe, 50 mm tall, stands through a rubber pipe grommet in the tub floor and sits on the upper bearing plate, 10 mm below the hub. The tailings outlet is a 75 mm pipe through a rubber pipe grommet in the back wall, centred 64 mm above the floor, 12.5 mm clear of the frame. Four M8 bolts hold the tub floor on the tub members. | Rubber pipe grommets seal in a curved wall and need no plastic welding. The bowl and hub run clear of the standpipe (12 mm). |
| P7 | The feed pipe ran down through the lid's hole into the bowl, so the lid could not be lifted off for a flush; the hopper's bottom was closed; the hopper arm ended inside the cone. | The feed pipe stops 15 mm above the lid and drops the slurry through the 60 mm hole onto the bowl floor. The hopper bottom has a 32 mm hole into the pipe. The cone drops into a 6 mm ring on the support arm and wedges there; the support post bolts to the front top rail. | The lid now lifts straight off without touching the hopper, so R13's toolless flush stands. |
| P8 | The pedal chain's lower run crossed the jackshaft member; the outrigger's arms ended in the air at the frame end; the seat was too low for the crank. | The bottom bracket rises to 438 mm, 100 mm above the jackshaft (now 338 mm, on two pillow blocks on the gearbox pair), so the chain passes 4.6 mm over the left gearbox member. The outrigger is a welded spine with two cross feet, a pedal post, a round seat tube and a top arm, bolted by two end plates to the low end member and the end post. The saddle sits about 910 to 960 mm up, adjustable on a bicycle seat post. | Uses bought bicycle parts as before; the outrigger lifts off with four bolts for transport. |
| P9 | The gearbox floated. | The gearbox stands across the two gearbox members, four M8 bolts; its output shaft goes down between them to the 300 mm drive pulley. | |
| P10 | The table take-off pulley, inside the frame, ran into the members; and the table belt's loop enclosed the frame's table-end top rail, so the belt could not be fitted. | The jackshaft runs out 330 mm in front of the centre line, past the front rails; the take-off pulley and the table head pulley share a belt plane outside the frame. | Nothing passes between the two runs of the table belt. |
| P11 | The hub motor's body enclosed its own chain (review note of 2026-09-26, item 5) and overlapped the motor member. | The motor option bolts on: a 6 mm cradle on the back lower rail with two dropouts and open axle slots; the motor sits behind the frame with its sprocket on the disc mount, chained to a sprocket on the end of the jackshaft; a chain guard covers it. | The pedal-only machine carries no motor parts; the motor chain clears the hub by 3.5 mm. |
| P12 | The belt guard floated and the spindle and gearbox shaft ran through its top; the table belt had no guard (safety note of 2026-09-26). | The bowl belt guard hangs on four straps from the members, with holes for the two shafts. The pedal chain case rests on the left gearbox member and is tabbed to the pedal post. A table belt guard covers the table belt and its tensioner. | Every belt, chain and pulley is guarded (R12). |
| P13 | The water hose dropped through the belt guard, the drive pulley and the tank post member; the tank post was not drawn (review note of 2026-09-26, item 3). | The tank post and a 250 x 250 x 5 mm cradle with gussets are drawn and welded to the frame. The valve is on the back of the drum; the rotameter is on a bracket on the back top rail; the hose runs down outside the back of the frame, then under the belt guard to the union. | Follows the route proposed in the review note of 2026-09-26 (item 2), adapted to the new frame. |
| P14 | The table legs were solid blocks; the head stood on a single 25 mm post on a foot plate (about 134 MPa under the belt pull, a factor of about 1.8); the table belt had no clutch mechanism; the concentrate tray ran along the front, where the tailings fall, and the deck's front edge overhung it. | Four 18 mm plywood flexure legs on angle cleats, on a welded base, thin side along the table so they bend with the stroke. The head is a 6 mm plate and shelf bolted to the frame's table end, with two pillow blocks, a 20 mm head shaft and an eccentric of 15 mm stroke; a pitman links it to cheeks under the deck. A tensioner (idler on a latched arm) is the table clutch. A tailings launder runs under the deck's front edge; the lockable concentrate box sits under the far end, where gold leaves the riffles. A drilled wash water pipe runs along the back edge (review note of 2026-09-26, item 6). | Uses the frame as the head's anchor (the table runs only when the bowl is stopped), and puts each product where the table delivers it. |
| P15 | The speed display faced away from the rider and the brake caliper's bracket floated. | The display and the brake lever sit on the pedal-end top rail, facing the rider. The caliper sits on a 6 mm L bracket bolted to the right spindle member; the disc sits on a flange welded to a shaft collar. | |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 77.3 kg to **95.7 kg** in six loads; heaviest load 25.2 kg (the base frame with the spindle and brake) (GVS-CAL-001 v0.4, section 11). R11 (80 kg) moves from met on paper to **not met, 16 kg over**; every load is still under 30 kg. | About 2.7 m more tube, about 9 kg of plate, and parts the concept left out (hopper support, tank cradle, standpipe and pipes, head plate, tensioner, table belt guard, launder legs). |
| Cost | BOM $455 to **$558**: value-engineering target USD 455; estimated cost of the constructable design USD 558 (USD 103 over the target). Lines 1 to 4, 6, 8, 11, 13 to 17 repriced and line 20 (motor cradle) added. | Parts added for construction. |
| Spindle | First critical speed 4,820 to 2,710 rpm (2.3 times the sprint speed); bending 18 to 21 MPa. | Hollow spindle (P3) and bearing positions (P2). |
| Size | 2.72 x 0.78 x 1.65 m to 2.78 x 0.79 x 1.65 m. | Outrigger feet and the outboard table belt. |
| Drawings | GVS-DWG-001 Rev P3; making sketches GVS-DWG-101 to 120 added. | Follows the model. |
| Documents | GVS-CAL-001 v0.4, GVS-REQ-001 v0.6, GVS-PRC-001 v0.6: mass, cost, spindle and R9, R10, R11 updated. | Follows the model. |
| Table bump stop (A2, carried out in v0.3; the slotted pitman pin and leaning legs accepted by Amish 2026-10-01) | A bracket of 25 mm tube bolted on top of the frame's table-end top rail, 205 mm behind the centre line, carries a bought rubber buffer (40 mm across, 30 mm long, about 55 Shore A) on an M8 stud with a lock nut each side of its upright; a 6 mm steel striker angle under the deck's head end strikes it at the end of each forward stroke. The pitman pin works in a 20 mm slot in the deck cheeks (8 mm of free play), and the plywood legs are set leaning so they press the deck on the buffer with about 200 N. The stop is set 3 mm short of full forward travel (2 to 6 mm useful): 0.24 J per stroke, 2.1 G at the stop against 0.6 G at the head end (GVS-CAL-001 v0.6, section 9). Mass 95.7 to 96.5 kg; cost $558 to $569 (BOM lines 21 and 22); 13 checks added to the model (115 in all); GA Rev P4; making sketch GVS-DWG-121; build plan v0.3. | A rigid pitman drags the deck through the whole circle of the eccentric and cannot strike a stop, so the slot and the legs' push are needed for the stop to make the stroke asymmetric. The concept asked for a "toggle or spring return"; the legs are the spring. |
| Unchanged | Bowl speed, G, drive ratio, power, water, settling, fluidization supply, burst factors, brake and gold balance. | The bowl, jacket and drive geometry did not change. |

*Table 3. Items that change a requirement or what the machine does: proposed, then accepted by Amish as recommended on 2026-10-01.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | R11 asks for 80 kg or less in all; the constructable design is about 96 kg, though every load stays under 30 kg (heaviest 25 kg) so two people can still carry each one. | (a) restate R11's total as 100 kg or less, keeping loads of 30 kg or less; (b) find about 16 kg (for example aluminium hopper, guards and launder, 4 mm plates, a lighter table base), then re-estimate; (c) keep 80 kg and leave R11 not met. | (a), because the per-load limit is what decides whether two people can carry the machine to site; try the savings in (b) at TRL 4 anyway. |
| A2 | The concept asks for an asymmetric table stroke ("toggle or spring return"); the model has a plain eccentric on flexure legs, which gives a nearly symmetric stroke, and a symmetric stroke does not walk gold along a shaking table. | (a) add an adjustable rubber bump stop at the return end of the stroke, the simplest way to make the stroke asymmetric; (b) a toggle (Rittinger-type) head; (c) a spring return with a cam. | (a) for the prototype, adjustable by a screw, because it adds one part to the frame end; (b) if the first test shows (a) is not enough. |
| A3 | The pedal position: the saddle is about 910 to 960 mm up and 170 mm behind a bottom bracket at 438 mm. This has not been checked against riders of different sizes. | (a) keep, with the seat post adjustable over about 200 mm; (b) move to a recumbent seat further back. | (a); check at TRL 4 with two riders. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan GVS-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); the open questions are in the design decisions register GVS-DEC-001.
- Requirement status: R11 moved to not met (16 kg over 80 kg, every load under 30 kg) and R9 is now reported against the value-engineering target (USD 103 over). R2, R5 and R6 stay at risk, R4 and R14 not verifiable, the rest met on paper or by design review (GVS-CAL-001 v0.4).
- With A1 accepted, R11 is restated to 100 kg or less in all, every load 30 kg or less, and is met on paper at 95.7 kg (GVS-REQ-001 v0.7, GVS-CAL-001 v0.5); the savings of option (b) are to be tried at TRL 4. With A2 accepted, the table stroke is made asymmetric by an adjustable rubber bump stop at the return end (the far end of the forward stroke, where the deck turns back), with a toggle head only if the first test shows it is not enough; the stop is now in the model, the BOM (lines 21 and 22), the calculations (GVS-CAL-001 v0.6, section 9), making sketch GVS-DWG-121 and the build plan (GVS-BLD-001 v0.3, section 3.16 and step 16), as Table 2 describes. With A3 accepted, the pedal position is kept and checked with two riders at TRL 4.
- With the bump stop change accepted (2026-10-01), the pitman pin works in a 12 x 20 mm slot in the deck cheeks with 8 mm of free play, and the plywood legs are set leaning about 5 mm so they press the deck on the buffer with about 200 N; this is the design as drawn in the model, the making sketches and the build plan (GVS-BLD-001 v0.3, sections 3.15 and 3.16). The toggle head of A2, option (b), stays the fallback if the first table test shows the stop is not enough.
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept frame, outrigger, table stand, hose and motor position; they need updating on Amish's Mac, where Blender is.
- The bought parts that set dimensions (bearing units, shaft flange hub, rotary union, gearbox, pillow blocks, rubber grommets, hub motor) must be checked against the model when bought; they are listed in GVS-DEC-001.
