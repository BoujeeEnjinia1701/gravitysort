"""GravitySort product appearance model (build123d), TRL 3, constructable design.

Finished-product look for photoreal renders. Every part of the constructable design is taken
directly from build_components() in model.py (the welded frame with the 1.7 m braced header tank
post, the bowl, jacket, spindle, brake and drive, the splash tub and plain HDPE lid with its two
clamps, the hopper on its support, the pedal outrigger and seat, the guards, the water tank,
valve, rotameter and hose, the shaking table on plywood flexure legs with its head, pitman,
tensioner and bump stop, the tailings launder and the lockable concentrate box, the loose flush
container with its padlock hasp, and the motor option), so every main dimension comes from
model.py. This file only gives each part a product colour and material, sets the render pose of
the cranks (100 degrees from top dead centre; a render pose only, the model keeps its crank
angle; GVS-DEC-001, 2026-10-01), and adds appearance detail that is not in model.py: a
label and bung caps on the tank, the display's screen and readout, a padlock on the flush
container's hasp, the tailings hose to the pond, a patch of ground and the shared clay
mannequin seated on the pedal station with its feet on the pedals. Those additions are listed in
docs/REVIEW.md (session 2026-10-02, approved follow-ups) as proposed, awaiting Amish.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Axes as model.py: X along the machine (pedal station at -X, table at +X), Y front (-Y) to back
(+Y), Z up from the ground. Units mm.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / ".kit"))

from build123d import Box, Cylinder, Pos, Rot  # noqa: E402
from model import PARAMS, EXPLODE_BOM as _EXPLODE_MODEL, build_components, derived  # noqa: E402

# Exploded offsets for the renders: model.py's, except the flush container (23), which is moved further
# forward so it clears the table belt guard (11) in the exploded render.
EXPLODE_BOM = {**_EXPLODE_MODEL, 23: (0, -600, 0)}

TITLE = "GravitySort: mercury-free gold concentrator with centrifugal bowl and shaking table"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 24, "az": -38,
     "note": "Product render from the front right and above (about 24 deg elevation); shaking table nearest, "
             "centrifuge with hopper and lid in the middle under the water tank on its braced 1.7 m post, "
             "flush container in front, operator pedalling at the far left"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): hopper and screen, lid, bowl, "
             "jacket and tub over the frame; spindle, brake and drive below; pedal station at left; water tank above; "
             "shaking table, head, bump stop, launder and concentrate box at right; flush container in front"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 22, "az": -40,
     "note": "Detail from the front right and above (about 22 deg elevation), without frame, guards or tub: "
             "bowl with riffle rings in its fluidization jacket, spindle, bearings and brake disc, the V-belt from "
             "the gearbox pulley, and the jackshaft with its table take-off pulley"},
]

MQ_HEIGHT = 1700.0
CRANK_DEG = 100.0      # front crank angle from top dead centre, toward +X (render pose only)

# Colours (restrained product palette; kit accent)
C_FRAME = "#3A414B"
C_ACCENT = "#0F766E"
C_TUB = "#3A6A93"
C_HDPE = "#E7E8E4"
C_TANK = "#E3E2DC"
C_GALV = "#B9BFC6"
C_STEEL = "#9AA1A9"
C_CAST = "#565D66"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_RUBBER = "#23262B"
C_PU = "#B8621F"
C_GFRP = "#A7B7A5"
C_PLY = "#C9A06B"
C_DECK = "#E1DED6"
C_BRASS = "#C9A227"
C_RED = "#B91C1C"
C_WINDOW = "#DCEBF5"
C_LABEL = "#F4F4F2"
C_LCD = "#9FB7A0"
C_GROUND = "#CBBFA9"
C_CLAY = "#9CA3AF"
C_MOTOR = "#2F3A33"

# model.py component key -> (name, colour, material, group). "crankset" is redrawn below in the render pose.
SPEC = {
    "frame": ("Base frame with the braced tank post, welded 25 mm tube", C_FRAME, "painted", "shell"),
    "tank_braces": ("Tank post braces", C_FRAME, "painted", "shell"),
    "bearing_plates": ("Bearing plates", C_FRAME, "painted", "shell"),
    "tank_cradle": ("Tank cradle plate and gussets", C_FRAME, "painted", "shell"),
    "outrigger": ("Pedal outrigger", C_FRAME, "painted", "shell"),
    "outrigger_plates": ("Outrigger end plates", C_FRAME, "painted", "shell"),
    "seat": ("Seat and seat post", C_BLACK, "fabric", "shell"),
    "pillow_blocks": ("Jackshaft pillow block bearings", C_CAST, "painted", "internal"),
    "gearbox": ("Right-angle bevel gearbox", C_CAST, "painted", "internal"),
    "jackshaft": ("Jackshaft, 20 mm", C_STEEL, "metal", "internal"),
    "jack_wheels": ("Freewheel, motor sprocket and table take-off pulley", C_DARK, "metal", "internal"),
    "drive_pulley": ("Gearbox output shaft and 300 mm drive pulley", C_STEEL, "metal", "internal"),
    "pedal_chain": ("Pedal chain", "#50555C", "metal", "shell"),
    "spindle": ("Spindle, 25 mm stainless tube", C_STEEL, "metal", "internal"),
    "bearings": ("Flanged bearing units, UCF205", C_CAST, "painted", "internal"),
    "driven_pulley": ("Driven pulley, 100 mm", C_STEEL, "metal", "internal"),
    "union": ("Rotary union", C_BRASS, "metal", "internal"),
    "brake_flange": ("Brake flange", C_STEEL, "metal", "internal"),
    "rotor": ("Brake disc, 160 mm", C_STEEL, "metal", "internal"),
    "caliper": ("Mechanical brake caliper", C_BLACK, "plastic", "internal"),
    "caliper_bracket": ("Caliper bracket", C_FRAME, "painted", "internal"),
    "bowl_belt": ("Bowl V-belt", C_RUBBER, "rubber", "internal"),
    "belt_guard": ("Bowl belt guard", C_ACCENT, "painted", "shell"),
    "sensor": ("Speed sensor", C_BLACK, "plastic", "internal"),
    "chain_case": ("Pedal chain case", C_ACCENT, "painted", "shell"),
    "tub": ("Splash tub (HDPE drum)", C_TUB, "plastic", "shell"),
    "standpipe": ("Standpipe and grommet", C_DARK, "rubber", "shell"),
    "tail_pipe": ("Tailings pipe and grommet", C_DARK, "plastic", "shell"),
    "tub_bolts": ("Tub bolts", C_STEEL, "metal", "shell"),
    "liner": ("Cast PU bowl liner with riffle rings", C_PU, "rubber", "internal"),
    "shell": ("GFRP bowl shell", C_GFRP, "plastic", "internal"),
    "jacket": ("Fluidization jacket (GFRP)", "#8FA69A", "plastic", "internal"),
    "hub": ("Shaft flange hub", C_CAST, "metal", "internal"),
    "bowl_bolts": ("Bowl bolts and spacers", C_STEEL, "metal", "internal"),
    "lid": ("Bowl lid guard, 10 mm HDPE", C_HDPE, "plastic", "shell"),
    "clamps": ("Over-centre lid clamps", C_ACCENT, "painted", "shell"),
    "hopper": ("Feed hopper and feed pipe (galvanized)", C_GALV, "metal", "shell"),
    "screen": ("Hopper screen in its frame", "#7E858D", "metal", "shell"),
    "hopper_post": ("Hopper support", C_FRAME, "painted", "shell"),
    "tank": ("Water header tank, 60 L HDPE drum", C_TANK, "plastic", "shell"),
    "valve_meter": ("Ball valve, rotameter and bracket", C_BRASS, "metal", "shell"),
    "hose": ("Water hose, 3/4 in", C_RUBBER, "rubber", "shell"),
    "display": ("Speed display head unit", C_BLACK, "plastic", "shell"),
    "brake_lever": ("Brake lever with parking latch", C_RED, "painted", "shell"),
    "motor_cradle": ("Motor cradle (motor option)", C_FRAME, "painted", "accessory"),
    "motor": ("Reference hub motor, 250 W (motor option)", C_MOTOR, "metal", "accessory"),
    "motor_chain": ("Motor chain (motor option)", "#50555C", "metal", "accessory"),
    "motor_guard": ("Motor chain guard (motor option)", C_ACCENT, "painted", "accessory"),
    "mcore": ("MotionCore module", C_DARK, "plastic", "accessory"),
    "deck": ("Shaking table deck, HDPE-faced plywood with riffles", C_DECK, "plastic", "shell"),
    "wash_pipe": ("Wash water pipe", C_HDPE, "plastic", "shell"),
    "table_base": ("Table base, 25 mm tube", C_FRAME, "painted", "shell"),
    "flex_legs": ("Flexure legs, 18 mm plywood", C_PLY, "wood", "shell"),
    "cleats": ("Leg cleats, steel angle", C_FRAME, "painted", "shell"),
    "head": ("Table head plate and shelf", C_FRAME, "painted", "shell"),
    "head_bearings": ("Head shaft pillow blocks", C_CAST, "painted", "shell"),
    "head_shaft": ("Head shaft, eccentric and pulley", C_STEEL, "metal", "shell"),
    "stop_bracket": ("Bump stop bracket", C_FRAME, "painted", "shell"),
    "bump_stop": ("Bump stop rubber buffer and stud", C_RUBBER, "rubber", "shell"),
    "striker": ("Bump stop striker angle", C_FRAME, "painted", "shell"),
    "pitman": ("Pitman arm", C_STEEL, "metal", "shell"),
    "tensioner": ("Table belt tensioner", C_ACCENT, "painted", "shell"),
    "table_belt": ("Table V-belt", C_RUBBER, "rubber", "shell"),
    "table_guard": ("Table belt guard", C_ACCENT, "painted", "shell"),
    "launder": ("Tailings launder (galvanized)", C_GALV, "metal", "shell"),
    "conc_box": ("Lockable concentrate box (galvanized)", C_GALV, "metal", "shell"),
    "flush_box": ("Flush container, 10 L HDPE pail", C_HDPE, "plastic", "shell"),
    "flush_staple": ("Flush container hasp staple", C_STEEL, "metal", "shell"),
    "flush_hasp": ("Flush container hasp strap", C_STEEL, "metal", "shell"),
}


def _b(x0, x1, y0, y1, z0, z1):
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    z0, z1 = sorted((z0, z1))
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zc(x, y, z0, z1, r):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _yc(x, y0, y1, z, r):
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def _rod(a, c, r):
    from build123d import Plane, Solid, Vector
    a, c = Vector(*a), Vector(*c)
    d = c - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _pipe(points, r):
    from build123d import Sphere
    out = None
    for a, c in zip(points, points[1:]):
        seg = _rod(a, c, r)
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _rider_joints(pedals, seat_x, seat_z):
    """Sit pose with the feet solved onto the pedals and the hands resting on the thighs."""
    from context_parts import mannequin_landmarks as ml
    base = ml(MQ_HEIGHT, "sit")
    tx = seat_x + base["seat"][1]          # world X = -local y + tx
    tz = seat_z - base["seat"][2]

    def local(w):
        return (w[1], -(w[0] - tx), w[2] - tz)

    def descend(err, x):
        step, best = 8.0, err(x)
        while step > 0.05:
            moved = False
            for i in range(len(x)):
                for sg in (1, -1):
                    y = list(x)
                    y[i] += sg * step
                    e = err(y)
                    if e < best:
                        best, x, moved = e, y, True
            if not moved:
                step /= 2
        return x

    j = {}
    for side, tgt, idx in (("l", pedals[0], 0), ("r", pedals[1], 1)):
        T = local(tgt)

        def err(v, side=side, T=T, idx=idx):
            jj = dict(j)
            jj[f"hip_flex_{side}"], jj[f"knee_flex_{side}"], jj[f"ankle_flex_{side}"] = v
            f = ml(MQ_HEIGHT, "sit", **jj)["feet"][idx]
            return (f[1] - T[1]) ** 2 + (f[2] - T[2]) ** 2 + 4 * (v[2] - 10) ** 2
        j[f"hip_flex_{side}"], j[f"knee_flex_{side}"], j[f"ankle_flex_{side}"] = descend(err, [60.0, 80.0, 10.0])
    lm = ml(MQ_HEIGHT, "sit", **j)
    for side, idx in (("l", 0), ("r", 1)):
        sg = 1 if side == "l" else -1
        hip = (sg * abs(lm["feet"][idx][0]), lm["pelvis"][1], lm["pelvis"][2])
        k = lm["knees"][idx]
        T = tuple(hip[i] + 0.68 * (k[i] - hip[i]) for i in range(3))
        T = (T[0], T[1], T[2] + 85)

        def err(v, side=side, T=T, idx=idx):
            jj = dict(j)
            jj[f"shoulder_flex_{side}"], jj[f"elbow_flex_{side}"], jj[f"shoulder_abd_{side}"] = v
            h = ml(MQ_HEIGHT, "sit", **jj)["hands"][idx]
            return sum((a - b) ** 2 for a, b in zip(h, T))
        j[f"shoulder_flex_{side}"], j[f"elbow_flex_{side}"], j[f"shoulder_abd_{side}"] = descend(err, [10.0, 60.0, 0.0])
    return j, tx, tz


def _crank_pose(P):
    """Crank arms, axle, 48T chainring and level pedals in the render pose, sized as model.py's crankset."""
    PX, BZ, CL = P["pedal_x"], P["bb_z"], P["crank_l"]
    cr_r = derived(P)["chain_r"][0]
    th = math.radians(CRANK_DEG)
    arms, pedals, pts = [], [], []
    for a, y0, y1, py0, py1 in ((th, 76, 88, 88, 138), (th + math.pi, -88, -76, -138, -88)):
        ex, ez = PX + CL * math.sin(a), BZ + CL * math.cos(a)
        arms.append(_rod((PX, (y0 + y1) / 2, BZ), (ex, (y0 + y1) / 2, ez), 8))
        pedals.append(_b(ex - 50, ex + 50, py0, py1, ez - 7, ez + 7))
        pts.append((ex, (py0 + py1) / 2, ez + 7))
    axle = _yc(PX, -70, 70, BZ, 8) + _yc(PX, -34, -24, BZ, 17) + _yc(PX, 24, 34, BZ, 17)
    ring = Pos(PX, 60, BZ) * Rot(90, 0, 0) * Cylinder(cr_r, 6)
    return arms[0] + arms[1] + axle, ring, pedals[0] + pedals[1], pts


# ------------------------------------------------------------------ parts
def product_parts(P=PARAMS, with_rider=True):
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    C = build_components(P)
    for key, comp in C.items():
        if key == "crankset":
            continue
        name, col, mat, grp = SPEC[key]
        bom = 21 if comp.bom == 22 else comp.bom
        add(name, comp.shape, col, mat, comp.bom, grp, EXPLODE_BOM.get(bom, (0, 0, 0)))

    # pedal crank in the render pose (model.py keeps top dead centre)
    E8 = EXPLODE_BOM[8]
    arms, ring, pedals, pts = _crank_pose(P)
    add("Crank arms and axle", arms, C_STEEL, "metal", 8, "shell", E8)
    add("Chainring, 48T", ring, C_STEEL, "metal", 8, "shell", E8)
    add("Pedals", pedals, C_RUBBER, "rubber", 8, "shell", E8)

    # ---------------------------------------------------------------- appearance detail not in model.py
    FX0, RZ = P["frame_x0"], P["rail_z"]

    TX, TY, tr = P["tank_x"], P["tank_y"], P["tank_d"] / 2
    tk0, tk1 = P["tank_z"]
    E13 = EXPLODE_BOM[13]
    tlab = (_zc(TX, TY, tk0 + 160, tk0 + 250, tr + 0.5) - _zc(TX, TY, tk0 + 159, tk0 + 251, tr - 1)) \
        & _b(TX - 110, TX + 110, TY - tr - 5, TY - tr + 70, tk0 + 150, tk0 + 260)
    add("Tank label", tlab, C_LABEL, "paper", 13, "shell", E13)
    caps = _zc(TX + 90, TY - 60, tk1, tk1 + 16, 34) + _zc(TX - 100, TY + 40, tk1, tk1 + 10, 16)
    add("Tank bung caps", caps, C_ACCENT, "plastic", 13, "shell", E13)

    # speed display screen and readout on the rider-facing side of the display (model.py: x FX0 - 30 .. FX0 - 6)
    xd = FX0 - 30
    lcd = _b(xd - 1.5, xd, -125, -75, RZ - 55, RZ - 20)
    add("Speed display screen", lcd, C_LCD, "screen", 19, "shell", EXPLODE_BOM[19])
    dig = None
    for k in range(3):
        d_ = _b(xd - 2.1, xd - 1.5, -117 + 12 * k, -108 + 12 * k, RZ - 48, RZ - 27)
        dig = d_ if dig is None else dig + d_
    add("Speed display readout", dig, "#1B2A22", "paper", 19, "shell", EXPLODE_BOM[19])

    # padlocks (bought by the partner; not in the BOM): on the flush container hasp and on the concentrate box
    FCX, FCY, FR = P["flush_x"], P["flush_y"], P["flush_d"] / 2
    yw = FCY - FR
    lock = _b(FCX - 14, FCX + 14, yw - 24, yw - 10, 160, 190)
    shackle = (_yc(FCX, yw - 19, yw - 15, 196, 9) - _yc(FCX, yw - 20, yw - 14, 196, 6)) & _b(FCX - 12, FCX + 12, yw - 20, yw - 14, 190, 210)
    add("Padlock on the flush container", lock, C_BRASS, "metal", 23, "shell", EXPLODE_BOM[23])
    add("Padlock shackle (flush container)", shackle, C_STEEL, "metal", 23, "shell", EXPLODE_BOM[23])

    # ---------------------------------------------------------------- context (not in the BOM)
    TBX1 = P["table_x0"] + P["table_l"]
    gx0, gx1, gy0, gy1 = P["pedal_x"] - 350, TBX1 + 250, -760.0, 640.0
    ground = _b(gx0, gx1, gy0, gy1, -40, -1)
    add("Ground patch (compacted earth)", ground, C_GROUND, "paper", None, "context", (0, 0, 0))
    CX, ty = P["bowl_x"], P["tail_pipe_z"]
    th_ = _pipe([(CX, 440, ty), (CX, 500, ty - 60), (CX + 40, gy1 - 60, 15), (CX + 140, gy1 + 10, 15)], P["tail_pipe_d"] / 2 - 3)
    add("Tailings hose to the settling pond", th_, C_RUBBER, "rubber", None, "context", (0, 0, 0))
    if with_rider:
        from context_parts import mannequin
        sx = P["pedal_x"] - 172.5                        # seat tube axis in model.py
        j, tx, tz = _rider_joints(pts, sx - 5, P["seat_z"] + 50)
        person = Pos(tx, 0, tz) * Rot(0, 0, 90) * mannequin(MQ_HEIGHT, "sit", **j)
        add("Operator, 1.70 m (clay mannequin, pedalling)", person, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:52s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:10.2f} cm3")
