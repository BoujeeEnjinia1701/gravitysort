---
doc_id: GVS-CAL-001
title: GravitySort sizing calculations
project: GravitySort
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (speed and G, throughput, water, settling, fluidization supply, power, mass balance, table drive, rotor safety and brake, mass, cost, gold balance)
---

# GravitySort sizing calculations

On paper, GravitySort meets six of its fourteen requirements, by calculation or design review. **Three are not met:** R9 (parts cost $465 against $350, and against the recommended $450), R11 (about 88 kg against 80 kg) and R12 as written (a pedal drive cannot cap the bowl at 900 rpm by gearing). R2 (throughput per shift), R5 (table ratio) and R6 (pedal power at 80 G) are at risk. R4 (recovery) and R14 (liner life) cannot be verified before testing. The bowl, jacket and spindle have large structural margins at 1,200 rpm, and a bicycle disc brake stops the bowl well inside 15 s. Two findings are new at TRL 3: the fluidization supply only works with a 3/4 in hose from the 1.25 m header post, and the machine needs a water pump that is not in the design.

Every number here is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry from `cad/src/model.py` and the costs from `bom/bom.csv`. All values are first-principles estimates for a paper design; nothing is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions.*

| Input | Value | Basis |
| --- | --- | --- |
| Feed | 200 kg/h dry solids below 2 mm, 30 % solids by mass; 8 h shift; flush every 2 h, 5 min per flush | GVS-REQ-001 R2 and R13 |
| Fluidization water | 12 L/min | Mid-range of 8 to 15 L/min (GVS-PRC-001) |
| Bowl geometry | Liner surface 220 mm lip, 130 mm base, 180 mm deep; four rings 6 mm thick, 12 mm deep, 38 mm pitch; 8 mm PU liner on a 4 mm GFRP shell; 12 mm jacket gap, 4 mm jacket wall | `cad/src/model.py` PARAMS |
| Drive | 48T chainring, 12T freewheel, 1:1 bevel box, 300 mm to 100 mm V-belt: 12:1 | `cad/src/model.py` PARAMS |
| Drivetrain efficiency | Chain 0.97, jackshaft bearings 0.99, bevel box 0.93, V-belt 0.94: 0.839 overall | Typical values for used parts |
| Spindle drag | 0.03 N m per contact-sealed bearing unit, 0.10 N m for the rotary union seal, 1 W windage and splash at 730 rpm | Assumed; no datasheet chosen |
| Motor option | MotionCore reference 250 W geared hub motor, no-load 250 rpm at full pack voltage, 85 % of that under load; motor and controller 70 % efficient at about 60 W | MTC-PRC-001; motor speed assumed |
| Bed and film | Bed 12 mm deep when full, 50 % solids of 4,000 kg/m3 (2,500 kg/m3 bulk); 60 % fill at flush, 2.5 kg/L wet; slurry film 5 mm | Assumed; heavy minerals such as magnetite and pyrite dominate the bed |
| Gold shape | Flaky gold settles at half the velocity of a sphere of the same sieve size | Assumed shape factor |
| Fluidization supply | Tank water level 1.45 m, union 0.15 m above ground; 4 m of 3/4 in hose, friction factor 0.03; union, rotameter and valve K = 6 on a 1/2 in bore; hole discharge coefficient 0.62 | Model layout; typical hydraulics |
| Rotor materials | PU 1,150 kg/m3, 20 MPa tensile; hand-laid GFRP 1,800 kg/m3, 80 MPa tensile; stainless spindle E = 193 GPa | Typical values |
| Brake | Bicycle mechanical disc, 160 mm rotor, pad radius 70 mm, friction 0.4, 150 N per pad with a light pull | Typical values |
| Gold balance | 5 g/t reference ore; oversize loss 5 %, bowl 71 %, table 93 %, smelting 96 % | GVS-PRC-001 Figure 2; assumptions, not calculations |
| Budget | `budget_usd` $350; recommended $450 (awaiting Amish) | `project.yaml`, GVS-DDR-001 |

## 2. Speed and G (R3)

The pedal drive gives 12:1, so a 61 rpm cadence turns the bowl at 730 rpm: **59.6 G at 100 mm radius**. The R3 range of 40 to 80 G at 100 mm needs 598 to 846 rpm, a cadence of 50 to 71 rpm; the comfortable 55 to 70 rpm band gives 660 to 840 rpm (49 to 79 G). At 730 rpm the four riffle rings run at 46, 52, 57 and 63 G (wall radii 77.5, 87.0, 96.5 and 106.0 mm), and the lip speed is 8.41 m/s.

R3 asks for the speed to be shown to the operator. A wired bicycle computer (BOM item 19) with its magnet on the spindle pulley and its wheel size set to 1,667 mm reads km/h equal to bowl rpm divided by 10, so 730 rpm reads 73.0. **R3 is met on paper.**

## 3. Throughput (R2)

At 200 kg/h the bowl is flushed every 2 h, so an 8 h shift has three mid-shift stops of 5 min and 7.75 h of feed time: **1.55 t per shift**, not 1.6 t. Meeting 1.6 t needs 206 kg/h, or an 8.25 h shift. The bowl's hydraulic capacity at 200 kg/h is supported by the settling check in section 5 but is not proven. **R2 is at risk** (GVS-DDR-001 item 13).

## 4. Water (R8)

Slurry at 30 % solids carries 0.467 m3/h of water, and fluidization adds 0.72 m3/h: **1.19 m3/h**, 9.2 m3 per shift, against 1.5 m3/h. The slurry is 0.542 m3/h at 1,230 kg/m3, and 0.351 L/s leaves over the lip. **R8 is met on paper.**

The 60 L header tank holds only 3.0 min at full flow. Water must be pumped from the settling pond continuously; lifting 1.19 m3/h by about 1.7 m takes 5.5 W of hydraulic power. The pump is not in the BOM and is not driven by the pedals, so a pedal-only site still needs a hand pump, a second rider or gravity supply from upstream (GVS-DDR-001 item 12).

## 5. Settling in the bowl (R4 plausibility)

This check shows only that the bowl is not too short for fine gold to reach the wall; whether the bed keeps it is the question that only testing answers. At 730 rpm and 100 mm the acceleration is 584 m/s2. The wetted wall is 186 mm long; with an assumed 5 mm film the mean film velocity is 0.091 m/s and the transit time about 2.0 s.

*Table 2. Settling velocity at 60 G (Schiller and Naumann drag) and the ratio of transit time to the time to cross the film.*

| Particle | Settling velocity | Time to cross 5 mm | Ratio |
| --- | --- | --- | --- |
| Gold, 20 µm flake | 88 mm/s | 57 ms | 36 |
| Gold, 38 µm flake | 213 mm/s | 23 ms | 87 |
| Gold, 38 µm sphere | 426 mm/s | 12 ms | 173 |
| Gold, 75 µm flake | 450 mm/s | 11 ms | 183 |
| Quartz, 38 µm | 61 mm/s | 82 ms | 25 |
| Quartz, 150 µm | 362 mm/s | 14 ms | 147 |

Every particle, quartz included, reaches the wall many times over. Separation therefore depends on the fluidized bed letting dense grains displace light ones in the rings, not on reaching the wall. The fluidization upflow of 2.7 mm/s through 0.074 m2 of groove is 4 % of the settling velocity of 38 µm quartz, so it loosens the bed without washing out fine particles. **R4 cannot be verified at TRL 3 and remains the main technical risk.**

## 6. Fluidization jacket and supply (R4, R8)

The jacket rotates with the bowl, so the water in it gains centrifugal pressure ρω²r²/2 on its way out from the rotary union at the axis. Against it, each ring's loaded bed and film push back with a pressure that also rises with ω². At 730 rpm with a full bed, the net pressure across a hole is 6.5, 9.0, 12.1 and 15.7 kPa at rings 1 to 4, falling to 5.6 to 11.8 kPa at 600 rpm. It stays positive, so water always flows into the bed, but the lowest ring gets 0.64 times the flow per hole of the top ring.

Delivering 12 L/min takes about **89 holes of 1.0 mm** (about 22 per ring); grading them toward the lower rings evens out the flow.

The supply works only with a 3/4 in hose. The header gives 12.8 kPa of static head; the 3/4 in hose loses 1.6 kPa and the union, rotameter and valve 7.5 kPa, leaving 3.7 kPa at the union. With a 1/2 in hose the hose loss is 11.8 kPa and the union would see a suction of 6.5 kPa, so the jacket would run partly empty. For a net 10 kPa at every ring at 600 rpm the union needs 8.1 kPa, a water level of 1.90 m (about a 1.7 m post) or a small pump (GVS-DDR-001 item 11).

## 7. Power (R6, R7)

The power to bring the slurry and fluidization water (0.385 kg/s) up to lip speed is m·v², an upper bound that counts the slip loss. The drag from the two bearing units and the union seal is added, then divided by the drivetrain efficiency of 0.839.

*Table 3. Power at the pedals.*

| Bowl speed | Slurry and water | Drag | At the pedals |
| --- | --- | --- | --- |
| 600 rpm (40 G) | 18.4 W | 10.6 W | 34.6 W |
| 730 rpm (60 G) | 27.2 W | 13.2 W | **48.2 W** |
| 850 rpm (80 G) | 36.9 W | 15.8 W | **62.8 W** |
| 1,200 rpm (100 rpm sprint) | 73.6 W | 24.5 W | 116.9 W |

At 60 G the rider supplies 48.2 W with a crank torque of 7.6 N m, inside the 60 W target. At 80 G the target is exceeded. The union seal drag is a guess and makes up most of the drag. **R6 is at risk** (met at 60 G, not at 80 G). The TRL 2 estimate of about 45 W is corrected to 48.2 W.

With the motor, the 250 W MotionCore reference drive has a margin of **5.2 times** at 60 G and 4.0 times at 80 G, so **R7 is met on paper**. At 70 % motor and controller efficiency a shift takes **0.55 kWh** from the pack (TRL 2: about 0.5 kWh). A motor chain step-up of 1.20:1 means the motor's 250 rpm no-load speed gives at most 900 rpm at the bowl, and about 765 rpm under load; the ratio must be set for each motor so that its no-load speed at full pack voltage stays within 900 rpm.

## 8. Mass balance (R5)

The four ring grooves hold 0.89 L. At 60 % fill and 2.5 kg/L each flush yields **1.33 kg**, a mass pull of **0.33 %** of the 400 kg fed in 2 h, against 0.5 %. Four flushes give 5.3 kg per shift. Reaching 100 g needs a table reduction of **53:1**; a single pass on a small table is unlikely to achieve that, but two passes at about 8:1 each (64:1) would give about 83 g. **R5 is at risk** until the table ratio is shown.

## 9. Shaking table drive

The table head turns at cadence x 4.48 (4:1 chain, 140 mm take-off to 125 mm head pulley): 246 to 314 strokes/min at 55 to 70 rpm. The 240 to 300 strokes/min range needs a cadence of 54 to 67 rpm. At 270 strokes/min and a 15 mm stroke the deck's peak speed is 0.21 m/s and the head takes about 13 W, about 15 W at the pedals, so table clean-up is light work.

## 10. Rotor safety: inertia, burst, spindle and brake (R12)

**Inertia and energy.** Integrating the liner, shell, jacket, jacket water, rings and a full bed along the cone gives a rotating group of 6.47 kg with I = 0.0535 kg m2, plus 0.0031 kg m2 reflected from the drive pulley: 0.0566 kg m2 in total. The stored energy is **165 J at 730 rpm**, 224 J at 850 rpm, 252 J at 900 rpm and 447 J at 1,200 rpm (TRL 2: about 150 J at 730 rpm).

**Burst.** The checks run at 1.2 x 900 = 1,080 rpm and at 1,200 rpm, the speed a rider sprinting at a 100 rpm cadence could reach.

*Table 4. Stresses at the lip region.*

| Item | 1,080 rpm | 1,200 rpm | Safety factor at 1,200 rpm |
| --- | --- | --- | --- |
| Jacket wall hoop (water 106 and 130 kPa) | 3.8 MPa | 4.7 MPa | 17 on 80 MPa GFRP |
| Bowl shell hoop, jacket empty (75 kPa at 1,200 rpm) | 2.1 MPa | 2.6 MPa | 30 |
| PU liner, unsupported hoop | 0.19 MPa | 0.24 MPa | Liner is pressed onto the shell |
| Ring lip bending under the bed | 0.32 MPa | 0.39 MPa | 51 on 20 MPa PU |

The margins are large because the bowl is small and slow. They do not cover poor lamination, voids or a liner that debonds, which is why the liner must be checked before every run. A quarter of the liner and shell (0.52 kg) leaving the lip at 15.3 m/s carries 61 J; whether the 6 mm HDPE tub and 10 mm lid contain it has not been checked.

**Spindle.** A 300 N belt pull at 90 mm below the lower bearing gives 18 MPa of bending in the 25 mm stainless spindle. With the bowl 180 mm above the upper bearing, the first critical speed is about 4,820 rpm, four times the sprint speed. A 50 g lump of uneven concentrate at 100 mm radius adds a 29 N rotating load at 730 rpm.

**Stopping.** With the drive stopped, the freewheel lets the bowl coast. From 850 rpm it takes about **20 s** to stop with fluidization water running (the water leaving the lip acts as a brake) and 32 s with the water off, both longer than the 15 s in R12. A bicycle mechanical disc brake on the spindle (BOM item 18) gives 8.4 N m with a light pull and stops the bowl in 0.6 s; only 0.18 N m is needed for a 15 s stop, so the operator should brake gradually. Each stop warms the rotor by 4.1 K. The brake lever has a parking latch, and a pin on the same cable locks one lid clamp, so the lid can be opened only with the brake applied. With the motor, a lid switch on a MotionCore brake input removes torque (MotionCore stop category 0 does not brake, so the mechanical brake is still needed).

**Speed limit.** The motor case is capped twice: by the 1.20:1 step-up (section 7) and by the MotionCore speed limit, with its sensor on the spindle. The pedal case is not capped by gearing, because 900 rpm needs a cadence of only 75 rpm. **R12 is not met as written.** GVS-DDR-001 item 9 proposes rewording it to rely on the structural margin above and the speed display.

## 11. Mass and size (R11)

*Table 5. Transport loads (estimates).*

| Load | Mass |
| --- | --- |
| 1. Base frame with spindle, bearings, brake and union (11.75 m of tube at 1.76 kg/m) | 25.8 kg |
| 2. Drive and pedal station | 19.5 kg |
| 3. Bowl, jacket, tub, lid and hopper | 11.5 kg |
| 4. Table deck | 7.2 kg |
| 5. Table stand, head motion and tray | 17.3 kg |
| 6. Water tank and hoses | 5.0 kg |
| Hardware | 2.0 kg |
| **Total** | **88.3 kg** |

Every load is under 30 kg, but the total is over 80 kg, so **R11 is not met** (TRL 2: about 75 kg). Framing in 25 x 25 x 1.5 mm tube (1.11 kg/m) would save 7.7 kg. The overall size from the model is 2.72 x 0.78 x 1.65 m.

## 12. Cost (R9)

The BOM totals **$465**, excluding the MotionCore kit and reference motor ($335 per MTC-CAL-001) and the battery. That is $115 (33 %) over the $350 in `project.yaml` and $15 (3.3 %) over the recommended $450, which is awaiting Amish. The TRL 2 total of $437 rose by the brake and lid interlock ($18) and the speed display ($10). **R9 is not met** against either figure. Cost-down options are listed in GVS-DDR-001 item 1.

## 13. Gold balance

On the 5 g/t reference ore, 8.0 g of gold enters per shift at 200 kg/h for 8 h; 7.6 g passes the screen, 5.4 g is held in the bowl, 5.0 g stays on the table and 4.8 g is smelted: **about 60 % overall**. Losses are 0.4 g to oversize, 2.2 g to bowl tailings, 0.4 g to table tailings (re-run) and 0.2 g to slag. The stage recoveries are assumptions, not results of this note, and they use the full 8 h of feed.

## 14. Results

*Table 6. Requirements against the calculations, not met items first.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R9 | Parts cost | $465 | $350 or less (recommended $450, awaiting Amish) | **Not met** (over both) |
| R11 | Transport mass | 88 kg in 6 loads, heaviest 26 kg | 80 kg or less; loads 30 kg or less | **Not met** |
| R12 | Guards, speed limit, stop time | Brake stop 0.6 s (coast 20 s); motor capped; pedal reaches 900 rpm at 75 rpm cadence | Guarded; 900 rpm or less; stop within 15 s | **Not met as written** (pedal speed not capped) |
| R2 | Ore per shift | 200 kg/h; 1.55 t with 3 flush stops | 200 kg/h, 1.6 t per 8 h | At risk (needs 206 kg/h) |
| R5 | Concentrate for smelting | Bowl pull 0.33 %; 5.3 kg/day needs 53:1 on the table | 0.5 % or less; 100 g or less | At risk (two table passes) |
| R6 | Pedal power | 48.2 W at 60 G; 62.8 W at 80 G | 60 W or less | At risk (met at 60 G, not at 80 G) |
| R4 | Fine-gold recovery | Settling ratio 36 or more for 20 µm flakes; overall 60 % assumed | 80 % and 50 % in the bowl; 60 % overall | Not verifiable at TRL 3 (at risk) |
| R14 | Liner life | No wear data for this PU on quartz | 500 h; replace in 30 min | Not verifiable at TRL 3 |
| R1 | No mercury | No amalgamation step | No mercury at any step | Met (design review) |
| R3 | Bowl G and speed display | 40 to 81 G over 600 to 850 rpm; display item 19 | 40 to 80 G, speed shown | Met (paper) |
| R7 | Motor margin | 5.2 times at 60 G (4.0 at 80 G) | 3 times or more | Met (paper) |
| R8 | Water use | 1.19 m3/h | 1.5 m3/h or less | Met (paper) |
| R10 | Local workshop build | Welding, drill press, printed mold; set-screw inserts and taper bush | No lathe | Met (design review); casting route unproven |
| R13 | Quick, secure clean-up | Toolless lid clamps; lockable container and tray | 5 min, no tools | Met (paper); time not verified |

## 15. Corrections to TRL 2 figures

- Pedal power 45 W to 48.2 W; motor energy 0.5 to 0.55 kWh per shift.
- Stored energy at 730 rpm 150 J to 165 J.
- Machine mass 75 kg to 88 kg (the TRL 2 figure is replaced by a load-by-load estimate).
- Parts cost $437 to $465 (brake and speed display added); MotionCore $325 to $335.
- Throughput per shift 1.6 t to 1.55 t once flush stops are counted.
- Table reduction "about 50:1" to 53:1 needed for 100 g.

> **Safety:** Every rotor figure here is a paper estimate. The large burst margins assume sound lamination and a bonded liner; a cracked or debonded liner must never be run. The bowl coasts for about 20 s after the drive stops, so the brake must be applied and parked before the lid is opened. Nobody should run the bowl above 900 rpm, even though a rider can reach it; the speed display is the only warning on the pedal drive.
