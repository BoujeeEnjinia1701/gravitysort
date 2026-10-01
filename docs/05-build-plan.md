---
doc_id: GVS-BLD-001
title: GravitySort prototype build plan
project: GravitySort
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan; design made constructable (GVS-DDR-003)
---

# GravitySort prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order; 26, the motor, is an option.*

The prototype is one GravitySort machine: a welded steel frame about 900 mm long, 600 mm wide and 700 mm tall that carries a spinning bowl inside a plastic tub, a pedal seat bolted to one end and a shaking table bolted to the other, with a water tank on a post above. Pedalling turns a jackshaft under the frame; a right-angle gearbox and a V-belt spin the bowl at about 730 rpm, and a second belt, engaged by a hand lever, drives the table at clean-up. Figure 1 shows the 26 groups of parts in the order you make or fit them. The work is sawing, drilling and MIG or stick welding square steel tube and plate; laying up glass fibre over 3D-printed plugs and casting polyurethane in the bowl; cutting a plastic drum and HDPE sheet; plywood work for the table; and fitting bought bicycle, bearing and belt-drive parts. The whole machine weighs about 96 kg in six loads of 25 kg or less. The parts cost about $558 from the bill of materials.

> **Safety:** GravitySort is rotating machinery. The bowl stores about 165 J at 730 rpm and coasts for about 20 s after the drive stops; belts, chains and pulleys can trap fingers, hair and clothing. Keep every guard on whenever the drive can turn, and keep the lid clamps shut and the brake parked whenever the bowl is not in use. Welding, grinding and cutting steel need a welding helmet, gloves, eye and hearing protection and a fire-safe area. Epoxy, glass fibre and polyurethane casting need gloves, a respirator rated for organic vapour and good ventilation. Never use the machine with mercury.

## 2. What changed to make it buildable

The concept showed what GravitySort does; some of its parts could not be made, fixed or assembled as drawn. Each change below keeps what the machine does, and all of them are recorded in decision record GVS-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Frame | Cross members at heights where no rail met them, and two members that the spindle and the gearbox shaft passed straight through | Lower side rails carrying two pairs of members, one pair each side of each shaft; the tub members hung on four drop posts; end post and end members (Figure 3) | Every tube now welds to two others, and the shafts pass between members |
| Spindle bearings | Flanged bearings with nothing to bolt to | Two 6 mm plates welded under the member pairs; each bearing hangs under its plate (Figure 7) | A bearing needs a flat face for its four bolts |
| Spindle | A solid 25 mm shaft, though water must pass up it to the jacket | A 25 x 2 mm stainless tube with a nipple welded in its foot for the rotary union (Figure 6) | Water reaches the jacket without drilling a long hole |
| Bowl and jacket | No fixing to the spindle; the jacket open at the top | A flange hub pinned to the spindle, four bolts with spacers into nuts cast in the liner; a bonded ring closes the jacket (Figure 13) | The water can only leave through the ring holes |
| Liner core | A one-piece core that could not come out past the riffle rings | A printed core in six segments round a key (Figure 11) | The rings are undercuts |
| Tub | A centre hole over the upper bearing; a launder box through an uncut wall | A standpipe in a rubber grommet; a tailings pipe through a rubber grommet in the back wall (Figures 15 and 16) | Spilt slurry cannot reach the bearing; no plastic welding |
| Feed pipe | Ran down through the lid into the bowl, so the lid could not come off | Stops 15 mm above the lid (Figure 21) | The lid lifts straight off to flush the bowl |
| Pedal drive | The chain crossed a frame member; the outrigger arms ended in the air | Bottom bracket 100 mm above the jackshaft; outrigger bolted to the frame end by two plates (Figure 5) | The chain clears the frame; the outrigger lifts off for transport |
| Table drive | The take-off pulley ran into the members; the table belt looped round a frame rail | The jackshaft runs out in front of the frame; the table belt runs outside the frame | Nothing passes between the belt's two runs |
| Table | Solid legs; head on a single post; no clutch; concentrate tray where the tailings fall | Plywood flexure legs; head bolted to the frame end; a latched belt tensioner; tailings launder at the front and concentrate box at the far end (Figures 25 to 33) | Each product goes where the table delivers it |
| Motor option | The motor enclosed its own chain | A bolt-on cradle behind the frame (Figure 35) | The chain clears the motor |
| Water | The hose ran through the drive pulley; the tank post was not drawn | Tank post and cradle; the hose runs down outside the back of the frame | Clear path, easy to reach |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Front" is the side the hopper post stands on; "left" and "right" are as seen standing in front, so the pedal end is on the left and the table on the right. Heights are from the ground with the frame standing on level ground. Workshop tolerance is 1 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Base frame

![Figure 2. Making sketch of the base frame](../cad/drawings/GVS-DWG-101.png)

*Figure 2. Base frame making sketch (GVS-DWG-101).*

![Figure 3. Where every tube of the frame goes](05-build-plan/frame-cuts.png)

*Figure 3. Plan, elevation and cut list of the frame.*

**What it is and what it is made from.** The welded frame that carries everything else: the spindle and its bearings, the gearbox and jackshaft, the tub, the hopper and the water tank. Mild steel square tube 25 x 25 x 1.5 mm, 14.5 m in all; two bearing plates 150 x 130 x 6 mm; a tank cradle plate 250 x 250 x 5 mm with four gussets.

**How to make it.**

1. Cut the tubes to the cut list of Figure 3; square and deburr every end.
2. Build the two end frames flat on the floor: two legs 700 tall, a top end rail 550 long between them at the top, and, at the pedal end only, the low end member 550 long with its bottom 90 above the ground.
3. Stand the end frames up 900 apart (outside to outside) and join them with the four side rails, 850 long: two at the top and two with their bottom 255 above the ground. Tack, check that the diagonals of the top and of each side match within 2 mm, then weld.
4. Lay the four 600 mm members across the lower side rails: the two gearbox members with their centres 152.5 and 247.5 from the pedal end, and the two spindle members at 487.5 and 612.5. Weld.
5. Weld the two tub members, 600 long, 445 above the ground, each held up by two drop posts 205 long from the top side rails, directly above the spindle members.
6. Weld the end post (560) upright at the middle of the pedal end, from the low end member to the top end rail, and the head member (550) between the table-end legs with its bottom 600 above the ground.
7. Weld the tank post member (550) between the top side rails, 120 from the pedal end, and the tank post (545) upright on it, 180 behind the centre line. Weld the cradle plate on top and a pair of gussets each way at both ends of the post.
8. Drill each bearing plate: a 40 mm centre hole and four 11 mm holes at the corners of a 70 mm square. Clamp one plate under the spindle members and one under the tub members, both centred on the bowl axis, 550 from the pedal end on the centre line. Hang a plumb line through both centre holes; when it passes through both centres, weld the plates.
9. Drill the bolt holes listed in the later sections (tub, hopper foot, outrigger plates, head plate, caliper bracket, belt guard hangers, tensioner bracket, motor cradle). Prime and paint.

**How it fits the parts next to it.** Everything else bolts to it; see each section.

**Check before moving on.** The frame stands on all four feet without rocking; a plumb line through the two bearing plate holes is within 1 mm of both centres; the gearbox members are level across.

### 3.2 Pedal outrigger

![Figure 4. Making sketch of the pedal outrigger](../cad/drawings/GVS-DWG-102.png)

*Figure 4. Pedal outrigger making sketch (GVS-DWG-102).*

**What it is and what it is made from.** The rider's seat and the bottom bracket for the crank, on a welded stand that bolts to the pedal end of the frame. Square tube 25 x 25 x 1.5 mm (2.1 m), round tube 32 x 2 mm (675 mm), plate 6 mm, and a bottom bracket shell cut from a scrap bicycle frame.

**How to make it.**

1. Cut the spine 529, the seat cross foot 400, the pedal cross foot 300, the pedal post 393 and the top arm 504.
2. Weld the two cross feet under the spine: the seat foot at the far end, the pedal foot 185 from the far end.
3. Weld the pedal post upright on the spine over the pedal foot. Weld the bottom bracket shell on top of it, its axis across the machine, centre 438 above the ground.
4. Weld the seat tube upright on the spine 172 behind the pedal post (toward the far end). Cut a 40 mm slot down its top for a bicycle seat clamp.
5. Weld the top arm from the seat tube to the frame end, 600 to 625 above the ground.
6. Weld an end plate 80 wide across the end of the spine (125 tall) and across the end of the top arm (65 tall). Drill two 9 mm holes in each to match the low end member and the end post.

**How it fits the parts next to it.**

![Figure 5. Joint 5: outrigger end plates on the frame end](05-build-plan/joint-05.png)

*Figure 5. Each end plate lies flat on the frame end; two M8 bolts through each. The outrigger itself stays 6 mm clear of the frame.*

**Check before moving on.** Bolted on, the bottom bracket axis is level and square to the frame end; the outrigger stands on its feet without rocking.

### 3.3 Spindle

![Figure 6. Making sketch of the spindle](../cad/drawings/GVS-DWG-103.png)

*Figure 6. Spindle making sketch (GVS-DWG-103).*

**What it is and what it is made from.** The vertical shaft that carries the bowl and the brake disc, turns in two bearings and carries the fluidization water up its bore. Stainless 316 tube 25 x 2 mm, 372 long, and a 1/2 in BSP stainless hex nipple.

**How to make it.**

1. Cut 372 long; square both ends and deburr the bore.
2. TIG weld the nipple into the bottom end so its thread stands below the tube, and check that water runs through freely.
3. From the bottom end, mark: driven pulley 16 to 56; lower bearing 71 to 111; brake collar 173 to 196; upper bearing 236 to 276; hub 341 to 368.
4. Drill a 6 mm cross hole for the hub pin 349 from the bottom end. File a small flat under each bearing's set screws.

**How it fits the parts next to it.**

![Figure 7. Joint 1: the spindle in its bearings](05-build-plan/joint-01.png)

*Figure 7. Each bearing hangs under its plate on four M10 bolts; the brake disc runs between the two plates; the driven pulley and the rotary union are below.*

The two flanged bearing units hang under the bearing plates, 255 and 420 above the ground at their centres, and hold the spindle by their set screws on the flats. The driven pulley sits on its taper bush below the lower bearing, 180 to 220 above the ground; the rotary union screws onto the nipple below that.

**Check before moving on.** Rolled on a flat sheet of glass the spindle is straight within 0.2 mm; fitted in its bearings it turns freely by hand.

### 3.4 Brake flange and caliper bracket

![Figure 8. Making sketch of the brake flange and caliper bracket](../cad/drawings/GVS-DWG-113.png)

*Figure 8. Brake flange and caliper bracket making sketch (GVS-DWG-113).*

**What it is and what it is made from.** The flange that carries the 160 mm bicycle brake disc on the spindle, and the bracket that holds the caliper. Steel plate 6 mm and a 25 mm bore shaft collar.

**How to make it.**

1. Flange: cut a 6 mm disc 56 across; drill six M5 holes on a 44 mm circle to match the disc. Weld it square on the collar (40 across, 20 long) and face it true.
2. Bracket: cut and bend an L of 6 mm plate, foot 41 x 60, upright 60 wide and 75 tall. Drill two 7 mm holes in the foot and the caliper's mounting holes in the upright to suit the caliper bought.

**How it fits the parts next to it.**

![Figure 9. Joint 13: caliper on its bracket](05-build-plan/joint-13.png)

*Figure 9. The bracket foot bolts on top of the right spindle member (two M6); the disc runs in the caliper slot.*

The collar clamps the spindle 337 to 360 above the ground; the disc sits on the flange, 360 above the ground, between the two bearing plates. The caliper bolts to the upright with 2 mm each side of the disc.

**Check before moving on.** Spun by hand the disc runs true within 0.3 mm at the pads and does not rub.

### 3.5 Bowl shell

![Figure 10. Making sketch of the bowl shell](../cad/drawings/GVS-DWG-104.png)

*Figure 10. Bowl shell making sketch (GVS-DWG-104).*

**What it is and what it is made from.** The glass fibre cup that is both the outer mould for the liner and the bowl's strength. Glass mat and epoxy, 4 mm, hand laid over a printed plug.

**How to make it.**

1. Print a plug the shape of the liner's outside: 146 across the base, 236 across the top, 188 tall. Sand it smooth, seal it and wax it.
2. Lay up 4 mm of glass mat and epoxy over the plug, floor and walls. Cure as the resin maker says.
3. Trim the lip square, 192 above the outside of the floor; pull the plug.
4. Drill four 6 mm holes in the floor on a 60 mm circle, at 45 degrees to the machine's axes.

**How it fits the parts next to it.** The liner is cast inside it (section 3.6); the jacket goes round it with a 12 mm gap (section 3.7).

**Check before moving on.** The wall is 4 mm thick, give or take 0.5, all round the lip; no dry glass or air bubbles.

### 3.6 Bowl liner

![Figure 11. Making sketch of the bowl liner](../cad/drawings/GVS-DWG-105.png)

*Figure 11. Bowl liner making sketch (GVS-DWG-105).*

**What it is and what it is made from.** The wear surface of the bowl, with the four riffle rings that hold the gold. Cast polyurethane, Shore 80 to 90A, 8 mm thick, cast inside the shell.

**How to make it.**

1. Print the core: the inside of the bowl (130 across the floor, 220 across the lip, 180 deep) with the four ring grooves, split into six segments round a central key, plus a lip spigot that centres it on the shell.
2. Set four M6 stainless nuts on the shell floor over its holes, held by bolts from below with release on their threads.
3. Coat the core with release, assemble it and centre it in the shell.
4. Mix and pour the polyurethane slowly down one side; cure as the maker says.
5. Pull the key, lift the segments inward one at a time, and take out the bolts (the nuts stay cast in).
6. Drill about 89 holes of 1.0 mm from the outside of the shell through shell and liner into the ring grooves, more in the lower grooves.

**How it fits the parts next to it.** The liner stays bonded in the shell; they are replaced together.

**Check before moving on.** Rings are 6 thick, stand 12 in from the wall and have no voids; the floor is 8 thick over the nuts; air blown into the holes comes out in every groove.

### 3.7 Fluidization jacket and hub

![Figure 12. Making sketch of the fluidization jacket](../cad/drawings/GVS-DWG-106.png)

*Figure 12. Fluidization jacket making sketch (GVS-DWG-106).*

**What it is and what it is made from.** The glass fibre cup round the bowl that holds the fluidization water at 12 mm from the shell, so that it is pushed through the ring holes as the bowl spins. Glass mat and epoxy, 4 mm; a closing ring of 4 mm GFRP sheet; a bought 25 mm bore shaft flange hub.

**How to make it.**

1. Print a plug 12 mm larger all round than the shell; lay up 4 mm of glass and epoxy over it; trim the top 178 above the outside of the floor.
2. Drill a 25.5 mm centre hole and four 6 mm holes on a 60 mm circle, lined up with the shell's.
3. Cut a closing ring from 4 mm GFRP sheet, 253 outside and 229 inside.
4. Drill a 6 mm cross hole through the hub's boss for the pin.

**How it fits the parts next to it.**

![Figure 13. Joint 2: bowl, jacket and hub](05-build-plan/joint-02.png)

*Figure 13. Four M6 bolts pass up through the hub flange, the jacket floor and four 12 mm spacer bushes into the nuts cast in the liner. The spindle's top end is flush with the jacket floor, so water leaves it into the gap.*

Stand four 12 mm spacer bushes on the jacket floor over its holes, lower the bowl in, and bolt through from below with the hub flange under the jacket floor. Bond the closing ring between the shell and the jacket's top with epoxy, and seal the spindle hole in the jacket floor with an O-ring.

**Check before moving on.** Fill the jacket through the hub at about 10 kPa (1 m of water): no leak at the closing ring, and water comes out of every groove hole. Balance the bowl group on a knife edge through the hub: it must not turn to one side.

### 3.8 Splash tub

![Figure 14. Making sketch of the splash tub](../cad/drawings/GVS-DWG-107.png)

*Figure 14. Splash tub making sketch (GVS-DWG-107).*

**What it is and what it is made from.** The plastic tub round the bowl that catches the tailings thrown over the lip and sends them to the settling pond. A used HDPE drum about 430 across with a 6 mm wall, a 63 mm standpipe, a 75 mm tailings pipe and two rubber pipe grommets.

**How to make it.**

1. Cut the drum 320 above its own floor; file the rim smooth and level.
2. Floor: a 76 mm centre hole for the standpipe grommet, and four 9 mm bolt holes, 62.5 each side of centre along the machine and 150 each side across it.
3. Back wall: a 98 mm hole for the tailings pipe grommet, centre 64 above the floor, on the line from the tub centre to the back.
4. Drill the two lid clamp bases on the wall, 45 degrees each side of the front.
5. Cut the standpipe 50 long and the tailings pipe about 240 long, with a hose to the pond beyond.

**How it fits the parts next to it.**

![Figure 15. Joint 3: tub floor, standpipe and tub members](05-build-plan/joint-03.png)

*Figure 15. The tub floor sits on the two tub members (four M8 bolts). The standpipe stands through its grommet on the upper bearing plate, 10 mm below the bowl hub, so slurry spilt in the tub cannot reach the bearing.*

![Figure 16. Joint 14: tailings pipe through the tub wall](05-build-plan/joint-14.png)

*Figure 16. A rubber pipe grommet seals the pipe in the curved wall; the pipe runs out between the drop posts, 12 mm clear of the frame.*

**Check before moving on.** Fill the tub 50 mm deep with water: no leak at either grommet; the water runs out of the tailings pipe once it reaches the pipe.

### 3.9 Lid guard and clamps

![Figure 17. Making sketch of the lid guard](../cad/drawings/GVS-DWG-108.png)

*Figure 17. Lid guard making sketch (GVS-DWG-108).*

**What it is and what it is made from.** The cover that keeps hands out of the spinning bowl and holds back splash. HDPE sheet 10 mm, and two bought over-centre toggle clamps.

**How to make it.**

1. Scribe a 446 circle and a 60 circle at its centre; cut both with a jigsaw and file the edges smooth.
2. Bolt the two clamps to the tub wall at the holes drilled in section 3.8, with their hooks over the lid edge. Drill the right-hand clamp's lever for the interlock pin on the brake cable.

**How it fits the parts next to it.**

![Figure 18. Joint 6: lid clamp](05-build-plan/joint-06.png)

*Figure 18. The clamp's hook closes over the lid edge; the lid overhangs the tub rim by 8 mm all round.*

**Check before moving on.** With both clamps shut the lid cannot be lifted by hand; with the brake released, the interlock pin stops the right clamp opening.

### 3.10 Hopper support

![Figure 19. Making sketch of the hopper support](../cad/drawings/GVS-DWG-110.png)

*Figure 19. Hopper support making sketch (GVS-DWG-110).*

**What it is and what it is made from.** A post, an arm and a ring that hold the hopper over the bowl. Square tube 25 x 25 x 1.5 mm and 6 mm plate.

**How to make it.**

1. Cut a foot plate 75 x 25 x 6 and drill two 9 mm holes 50 apart.
2. Weld a 294 post upright on it, and a 175 arm on the post top, pointing toward the back.
3. Cut a ring from 6 mm plate, 176 inside and 216 outside; weld it flat on the arm end.

**How it fits the parts next to it.** The foot bolts on the front top rail on the bowl's centre line (two M8). The ring centre must sit over the spindle; check with a plumb line from the ring to the spindle top. The hopper cone drops into the ring, which holds it 40 above its bottom.

**Check before moving on.** The ring is level and its centre within 3 mm of the spindle axis.

### 3.11 Hopper and screen

![Figure 20. Making sketch of the hopper](../cad/drawings/GVS-DWG-109.png)

*Figure 20. Feed hopper making sketch (GVS-DWG-109).*

**What it is and what it is made from.** The funnel the milled ore is shovelled into, with a 2 mm screen on top and the feed pipe below. Galvanized sheet 1.2 mm, steel tube 44 x 6 mm, 2 mm punched stainless sheet and flat bar for the screen rim.

**How to make it.**

1. Mark out the flat pattern, a ring sector of inner radius 169, outer radius 411 and 149 degrees, plus a 15 mm seam lap. Cut, roll into a cone 140 across the bottom and 340 across the top, rivet and seal the seam.
2. Rivet and seal a 140 mm bottom disc with a 32 mm centre hole.
3. Weld or bond a 145 long feed pipe under the hole.
4. Screen: roll a 360 mm ring of flat bar and fix the punched sheet inside it.

**How it fits the parts next to it.**

![Figure 21. Joint 7: hopper in its support ring](05-build-plan/joint-07.png)

*Figure 21. The cone drops into the ring and wedges; it lifts out for cleaning. The screen rests on the hopper rim.*

The feed pipe ends 15 above the lid, over the bowl centre: the slurry falls through the lid's hole onto the bowl floor, and the lid lifts off without touching the hopper.

**Check before moving on.** Water poured in runs out of the pipe and not at the seam; the pipe end is 15 mm, give or take 3, above the lid.

### 3.12 Bowl belt guard

![Figure 22. Making sketch of the bowl belt guard](../cad/drawings/GVS-DWG-111.png)

*Figure 22. Bowl belt guard making sketch (GVS-DWG-111).*

**What it is and what it is made from.** A shallow box under the frame round the two bowl drive pulleys and their belt. Perforated steel sheet 1.2 mm and flat bar 25 x 3 mm.

**How to make it.**

1. Fold a tray (bottom and four sides) 566 x 316 x 60 and a separate top panel.
2. Cut a 40 mm hole in the top over the gearbox shaft and another over the spindle, and a 32 mm hole in the bottom for the spindle foot.
3. Cut four hangers 50 long from flat bar; bend a tab on each end and drill them.
4. Fix the speed sensor's bracket under the top, beside the driven pulley.

**How it fits the parts next to it.** The four hangers bolt to the top and up to the undersides of the left gearbox member and the left spindle member. The guard stays 6 mm clear of both pulleys and the belt, 5 mm below the lower bearing and above the rotary union.

**Check before moving on.** No finger can reach a pulley or the belt through any opening; the tray comes off without moving the top.

### 3.13 Pedal chain case

![Figure 23. Making sketch of the pedal chain case](../cad/drawings/GVS-DWG-112.png)

*Figure 23. Pedal chain case making sketch (GVS-DWG-112).*

**What it is and what it is made from.** A closed sheet case round the pedal chain from the chainring to the freewheel. Steel sheet 1.2 mm.

**How to make it.**

1. Cut two side plates to the outline of Figure 23 (round both sprockets, 12 mm outside the chain), 703 long and 253 tall.
2. Cut 28 mm holes in both plates for the crank axle and the jackshaft.
3. Join the plates with a rim strip 26 wide, leaving the bottom flat where it crosses the left gearbox member. Make the outer plate removable (screws into tabs on the rim).
4. Fold a tab 25 wide for the pedal post.

**How it fits the parts next to it.**

![Figure 24. Joint 4: jackshaft and gearbox on the gearbox members](05-build-plan/joint-04.png)

*Figure 24. The two pillow blocks and the gearbox bolt straight onto the two gearbox members; the chain case (left off here) rests on the left member.*

The case rests on the left gearbox member (one M6 bolt) and is tabbed to the pedal post (one M6). Its inner plate is 4 mm from the gearbox; its outer plate is 2 mm inside the right crank arm.

**Check before moving on.** Turn the cranks a full turn: nothing rubs, and the chain does not touch the case.

### 3.14 Table base and flexure legs

![Figure 25. Making sketch of the table base and flexure legs](../cad/drawings/GVS-DWG-115.png)

*Figure 25. Table base and flexure legs making sketch (GVS-DWG-115).*

**What it is and what it is made from.** The stand of the shaking table: a welded base on the ground and four plywood legs that bend as the deck shakes along the table. Square tube 25 x 25 x 1.5 mm (2.4 m), marine plywood 18 mm, angle 40 x 40 x 4 mm.

**How to make it.**

1. Cut two base rails 940 and two cross tubes 245; weld them flat into a rectangle with the rails 270 apart at their centres.
2. Cut four legs 80 wide from 18 mm marine plywood: the front two 772 long, the back two 786 (the deck slopes 3 degrees to the front). Cut each top to that slope. Seal the edges.
3. Cut eight cleats 80 long from the angle; drill each for two M8 bolts in each leg.

**How it fits the parts next to it.**

![Figure 26. Joint 9: flexure leg, cleats, base and deck](05-build-plan/joint-09.png)

*Figure 26. The thin side of each leg faces along the table, so the leg bends as the deck moves 15 mm.*

The legs stand on the rails 40 and 900 from the head end of the base. A cleat bolts each leg's foot to the rail and each leg's top to the underside of the deck. Packers under the top cleats set the deck slope between 2 and 4 degrees.

**Check before moving on.** With the deck on, push it along by hand: it moves about 10 mm each way and springs back to the middle; it does not rock across.

### 3.15 Table deck

![Figure 27. Making sketch of the table deck](../cad/drawings/GVS-DWG-114.png)

*Figure 27. Shaking table deck making sketch (GVS-DWG-114).*

**What it is and what it is made from.** The riffled top that sorts the bowl concentrate by density. Marine plywood 18 mm, HDPE sheet 3 mm and strip, 40 mm PVC pipe, two small steel plates.

**How to make it.**

1. Cut the deck 1000 x 450; glue and screw 3 mm HDPE over its top.
2. Glue nine riffles of HDPE strip, 6 wide and 8 tall, along the deck, the first 60 in from the front edge and the rest every 38. Each starts 30 later than the one in front (60, 90 and so on up to 300 from the head end) and all stop 40 short of the far end.
3. Build a feed box 180 x 90 x 70 at the back of the head end.
4. Drill a 40 mm PVC pipe with 3 mm holes every 25, cap one end, fit a hose tail on the other, and clip it along the back edge from 190 to 960 from the head end.
5. Screw two steel cheeks 40 x 22 x 6, 12 apart, under the head end on the centre line; drill them 12 mm for the pitman pin.

**How it fits the parts next to it.** The deck sits on the four leg tops; the pitman pin joins its cheeks to the head (section 3.17); the launder runs under its front edge and the concentrate box under its far end (section 3.18).

**Check before moving on.** The deck is flat within 1 mm across each diagonal; the riffles are straight and well stuck.

### 3.16 Table head plate and shelf

![Figure 28. Making sketch of the table head plate and shelf](../cad/drawings/GVS-DWG-116.png)

*Figure 28. Table head plate and shelf making sketch (GVS-DWG-116).*

**What it is and what it is made from.** The bracket on the table end of the frame that carries the head shaft, the eccentric that shakes the deck, and the 125 mm pulley the table belt turns. Steel plate 6 mm; a 20 mm shaft; two 20 mm pillow blocks; a 60 mm eccentric disc.

**How to make it.**

1. Cut the head plate 375 x 110 and drill four 9 mm holes to match the head member and the top end rail.
2. Cut the shelf 184 deep, with a cut-out 130 x 280 between the bearing positions; weld it square to the plate, 677 above the ground, with two triangular gussets 90 x 90 under it.
3. Drill two pairs of 12 mm holes in the shelf, 95 apart, for the pillow blocks, 330 apart across the machine.
4. Eccentric: a 60 mm steel disc with its 20 mm bore 7.5 off centre (a 15 mm stroke) and two set screws.

**How it fits the parts next to it.** The plate bolts to the frame's table end (four M8). The pillow blocks bolt on the shelf; the head shaft runs through them with the eccentric at the centre line and the 125 mm pulley 330 in front of the centre line, in line with the take-off pulley on the jackshaft.

**Check before moving on.** The shelf is square to the plate; the shaft turns freely by hand; the head pulley lines up with the take-off pulley (straight edge across both faces).

### 3.17 Pitman arm

![Figure 29. Making sketch of the pitman arm](../cad/drawings/GVS-DWG-117.png)

*Figure 29. Pitman arm making sketch (GVS-DWG-117).*

**What it is and what it is made from.** The link that turns the eccentric's rotation into the deck's to-and-fro stroke. Flat bar 22 x 12 mm, 12 mm plate, a 60 mm bore bronze bush and a 12 mm pin.

**How to make it.**

1. Cut a ring 84 across from 12 mm plate with a 61 mm bore; press the bronze bush in.
2. Weld the flat bar arm to the ring so the pin hole is 111 from the eccentric centre; drill the pin hole 12 mm.

**How it fits the parts next to it.**

![Figure 30. Joint 10: head, pitman and deck](05-build-plan/joint-10.png)

*Figure 30. The eye runs on the eccentric through the shelf cut-out; the pin joins the arm to the cheeks under the deck.*

**Check before moving on.** Turning the head shaft one full turn moves the deck 15 mm and back; the eye clears the shelf all round.

### 3.18 Tailings launder and concentrate box

![Figure 31. Making sketch of the launder and box](../cad/drawings/GVS-DWG-118.png)

*Figure 31. Tailings launder and concentrate box making sketch (GVS-DWG-118).*

**What it is and what it is made from.** The launder catches the light material washed off the deck's front edge; the lockable box catches the gold concentrate that walks off the end of the riffles. Galvanized sheet 1.2 mm and square tube for the legs.

**How to make it.**

1. Launder: fold a U channel 100 wide, 60 deep and 810 long with a 60 mm spout at the head end; weld or rivet two legs 640 tall.
2. Box: fold a box 120 x 290 x 120 tall, open top, with a hinged lid and a padlock hasp; four legs 640 tall.

**How it fits the parts next to it.** The launder stands under the deck's front edge, the box under its far end; both are 15 mm or more clear of the moving deck.

**Check before moving on.** With the deck at both ends of its stroke, nothing touches the launder or the box; the lid locks.

### 3.19 Table belt tensioner and guard

![Figure 32. Making sketch of the table belt tensioner](../cad/drawings/GVS-DWG-119.png)

*Figure 32. Table belt tensioner making sketch (GVS-DWG-119).*

**What it is and what it is made from.** The table belt runs slack (no drive) until this lever presses an idler onto it, so it is the clutch between bowl and table. Flat bar 25 x 6 and 20 x 6, a 60 mm flat idler pulley, a 12 mm stub axle and pivot bolt, 6 mm plate; the guard is 1.2 mm steel sheet.

**How to make it.**

1. Arm 150 between the pivot hole and the idler axle hole; handle 135 long welded to the arm at the pivot.
2. Bracket: a 6 mm plate with two 7 mm holes for the front top rail, 430 from the pedal end, and a 12 mm pivot hole, and a notched latch plate that holds the handle down (driving) or up (slack).
3. Guard: an outer plate shaped round both table pulleys and the idler, 22 mm outside them, with a 40 mm rim toward the frame and a slot for the arm and handle.

**How it fits the parts next to it.**

![Figure 33. Joint 11: the tensioner on the table belt](05-build-plan/joint-11.png)

*Figure 33. Handle down presses the idler onto the belt's top run and the table runs; handle up and the belt goes slack.*

**Check before moving on.** Handle down, the head turns with the jackshaft without the belt slipping; handle up, the jackshaft turns and the head stays still.

### 3.20 Motor cradle (motor option)

![Figure 34. Making sketch of the motor cradle](../cad/drawings/GVS-DWG-120.png)

*Figure 34. Motor cradle making sketch (GVS-DWG-120).*

**What it is and what it is made from.** Only for the motor option: the bracket that holds the MotionCore reference hub motor behind the frame. Steel plate 6 mm; a sheet steel chain guard.

**How to make it.**

1. Cut a base plate 130 x 117 and drill two 9 mm holes for the back lower rail.
2. Cut two dropouts 60 wide and 110 tall with a 12 mm slot open upward, centre 96 above the base; weld them upright on the base, 76 apart inside.
3. Make the chain guard: an outer plate round both sprockets with a rim round the jackshaft sprocket, on two spacers from the outer dropout.

**How it fits the parts next to it.**

![Figure 35. Joint 12: motor cradle on the back rail](05-build-plan/joint-12.png)

*Figure 35. The cradle bolts on the back lower rail; the motor drops into the open slots and its torque washers stop it turning.*

**Check before moving on.** The motor sprocket lines up with the jackshaft sprocket (straight edge); the motor is 10 mm clear of the base and 17 mm clear of the frame.

### 3.21 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Flanged bearing units (line 5).** Two 25 mm bore insert bearings in square flanged housings (UCF205 class), set-screw locking, contact seals.
- **Driven pulley (line 5).** 100 mm A-section V-pulley with a taper bush for 25 mm.
- **Rotary union (line 4).** Single-passage water rotary union, 1/2 in BSP on the shaft side, side port for a 3/4 in hose tail.
- **Shaft flange hub (line 4).** 25 mm bore, about 80 mm flange with four holes on a 60 mm circle.
- **Gearbox (line 9).** Right-angle 1:1 bevel gearbox with a through 20 mm input shaft about 33 mm above its feet and a downward output shaft; a used agricultural or garden machine gearbox is fine.
- **Jackshaft parts (line 9).** 20 mm bright steel shaft 740 long; two 20 mm pillow blocks (UCP204 class); a 12T bicycle freewheel on an adapter; a 140 mm A-section take-off pulley; the 300 mm A-section drive pulley for the gearbox output; the motor sprocket if the motor is fitted.
- **Belts and chain (lines 9 and 10).** An A-section link V-belt for the bowl drive (fixed centres, so the length is set by its links); an A-section V-belt to length for the table drive (measure on the machine); 1/2 x 1/8 in bicycle chain.
- **Bicycle parts (line 8).** Bottom bracket shell (cut from a scrap frame), bottom bracket bearings and axle, crank arms with a 48T chainring, pedals, saddle, 27.2 mm seat post and seat clamp.
- **Brake (line 18).** 160 mm 6-bolt disc, mechanical disc caliper, brake lever with a parking latch, cable and housing; a pin on the cable for the lid clamp.
- **Speed display (line 19).** Wired bicycle computer with its magnet and sensor.
- **Water (line 13).** 60 L HDPE drum, 3/4 in ball valve and tank connector, 2 to 20 L/min rotameter, 3/4 in hose and clips, a ratchet strap, a tee, valve and hose to the wash pipe.
- **Tub fittings (line 6).** Rubber pipe grommets for 63 and 75 mm pipe in a 6 mm wall; 63 and 75 mm pipe offcuts.
- **Fixings (line 17).** M6, M8 and M10 bolts with nylon-insert nuts and washers (about 60 in all), six M6 x 4 stainless nuts for the liner, a 6 mm pin and R-clip for the hub and a 12 mm pin for the pitman, hose clamps, sealant, an O-ring for the jacket floor, primer and paint.
- **Motor option (lines 12 and 20).** The MotionCore kit and its reference 250 W geared hub motor with a sprocket on its disc mount (from the MotionCore project), and a battery the user chooses.

## 4. Putting it together

In each picture the parts already fitted are grey and the parts being fitted are in colour, with an arrow showing the way they go in.

### Step 1: set the frame on level ground

![Step 1](05-build-plan/step-01.png)

Put a packer under any foot that rocks. Check the bearing plates are level with a spirit level.

### Step 2: bolt the pedal outrigger to the frame end

![Step 2](05-build-plan/step-02.png)

Four M8 bolts through the two end plates, with washers and nylon-insert nuts.

### Step 3: gearbox, jackshaft and drive pulley

![Step 3](05-build-plan/step-03.png)

Bolt the gearbox across the two gearbox members (four M8). Slide the jackshaft through the front pillow block, the gearbox's input, the freewheel and the back pillow block, with the take-off pulley on its front end and the motor sprocket (if fitted) on its back end; bolt the pillow blocks down (four M10 each pair). Fit the 300 mm drive pulley on the gearbox output shaft under the members.

### Step 4: crankset and pedal chain

![Step 4](05-build-plan/step-04.png)

Fit the bottom bracket bearings and axle, the cranks and the 48T chainring. Fit the chain round the chainring and the freewheel and set its slack to about 10 mm at the middle of the lower run.

### Step 5: bearings, spindle, brake disc and driven pulley

![Step 5](05-build-plan/step-05.png)

Bolt the two bearing units under their plates (four M10 each), loosely. Feed the spindle down through the upper bearing, the brake flange (with the disc bolted on), the lower bearing and the driven pulley. Set the spindle so its top is 536 above the ground, tighten the bearing bolts, then the set screws on the flats; clamp the brake collar and the pulley's taper bush. **Hold point:** the spindle turns freely by hand and the disc runs true.

### Step 6: rotary union and bowl belt

![Step 6](05-build-plan/step-06.png)

Seen from below. Screw the rotary union onto the nipple at the spindle foot with thread sealant, its side port toward the pedal end. The bowl belt is a link V-belt, because the pulley centres are fixed: fit it round both pulleys and add or remove links until it deflects about 10 mm under a firm thumb.

### Step 7: belt guard and chain case

![Step 7](05-build-plan/step-07.png)

Seen from below. Bolt the belt guard on its four hangers and fit its tray. Fit the chain case: flat on the left gearbox member (one M6) and tabbed to the pedal post (one M6), then its outer plate.

### Step 8: brake caliper, lever and speed display

![Step 8](05-build-plan/step-08.png)

Bolt the caliper bracket on the right spindle member (two M6) and the caliper on it. Fix the brake lever and the speed display to the pedal-end top rail, facing the rider; run the brake cable to the caliper and the interlock pin's branch to the right lid clamp; run the sensor wire from under the guard to the display. Set the display's wheel size to 1,667 mm.

### Step 9: splash tub, standpipe and tailings pipe

![Step 9](05-build-plan/step-09.png)

Set the tub on the tub members and bolt it down (four M8 with large washers). Push the standpipe through its grommet until it stands on the upper bearing plate. Fit the tailings pipe through its grommet at the back and connect the hose to the settling pond.

### Step 10: bowl onto the spindle

![Step 10](05-build-plan/step-10.png)

Lower the bowl, jacket and hub together over the spindle top until the hub flange sits on the spindle's stop, line up the cross holes, and push the 6 mm pin through with its clip. **Hold point:** the bowl spins true by hand, at least 12 mm clear of the standpipe and 50 mm clear of the tub wall.

### Step 11: lid guard and clamps

![Step 11](05-build-plan/step-11.png)

Fit the lid on the rim and close both clamps. Fit the interlock pin to the right clamp.

### Step 12: hopper support, hopper and screen

![Step 12](05-build-plan/step-12.png)

Bolt the support foot on the front top rail (two M8). Drop the hopper into its ring and lay the screen on top. Check the pipe end is 15 mm above the lid.

### Step 13: header tank, valve, rotameter and hose

![Step 13](05-build-plan/step-13.png)

Fit the tank connector and valve near the bottom of the drum, on its back; set the drum on the cradle and strap it to the post. Bolt the rotameter bracket on the back top rail. Run the 3/4 in hose from the valve down the back to the rotameter, then down outside the back of the frame, along the ground under the belt guard, to the rotary union's side port. Clip it every 300 mm.

### Step 14: table base and flexure legs

![Step 14](05-build-plan/step-14.png)

Set the base on level ground, in line with the frame, with its head end 190 from the frame's table end. Bolt the four legs to the base rails with their bottom cleats.

### Step 15: deck onto the legs

![Step 15](05-build-plan/step-15.png)

With a helper, lay the deck on the leg tops and bolt the top cleats to its underside. Set the slope to 3 degrees down to the front with packers under the back cleats.

### Step 16: table head and pitman

![Step 16](05-build-plan/step-16.png)

Bolt the head plate to the frame's table end (four M8). Bolt the pillow blocks on the shelf, slide the head shaft through with the eccentric and the pulley, and tighten them. Fit the pitman eye over the eccentric through the shelf cut-out and pin its other end between the deck cheeks.

### Step 17: table belt, tensioner and guard

![Step 17](05-build-plan/step-17.png)

Bolt the tensioner bracket on the front top rail (two M6) and fit the arm and idler. With the handle up, fit the table belt round the take-off and head pulleys. Bolt the table belt guard to the frame and the head plate. **Hold point:** handle down, the table runs; handle up, it stops.

### Step 18: tailings launder and concentrate box

![Step 18](05-build-plan/step-18.png)

Stand the launder under the deck's front edge with its spout at the head end over a bucket, and the box under the deck's far end. Check 15 mm clearance to the deck at both ends of its stroke.

### Step 19: motor option

![Step 19](05-build-plan/step-19.png)

Seen from the back. Only for the motor option: bolt the cradle on the back lower rail (two M8), drop the motor into the dropouts with its torque washers, fit the chain to the jackshaft sprocket and the guard. Hang the MotionCore module under the top rails at the pedal end on two straps, wire it as the MotionCore build plan says, set its speed limit to 900 rpm at the spindle, and wire the lid switch to a brake input. **Hold point:** safety stop S6 in section 6.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of GVS-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Guards fitted | R12 | Try to reach every belt, chain, pulley and sprocket by hand with the drive still | No moving part can be reached |
| Brake and interlock | R12, R13 | Spin the bowl to about 600 rpm (pedals, no water), stop pedalling, pull the brake; try to open the right clamp before and after parking | Stops within 15 s; the clamp opens only with the brake parked |
| Speed display | R3 | Pedal at a steady cadence; count the cadence | The display reads bowl rpm / 10, matching 12 times the cadence within 5 % |
| Pedal speed range | R3, R6 | Pedal at 50, 60 and 71 rpm | 600 to 850 rpm at the bowl |
| Fluidization flow | R4, R8 | Fill the tank, open the valve, read the rotameter with the bowl still and turning at 730 rpm | 8 to 15 L/min; water from every ring groove |
| Water use | R8 | Rotameter plus the slurry water at the feed rate | 1.5 m3/h or less |
| Table drive | R5 | Handle down, pedal at 60 rpm; count the strokes; measure the stroke | 240 to 300 strokes per minute; 15 mm stroke |
| Lid off for a flush | R13 | Time stopping, braking, opening the lid and rinsing the rings into a container | 5 min or less, no tools |
| Loads and mass | R11 | Weigh each of the six loads | Every load 30 kg or less; total recorded (about 96 kg estimated) |
| Assembly time | R11 | Two people assemble the six loads with hand tools | 30 min or less |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before any welding.** Fire extinguisher and a clear, non-flammable floor; no solvents, resin or plastic nearby; helmet, gloves and covered skin.
- **S2. Before laminating or casting.** Ventilation running; gloves, eye protection and an organic vapour respirator; resin and polyurethane datasheets read; no flame or welding in the same space.
- **S3. Before the bowl turns for the first time (step 10).** The liner has no cracks, voids or debonding; all four bowl bolts and the hub pin are in; the bowl spins true by hand; the lid, clamps, belt guard and chain case are fitted.
- **S4. Before any spin above hand speed.** The brake stops the bowl and parks; the interlock pin stops the right clamp opening; the speed display works; nobody stands in line with the tub; a calculation shows that the tub and lid contain a piece of liner thrown at 1,200 rpm.
- **S5. Every run.** Never above 900 rpm (90 on the display). Before opening the lid: stop pedalling, apply and park the brake, and wait for the bowl to stop. Never remove or bypass the interlock pin.
- **S6. Before the motor is powered (motor option).** The MotionCore emergency stop works and is within the operator's reach; its speed limit is set to 900 rpm at the spindle and checked; the lid switch removes torque; the battery is out of the wet.
- **S7. Before water and slurry.** The settling pond is fenced; boots with grip; no mercury anywhere on site.

## 7. Tools, skills and workspace

**Tools.** Angle grinder with cutting and flap discs, or a metal bandsaw; MIG or stick welder; bench drill and hand drill with drills 3 to 12 mm, a 40 mm hole saw and step drill, and 76 and 98 mm hole saws for plastic; taps M5 and M6; files, deburring tool, square, tape, scriber, spirit level, plumb line and callipers; jigsaw with wood, plastic and metal blades; sheet snips, a folder or bending bar for 1.2 mm sheet, and a rivet tool; TIG welder (or a fabricator) for the stainless nipple; FDM 3D printer for the plugs and the core; laminating brushes, rollers and mixing gear; spanners and sockets to 17 mm; torque wrench; tachometer or the speed display; stopwatch; scale to 30 kg.

**Skills.** Welding steel tube to a square, accurate frame; glass fibre lay-up and polyurethane casting; drive alignment of belts and chains. No certified trade is needed, but the welds that carry the spindle and the gearbox should be made by someone who welds regularly.

**Workspace.** A flat concrete floor about 4 x 3 m for the frame and table; a separate ventilated area for laminating and casting; a fire-safe area for welding and grinding; outdoor space with water for the first runs.

**Personal protective equipment.** Welding helmet and gloves; safety glasses; hearing protection for grinding; nitrile gloves and an organic vapour respirator for resin work; cut-resistant gloves for sheet metal; boots with grip near water.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 102 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/GVS-DWG-101` to `GVS-DWG-120`.
- General arrangement: `cad/drawings/GVS-DWG-001.pdf`, Rev P3.
- Calculations: `docs/04-calcs/01-sizing.md` (GVS-CAL-001 v0.4) and `docs/04-calcs/sizing.py`; mass and loads in section 11, spindle in section 10, cost in section 12.
- Bill of materials: `bom/bom.csv` and `bom/bom-notes.md`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (GVS-DDR-003), with GVS-DDR-001 and GVS-DDR-002; open decisions in `docs/06-design-decisions.md` (GVS-DEC-001).
- Requirements: `docs/03-requirements.md` (GVS-REQ-001 v0.6).
