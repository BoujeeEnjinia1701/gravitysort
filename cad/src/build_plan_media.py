"""GravitySort prototype build plan pictures (GVS-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|layouts ...]
A sheet, joint or step can be drawn alone:  python cad/src/build_plan_media.py sheet 101  (or joint 3, step 7)
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/GVS-DWG-101 to 120        making sketches for the made and modified components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/frame-cuts.png      frame cut list and member positions (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, frame_members, _box, _cyl, _cyly, _fuse  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
C = build_components(P)
S = lambda *ks: _fuse([C[k].shape for k in ks])  # noqa: E731
BOLT = "#111827"


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def cp(key, name=None, explode=(0, 0, 0), color=None):
    c = C[key]
    return part(name or c.name, c.shape, color or c.color, explode)


def grp(name, keys, color, explode=(0, 0, 0)):
    return part(name, S(*keys), color, explode)


def win(shape, x0, x1, y0, y1, z0, z1):
    return shape & _box(x0, x1, y0, y1, z0, z1)


# ----------------------------------------------------------------- named groups, in build order
GROUPS = [
    ("Base frame with bearing plates and tank cradle", ("frame", "bearing_plates", "tank_cradle"), "#4B5563"),
    ("Pedal outrigger and seat", ("outrigger", "outrigger_plates", "seat"), "#374151"),
    ("Jackshaft, bearings, gearbox, pulleys", ("pillow_blocks", "gearbox", "jackshaft", "jack_wheels", "drive_pulley"), "#78716C"),
    ("Crankset and pedal chain", ("crankset", "pedal_chain"), "#1F2937"),
    ("Spindle, bearings, brake disc, pulley", ("spindle", "bearings", "brake_flange", "rotor", "driven_pulley"), "#9CA3AF"),
    ("Rotary union", ("union",), "#B45309"),
    ("Bowl belt", ("bowl_belt",), "#111827"),
    ("Belt guard and speed sensor", ("belt_guard", "sensor"), "#CA8A04"),
    ("Pedal chain case", ("chain_case",), "#EAB308"),
    ("Brake caliper and bracket", ("caliper", "caliper_bracket"), "#DC2626"),
    ("Splash tub, standpipe, tailings pipe", ("tub", "standpipe", "tail_pipe"), "#60A5FA"),
    ("Bowl: liner, shell, jacket, hub", ("liner", "shell", "jacket", "hub"), "#0F766E"),
    ("Lid guard and clamps", ("lid", "clamps"), "#1F2937"),
    ("Hopper support", ("hopper_post",), "#6B7280"),
    ("Hopper and screen", ("hopper", "screen"), "#D97706"),
    ("Header tank", ("tank",), "#38BDF8"),
    ("Valve, rotameter and hose", ("valve_meter", "hose"), "#0369A1"),
    ("Speed display and brake lever", ("display", "brake_lever"), "#7C3AED"),
    ("Table base", ("table_base",), "#6B7280"),
    ("Flexure legs and cleats", ("flex_legs", "cleats"), "#A16207"),
    ("Table deck and wash pipe", ("deck", "wash_pipe"), "#C9A27E"),
    ("Table head: plate, bearings, shaft", ("head", "head_bearings", "head_shaft"), "#57534E"),
    ("Pitman arm", ("pitman",), "#B45309"),
    ("Table belt, tensioner and guard", ("table_belt", "tensioner", "table_guard"), "#0F766E"),
    ("Tailings launder and concentrate box", ("launder", "conc_box"), "#92400E"),
    ("Motor option: cradle, motor, chain, module", ("motor_cradle", "motor", "motor_chain", "motor_guard", "mcore"), "#15803D"),
]


def overview():
    off = [(0, 0, 0), (-550, 0, 0), (-150, 0, -700), (-650, -350, 750), (250, 0, -800), (250, 0, -1100), (-150, 0, -1000),
           (-150, 0, -1300), (-550, -450, 0), (550, -200, -700), (0, 0, 700), (0, 0, 1050), (0, 0, 1400), (0, -450, 1100),
           (0, 0, 1750), (-350, 250, 250), (0, 900, -150), (-700, 0, 700), (1050, 0, -450), (1050, 0, -150), (1050, 0, 300),
           (550, 0, 150), (650, -350, 450), (700, -450, -1350), (1050, -700, -150), (0, 1300, 0)]
    parts = [grp(n, ks, col, off[i]) for i, (n, ks, col) in enumerate(GROUPS)]
    return bv.overview(parts, OUT / "overview.png", "GravitySort prototype: every component, pulled apart",
                       subtitle="Numbered in build order; 26 is the motor option. Seen from the front right and above",
                       elev=20, azim=-62, size=(12, 8.5), dpi=150, key=True)



# ----------------------------------------------------------------- making sketches
def flat(shape, origin, x_dir, z_dir):
    import build123d as b
    return b.Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_local_coords(shape)


def ctx(*keys, color=None):
    return [cp(k) for k in keys]


SHEETS = {}


def sheet(n):
    def deco(fn):
        SHEETS[n] = fn
        return fn
    return deco


def _sheet(key, neighbours, dwg, title, material, notes, view_shape=None, inset=(22, -60), shape=None, name=None):
    pt = Part(name or C[key].name, shape if shape is not None else C[key].shape, C[key].color if key in C else "#6B7280")
    return bv.component_sheet(pt, [cp(k) for k in neighbours], project="GravitySort", dwg_no=dwg, title=title,
                              material=material, notes=notes, date=DATE, view_shape=view_shape, inset_view=inset,
                              out_dir=str(DWG))


@sheet(101)
def s101():
    import build123d as b
    fr = S("frame", "bearing_plates", "tank_cradle")
    return _sheet("frame", ["outrigger", "tub", "gearbox", "pillow_blocks"], "GVS-DWG-101",
                  "GravitySort base frame: making sketch", "Mild steel square tube 25 x 25 x 1.5 mm; plate 5 and 6 mm",
                  ["Cut list (frame cut picture in the plan gives every position):",
                   "  4 legs 700; 4 side rails 850 (top pair and lower pair, 255 up);",
                   "  2 top end rails, low end member (90 up), head member (600 up), 550;",
                   "  6 members 600 laid across: gearbox pair, spindle pair on top of",
                   "  the lower rails, tub pair hung on 4 drop posts 205 at 445 up;",
                   "  tank post member 550, end post 560, tank post 545. 14.5 m in all.",
                   "Tack on a flat floor, check diagonals within 2 mm, then weld.",
                   "Bearing plates 150 x 130 x 6, 40 mm centre hole, four 11 mm holes",
                   "  70 apart: one under the spindle pair, one under the tub pair,",
                   "  centres in line (plumb bob) before welding.",
                   "Tank cradle 250 x 250 x 5 on the tank post, two gussets each way.",
                   "Drill the bolt holes each later section lists; prime and paint.",
                   "Check: frame sits on all four feet; bearing plate holes in line."],
                  shape=fr, inset=(20, -55))


@sheet(102)
def s102():
    return _sheet("outrigger", ["frame", "crankset", "seat", "chain_case"], "GVS-DWG-102",
                  "GravitySort pedal outrigger: making sketch", "Square tube 25 x 25 x 1.5; round tube 32 x 2; plate 6 mm",
                  ["Spine 529 on the ground, toward the frame; cross feet 400 (seat end)",
                   "  and 300 (under the pedal post), welded under it.",
                   "Pedal post 393 tall on the spine, 185 from its far end; weld a",
                   "  bottom bracket shell cut from a scrap bicycle frame on top, its",
                   "  axis across the machine, centre 438 above the ground.",
                   "Seat tube: round 32 x 2 tube, 675 long, 172 behind the pedal post;",
                   "  slot its top 40 mm and fit a bicycle seat clamp.",
                   "Top arm 504 from the seat tube to the frame end, 600 to 625 up.",
                   "End plates 80 wide, 6 mm, welded across the spine end (125 tall)",
                   "  and the top arm end (65 tall); two 9 mm holes in each.",
                   "Fit: the lower plate bolts to the low end member, the upper plate",
                   "  to the end post; four M8 bolts. Outrigger 6 mm clear of the frame.",
                   "Check: bottom bracket axis square to the spine and level."],
                  shape=S("outrigger", "outrigger_plates"), inset=(18, -40))


@sheet(103)
def s103():
    import build123d as b
    return _sheet("spindle", ["bearings", "bearing_plates", "driven_pulley", "rotor", "hub", "union"], "GVS-DWG-103",
                  "GravitySort spindle: making sketch", "Stainless 316 tube 25 x 2 mm, 372 long; 1/2 in BSP nipple",
                  ["Cut 372 long, square both ends; deburr the bore.",
                   "Water runs up the bore from the rotary union to the jacket.",
                   "Bottom end: weld (TIG) a 1/2 in BSP stainless hex nipple into the",
                   "  bore so its thread stands below the tube for the union.",
                   "Positions from the bottom end: driven pulley 16 to 56; lower",
                   "  bearing 71 to 111; brake collar 173 to 196; upper bearing 236",
                   "  to 276; hub 341 to 368; top end flush with the jacket floor.",
                   "Drill a 6 mm cross hole for the hub pin 349 from the bottom end.",
                   "File a small flat for each bearing set screw.",
                   "Fit: two flanged bearing units under the plates, set screws on",
                   "  the flats; spindle turns freely by hand before the bowl goes on.",
                   "Check: straight within 0.2 mm over its length (roll it on glass)."],
                  view_shape=b.Pos(-P["bowl_x"], 0, -164) * C["spindle"].shape, inset=(15, -50))


@sheet(104)
def s104():
    import build123d as b
    return _sheet("shell", ["liner", "hub", "spindle"], "GVS-DWG-104",
                  "GravitySort bowl shell: making sketch", "Glass fibre and epoxy (GFRP), 4 mm, hand laid",
                  ["A cone cup: 148 across the base, 244 across the lip, 192 tall.",
                   "Print a plug the shape of the liner's outside (146 to 236 across,",
                   "  188 tall), sand it smooth and wax it.",
                   "Lay up 4 mm of glass mat and epoxy over the plug; cure, trim the",
                   "  lip square at 192 and pull the plug.",
                   "Floor: four 6 mm holes on a 60 mm circle, at 45 degrees to the",
                   "  machine axes, for the bowl bolts.",
                   "The shell is the outer mould for the liner (sketch 105).",
                   "After the liner is cast: drill about 89 holes of 1.0 mm through",
                   "  shell and liner into the four ring grooves, more in the lower",
                   "  grooves, so jacket water reaches every groove.",
                   "Check: wall 4 mm, plus or minus 0.5, all round (callipers at the lip)."],
                  view_shape=b.Pos(-P["bowl_x"], 0, 0) * C["shell"].shape, inset=(25, -55))


@sheet(105)
def s105():
    import build123d as b
    return _sheet("liner", ["shell", "jacket"], "GVS-DWG-105",
                  "GravitySort bowl liner: making sketch", "Cast polyurethane, Shore 80 to 90A, 8 mm",
                  ["Inside: 130 across the floor, 220 across the lip, 180 deep.",
                   "Four riffle rings, 6 thick, standing 12 in from the wall, the first",
                   "  50 above the floor, then every 38.",
                   "Core: print the inside shape (with the ring grooves) in six",
                   "  segments round a central key, so it comes out past the rings:",
                   "  pull the key, then lift the segments inward one by one.",
                   "Set four M6 stainless nuts on the shell floor over its holes,",
                   "  bolts through from below to hold them, release-coated threads.",
                   "Centre the core in the shell on its lip spigot; pour the",
                   "  polyurethane slowly from one side; cure as the maker says.",
                   "The liner bonds to the shell; it is replaced with the shell.",
                   "Check: no voids at the ring lips; floor 8 mm thick over the nuts."],
                  view_shape=b.Pos(-P["bowl_x"], 0, 0) * C["liner"].shape, inset=(25, -55))


@sheet(106)
def s106():
    import build123d as b
    return _sheet("jacket", ["shell", "hub", "spindle"], "GVS-DWG-106",
                  "GravitySort fluidization jacket: making sketch", "GFRP 4 mm, hand laid; closing ring 4 mm GFRP sheet",
                  ["A cone cup round the shell with a 12 mm water gap: inside 172",
                   "  across the floor, 253 at the top, 178 tall; outside 180 to 261.",
                   "Print a plug 12 mm bigger all round than the shell; lay up 4 mm.",
                   "Floor: 25.5 mm centre hole for the spindle; four 6 mm holes on",
                   "  a 60 mm circle, lined up with the shell's.",
                   "Closing ring: 4 mm GFRP annulus, 253 outside, 229 inside.",
                   "Fit: four 12 mm spacer bushes stand on the jacket floor over its",
                   "  holes; lower the bowl in, bolt through from below (M6), then",
                   "  bond the closing ring between the shell and the jacket top",
                   "  with epoxy. Seal the spindle hole with an O-ring.",
                   "Check: fill through the spindle at 10 kPa; no leak at the ring;",
                   "  water comes out of every groove hole."],
                  view_shape=b.Pos(-P["bowl_x"], 0, 0) * C["jacket"].shape, inset=(25, -55))


@sheet(107)
def s107():
    import build123d as b
    return _sheet("tub", ["frame", "standpipe", "tail_pipe", "lid"], "GVS-DWG-107",
                  "GravitySort splash tub: making sketch", "HDPE drum, 430 mm across, 6 mm wall (used food-grade drum)",
                  ["Cut the drum 320 above its own floor; the drum floor is the tub",
                   "  floor. File the rim smooth and level.",
                   "Floor: 76 mm centre hole for the standpipe grommet; four 9 mm",
                   "  holes 62.5 each side of centre along the machine and 150 each",
                   "  side across it, onto the two tub members.",
                   "Back wall: 98 mm hole, centre 64 above the floor, on the line",
                   "  through the tub centre toward the back, for the tailings pipe.",
                   "Lid clamps: drill their bases 45 degrees each side of the front.",
                   "Fit: standpipe (63 mm pipe, 50 long) through its grommet, sitting",
                   "  on the upper bearing plate; tailings pipe through its grommet.",
                   "Check: fill 50 mm deep with water; no leaks at either grommet."],
                  view_shape=b.Pos(-P["bowl_x"], 0, 0) * C["tub"].shape, inset=(22, -55))


@sheet(108)
def s108():
    import build123d as b
    return _sheet("lid", ["tub", "clamps", "hopper"], "GVS-DWG-108",
                  "GravitySort lid guard: making sketch", "HDPE sheet 10 mm",
                  ["A disc 446 across, 10 thick, with a 60 mm feed hole in the centre.",
                   "Cut with a jigsaw to a scribed circle; file the edge smooth.",
                   "The lid rests on the tub rim; it overhangs 8 mm all round.",
                   "Two over-centre clamps on the tub, 45 degrees each side of the",
                   "  front, hook over the lid edge; no tools to open or close.",
                   "The right-hand clamp's lever carries the interlock pin on the",
                   "  brake cable: it cannot open unless the brake is set.",
                   "The feed pipe stops 15 mm above the lid: the lid lifts straight",
                   "  up and off without moving the hopper.",
                   "Check: with the clamps shut the lid cannot be lifted by hand."],
                  view_shape=b.Pos(-P["bowl_x"], 0, 0) * C["lid"].shape, inset=(28, -60))


@sheet(109)
def s109():
    import build123d as b
    return _sheet("hopper", ["hopper_post", "screen", "lid"], "GVS-DWG-109",
                  "GravitySort feed hopper: making sketch", "Galvanized sheet 1.2 mm; steel tube 44 x 6; stainless screen",
                  ["Cone 140 across the bottom, 340 across the top, 220 tall.",
                   "Flat pattern: a ring sector, inner radius 169, outer radius 411,",
                   "  149 degrees, plus a 15 mm seam lap. Roll, rivet the seam, seal.",
                   "Bottom: a 140 mm disc with a 32 mm hole, riveted and sealed.",
                   "Feed pipe 44 x 6, 145 long, welded or bonded under the hole.",
                   "Screen: 2 mm punched stainless sheet in a 360 mm flat bar rim,",
                   "  resting on the hopper rim (lifts off for cleaning).",
                   "Fit: the cone drops into the support ring and wedges there.",
                   "The pipe end is 15 above the lid and over the bowl centre.",
                   "Check: water poured in runs out of the pipe with none at the seam."],
                  view_shape=b.Pos(-P["bowl_x"], 0, 0) * C["hopper"].shape, inset=(22, -55))


@sheet(110)
def s110():
    return _sheet("hopper_post", ["frame", "hopper", "lid"], "GVS-DWG-110",
                  "GravitySort hopper support: making sketch", "Square tube 25 x 25 x 1.5; plate 6 mm",
                  ["Foot plate 75 x 25 x 6 with two 9 mm holes 50 apart.",
                   "Post 294 tall welded upright on the foot plate.",
                   "Arm 175 welded to the post top, pointing to the back.",
                   "Ring: 6 mm plate, 176 inside, 216 outside, welded flat on the",
                   "  arm end; its inside edge is the cone's size 40 above its bottom.",
                   "Fit: the foot bolts on the front top rail at the bowl centre line",
                   "  (two M8). The ring centre must sit over the spindle centre:",
                   "  check with a plumb line from the ring to the spindle top.",
                   "Lift off with two bolts for transport.",
                   "Check: ring level; hopper sits in it without rocking."],
                  inset=(22, -55))


@sheet(111)
def s111():
    return _sheet("belt_guard", ["frame", "drive_pulley", "driven_pulley", "bowl_belt", "bearings"], "GVS-DWG-111",
                  "GravitySort bowl belt guard: making sketch", "Perforated steel sheet 1.2 mm; flat bar 25 x 3",
                  ["A shallow box round both pulleys: 566 x 316 x 60 tall.",
                   "Fold a tray (bottom and sides) and a separate lid (top), so the",
                   "  belt can be fitted and checked with the tray off.",
                   "Top: 40 mm holes over the gearbox shaft and the spindle.",
                   "Bottom: 32 mm hole for the spindle foot; the union stays below.",
                   "Four hangers 25 x 3 flat bar, 50 tall, bolted to the top and to",
                   "  the undersides of a gearbox member and a spindle member.",
                   "Speed sensor: on a bracket under the top, beside the driven pulley.",
                   "Fit: 6 mm clear of both pulleys and the belt all round.",
                   "Check: no finger can reach a pulley through any opening.",
                   "Never run the machine with this guard off."],
                  inset=(-30, -60))


@sheet(112)
def s112():
    import build123d as b
    return _sheet("chain_case", ["outrigger", "crankset", "gearbox", "pillow_blocks"], "GVS-DWG-112",
                  "GravitySort pedal chain case: making sketch", "Steel sheet 1.2 mm",
                  ["Two side plates shaped round both sprockets, 12 mm outside the",
                   "  chain, joined by a 26 mm rim strip; 703 long, 253 tall.",
                   "Holes: 28 mm for the crank axle and for the jackshaft.",
                   "Where it crosses the left gearbox member the bottom is flat and",
                   "  rests on the member (one M6 bolt).",
                   "Tab 25 wide to the pedal post (one M6 bolt).",
                   "Make the outer plate removable for fitting the chain.",
                   "Fit: inner plate 4 mm off the gearbox; outer plate 2 mm inside",
                   "  the crank arm.",
                   "Check: turn the cranks a full turn; nothing rubs."],
                  view_shape=flat(C["chain_case"].shape, (0, 0, 0), (1, 0, 0), (0, 1, 0)), inset=(20, -125))


@sheet(113)
def s113():
    import build123d as b
    pt = S("caliper_bracket", "brake_flange")
    return _sheet("caliper_bracket", ["rotor", "caliper", "spindle", "bearings", "bearing_plates", "driven_pulley"], "GVS-DWG-113",
                  "GravitySort brake flange and caliper bracket: making sketch", "Steel plate 6 mm; 25 mm bore shaft collar",
                  ["Brake flange: 6 mm disc 56 across, six M5 holes on a 44 mm",
                   "  circle (the disc's own pattern), welded square on a 25 mm bore",
                   "  shaft collar, 40 across and 20 long. Face it true after welding.",
                   "Caliper bracket: 6 mm plate, an L: foot 41 x 60 on the right",
                   "  spindle member (two M6), upright 60 wide, 75 tall, 6 off the",
                   "  disc edge. Drill the caliper's mounting holes to suit the",
                   "  caliper bought (post mount or the older standard).",
                   "Fit: collar 173 to 196 up the spindle, disc on the flange; the",
                   "  disc runs in the caliper slot with 2 mm each side.",
                   "Check: disc runs true within 0.3 mm (dial or feeler at the pads)."],
                  shape=pt, view_shape=b.Pos(-P["bowl_x"], 0, -300) * pt, inset=(25, -40))


@sheet(114)
def s114():
    import build123d as b
    t = math.radians(P["table_tilt"])
    v = b.Pos(0, 0, P["table_z"]) * b.Rot(-P["table_tilt"], 0, 0) * b.Pos(0, 0, -P["table_z"]) * S("deck", "wash_pipe")
    return _sheet("deck", ["flex_legs", "pitman", "launder", "conc_box"], "GVS-DWG-114",
                  "GravitySort shaking table deck: making sketch", "Marine plywood 18 mm; HDPE 3 mm; PVC pipe 40 mm",
                  ["Deck 1000 x 450: plywood, faced with 3 mm HDPE glued and screwed.",
                   "Nine riffles, HDPE strip 6 wide, 8 tall, glued along the deck,",
                   "  60 in from the front edge, then every 38 to the back; each",
                   "  starts 30 later than the one in front (60, 90 ... 300 from the",
                   "  head end) and all stop 40 short of the far end.",
                   "Feed box 180 x 90 x 70 at the back of the head end.",
                   "Wash pipe: 40 mm PVC, 770 long, 3 mm holes every 25 toward the",
                   "  deck, along the back edge from 190 to 960; end cap; hose tail.",
                   "Pitman cheeks: two steel plates 40 x 22 x 6 under the head end,",
                   "  12 mm apart, 12 mm hole for the pitman pin.",
                   "Check: deck flat within 1 mm; riffles straight and well stuck."],
                  view_shape=v, inset=(30, -50), shape=S("deck", "wash_pipe"))


@sheet(115)
def s115():
    return _sheet("table_base", ["flex_legs", "cleats", "deck"], "GVS-DWG-115",
                  "GravitySort table base and flexure legs: making sketch", "Square tube 25 x 25 x 1.5; marine plywood 18 mm; angle 40 x 40 x 4",
                  ["Base: two rails 940 long, 270 apart (centres), and two cross",
                   "  tubes 245 between them at the ends, welded flat on the floor.",
                   "Legs: four strips of 18 mm marine plywood, 80 wide; the front",
                   "  two 772 long, the back two 786 long (the deck slopes 3 degrees",
                   "  to the front); cut the tops to that slope.",
                   "Legs stand on the rails 40 and 900 from the head end of the",
                   "  base, thin side toward the head, so they flex along the table.",
                   "Cleats: eight 80 mm pieces of 40 x 40 x 4 angle, two M8 bolts",
                   "  into the leg and two into the rail or the deck underside.",
                   "Tilt: packers under the top cleats set 2 to 4 degrees.",
                   "Check: push the deck along by hand; it swings freely 10 mm each",
                   "  way and springs back to centre."],
                  shape=S("table_base", "flex_legs", "cleats"), inset=(20, -50))


@sheet(116)
def s116():
    return _sheet("head", ["frame", "head_bearings", "head_shaft", "pitman"], "GVS-DWG-116",
                  "GravitySort table head plate and shelf: making sketch", "Steel plate 6 mm",
                  ["Head plate 375 x 110 x 6, standing on the frame's table end.",
                   "Shelf 184 deep, welded square to the plate 677 above the ground,",
                   "  with two triangular gussets 90 x 90 under it.",
                   "Shelf cut-out 130 x 280 between the bearings: the pitman eye",
                   "  swings through it.",
                   "Plate holes: two 9 mm into the head member, two into the top",
                   "  end rail (four M8 bolts).",
                   "Shelf holes: two pairs of 12 mm holes 95 apart for the head",
                   "  shaft bearings, 330 apart across the machine.",
                   "Head shaft 20 mm, 410 long; eccentric: 60 mm disc with its 20 mm",
                   "  bore 7.5 off centre (15 mm stroke), two set screws.",
                   "Check: shelf square to the plate; shaft turns freely by hand."],
                  inset=(22, -45))


@sheet(117)
def s117():
    import build123d as b
    return _sheet("pitman", ["head_shaft", "deck", "head", "head_bearings"], "GVS-DWG-117",
                  "GravitySort pitman arm: making sketch", "Steel flat bar 22 x 12; plate 12 mm; bronze bush",
                  ["Eye: a ring 84 across from 12 mm plate with a 61 mm bore and a",
                   "  60 mm bore bronze bush pressed in (it runs on the eccentric).",
                   "Arm: 22 x 12 flat bar welded to the eye; 111 mm between the",
                   "  eccentric centre and the pin centre.",
                   "Pin end: 12 mm hole; a 12 mm pin with washers and an R-clip",
                   "  joins it to the cheeks under the deck.",
                   "Fit: the arm rises at 46 degrees from the head to the deck;",
                   "  the eye swings 3 mm clear of the shelf cut-out.",
                   "Grease the bush; it must turn freely with no side play.",
                   "Check: the deck moves 15 mm per turn of the head shaft."],
                  view_shape=flat(C["pitman"].shape, (0, 0, 0), (1, 0, 0), (0, 1, 0)), inset=(4, -90))


@sheet(118)
def s118():
    return _sheet("conc_box", ["deck", "flex_legs", "table_base"], "GVS-DWG-118",
                  "GravitySort tailings launder and concentrate box: making sketch", "Galvanized sheet 1.2 mm; square tube 25 x 25 x 1.5",
                  ["Launder: a U channel 100 wide, 60 deep, 810 long, under the",
                   "  deck's front edge, with a 60 mm spout at the head end.",
                   "  Two legs 640 tall. Tailings run to a bucket under the spout.",
                   "Concentrate box: 120 x 290 x 120 tall, open top, under the far",
                   "  end of the deck (gold walks off the riffle ends into it).",
                   "  Hinged lid with a hasp for a padlock; four legs 640 tall.",
                   "Both stand on the ground 15 mm clear of the moving deck.",
                   "Check: box top 30 below the deck end at its lowest point;",
                   "  the lid locks with the deck in place."],
                  shape=S("conc_box", "launder"), inset=(22, -45))


@sheet(119)
def s119():
    import build123d as b
    return _sheet("tensioner", ["frame", "table_belt", "jack_wheels", "head_shaft"], "GVS-DWG-119",
                  "GravitySort table belt tensioner: making sketch", "Flat bar 25 x 6; 60 mm idler pulley; plate 6 mm",
                  ["The table belt is slack (no drive) until the tensioner is set:",
                   "  this is the clutch between bowl drive and table drive.",
                   "Arm: 25 x 6 flat bar, 150 between pivot and idler axle.",
                   "Handle: 20 x 6 flat bar, 135 long, welded to the arm at the pivot.",
                   "Idler: a 60 mm flat-faced pulley on a 12 mm stub axle.",
                   "Pivot: 12 mm bolt through a 6 mm bracket bolted on the front",
                   "  face of the front top rail, 430 from the pedal end (two M6).",
                   "Latch: a notched plate on the bracket holds the handle down",
                   "  (belt driving) or up (belt slack).",
                   "Check: handle down, the belt drives the head without slipping."],
                  view_shape=flat(C["tensioner"].shape, (0, 0, 0), (1, 0, 0), (0, 1, 0)), inset=(15, -35))


@sheet(120)
def s120():
    return _sheet("motor_cradle", ["frame", "motor_chain", "jack_wheels"], "GVS-DWG-120",
                  "GravitySort motor cradle (motor option): making sketch", "Steel plate 6 mm",
                  ["Only for the motor option. Base plate 130 x 117 x 6 on top of the",
                   "  back lower rail, two M8 bolts through the rail.",
                   "Two dropouts 60 wide, 6 thick, 110 tall, welded upright on the",
                   "  base, 76 apart inside: they take the hub motor's axle.",
                   "Axle slots 12 mm wide, centre 96 above the base, open upward",
                   "  so the motor drops in; torque washers stop it turning.",
                   "Chain guard: sheet cover outside the motor chain on two spacers",
                   "  from the outer dropout, with a rim round the jackshaft sprocket.",
                   "Check: hub motor 10 mm clear of the base and 17 clear of the frame;",
                   "  its sprocket in line with the jackshaft sprocket (straight edge)."],
                  inset=(30, 60))


def sheets(only=None):
    out = []
    for n, fn in SHEETS.items():
        if only is None or n == only:
            out.append(fn())
    return out


# ----------------------------------------------------------------- joints
JOINTS = {}


def joint_(n):
    def deco(fn):
        JOINTS[n] = fn
        return fn
    return deco


def J(n, parts, title, sub, **kw):
    return bv.joint([p for p in parts], OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw)


@joint_(1)
def j1():
    bx = (20, 180, 0, 80, 110, 475)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(1, [part("Spindle members and tub members", w("frame"), "#4B5563"),
                 part("Bearing plates", w("bearing_plates"), "#9CA3AF"),
                 part("Flanged bearing units", w("bearings"), "#57534E"),
                 part("Spindle (water up the bore)", w("spindle"), "#A8A29E"),
                 part("Brake flange and disc", win(S("brake_flange", "rotor"), *bx), "#DC2626"),
                 part("Driven pulley", w("driven_pulley"), "#78716C"),
                 part("Rotary union", w("union"), "#B45309")],
             "the spindle in its bearings (cut through the axis)",
             "Seen from the front. Each bearing bolts under its plate; the plates are welded under the members",
             elev=8, azim=-90, size=(8, 7))


@joint_(2)
def j2():
    bx = (-45, 245, 0, 140, 440, 760)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(2, [part("Liner (cast PU)", w("liner"), "#D97706"), part("Shell (GFRP)", w("shell"), "#0F766E"),
                 part("Jacket (12 mm water gap)", w("jacket"), "#5EEAD4"), part("Flange hub, pinned to the spindle", w("hub"), "#57534E"),
                 part("M6 bolts, spacers, cast-in nuts", w("bowl_bolts"), BOLT), part("Spindle top", w("spindle"), "#A8A29E"),
                 part("Standpipe", w("standpipe"), "#1D4ED8"), part("Tub floor", w("tub"), "#60A5FA")],
             "bowl, jacket and hub (cut through the axis)",
             "Seen from the front. Water leaves the spindle top into the gap and passes through the shell into the rings",
             elev=8, azim=-90, size=(8, 6.5))


@joint_(3)
def j3():
    bx = (0, 200, 0, 160, 430, 510)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(3, [part("Tub floor", w("tub"), "#60A5FA"), part("Standpipe and grommet", w("standpipe"), "#1D4ED8"),
                 part("Tub members", w("frame"), "#4B5563"), part("Upper bearing plate", w("bearing_plates"), "#9CA3AF"),
                 part("M8 tub bolts", w("tub_bolts"), BOLT), part("Spindle", w("spindle"), "#A8A29E"),
                 part("Upper bearing", w("bearings"), "#57534E")],
             "tub floor, standpipe and tub members (cut)",
             "The standpipe stands on the bearing plate through a rubber grommet; spilt slurry cannot reach the bearing",
             elev=14, azim=-80, size=(8, 6))


@joint_(4)
def j4():
    bx = (-345, -150, -260, 110, 255, 400)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(4, [part("Gearbox members on the lower rail", w("frame"), "#4B5563"),
                 part("Pillow blocks", w("pillow_blocks"), "#57534E"), part("Right-angle gearbox", w("gearbox"), "#78716C"),
                 part("Jackshaft", w("jackshaft"), "#A8A29E"), part("Freewheel (chain case left off)", w("jack_wheels"), "#B45309")],
             "jackshaft and gearbox on the gearbox members",
             "Seen from the front right. Both bearings and the gearbox bolt straight onto the two members",
             elev=30, azim=-55, size=(8, 6))


@joint_(5)
def j5():
    bx = (-520, -400, -90, 90, 0, 700)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(5, [part("Frame: low end member and end post", w("frame"), "#4B5563"),
                 part("Outrigger end plates (2 M8 each)", w("outrigger_plates"), "#9CA3AF"),
                 part("Outrigger spine and top arm", w("outrigger"), "#0F766E")],
             "outrigger to the frame end",
             "Seen from the pedal side. Two bolted plates; the outrigger lifts off for transport",
             elev=20, azim=-150, size=(7, 6.5))


@joint_(6)
def j6():
    a = math.radians(-45)
    cx, cy = P["bowl_x"] + 225 * math.cos(a), 225 * math.sin(a)
    bx = (cx - 60, cx + 60, cy - 60, cy + 60, 730, 820)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(6, [part("Lid guard on the tub rim", win(S("tub", "lid"), *bx), "#60A5FA"),
                 part("Over-centre clamp; its hook holds the lid", w("clamps"), "#0F766E")],
             "lid clamp (front right)",
             "Seen side on. The clamp base bolts to the tub wall; its hook closes over the lid edge", elev=8, azim=45, size=(7, 5.5))


@joint_(7)
def j7():
    bx = (-20, 220, -310, 120, 940, 1060)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(7, [part("Hopper cone", w("hopper"), "#D97706"), part("Support ring, arm and post", w("hopper_post"), "#6B7280")],
             "hopper in its support ring",
             "The cone drops into the ring and wedges; it lifts out for cleaning", elev=25, azim=-55, size=(7, 5.5))


@joint_(8)
def j8():
    bx = (-470, -190, 40, 320, 660, 1330)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(8, [part("Tank post on its member", win(C["frame"].shape, -470, -190, 40, 320, 660, 1000), "#4B5563"), part("Cradle plate and gussets", w("tank_cradle"), "#9CA3AF"),
                 part("Header tank (lower part)", w("tank"), "#38BDF8"), part("Rotameter bracket on the back top rail", w("valve_meter"), "#0EA5E9")],
             "header tank on its cradle",
             "Gussets each way at both ends of the post; a ratchet strap holds the drum", elev=15, azim=-60, size=(7, 6.5))


@joint_(9)
def j9():
    x = P["flex_x"][0]
    bx = (x - 40, x + 70, 80, 190, 0, 830)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(9, [part("Flexure leg (18 mm plywood)", w("flex_legs"), "#A16207"), part("Steel angle cleats", w("cleats"), "#374151"),
                 part("Base rail", w("table_base"), "#6B7280"), part("Deck", w("deck"), "#D6D3D1")],
             "flexure leg, cleats, base and deck (back left leg)",
             "The thin side faces along the table, so the leg bends as the deck moves", elev=12, azim=-60, size=(6.5, 7))


@joint_(10)
def j10():
    bx = (440, 700, -60, 60, 580, 830)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(10, [part("Head plate and shelf", w("head"), "#6B7280"), part("Head shaft and eccentric", w("head_shaft"), "#57534E"),
                  part("Pitman arm", w("pitman"), "#B45309"), part("Deck with its cheeks", w("deck"), "#D6D3D1"),
                  part("Frame table end", w("frame"), "#4B5563")],
              "head, pitman and deck",
              "Seen from the front, cut at the centre line. The eccentric pushes and pulls the deck 15 mm", elev=6, azim=-90, size=(7.5, 6))


@joint_(11)
def j11():
    bx = (-100, 260, -360, -290, 520, 840)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(11, [part("Table belt (top run)", w("table_belt"), "#111827"), part("Tensioner arm, idler and handle", w("tensioner"), "#0F766E"),
                  part("Front top rail", w("frame"), "#4B5563")],
              "table belt tensioner",
              "Seen from the front, guard off. Handle down presses the idler on the belt and the table runs", elev=8, azim=-90, size=(7.5, 5.5))


@joint_(12)
def j12():
    bx = (-310, 0, 260, 420, 270, 470)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(12, [part("Back lower rail", win(C["frame"].shape, -170, 0, 260, 420, 270, 470), "#4B5563"), part("Motor cradle and dropouts", w("motor_cradle"), "#9CA3AF"),
                  part("Hub motor and sprocket", w("motor"), "#166534"), part("Motor chain", w("motor_chain"), "#111827"),
                  part("Jackshaft sprocket", w("jack_wheels"), "#57534E")],
              "motor cradle on the back rail (motor option)",
              "Seen from the back, guard off. The motor drops into open slots in the dropouts", elev=18, azim=60, size=(7.5, 6))


@joint_(13)
def j13():
    bx = (120, 210, -70, 70, 295, 395)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(13, [part("Brake disc", w("rotor"), "#DC2626"), part("Caliper", w("caliper"), "#F59E0B"),
                  part("Caliper bracket", w("caliper_bracket"), "#9CA3AF"), part("Right spindle member", w("frame"), "#4B5563")],
              "brake caliper on its bracket",
              "Seen from the spindle side. The bracket foot bolts on the spindle member; the disc runs in the caliper slot", elev=25, azim=-140, size=(7, 5.5))


@joint_(14)
def j14():
    bx = (20, 180, 150, 300, 470, 600)
    w = lambda k: win(C[k].shape, *bx)  # noqa: E731
    return J(14, [part("Tub wall", w("tub"), "#60A5FA"), part("Tailings pipe and rubber grommet", w("tail_pipe"), "#374151"),
                  part("Tub member and drop post", w("frame"), "#4B5563")],
              "tailings pipe through the tub wall (cut)",
              "A rubber pipe grommet seals the pipe in the curved wall; the pipe runs out to the settling pond", elev=20, azim=-130, size=(7, 5.5))


def joints(only=None):
    return [fn() for n, fn in JOINTS.items() if only is None or n == only]


# ----------------------------------------------------------------- assembly steps
def _mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def steps(only=None):
    out = []

    def st(n, done, new, title, sub, **kw):
        if only is None or n == only:
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    G = {n: grp(n, ks, col) for n, ks, col in GROUPS}
    names = [g[0] for g in GROUPS]
    fr = G[names[0]]
    st(1, [], [_mv(fr, (0, 0, 0))], "set the frame on level ground", "Packers under any foot that rocks; the bearing plates must be level",
       elev=22, azim=-60, label_done=False)
    st(2, [fr], [_mv(grp("Pedal outrigger and seat", ("outrigger", "outrigger_plates", "seat"), "#374151"), (-250, 0, 0))],
       "bolt the pedal outrigger to the frame end", "Four M8 bolts through the two end plates", elev=20, azim=-120, label_done=False)
    done = [fr, G[names[1]]]
    st(3, done, [_mv(cp("gearbox"), (0, 0, 180)), _mv(cp("pillow_blocks"), (0, 0, 180)),
                 _mv(grp("Jackshaft with freewheel, sprocket and take-off pulley", ("jackshaft", "jack_wheels"), "#A8A29E"), (0, -250, 0)),
                 _mv(cp("drive_pulley"), (0, 0, -200))],
       "gearbox, jackshaft and drive pulley", "Gearbox and both bearings bolt on the gearbox members; slide the shaft through",
       elev=22, azim=-60, label_done=False)
    done += [grp("Jackshaft group", ("pillow_blocks", "gearbox", "jackshaft", "jack_wheels", "drive_pulley"), "#78716C")]
    st(4, done, [_mv(cp("crankset"), (0, -200, 0)), _mv(cp("pedal_chain"), (0, -120, 120))],
       "crankset and pedal chain", "Crank axle into the bottom bracket; chain on the 48T ring and the freewheel",
       elev=18, azim=-120, label_done=False)
    done += [G[names[3]]]
    st(5, done, [_mv(cp("bearings"), (0, 0, 0)), _mv(grp("Spindle with brake flange and disc", ("spindle", "brake_flange", "rotor"), "#A8A29E"), (0, 0, 600)),
                 _mv(cp("driven_pulley"), (0, -220, 0))],
       "bearings, spindle, brake disc and driven pulley", "Bearings under their plates (M10); spindle down through both; pulley on its taper bush",
       elev=15, azim=-60, label_done=False)
    done += [G[names[4]]]
    st(6, done, [_mv(cp("union"), (0, 0, -200)), _mv(cp("bowl_belt"), (0, -250, 0))],
       "rotary union and bowl belt", "Union onto the nipple at the spindle foot, sealant on the thread; belt round both pulleys",
       elev=-12, azim=-60, label_done=False)
    done += [G[names[5]], G[names[6]]]
    st(7, done, [_mv(grp("Belt guard and speed sensor", ("belt_guard", "sensor"), "#CA8A04"), (0, 0, -250)),
                 _mv(cp("chain_case"), (0, -200, 0))],
       "belt guard and chain case", "Guard on its four hangers; chain case on the gearbox member and the pedal post",
       elev=-10, azim=-60, label_done=False)
    done += [G[names[7]], G[names[8]]]
    st(8, done, [_mv(cp("caliper_bracket"), (200, 0, 0)), _mv(cp("caliper"), (200, 0, 80)),
                 _mv(grp("Brake lever and speed display", ("brake_lever", "display"), "#7C3AED"), (-150, 0, 0))],
       "brake caliper, lever and speed display", "Bracket on the spindle member; caliper on the bracket; lever and display face the rider",
       elev=22, azim=-60, label_done=False)
    done += [G[names[9]], G[names[17]]]
    st(9, done, [_mv(cp("tub"), (0, 0, 400)), _mv(cp("standpipe"), (0, 0, 650)), _mv(cp("tail_pipe"), (0, 300, 0))],
       "splash tub, standpipe and tailings pipe", "Tub on the tub members (four M8); standpipe through its grommet; tailings pipe at the back",
       elev=24, azim=-60, label_done=False)
    done += [G[names[10]]]
    st(10, done, [_mv(grp("Bowl assembly (liner, shell, jacket, hub)", ("liner", "shell", "jacket", "hub", "bowl_bolts"), "#0F766E"), (0, 0, 450))],
       "bowl onto the spindle", "Hub over the spindle top, 6 mm pin through; check it spins true by hand",
       elev=24, azim=-60, label_done=False)
    done += [G[names[11]]]
    st(11, done, [_mv(cp("lid"), (0, 0, 300)), _mv(cp("clamps"), (0, -150, 0))],
       "lid guard and clamps", "Clamps on the tub wall; lid on the rim; the right clamp takes the interlock pin",
       elev=24, azim=-60, label_done=False)
    done += [G[names[12]]]
    st(12, done, [_mv(cp("hopper_post"), (0, -200, 0)), _mv(grp("Hopper and screen", ("hopper", "screen"), "#D97706"), (0, 0, 400))],
       "hopper support, hopper and screen", "Support foot on the front top rail (two M8); cone drops into its ring; screen on top",
       elev=22, azim=-60, label_done=False)
    done += [G[names[13]], G[names[14]]]
    st(13, done, [_mv(cp("tank"), (0, 0, 350)), _mv(grp("Valve, rotameter and hose", ("valve_meter", "hose"), "#0369A1"), (0, 300, 0))],
       "header tank, valve, rotameter and hose", "Drum on its cradle with a ratchet strap; hose down the back to the rotary union",
       elev=22, azim=-35, label_done=False)
    done += [G[names[15]], G[names[16]]]
    st(14, [], [_mv(cp("table_base"), (0, 0, 0)), _mv(grp("Flexure legs and cleats", ("flex_legs", "cleats"), "#A16207"), (0, 0, 250))],
       "table base and flexure legs", "Base flat on level ground in line with the frame; legs on the rails with their bottom cleats",
       elev=22, azim=-60, label_done=False)
    tb = [G[names[18]], G[names[19]]]
    st(15, tb, [_mv(grp("Deck and wash pipe", ("deck", "wash_pipe"), "#C9A27E"), (0, 0, 300))],
       "deck onto the legs", "Top cleats to the deck underside; packers set the 3 degree slope to the front",
       elev=22, azim=-60, label_done=False)
    tb += [G[names[20]]]
    st(16, [fr] + tb, [_mv(grp("Head plate, shelf, bearings and shaft", ("head", "head_bearings", "head_shaft"), "#57534E"), (0, -450, 0)),
                       _mv(cp("pitman"), (0, -300, 150))],
       "table head and pitman", "Head plate on the frame end (four M8); pitman from the eccentric to the deck cheeks, 12 mm pin",
       elev=22, azim=-60, label_done=False)
    done += [G[names[21]], G[names[22]]]
    st(17, [fr, G[names[2]]] + tb + [G[names[21]], G[names[22]]], [_mv(cp("table_belt"), (0, -150, 0)), _mv(cp("tensioner"), (0, -300, 250)), _mv(cp("table_guard"), (0, -800, -450))],
       "table belt, tensioner and guard", "Belt on the take-off and head pulleys; tensioner on the front top rail; guard over both",
       elev=15, azim=-70, label_done=False)
    done += [G[names[23]]]
    st(18, [fr] + tb + [G[names[21]], G[names[22]], G[names[23]]], [_mv(grp("Tailings launder and concentrate box", ("launder", "conc_box"), "#92400E"), (0, -350, 0))],
       "tailings launder and concentrate box", "Launder under the deck's front edge; box under its far end, 15 mm clear of the deck",
       elev=22, azim=-60, label_done=False)
    done += [G[names[24]]]
    st(19, [fr, G[names[2]]], [_mv(cp("motor_cradle"), (0, 200, 0)), _mv(cp("motor"), (0, 420, 200)),
                               _mv(grp("Motor chain and guard", ("motor_chain", "motor_guard"), "#CA8A04"), (0, 650, 0)),
                               _mv(cp("mcore"), (0, 0, 350))],
       "motor option", "Cradle on the back lower rail; motor into the dropouts; chain and guard; module under the top rails",
       elev=22, azim=50, label_done=False)
    return out



# ----------------------------------------------------------------- frame cut list and positions
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    INK, MUT, AC, TUBE, PL = "#111827", "#4B5563", "#0F766E", "#9CA3AF", "#D1D5DB"
    Sz = P["tube"]; x0 = P["frame_x0"]; FY = P["frame_y"]
    X = lambda x: x - x0          # noqa: E731  distance from the pedal end
    fig = plt.figure(figsize=(13, 9.2), dpi=150)
    fig.text(0.03, 0.975, "Base frame: where every tube goes", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.948, "Sizes in mm from the model. Along the machine: from the pedal end (left). Across: from the centre line. Up: from the ground.",
             fontsize=8.5, color=MUT, va="top")
    # plan at the lower rail level (the members that lie on the lower rails, and the tub members above them)
    ax = fig.add_axes([0.04, 0.47, 0.56, 0.44]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.set_title("Plan, looking down (top rails left off)", fontsize=9.5, color=INK, loc="left")
    for xx in (0, 900 - Sz):
        for yy in (-FY, FY - Sz):
            ax.add_patch(Rectangle((xx, yy), Sz, Sz, fc=INK, ec=INK))
    for yy in (-FY, FY - Sz):
        ax.add_patch(Rectangle((Sz, yy), 900 - 2 * Sz, Sz, fc=TUBE, ec=INK, lw=0.6))
    ax.text(450, FY + 14, "lower side rails 850, 255 to 280 up (front and back)", ha="center", fontsize=7.5, color=INK)
    mem = [("gearbox", D["gbx_members"], "#78716C"), ("spindle", D["sp_members"], "#57534E")]
    for name, xs, col in mem:
        for xc in xs:
            ax.add_patch(Rectangle((X(xc) - Sz / 2, -FY), Sz, 2 * FY, fc=col, ec=INK, lw=0.6, alpha=0.9))
    ax.add_patch(Rectangle((X(D["sp_members"][0]) - Sz / 2, -65), 150, 130, fc=PL, ec=INK, lw=0.6, hatch="////", alpha=0.6))
    ax.add_patch(Rectangle((0, -Sz / 2), Sz, Sz, fc=AC, ec=INK, lw=0.6))
    ax.add_patch(Rectangle((X(P["tank_x"]) - Sz / 2, -FY + Sz), Sz, 2 * FY - 2 * Sz, fc="none", ec=AC, lw=0.9, ls="--"))
    ax.plot([-60, 960], [0, 0], color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    ax.text(965, 0, "centre line", va="center", fontsize=7, color=MUT)
    labs = [(X(D["gbx_members"][0]), "gearbox\nmember"), (X(D["gbx_members"][1]), "gearbox\nmember"),
            (X(D["sp_members"][0]), "spindle and\ntub member"), (X(D["sp_members"][1]), "spindle and\ntub member")]
    for k, (xc, t) in enumerate(labs):
        ax.plot([xc, xc], [-FY - 10, -FY - 55 - 40 * (k % 2)], color=AC, lw=0.5, ls=":")
        ax.text(xc, -FY - 60 - 40 * (k % 2), f"{xc:g}", ha="center", va="top", fontsize=8, color=AC, fontweight="bold")
        ax.text(xc + 16, FY - 70, t, ha="left", va="top", fontsize=6.8, color=INK, rotation=90)
    ax.plot([X(P["tank_x"])] * 2, [-FY - 10, -FY - 135], color=AC, lw=0.5, ls=":")
    ax.text(X(P["tank_x"]), -FY - 140, f"{X(P['tank_x']):g} (tank post member)", ha="center", va="top", fontsize=8, color=AC)
    ax.text(X(P["tank_x"]) - 16, FY - 70, "tank post member\n(top level)", ha="right", va="top", fontsize=6.8, color=AC, rotation=90)
    ax.text(X(P["bowl_x"]), 0, "bearing\nplates", ha="center", va="center", fontsize=6.8, color=INK,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    ax.text(-8, -40, "end post", ha="right", va="center", fontsize=7, color=AC)
    ax.text(450, -FY - 215, "distance from the pedal end to each member centre, mm; members 600 long", ha="center", fontsize=7.5, color=MUT)
    ax.set_xlim(-90, 1000); ax.set_ylim(-FY - 230, FY + 40)
    # elevation from the front
    ay = fig.add_axes([0.04, 0.05, 0.56, 0.38]); ay.set_aspect("equal"); ay.set_axis_off()
    ay.set_title("Elevation, from the front", fontsize=9.5, color=INK, loc="left")
    for xx in (0, 900 - Sz):
        ay.add_patch(Rectangle((xx, 0), Sz, 700, fc=INK, ec=INK))
    rows = [(675, 850, "top side rail"), (255, 850, "lower side rail")]
    for z, L, t in rows:
        ay.add_patch(Rectangle((Sz, z), L, Sz, fc=TUBE, ec=INK, lw=0.6))
    for name, xs, col in mem:
        for xc in xs:
            ay.add_patch(Rectangle((X(xc) - Sz / 2, 280), Sz, Sz, fc=col, ec=INK, lw=0.6))
    for xc in D["sp_members"]:
        ay.add_patch(Rectangle((X(xc) - Sz / 2, 445), Sz, Sz, fc="#57534E", ec=INK, lw=0.6))
        ay.add_patch(Rectangle((X(xc) - Sz / 2, 470), Sz, 205, fc=TUBE, ec=INK, lw=0.6))
    ay.add_patch(Rectangle((X(D["sp_members"][0]) - Sz / 2, 275), 150, 5, fc=PL, ec=INK, lw=0.5))
    ay.add_patch(Rectangle((X(D["sp_members"][0]) - Sz / 2, 440), 150, 5, fc=PL, ec=INK, lw=0.5))
    ay.add_patch(Rectangle((0, 90), Sz, Sz, fc=AC, ec=INK, lw=0.6))
    ay.add_patch(Rectangle((900 - Sz, 600), Sz, Sz, fc=AC, ec=INK, lw=0.6))
    ay.add_patch(Rectangle((X(P["tank_x"]) - Sz / 2, 700), Sz, 545, fc=TUBE, ec=INK, lw=0.6))
    ay.add_patch(Rectangle((X(P["tank_x"]) - 125, 1245), 250, 5, fc=PL, ec=INK, lw=0.6))
    hts = [(0, ""), (90, "low end member (pedal end)"), (255, "lower side rails, 255 to 280"), (280, "members on the rails, 280 to 305"),
           (445, "tub members"), (600, "head member (table end)"), (675, "top rails"), (1245, "tank cradle")]
    last = -1e9
    for k, (z, t) in enumerate(hts):
        if z == 0:
            continue
        zt = max(z, last + 75); last = zt
        ay.plot([910, 940, 960], [z, z, zt], color=AC, lw=0.5, ls=":")
        ay.text(965, zt, f"{z:g}  {t}", va="center", fontsize=7.5, color=AC)
    ay.text(X(D["sp_members"][0]) + 75, 560, "drop\nposts\n205", ha="center", va="center", fontsize=6.8, color=INK)
    ay.text(X(P["tank_x"]) + 18, 960, "tank post 545", ha="left", va="center", fontsize=7, color=INK, rotation=90)
    ay.plot([-30, 1300], [0, 0], color=MUT, lw=0.8)
    ay.set_xlim(-30, 1300); ay.set_ylim(-20, 1300)
    # cut list
    from collections import Counter
    cnt = Counter((n, round(l)) for n, l in frame_members())
    fig.text(0.64, 0.905, "Cut list, 25 x 25 x 1.5 mm tube", fontsize=10, fontweight="bold", color=INK, va="top")
    yy = 0.87
    order = ["leg", "top side rail", "lower side rail", "top end rail", "low end member (pedal end)", "head member (table end)",
             "gearbox member", "spindle member", "tub member", "drop post", "tank post member", "end post", "tank post"]
    tot = 0
    for n in order:
        for (nn, l), q in cnt.items():
            if nn == n:
                fig.text(0.64, yy, f"{q} x {l}", fontsize=8.5, color=INK, va="top", family="monospace")
                fig.text(0.72, yy, n, fontsize=8.5, color=INK, va="top")
                yy -= 0.027; tot += q * l
    fig.text(0.64, yy - 0.005, f"{tot / 1000:.1f} m in all", fontsize=8.5, color=INK, va="top", fontweight="bold")
    notes = ["Plates, 6 mm unless noted:", "  2 bearing plates 150 x 130, 40 mm centre hole,",
             "    four 11 mm holes 70 apart, welded under the", "    spindle members and under the tub members",
             "  tank cradle 250 x 250 x 5, two gussets each way", "", "Order of welding:",
             "  1 two end frames (legs, top and lower rails)", "  2 join with the side rails; check diagonals",
             "  3 members on the lower rails; tub members on", "    their drop posts; end post; low end member",
             "  4 bearing plates: line up both holes with a", "    plumb line, then weld",
             "  5 tank post member, tank post, cradle", "  6 drill the bolt holes; prime and paint"]
    for k, t in enumerate(notes):
        fig.text(0.64, yy - 0.05 - k * 0.025, t, fontsize=8.2, color=INK, va="top")
    fig.text(0.03, 0.012, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.012, "github.com/BoujeeEnjinia1701/gravitysort", fontsize=7, color=AC, ha="right", family="monospace")
    out = OUT / "frame-cuts.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "layouts", "sheets", "joints", "steps"]
    if args[0] in ("sheet", "joint", "step"):
        n = int(args[1])
        print({"sheet": sheets, "joint": joints, "step": steps}[args[0]](n))
    else:
        fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "layouts": layouts}
        for w in args:
            print(w, "->", fns[w]())
