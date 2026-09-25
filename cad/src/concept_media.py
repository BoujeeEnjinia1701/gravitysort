"""GravitySort concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the machine (pedal station at -X, shaking table at +X), Y front (-Y, operator
side for the table) to back (+Y), Z up from the ground. Units mm.

Layout: a welded steel base frame carries the centrifugal concentrator (bowl on a vertical
spindle inside a splash tub), a feed hopper with a 2 mm screen above it, a water header tank
on a post, and the drive (pedal crank or a MotionCore motor, through one jackshaft and belt).
The small shaking table stands on its own legs at the +X end and takes its stroke from an
eccentric head driven by the same jackshaft (time-shared: bowl by day, table at clean-up).
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Cone, Pos, Rot
from concept import Part, render_all


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def cyl(x, y, z0, z1, r):
    """Vertical cylinder from z0 to z1."""
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


# Key dimensions (mm)
FX0, FX1, FY = -450.0, 450.0, 300.0      # base frame footprint: X -450..450, Y -300..300
RAIL_Z = 700.0                          # top of frame rails
S = 30.0                                # square tube size
CX, CY = 100.0, 0.0                     # centrifuge axis
BOWL_R_TOP, BOWL_R_BOT = 110.0, 65.0    # bowl inner radius at the lip and at the base (220 mm lip)
BOWL_Z0, BOWL_Z1 = 560.0, 740.0         # bowl base and lip
TUB_R, TUB_Z0, TUB_Z1 = 215.0, 470.0, 790.0
JX = -250.0                             # jackshaft X
DRIVE_Z = 330.0                         # jackshaft height
TAN3 = math.tan(math.radians(3.0))

# 1 Base frame: four legs, top rails, low stretchers and cross members
frame = None
for x in (FX0, FX1 - S):
    for y in (-FY, FY - S):
        leg = box(x, x + S, y, y + S, 0, RAIL_Z)
        frame = leg if frame is None else frame + leg
frame = frame + box(FX0, FX1, -FY, -FY + S, RAIL_Z - S, RAIL_Z) + box(FX0, FX1, FY - S, FY, RAIL_Z - S, RAIL_Z)
frame = frame + box(FX0, FX0 + S, -FY, FY, RAIL_Z - S, RAIL_Z) + box(FX1 - S, FX1, -FY, FY, RAIL_Z - S, RAIL_Z)
frame = frame + box(FX0, FX1, -FY, -FY + S, 90, 120) + box(FX0, FX1, FY - S, FY, 90, 120)
for x in (CX - 165, CX + 135):                                          # tub cross members
    frame = frame + box(x, x + S, -FY, FY, 440, 470)
frame = frame + box(CX - 15, CX + 15, -FY, FY, 250, 280)              # lower spindle bearing member
frame = frame + box(JX - 15, JX + 15, -FY, FY, 250, 280)              # jackshaft and gearbox member
frame = frame + box(-115, -85, -FY, FY, 235, 265)                     # motor member
frame = frame + box(-345, -315, -FY, FY, RAIL_Z - S, RAIL_Z)          # tank post member

# 2 Feed hopper with 2 mm punched screen on top, and a feed pipe down to the bowl centre
hop_top, hop_bot = 1180.0, 960.0
hopper = (Pos(CX, CY, (hop_top + hop_bot) / 2) * Cone(70, 170, hop_top - hop_bot)) - \
         (Pos(CX, CY, (hop_top + hop_bot) / 2 + 3) * Cone(62, 162, hop_top - hop_bot))
hopper = hopper + cyl(CX, CY, 760, hop_bot, 22) - cyl(CX, CY, 750, hop_bot + 1, 16)
hopper = hopper + box(CX - 12, CX + 12, -FY, -FY + 24, RAIL_Z, 1000) + box(CX - 12, CX + 12, -FY, CY - 76, 976, 1000)
screen = cyl(CX, CY, hop_top, hop_top + 6, 180)

# 3 Centrifugal bowl with riffle rings (cast polyurethane liner on a spun or printed shell)
bowl_out = Pos(CX, CY, (BOWL_Z0 + BOWL_Z1) / 2) * Cone(BOWL_R_BOT + 8, BOWL_R_TOP + 8, BOWL_Z1 - BOWL_Z0)
bowl_in = Pos(CX, CY, (BOWL_Z0 + BOWL_Z1) / 2 + 8) * Cone(BOWL_R_BOT, BOWL_R_TOP, BOWL_Z1 - BOWL_Z0)
bowl = bowl_out - bowl_in
for i in range(4):                                                       # four riffle rings
    z = BOWL_Z0 + 50 + i * 38
    r = BOWL_R_BOT + (BOWL_R_TOP - BOWL_R_BOT) * (z - BOWL_Z0) / (BOWL_Z1 - BOWL_Z0)
    bowl = bowl + (cyl(CX, CY, z, z + 6, r + 2) - cyl(CX, CY, z - 1, z + 7, r - 12))

# 4 Fluidization water jacket around the bowl (rotates with it) and rotary union at the spindle foot
jz0, jz1 = BOWL_Z0 - 20, BOWL_Z1 - 30
jacket = (Pos(CX, CY, (jz0 + jz1) / 2) * Cone(BOWL_R_BOT + 24, BOWL_R_TOP + 16, jz1 - jz0)) - \
         (Pos(CX, CY, (jz0 + jz1) / 2) * Cone(BOWL_R_BOT + 9, BOWL_R_TOP + 9, jz1 - jz0 + 1))
union = cyl(CX, CY, 120, 180, 28)

# 5 Spindle, bearing housings and driven pulley
spindle = cyl(CX, CY, 180, jz0, 14) + cyl(CX, CY, 280, 320, 45) + cyl(CX, CY, 430, 470, 45)
spindle = spindle + cyl(CX, CY, 190, 230, 50)

# 6 Splash tub with tailings outlet and launder toward the back (+Y)
tub = (cyl(CX, CY, TUB_Z0, TUB_Z1, TUB_R) - cyl(CX, CY, TUB_Z0 + 8, TUB_Z1 + 1, TUB_R - 6)) - cyl(CX, CY, TUB_Z0 - 1, TUB_Z0 + 9, 50)
tub = tub + box(CX - 40, CX + 40, TUB_R - 20, FY + 120, TUB_Z0 - 10, TUB_Z0 + 40) - \
      box(CX - 34, CX + 34, TUB_R - 10, FY + 121, TUB_Z0 - 4, TUB_Z0 + 41)

# 7 Lid guard over the bowl (feed hole), clamps to the tub
lid = cyl(CX, CY, TUB_Z1, TUB_Z1 + 10, TUB_R + 8) - cyl(CX, CY, TUB_Z1 - 1, TUB_Z1 + 11, 30)

# 8 Pedal station: seat, crank and chainring on an outrigger from the frame
PX = -800.0
pedal = box(PX - 20, FX0, -20, 20, 250, 280) + box(PX - 180, FX0, -20, 20, 90, 120)       # outrigger rails
pedal = pedal + box(PX - 180, PX - 150, -20, 20, 0, 780) + box(PX - 260, PX - 80, -90, 90, 780, 830)  # seat
pedal = pedal + box(PX - 20, PX + 20, -20, 20, 0, 350) + box(PX - 200, PX + 20, -150, 150, 0, 20)  # crank post, foot
pedal = pedal + Pos(PX, 60, DRIVE_Z) * Rot(90, 0, 0) * Cylinder(100, 6)                   # chainring
pedal = pedal + box(PX - 10, PX + 10, 76, 88, DRIVE_Z - 170, DRIVE_Z) + box(PX - 50, PX + 50, 88, 138, DRIVE_Z - 178, DRIVE_Z - 164)
pedal = pedal + box(PX - 10, PX + 10, -88, -76, DRIVE_Z, DRIVE_Z + 170) + box(PX - 50, PX + 50, -138, -88, DRIVE_Z + 164, DRIVE_Z + 178)

# 9 Jackshaft with freewheel sprocket and chain, right-angle gearbox, horizontal drive pulley,
#   motor chain, and the table take-off pulley at the -Y end
jack = Pos(JX, 5, DRIVE_Z) * Rot(90, 0, 0) * Cylinder(12, 550)
jack = jack + Pos(JX, 60, DRIVE_Z) * Rot(90, 0, 0) * Cylinder(35, 8)                      # freewheel sprocket
jack = jack + box(PX, JX, 56, 64, DRIVE_Z + 94, DRIVE_Z + 102) + box(PX, JX, 56, 64, DRIVE_Z - 38, DRIVE_Z - 30)  # chain
jack = jack + box(JX - 50, JX + 50, -40, 40, 280, 380)                                     # bevel gearbox
jack = jack + cyl(JX, 0, 190, 280, 12) + cyl(JX, 0, 190, 230, 150)                         # output shaft, drive pulley
jack = jack + Pos(JX, 220, DRIVE_Z) * Rot(90, 0, 0) * Cylinder(35, 8)                     # motor sprocket
jack = jack + box(JX, -100, 216, 224, DRIVE_Z + 30, DRIVE_Z + 38) + box(JX, -100, 216, 224, DRIVE_Z - 38, DRIVE_Z - 30)
jack = jack + Pos(JX, -250, DRIVE_Z) * Rot(90, 0, 0) * Cylinder(70, 20)                   # table take-off pulley

# 10 Drive belts: bowl belt (horizontal) and table belt (inclined, slack when disengaged)
belt = box(JX, CX, 138, 152, 200, 220) + box(JX, CX, -152, -138, 200, 220)
HX, HZ = 560.0, 710.0
dx, dz = HX - JX, HZ - DRIVE_Z
ang = math.degrees(math.atan2(dz, dx))
belt = belt + Pos((JX + HX) / 2, -250, (DRIVE_Z + HZ) / 2 + 70) * Rot(0, -ang, 0) * Box(math.hypot(dx, dz), 20, 8)

# 11 Guards over the bowl belt, the chain and the table belt take-off
guard = box(JX - 165, CX + 70, -170, 170, 175, 245) - box(JX - 159, CX + 64, -164, 164, 181, 239)
guard = guard + (box(PX - 115, JX + 45, 40, 80, 215, 445) - box(PX - 109, JX + 39, 44, 76, 221, 439))

# 12 MotionCore module and 250 W motor (bolts to the frame, chains to the jackshaft)
motor = Pos(-100, 220, DRIVE_Z) * Rot(90, 0, 0) * Cylinder(65, 60)
motor = motor + box(-130, -70, 190, 250, 265, 275)
mcore = box(-420, -170, 120, 290, 604, RAIL_Z - S)

# 13 Water header tank on a post with valve, flow meter and hose to the rotary union
TX, TY = -330.0, 180.0
tank = cyl(TX, TY, 1250, 1650, 190) + box(TX - 15, TX + 15, TY - 15, TY + 15, RAIL_Z, 1250)
water = box(TX - 10, TX + 10, TY - 200, TY - 180, 140, 1250) + box(TX - 25, TX + 25, TY - 215, TY - 165, 1050, 1150)
water = water + box(TX, CX - 20, -20, 0, 140, 160) + box(TX - 10, TX + 10, -20, TY - 180, 140, 160)

# 14 Shaking table deck with riffles, tilted 3 degrees toward the front (-Y)
TBX0, TBX1 = 620.0, 1620.0
TBW = 450.0
TB_Z = 820.0
deck = box(TBX0, TBX1, -TBW / 2, TBW / 2, TB_Z - 18, TB_Z)
for i in range(9):
    y = -TBW / 2 + 60 + i * 38
    deck = deck + box(TBX0 + 60 + i * 30, TBX1 - 40, y, y + 6, TB_Z, TB_Z + 8)
deck = deck + box(TBX0, TBX0 + 180, TBW / 2 - 90, TBW / 2, TB_Z, TB_Z + 70)                # feed box
deck = Pos(0, 0, TB_Z) * Rot(3, 0, 0) * Pos(0, 0, -TB_Z) * deck

# 15 Table stand (flexure legs) and head motion box with eccentric, pulley and pitman
tstand = None
for x in (TBX0 + 60, TBX1 - 80):
    for y in (-TBW / 2 + 20, TBW / 2 - 50):
        top = TB_Z - 18 + (y + 15) * TAN3
        l = box(x, x + 30, y, y + 30, 0, top)
        tstand = l if tstand is None else tstand + l
tstand = tstand + box(TBX0 + 60, TBX1 - 50, -TBW / 2 + 20, -TBW / 2 + 50, 150, 180) + box(TBX0 + 60, TBX1 - 50, TBW / 2 - 50, TBW / 2 - 20, 150, 180)
head = box(FX1 + 20, TBX0 + 40, -90, 90, 640, 780) + box(TBX0 - 10, TBX0 + 60, -15, 15, 760, 800)
head = head + box(FX1 + 60, FX1 + 90, -80, 80, 0, 640) + box(FX1 + 30, FX1 + 120, -120, 120, 0, 20)
head = head + Pos(HX, -170, HZ) * Rot(90, 0, 0) * Cylinder(12, 160) + Pos(HX, -250, HZ) * Rot(90, 0, 0) * Cylinder(70, 20)

# 16 Concentrate launder and lockable concentrate tray at the table's front edge
tray = box(TBX0 + 150, TBX1 + 40, -TBW / 2 - 130, -TBW / 2 - 30, 600, 660) - \
       box(TBX0 + 156, TBX1 + 34, -TBW / 2 - 124, -TBW / 2 - 36, 606, 661)
tray = tray + box(TBX0 + 160, TBX0 + 190, -TBW / 2 - 100, -TBW / 2 - 60, 0, 600) + box(TBX1, TBX1 + 30, -TBW / 2 - 100, -TBW / 2 - 60, 0, 600)

parts = [
    Part("Base frame, welded steel tube", frame, "#4B5563", 1, (0, 0, -250)),
    Part("Feed hopper, 2 mm screen, feed pipe", hopper, "#D97706", 2, (0, 0, 520)),
    Part("Screen", screen, "#92400E", None, (0, 0, 620)),
    Part("Centrifugal bowl with riffle rings", bowl, "#0F766E", 3, (0, 0, 360)),
    Part("Fluidization jacket and rotary union", jacket, "#5EEAD4", 4, (0, 0, 250)),
    Part("Rotary union", union, "#5EEAD4", None, (0, 0, -300)),
    Part("Spindle, bearings and pulley", spindle, "#9CA3AF", 5, (0, 0, -150)),
    Part("Splash tub and tailings outlet", tub, "#60A5FA", 6, (0, -150, 50)),
    Part("Bowl lid guard", lid, "#1F2937", 7, (0, 0, 440)),
    Part("Pedal station (seat, crank, chainring)", pedal, "#374151", 8, (-250, 0, -550)),
    Part("Jackshaft, gearbox, chains, pulleys", jack, "#78716C", 9, (-100, -150, -300)),
    Part("Drive belts (bowl and table)", belt, "#111827", 10, (0, -250, -450)),
    Part("Belt and chain guards", guard, "#FACC15", 11, (0, -450, -420)),
    Part("MotionCore module and 250 W motor", mcore, "#15803D", 12, (150, -230, 260)),
    Part("Motor", motor, "#166534", None, (0, 350, -250)),
    Part("Water header tank, valve, flow meter", tank, "#38BDF8", 13, (0, 250, 380)),
    Part("Water line", water, "#0EA5E9", None, (0, 250, 380)),
    Part("Shaking table deck with riffles", deck, "#E5E7EB", 14, (300, 0, 330)),
    Part("Table stand and head motion", tstand, "#6B7280", 15, (300, 0, 0)),
    Part("Head motion", head, "#6B7280", None, (150, 0, 0)),
    Part("Concentrate launder and lockable tray", tray, "#B45309", 16, (300, -300, 0)),
]

render_all(
    parts, project="GravitySort", title="Gravity concentrator concept", dwg_no="GVS-DWG-010",
    key_figures=["Bowl 220 mm lip; 60 G at 730 rpm (40 to 80 G)",
                 "Feed about 200 kg/h ore below 2 mm (estimate)",
                 "Water about 1.2 m3/h, recirculated (estimate)",
                 "About 45 W input: pedal or 250 W motor (est.)",
                 "Table 1000 x 450 mm cleans bowl concentrate",
                 "No mercury anywhere in the flowsheet",
                 "About 2.72 x 0.78 x 1.65 m, about 75 kg (est.)"],
    cut_exclude=("Water header tank, valve, flow meter", "Water line", "Belt and chain guards"),
    flow={"title": "gold balance for one 8 h day, 1.6 t of ore at 5 g/t (all values are estimates)", "unit": "g Au",
          "stages": [("Ore feed, milled", 8.0), ("Screened slurry", 7.6), ("Bowl concentrate", 5.4),
                     ("Table concentrate", 5.0), ("Smelted gold (borax)", 4.8)],
          "losses": [(0, "Oversize to regrind", 0.4), (1, "Bowl tailings", 2.2),
                     (2, "Table tailings, re-run", 0.4), (3, "Slag, re-smelt", 0.2)]},
)
