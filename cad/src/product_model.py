"""GravitySort product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a painted frame in 25 mm tube with rounded edges
and rubber feet; the galvanized feed hopper with its punched screen and support arm; the white
HDPE lid guard with a clear polycarbonate sight window over the bowl, two teal over-centre
clamps and the interlock pin; the blue HDPE splash tub with rolling hoops and the galvanized
tailings launder; inside, the cast polyurethane bowl liner and riffle rings on the GFRP shell,
the fluidization jacket, rotary union, spindle with flanged bearing units, the drilled brake
rotor and caliper and the V-belt drive; the pedal station with a padded seat, cranks, pedals
and a toothed chainring; the perforated teal belt and chain guards with a raised name; the water
header tank on its post with a ball valve, a clear rotameter and the hose to the union; the
shaking table (plywood deck with an HDPE face and riffles) on its stand with the eccentric head,
and the launder with its padlocked concentrate box; the bicycle speed display with a lit
readout; and the MotionCore module and reference hub motor. Context is a compact patch of
ground, the tailings hose and the shared clay mannequin seated on the pedal station with its
feet on the pedals.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, riffle_rings() and build_parts() in
model.py. Axes as model.py: X along the machine (pedal station at -X, table at +X), Y front (-Y)
to back (+Y), Z up from the ground. Units mm. Differences from model.py (crank angle, water hose
route, tank post, sight window) are listed in docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / ".kit"))

from build123d import (Align, Axis, Box, Circle, Compound, Cone, Cylinder, Plane, Polygon, Pos, Rot,
                       Solid, Sphere, Text, Vector, extrude, fillet)
from model import PARAMS, riffle_rings

TITLE = "GravitySort: mercury-free gold concentrator with centrifugal bowl and shaking table"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 24, "az": -38,
     "note": "Product render from the front right and above (about 24 deg elevation); shaking table nearest, "
             "centrifuge with hopper, lid window and water tank in the middle, operator pedalling at the far left"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): hopper and screen, lid, bowl, "
             "jacket and tub over the frame; spindle, brake and drive below; pedal station at left; water tank above; "
             "shaking table, stand and concentrate launder at right"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 22, "az": -40,
     "note": "Detail from the front right and above (about 22 deg elevation), without frame, guards or tub: "
             "bowl with riffle rings in its fluidization jacket, spindle, bearings and brake rotor, the V-belt from "
             "the gearbox pulley, and the jackshaft with its table take-off pulley"},
]

FONT = str(HERE.parents[1] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")
MQ_HEIGHT = 1700.0
CRANK_DEG = 100.0      # left crank angle from top dead centre, toward +X (render pose only)
SEAT_X = -970.0        # centre of the seat pad (model.py seat block spans PX - 260 to PX - 80)

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
C_BRASS = "#C9A227"
C_RED = "#B91C1C"
C_WINDOW = "#DCEBF5"
C_LABEL = "#F4F4F2"
C_LCD = "#9FB7A0"
C_LED = "#22C55E"
C_GROUND = "#CBBFA9"
C_CLAY = "#9CA3AF"


# ------------------------------------------------------------------ helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _b(x0, x1, y0, y1, z0, z1):
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    z0, z1 = sorted((z0, z1))
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _tb(x0, x1, y0, y1, z0, z1, r=2.5):
    """Box with the edges along its longest side rounded (steel tube look)."""
    s = _b(x0, x1, y0, y1, z0, z1)
    d = [x1 - x0, y1 - y0, z1 - z0]
    ax = [Axis.X, Axis.Y, Axis.Z][d.index(max(d))]
    return _fillet_try(s, s.edges().filter_by(ax), [r, r * 0.6])


def _zc(x, y, z0, z1, r):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _yc(x, y0, y1, z, r):
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def _xc(x0, x1, y, z, r):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def _cone(x, y, z0, z1, r0, r1):
    return Pos(x, y, (z0 + z1) / 2) * Cone(r0, r1, z1 - z0)


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _comp(shapes):
    return Compound(children=[s for s in shapes if s is not None])


def _hull2(p1, r1, p2, r2, w):
    """Solid hull of two circles (belt or chain outline) in the XY plane, extruded +Z by w."""
    ux, uy = p2[0] - p1[0], p2[1] - p1[1]
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    px, py = -uy, ux
    s = (r1 - r2) / L
    c = math.sqrt(max(1 - s * s, 0.0))
    np_ = (s * ux + c * px, s * uy + c * py)
    nm_ = (s * ux - c * px, s * uy - c * py)
    quad = Polygon((p1[0] + r1 * np_[0], p1[1] + r1 * np_[1]), (p2[0] + r2 * np_[0], p2[1] + r2 * np_[1]),
                   (p2[0] + r2 * nm_[0], p2[1] + r2 * nm_[1]), (p1[0] + r1 * nm_[0], p1[1] + r1 * nm_[1]),
                   align=None)
    sk = Pos(p1[0], p1[1]) * Circle(r1) + Pos(p2[0], p2[1]) * Circle(r2) + quad
    return extrude(sk, amount=w)


def _loop(p1, r1, p2, r2, t_in, t_out, w):
    """Closed belt or chain loop round two pulleys (XY plane, z 0 to w)."""
    return _hull2(p1, r1 + t_out, p2, r2 + t_out, w) - \
        Pos(0, 0, -1) * _hull2(p1, r1 - t_in, p2, r2 - t_in, w + 2)


def _xz(shape, y_front):
    """Map a part built in XY (u = X, v = Z, extruded +Z) into the XZ plane, spanning y_front - w .. y_front."""
    return Pos(0, y_front, 0) * Rot(90, 0, 0) * shape


def _sprocket(r, teeth, t):
    """Toothed disc about Z (z -t/2 .. t/2)."""
    disc = Cylinder(r + 2.5, t)
    gaps = _comp([Pos((r + 3) * math.cos(2 * math.pi * k / teeth), (r + 3) * math.sin(2 * math.pi * k / teeth), 0)
                  * Cylinder(max(2.2, math.pi * r / teeth * 0.45), t + 2) for k in range(teeth)])
    return disc - gaps


def _vpulley(x, y, z0, z1, r, bore=12.0, spokes=0):
    """Vertical-axis V-pulley with a groove and optional lightening holes."""
    p = _zc(x, y, z0, z1, r)
    p = _fillet_try(p, p.edges(), [2.0, 1.0])
    zm = (z0 + z1) / 2
    p -= _zc(x, y, zm - 7, zm + 7, r + 1) - _zc(x, y, zm - 8, zm + 8, r - 8)
    if spokes:
        for k in range(spokes):
            a = 2 * math.pi * k / spokes
            rr = (r - 8 + bore + 20) / 2
            p -= _zc(x + rr * math.cos(a), y + rr * math.sin(a), z0 - 1, z1 + 1, (r - 8 - bore - 20) / 2 * 0.62)
    return p


def _text(pl, txt, size, h):
    try:
        return extrude(pl * Text(txt, font_size=size, font_path=FONT, align=(Align.CENTER, Align.CENTER)), amount=h)
    except Exception:
        return None


def _sector(r0, r1, a0, a1, z0, z1, n=24):
    """Annular sector about the origin, angles in degrees."""
    pts = [(0.0, 0.0)] + [((r1 + 5) / math.cos(math.radians((a1 - a0) / (2 * n))) *
                           math.cos(math.radians(a0 + (a1 - a0) * k / n)),
                           (r1 + 5) / math.cos(math.radians((a1 - a0) / (2 * n))) *
                           math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
    wedge = Pos(0, 0, z0) * extrude(Polygon(*pts, align=None), amount=z1 - z0)
    ring = Pos(0, 0, (z0 + z1) / 2) * (Cylinder(r1, z1 - z0) - Cylinder(r0, z1 - z0 + 2))
    return ring & wedge


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


# ------------------------------------------------------------------ parts
def product_parts(P=PARAMS, with_rider=True):
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    FX0, FX1, FY, RZ, S = P["frame_x0"], P["frame_x1"], P["frame_y"], P["rail_z"], P["tube"]
    CX, CY = P["bowl_x"], 0.0
    JX, DZ, PX = P["jack_x"], P["drive_z"], P["pedal_x"]
    h = S / 2
    tz0, tz1 = P["tub_z"]
    ETANK = (-500, 250, 300)

    # ============================================================ 1 base frame (painted steel tube)
    E1 = (0, 0, 0)
    m = []
    for x in (FX0, FX1 - S):
        for y in (-FY, FY - S):
            m.append(_tb(x, x + S, y, y + S, 0, RZ))
    m += [_tb(FX0, FX1, -FY, -FY + S, RZ - S, RZ), _tb(FX0, FX1, FY - S, FY, RZ - S, RZ),
          _tb(FX0, FX0 + S, -FY, FY, RZ - S, RZ), _tb(FX1 - S, FX1, -FY, FY, RZ - S, RZ),
          _tb(FX0, FX1, -FY, -FY + S, 90, 90 + S), _tb(FX0, FX1, FY - S, FY, 90, 90 + S)]
    for x in (CX - 165, CX + 135):
        m.append(_tb(x, x + S, -FY, FY, tz0 - S, tz0))
    m += [_tb(CX - h, CX + h, -FY, FY, 280 - S, 280), _tb(JX - h, JX + h, -FY, FY, 280 - S, 280),
          _tb(-100 - h, -100 + h, -FY, FY, 265 - S, 265), _tb(-330 - h, -330 + h, -FY, FY, RZ - S, RZ)]
    # tank post (frame_members() in model.py: 550 mm from the rail to the tank)
    TX, TY = P["tank_x"], P["tank_y"]
    tk0, tk1 = P["tank_z"]
    m.append(_tb(TX - h, TX + h, TY - h, TY + h, RZ - S, tk0 - 8))
    m.append(_tb(TX - h, TX + h, -FY, TY + h, RZ - S, RZ))
    frame = _union(m)
    add("Base frame, welded 25 mm tube", frame, C_FRAME, "painted", 1, "shell", E1)
    cradle = _b(TX - 120, TX + 120, TY - 120, TY + 120, tk0 - 8, tk0)
    cradle = _fillet_try(cradle, cradle.edges().filter_by(Axis.Z), [20.0, 10.0])
    gus = _union([_b(TX + h, TX + 90, TY - 3, TY + 3, tk0 - 8 - 60, tk0 - 8) & _yc(TX + h, TY - 4, TY + 4, tk0 - 8, 68),
                   _b(TX - 90, TX - h, TY - 3, TY + 3, tk0 - 8 - 60, tk0 - 8) & _yc(TX - h, TY - 4, TY + 4, tk0 - 8, 68)])
    add("Tank cradle plate and gussets", cradle + gus, C_FRAME, "painted", 1, "shell", ETANK)
    feet = _comp([_b(x - 4, x + S + 4, y - 4, y + S + 4, -1, 8) for x in (FX0, FX1 - S) for y in (-FY, FY - S)])
    add("Frame rubber feet", feet, C_RUBBER, "rubber", 17, "shell", E1)

    # ============================================================ 2 feed hopper, screen, feed pipe
    E2 = (0, 0, 1000)
    hz0, hz1 = P["hopper_z"]
    hr = P["hopper_top_d"] / 2
    hop = _cone(CX, CY, hz0, hz1, 70, hr) - _cone(CX, CY, hz0 + 3, hz1 + 3, 62, hr - 8)
    hop += _zc(CX, CY, hz1 - 10, hz1, hr + 4) - _zc(CX, CY, hz1 - 11, hz1 + 1, hr - 6)      # rolled rim
    fr = P["feed_pipe_d"] / 2
    hop += _zc(CX, CY, 760, hz0 + 2, fr) - _zc(CX, CY, 750, hz0 + 3, fr - 3)
    hop += _zc(CX, CY, hz0 - 8, hz0 + 4, fr + 8) - _zc(CX, CY, hz0 - 9, hz0 + 5, fr - 3)    # spigot collar
    add("Feed hopper and feed pipe (galvanized)", hop, C_GALV, "metal", 2, "shell", E2)
    arm = _tb(CX - 12, CX + 12, -FY, -FY + 24, RZ, 1000) + _tb(CX - 12, CX + 12, -FY, CY - 70, 976, 1000)
    band = _zc(CX, CY, 976, 1000, 82) - _zc(CX, CY, 975, 1001, 76.5)
    band &= _b(CX - 90, CX + 90, -90, 90, 970, 1006)
    arm += band
    add("Hopper support arm and clamp band", arm, C_FRAME, "painted", 2, "shell", (0, 0, 0))
    sr = P["screen_d"] / 2
    sframe = _zc(CX, CY, hz1, hz1 + 8, sr) - _zc(CX, CY, hz1 - 1, hz1 + 9, sr - 10)
    add("Screen frame", sframe, C_STEEL, "metal", 2, "shell", (0, 0, 1150))
    bars = [_b(CX - sr, CX + sr, y - 1.2, y + 1.2, hz1 + 1, hz1 + 5) for y in range(-165, 166, 22)]
    bars += [_b(x - 1.2, x + 1.2, -sr, sr, hz1 + 2, hz1 + 6) for x in range(int(CX) - 165, int(CX) + 166, 22)]
    grid = _union(bars) & _zc(CX, CY, hz1, hz1 + 7, sr - 8)
    add("Punched screen, 2 mm (mesh texture)", grid, "#7E858D", "metal", 2, "shell", (0, 0, 1150))

    # ============================================================ 3 bowl: GFRP shell, PU liner, riffle rings
    E3 = (0, 0, 650)
    z0 = P["bowl_z0"]
    z1 = z0 + P["bowl_depth"]
    r0, r1 = P["bowl_base_d"] / 2, P["bowl_lip_d"] / 2
    lt, st = P["liner_t"], P["shell_t"]
    t = lt + st
    liner = _cone(CX, CY, z0 - lt, z1, r0 + lt, r1 + lt) - _cone(CX, CY, z0, z1 + 1, r0, r1 + 0.01)
    for z, r, ri in riffle_rings(P):
        liner += _zc(CX, CY, z, z + P["ring_t"], r + 2) - _zc(CX, CY, z - 1, z + P["ring_t"] + 1, ri)
    add("Cast PU bowl liner with riffle rings", liner, C_PU, "rubber", 3, "internal", E3)
    shell = _cone(CX, CY, z0 - t, z1, r0 + t, r1 + t) - _cone(CX, CY, z0 - lt, z1 + 1, r0 + lt, r1 + lt + 0.01)
    shell += _zc(CX, CY, z1 - 6, z1, r1 + t + 8) - _zc(CX, CY, z1 - 7, z1 + 1, r1 + lt)      # lip flange
    shell += _zc(CX, CY, z0 - t - 40, z0 - t, 30)
    add("GFRP bowl shell and hub", shell, C_GFRP, "plastic", 3, "internal", E3)
    hb = _comp([_zc(CX + 20 * math.cos(a), 20 * math.sin(a), z0 - t - 44, z0 - t - 40, 4.5)
                for a in [k * math.pi / 2 + math.pi / 4 for k in range(4)]])
    add("Bowl hub bolts", hb, C_STEEL, "metal", 3, "internal", E3)

    # ============================================================ 4 fluidization jacket and rotary union
    g, jt = P["jacket_gap"], P["jacket_t"]
    jz0, jz1 = z0 - t - g, z1 - 30
    rin0 = r0 + t
    rin1 = r0 + (r1 - r0) * (jz1 - z0) / P["bowl_depth"] + t
    jacket = _cone(CX, CY, jz0 - jt, jz1, rin0 + g + jt, rin1 + g + jt) - \
        _cone(CX, CY, jz0, jz1 + 1, rin0 + g, rin1 + g + 0.01)
    jacket += _zc(CX, CY, jz1 - 5, jz1, rin1 + g + jt + 5) - _zc(CX, CY, jz1 - 6, jz1 + 1, rin1 + g)
    add("Fluidization jacket (GFRP)", jacket, "#8FA69A", "plastic", 4, "internal", (0, 0, 450))
    uz0, uz1 = P["union_z"]
    ud = P["union_d"] / 2
    union = _zc(CX, CY, uz0, uz1, ud)
    union = _fillet_try(union, union.edges(), [3.0, 1.5])
    union += _xc(CX - ud - 18, CX - ud + 2, 0, 150, 11) + _xc(CX - ud - 26, CX - ud - 16, 0, 150, 13.5)
    union += _zc(CX, CY, uz1 - 2, uz1 + 10, 20)
    add("Rotary union", union, C_BRASS, "metal", 4, "internal", (0, -550, -150))

    # ============================================================ 5 spindle, flanged bearings, pulley
    E5 = (0, -550, 0)
    spr = P["spindle_d"] / 2
    add("Spindle, 25 mm stainless", _zc(CX, CY, uz1, jz0 - jt, spr), C_STEEL, "metal", 5, "internal", E5)
    bu, bb = [], []
    bz_lo, bz_hi = P["bearing_z"]
    bh = P["bearing_h"]
    for zb, up in ((bz_lo, False), (bz_hi, True)):
        fz0, fz1 = (zb + bh - 14, zb + bh) if up else (zb, zb + 14)
        fl = _b(CX - 43, CX + 43, -43, 43, fz0, fz1)
        fl = _fillet_try(fl, fl.edges().filter_by(Axis.Z), [14.0, 8.0])
        fl += _zc(CX, CY, zb, zb + bh, 32)
        fl -= _zc(CX, CY, zb - 1, zb + bh + 1, spr + 0.5)
        bu.append(fl)
        for sx in (-1, 1):
            for sy in (-1, 1):
                hz = fz0 - 5 if up else fz1
                bb.append(_zc(CX + sx * 30, sy * 30, hz, hz + 5, 6.5))
    add("Flanged bearing units, UCF205", _union(bu), C_CAST, "painted", 5, "internal", E5)
    add("Bearing unit bolts", _comp(bb), C_STEEL, "metal", 5, "internal", E5)
    pz = P["pulley_z"]
    dp = _vpulley(CX, CY, pz, pz + 40, P["driven_pulley_d"] / 2)
    dp -= _zc(CX, CY, pz - 1, pz + 41, spr + 0.5)
    add("Driven pulley, 100 mm, with taper bush", dp, C_STEEL, "metal", 5, "internal", E5)
    mag = _zc(CX + 38, 0, pz + 40, pz + 44, 4.0)
    add("Speed sensor magnet", mag, C_BLACK, "plastic", 19, "internal", E5)

    # ============================================================ 18 brake rotor and caliper
    E18 = (0, -550, 0)
    bz = P["brake_z"]
    br = P["brake_rotor_d"] / 2
    rotor = _zc(CX, CY, bz, bz + 3, br) - _zc(CX, CY, bz - 1, bz + 4, spr + 0.5)
    for k in range(6):
        a = 2 * math.pi * k / 6
        rotor -= _zc(CX + 50 * math.cos(a), 50 * math.sin(a), bz - 1, bz + 4, 13)
    for k in range(18):
        a = 2 * math.pi * (k + 0.5) / 18
        rotor -= _zc(CX + 70 * math.cos(a), 70 * math.sin(a), bz - 1, bz + 4, 2.5)
    add("Brake rotor, 160 mm", rotor, C_STEEL, "metal", 18, "internal", E18)
    cal = _b(CX + br - 25, CX + br + 15, -30, 30, bz - 15, bz + 20)
    cal = _fillet_try(cal, cal.edges(), [5.0, 3.0, 1.5])
    cal -= _b(CX + br - 30, CX + br - 4, -40, 40, bz - 2, bz + 5)
    cal += _yc(CX + br + 5, -38, -30, bz + 8, 7)
    add("Mechanical brake caliper", cal, C_BLACK, "plastic", 18, "internal", E18)
    brk = _tb(CX + br - 5, CX + br + 15, -15, 15, 280, bz - 15)
    add("Caliper bracket", brk, C_FRAME, "painted", 18, "internal", E18)
    cab = _pipe([(CX + br + 5, -44, bz + 8), (CX + br + 5, -120, bz + 30), (CX + br + 40, -270, RZ - 40),
                 (CX + br + 40, -300, RZ - 30)], 2.5)
    add("Brake and interlock cable", cab, C_BLACK, "rubber", 18, "shell", E18)

    # ============================================================ 6 splash tub and tailings launder
    E6 = (0, 0, 250)
    TR = P["tub_d"] / 2
    tt = P["tub_t"]
    tub = _zc(CX, CY, tz0, tz1, TR) - _zc(CX, CY, tz0 + tt + 2, tz1 + 1, TR - tt) - _zc(CX, CY, tz0 - 1, tz0 + 9, 50)
    for zh in (tz0 + 95, tz0 + 215):
        hoop = _zc(CX, CY, zh, zh + 12, TR + 5)
        hoop = _fillet_try(hoop, hoop.edges(), [4.0, 2.0])
        tub += hoop - _zc(CX, CY, zh - 1, zh + 13, TR - 2)
    tub += _zc(CX, CY, tz1 - 8, tz1, TR + 3) - _zc(CX, CY, tz1 - 9, tz1 + 1, TR - 2)
    add("Splash tub (HDPE drum)", tub, C_TUB, "plastic", 6, "shell", E6)
    lau = _b(CX - 40, CX + 40, TR - 20, FY + 120, tz0 - 10, tz0 + 40) - \
        _b(CX - 34, CX + 34, TR - 10, FY + 121, tz0 - 4, tz0 + 41)
    lau -= _zc(CX, CY, tz0 - 11, tz1, TR - tt)
    lau += _b(CX - 44, CX + 44, FY + 100, FY + 120, tz0 - 14, tz0 + 44) - \
        _b(CX - 34, CX + 34, FY + 99, FY + 121, tz0 - 4, tz0 + 45)
    add("Tailings launder (galvanized)", lau, C_GALV, "metal", 6, "shell", E6)
    # teal band and name plate on the tub front
    nb = (_zc(CX, CY, tz1 - 60, tz1 - 42, TR + 0.6) - _zc(CX, CY, tz1 - 61, tz1 - 41, TR - 1)) \
        & _b(CX - 150, CX + 150, -TR - 5, -TR + 80, tz1 - 62, tz1 - 40)
    add("Tub accent band", nb, C_ACCENT, "painted", 6, "shell", E6)

    # ============================================================ 7 lid guard with sight window and clamps
    E7 = (0, 0, 850)
    lr = TR + 8
    lid = _zc(CX, CY, tz1, tz1 + P["lid_t"], lr) - _zc(CX, CY, tz1 - 1, tz1 + P["lid_t"] + 1, P["lid_hole_d"] / 2)
    lid = _fillet_try(lid, lid.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 2.0, 1.0])
    WA0, WA1 = -135.0, -25.0
    lid -= Pos(CX, CY, 0) * _sector(62, 185, WA0, WA1, tz1 - 1, tz1 + P["lid_t"] + 1)
    add("Bowl lid guard (HDPE)", lid, C_HDPE, "plastic", 7, "shell", E7)
    pane = Pos(CX, CY, 0) * _sector(54, 193, WA0 - 3, WA1 + 3, tz1 + P["lid_t"], tz1 + P["lid_t"] + 3)
    add("Lid sight window (clear polycarbonate)", pane, C_WINDOW, "clear", 7, "shell", E7)
    ws = []
    for rr, a0, a1, n in ((58, WA0 - 1, WA1 + 1, 4), (189, WA0 - 1, WA1 + 1, 6)):
        for k in range(n):
            a = math.radians(a0 + (a1 - a0) * k / (n - 1))
            ws.append(_zc(CX + rr * math.cos(a), rr * math.sin(a), tz1 + P["lid_t"] + 3, tz1 + P["lid_t"] + 5, 3.2))
    add("Window screws", _comp(ws), C_STEEL, "metal", 7, "shell", E7)
    handle = _pipe([(CX - 60, 150, tz1 + P["lid_t"]), (CX - 60, 150, tz1 + P["lid_t"] + 30),
                    (CX + 60, 150, tz1 + P["lid_t"] + 30), (CX + 60, 150, tz1 + P["lid_t"])], 7)
    add("Lid handle", handle, C_ACCENT, "plastic", 7, "shell", E7)
    cl = []
    for sx in (-1, 1):
        x = CX + sx * (TR + 8)
        base = _b(x - 10, x + 10, -20, 20, tz1 - 45, tz1 - 20)
        base = _fillet_try(base, base.edges(), [3.0, 1.5])
        lever = _b(x + sx * 10 - 5, x + sx * 10 + 5, -12, 12, tz1 - 40, tz1 + P["lid_t"] + 6)
        lever = _fillet_try(lever, lever.edges(), [2.5, 1.2])
        hook = _b(x - sx * 8, x + sx * 14, -12, 12, tz1 + P["lid_t"], tz1 + P["lid_t"] + 6)
        cl.append(base + lever + hook)
    add("Over-centre lid clamps", _union(cl), C_ACCENT, "painted", 7, "shell", E7)
    pin = _xc(CX + TR + 20, CX + TR + 34, 0, tz1 - 30, 3.0) + _xc(CX + TR + 32, CX + TR + 36, 0, tz1 - 30, 5.0)
    add("Lid interlock pin", pin, C_RED, "painted", 18, "shell", E7)

    # ============================================================ 8 pedal station
    E8 = (-450, 0, 0)
    ped = [_tb(PX - 20, FX0, -20, 20, 250, 280), _tb(PX - 180, FX0, -20, 20, 90, 120),
           _tb(PX - 180, PX - 150, -20, 20, 0, 780), _tb(PX - 20, PX + 20, -20, 20, 0, DZ + 20)]
    ped.append(_yc(PX, -76, 76, DZ, 22))                                                     # bottom bracket shell
    plate = _b(PX - 200, PX + 20, -150, 150, 0, 20)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Z), [20.0, 10.0])
    ped.append(plate)
    ped.append(_b(PX - 260, PX - 80, -70, 70, 780, 792))                                     # seat pan
    add("Pedal station outrigger", _union(ped), C_FRAME, "painted", 8, "shell", E8)
    bolts = _comp([_yc(FX0 - 6, -26, 26, z, 5.5) for z in (265, 105)] +
                  [_zc(PX + sx * 80 - 90, sy * 110, 20, 26, 8) for sx in (-1, 1) for sy in (-1, 1)])
    add("Outrigger bolts", bolts, C_STEEL, "metal", 17, "shell", E8)
    seat = _b(PX - 260, PX - 80, -90, 90, 792, 830)
    seat = _fillet_try(seat, seat.edges().filter_by(Axis.Z), [30.0, 20.0])
    seat = _fillet_try(seat, seat.faces().sort_by(Axis.Z)[-1].edges(), [14.0, 10.0, 6.0])
    add("Seat pad", seat, C_BLACK, "fabric", 8, "shell", E8)
    cr = 170.0
    th = math.radians(CRANK_DEG)
    arms, pedals, pts = [], [], []
    for sgn, y0, y1 in ((1, 76, 88), (-1, -88, -76)):
        a = th if sgn > 0 else th + math.pi
        ex, ez = PX + cr * math.sin(a), DZ + cr * math.cos(a)
        arm = Pos(PX, (y0 + y1) / 2, DZ) * Rot(0, math.degrees(a), 0) * Pos(0, 0, cr / 2) * Box(24, y1 - y0, cr + 30)
        arm = _fillet_try(arm, arm.edges(), [5.0, 3.0])
        arms.append(arm)
        py0, py1 = (y1, y1 + 56) if sgn > 0 else (y0 - 56, y0)
        pb = _b(ex - 50, ex + 50, py0 + 3, py1, ez - 7, ez + 7)
        pb = _fillet_try(pb, pb.edges().filter_by(Axis.Y), [4.0, 2.0])
        for k in range(5):
            pb -= _b(ex - 44 + 22 * k - 1.5, ex - 44 + 22 * k + 1.5, py0, py1 + 1, ez + 5, ez + 8)
        pedals.append(pb)
        pts.append((ex, (py0 + py1) / 2, ez + 7))
    arms.append(_yc(PX, -76, 76, DZ, 10))
    add("Crank arms and axle", _union(arms), C_STEEL, "metal", 8, "shell", E8)
    add("Pedals", _union(pedals), C_RUBBER, "rubber", 8, "shell", E8)
    ring = Pos(PX, 60, DZ) * Rot(90, 0, 0) * _sprocket(97.0, 48, 5)
    ring -= _comp([_yc(PX + 58 * math.cos(2 * math.pi * k / 5), 50, 70, DZ + 58 * math.sin(2 * math.pi * k / 5), 22)
                   for k in range(5)])
    add("Chainring, 48T", ring, C_STEEL, "metal", 8, "shell", E8)

    # ============================================================ 9 jackshaft, gearbox, chains, pulleys
    E9 = (0, -550, 0)
    js = _yc(JX, -270, 280, DZ, 10)
    js += _yc(JX, 216, 224, DZ, 16)
    add("Jackshaft, 20 mm", js, C_STEEL, "metal", 9, "internal", E9)
    fw = Pos(JX, 60, DZ) * Rot(90, 0, 0) * _sprocket(24.3, 12, 8)
    fw += _yc(JX, 50, 70, DZ, 14)
    add("Freewheel, 12T", fw, C_DARK, "metal", 9, "internal", E9)
    ms = Pos(JX, 220, DZ) * Rot(90, 0, 0) * _sprocket(34.0, 17, 6)
    add("Motor chain sprocket", ms, C_DARK, "metal", 9, "internal", E9)
    gb = _b(JX - 50, JX + 50, -40, 40, 280, 380)
    gb = _fillet_try(gb, gb.edges(), [8.0, 5.0, 3.0])
    gb += _yc(JX, -50, -40, DZ, 26) + _yc(JX, 40, 50, DZ, 26) + _zc(JX, 0, 270, 280, 28)
    for k in range(6):
        gb -= _b(JX - 42 + 14 * k, JX - 38 + 14 * k, -41, -39, 300, 360)
    add("Right-angle bevel gearbox", gb, C_CAST, "painted", 9, "internal", E9)
    gbb = _comp([_yc(JX + sx * 38, -44, -40, zz, 4) for sx in (-1, 1) for zz in (292, 368)])
    add("Gearbox cover screws", gbb, C_STEEL, "metal", 9, "internal", E9)
    pbk = []
    for yb in (-180, 150):
        blk = _b(JX - 60, JX + 60, yb - 18, yb + 18, 280, 292) + _yc(JX, yb - 18, yb + 18, DZ, 30) + \
            _b(JX - 30, JX + 30, yb - 18, yb + 18, 280, DZ)
        blk = _fillet_try(blk, blk.edges().filter_by(Axis.Y), [4.0, 2.0])
        pbk.append(blk - _yc(JX, yb - 19, yb + 19, DZ, 10.5))
    add("Jackshaft pillow block bearings", _union(pbk), C_CAST, "painted", 9, "internal", E9)
    vs = _zc(JX, 0, 190, 280, 12)
    add("Vertical drive shaft", vs, C_STEEL, "metal", 9, "internal", E9)
    dr = P["drive_pulley_d"] / 2
    add("Drive pulley, 300 mm", _vpulley(JX, 0, 190, 230, dr, bore=14, spokes=5), C_STEEL, "metal", 9, "internal", E9)
    tr_ = P["take_off_d"] / 2
    top = Pos(JX, -250, DZ) * Rot(90, 0, 0) * Cylinder(tr_, 20)
    top = _fillet_try(top, top.edges(), [2.0, 1.0])
    top -= _yc(JX, -257, -243, DZ, tr_ + 1) - _yc(JX, -258, -242, DZ, tr_ - 8)
    add("Table take-off pulley, 140 mm", top, C_STEEL, "metal", 9, "internal", E9)
    # chains: pedal chain (y 56 to 64) and motor chain (y 216 to 224), in the XZ plane
    ch1 = _xz(_loop((PX, DZ), 97.0, (JX, DZ), 24.3, 3, 4, 8), 64)
    add("Pedal chain", ch1, "#50555C", "metal", 9, "shell", (-225, -275, 0))
    ch2 = _xz(_loop((JX, DZ), 34.0, (-100.0, DZ), 34.0, 3, 4, 8), 224)
    add("Motor chain", ch2, "#50555C", "metal", 9, "accessory", (0, 450, 0))

    # ============================================================ 10 belts
    E10 = (0, -550, -60)
    bowl_belt = Pos(0, 0, 203) * _loop((JX, 0), dr - 4, (CX, 0), P["driven_pulley_d"] / 2 - 4, 4, 4, 14)
    add("Bowl V-belt", bowl_belt, C_RUBBER, "rubber", 10, "internal", E10)
    HX, HZ = P["head_x"], P["head_z"]
    hpr = P["head_pulley_d"] / 2
    tbelt = _xz(_loop((JX, DZ), tr_ - 4, (HX, HZ), hpr - 4, 4, 4, 14), -243)
    add("Table V-belt", tbelt, C_RUBBER, "rubber", 10, "shell", E10)

    # ============================================================ 11 guards (perforated, teal)
    E11 = (0, -700, 420)
    gd = _b(JX - dr - 15, CX + 70, -dr - 20, dr + 20, 175, 245)
    gd = _fillet_try(gd, gd.edges().filter_by(Axis.Z), [16.0, 10.0])
    gi = _b(JX - dr - 9, CX + 64, -dr - 14, dr + 14, 181, 239)
    gi = _fillet_try(gi, gi.edges().filter_by(Axis.Z), [10.0, 6.0])
    gd -= gi
    holes = [_zc(x, y, 237, 247, 5.0) for x in range(int(JX - dr + 10), int(CX + 50), 26)
             for y in range(-int(dr) + 5, int(dr), 26)]
    gd -= _comp(holes)
    gd -= _zc(CX, CY, 170, 250, spr + 8) + _zc(JX, 0, 170, 250, 20)
    add("Bowl belt guard (perforated)", gd, C_ACCENT, "painted", 11, "shell", E11)
    cg = _b(PX - 115, JX + 45, 40, 80, 215, 445)
    cg = _fillet_try(cg, cg.edges().filter_by(Axis.Y), [30.0, 20.0])
    ci = _b(PX - 109, JX + 39, 44, 76, 221, 439)
    ci = _fillet_try(ci, ci.edges().filter_by(Axis.Y), [24.0, 14.0])
    cg -= ci
    cg -= _comp([_yc(x, 30, 90, z, 5.0) for x in range(int(PX - 80), int(JX + 20), 26) for z in range(245, 430, 26)])
    cg -= _yc(PX, 30, 90, DZ, 16) + _yc(JX, 30, 90, DZ, 13)
    add("Chain guard (perforated)", cg, C_ACCENT, "painted", 11, "shell", E11)
    name = _text(Plane(origin=(-120, -dr - 20, 210), x_dir=(1, 0, 0), z_dir=(0, -1, 0)), "GRAVITYSORT", 30, 1.0)
    if name is not None:
        add("Guard name (raised)", name, C_LABEL, "painted", 11, "shell", E11)

    # ============================================================ 12 MotionCore module and reference hub motor
    E12 = (0, 450, 0)
    mc = _b(-420, -177, 120, 288, RZ - S - 66, RZ - S)
    mc = _fillet_try(mc, mc.edges().filter_by(Axis.X), [8.0, 5.0])
    mc = _fillet_try(mc, mc.faces().sort_by(Axis.X)[0].edges(), [2.0, 1.0])
    add("MotionCore module", mc, C_DARK, "plastic", 12, "accessory", E12)
    ml = _b(-380, -220, 119.4, 120.2, RZ - S - 50, RZ - S - 16)
    add("MotionCore label", ml, C_ACCENT, "painted", 12, "accessory", E12)
    led = _yc(-200, 117, 120.5, RZ - S - 33, 3.5)
    add("MotionCore status light (lit)", led, C_LED, "emissive", 12, "accessory", E12)
    mg = _comp([_zc(x, 200, RZ - S - 76, RZ - S - 66, 7) for x in (-390, -350, -310)])
    add("MotionCore cable glands", mg, C_BLACK, "plastic", 12, "accessory", E12)
    hm = _yc(-100, 190, 250, DZ, 80)
    hm = _fillet_try(hm, hm.edges(), [10.0, 6.0])
    for k in range(10):
        a = 2 * math.pi * k / 10
        hm -= Pos(-100, 0, DZ) * Rot(0, math.degrees(a), 0) * _b(-2.5, 2.5, 245, 252, 44, 70)
    hm += _yc(-100, 170, 270, DZ, 7)
    add("Reference hub motor, 250 W", hm, C_BLACK, "metal", 12, "accessory", (0, 450, 0))
    tp = _b(-130, -70, 190, 250, 265, 275) + _b(-112, -88, 262, 272, 265, DZ + 12)
    add("Motor torque plate", tp, C_FRAME, "painted", 12, "accessory", (0, 450, 0))

    # ============================================================ 13 water tank, valve, rotameter, hose
    E13 = (0, 0, 0)
    tr = P["tank_d"] / 2
    tank = _zc(TX, TY, tk0, tk1, tr)
    tank = _fillet_try(tank, tank.edges(), [18.0, 10.0])
    for zh in (tk0 + 120, tk0 + 270):
        hp = _zc(TX, TY, zh, zh + 12, tr + 4)
        tank += _fillet_try(hp, hp.edges(), [4.0, 2.0])
    add("Water header tank, 60 L HDPE drum", tank, C_TANK, "plastic", 13, "shell", ETANK)
    caps = _zc(TX + 90, TY + 60, tk1 - 4, tk1 + 16, 34) + _zc(TX - 100, TY - 40, tk1 - 4, tk1 + 10, 16)
    caps = _fillet_try(caps, caps.edges(), [2.0, 1.0])
    add("Tank bung caps", caps, C_ACCENT, "plastic", 13, "shell", ETANK)
    tlab = (_zc(TX, TY, tk0 + 160, tk0 + 250, tr + 0.5) - _zc(TX, TY, tk0 + 159, tk0 + 251, tr - 1)) \
        & _b(TX - 100, TX + 100, TY - tr - 5, TY - tr + 60, tk0 + 150, tk0 + 260)
    add("Tank label", tlab, C_LABEL, "paper", 13, "shell", ETANK)
    VY = -10.0
    vz = tk0 - 45
    valve = _xc(TX - 26, TX + 26, VY, vz, 16) + _zc(TX, VY, vz, tk0 + 2, 11)
    add("Ball valve, 3/4 in", valve, C_BRASS, "metal", 13, "shell", E13)
    lever = _b(TX - 4, TX + 4, VY - 4, VY + 4, vz + 16, vz + 26) + _b(TX - 4, TX + 90, VY - 5, VY + 5, vz + 22, vz + 30)
    lever = _fillet_try(lever, lever.edges().filter_by(Axis.X), [3.0, 1.5])
    add("Ball valve lever", lever, C_RED, "rubber", 13, "shell", E13)
    f0, f1 = 1050.0, 1150.0
    rot = _zc(TX, VY, f0 + 12, f1 - 12, 16)
    add("Rotameter tube (clear)", rot, C_WINDOW, "clear", 13, "shell", E13)
    rfit = _zc(TX, VY, f0, f0 + 14, 22) + _zc(TX, VY, f1 - 14, f1, 22)
    rfit = _fillet_try(rfit, rfit.edges(), [2.0, 1.0])
    add("Rotameter end fittings", rfit, C_DARK, "plastic", 13, "shell", E13)
    flo = _zc(TX, VY, f0 + 50, f0 + 58, 12) + _zc(TX, VY, f0 + 36, f0 + 50, 3)
    add("Rotameter float", flo, C_ACCENT, "plastic", 13, "shell", E13)
    scale_ = _comp([_b(TX - 20, TX - 16.5, VY - 17, VY - 15.5, z, z + 1.2) for z in range(int(f0 + 20), int(f1 - 18), 8)])
    add("Rotameter scale", scale_, C_DARK, "paper", 13, "shell", E13)
    hr_ = 13.0
    hose = _pipe([(TX, VY, vz - 14), (TX, VY, f1)], 11)
    hose += _pipe([(TX, VY, f0), (TX, VY, f0 - 60), (TX + 60, -215, 900), (TX + 60, -215, 150),
                   (CX - 60, -215, 150), (CX - 60, 0, 150), (CX - 44, 0, 150)], hr_)
    add("Water hose, 3/4 in", hose, C_RUBBER, "rubber", 13, "shell", E13)
    clips = _comp([_xc(TX + 48, TX + 72, -215, z, hr_ + 3) - _xc(TX + 47, TX + 73, -215, z, hr_) for z in (820, 420)])
    add("Hose clips", clips, C_STEEL, "metal", 17, "shell", E13)

    # ============================================================ 14 shaking table deck (tilted)
    E14 = (350, 0, 450)
    TBX0 = P["table_x0"]
    TBX1 = TBX0 + P["table_l"]
    TBW = P["table_w"]
    TZ = P["table_z"]
    tilt = Pos(0, 0, TZ) * Rot(P["table_tilt"], 0, 0) * Pos(0, 0, -TZ)
    ply = _b(TBX0, TBX1, -TBW / 2, TBW / 2, TZ - 18, TZ - 3)
    ply = _fillet_try(ply, ply.edges().filter_by(Axis.Z), [6.0, 3.0])
    add("Table deck, 18 mm marine plywood", tilt * ply, C_PLY, "wood", 14, "shell", E14)
    face = _b(TBX0, TBX1, -TBW / 2, TBW / 2, TZ - 3, TZ)
    face = _fillet_try(face, face.edges().filter_by(Axis.Z), [6.0, 3.0])
    add("Table deck HDPE facing", tilt * face, C_HDPE, "plastic", 14, "shell", E14)
    rif = []
    for i in range(9):
        y = -TBW / 2 + 60 + i * 38
        x0r = TBX0 + 60 + i * 30
        rb = _b(x0r, TBX1 - 40, y, y + 6, TZ, TZ + 8)
        wedge = Pos(x0r, y + 3, TZ) * Rot(0, -math.degrees(math.atan2(8, 200)), 0) * Pos(100, 0, 20) * Box(200, 10, 40)
        rb -= wedge
        rif.append(_fillet_try(rb, rb.edges().filter_by(Axis.X), [1.2, 0.6]))
    add("Tapered riffles", tilt * _union(rif), "#D5D8DC", "plastic", 14, "shell", E14)
    fb = _b(TBX0, TBX0 + 180, TBW / 2 - 90, TBW / 2, TZ, TZ + 70)
    fb = _fillet_try(fb, fb.edges().filter_by(Axis.Z), [8.0, 4.0])
    fb -= _b(TBX0 + 6, TBX0 + 174, TBW / 2 - 84, TBW / 2 - 6, TZ + 6, TZ + 71)
    fb -= _b(TBX0 + 120, TBX0 + 160, TBW / 2 - 91, TBW / 2 - 83, TZ + 20, TZ + 71)
    add("Table feed box", tilt * fb, C_ACCENT, "plastic", 14, "shell", E14)
    wt = _b(TBX0 + 200, TBX1 - 20, TBW / 2 - 40, TBW / 2, TZ, TZ + 40)
    wt -= _b(TBX0 + 206, TBX1 - 26, TBW / 2 - 34, TBW / 2 - 6, TZ + 6, TZ + 41)
    add("Wash water trough", tilt * wt, C_HDPE, "plastic", 14, "shell", E14)

    # ============================================================ 15 table stand and head motion
    E15 = (350, 0, 0)
    tan_t = math.tan(math.radians(P["table_tilt"]))
    st_ = []
    for x in (TBX0 + 60, TBX1 - 80):
        for y in (-TBW / 2 + 20, TBW / 2 - 50):
            top_z = TZ - 18 + (y + 15) * tan_t - 3
            st_.append(_tb(x, x + 30, y, y + 30, 0, top_z - 60))
    st_ += [_tb(TBX0 + 60, TBX1 - 50, -TBW / 2 + 20, -TBW / 2 + 20 + S, 150, 150 + S),
            _tb(TBX0 + 60, TBX1 - 50, TBW / 2 - 20 - S, TBW / 2 - 20, 150, 150 + S),
            _tb(FX1 + 60, FX1 + 60 + S, -80, 80, 0, 640)]
    base = _b(FX1 + 30, FX1 + 120, -120, 120, 0, 20)
    st_.append(_fillet_try(base, base.edges().filter_by(Axis.Z), [12.0, 6.0]))
    add("Table stand, 25 mm tube", _union(st_), C_FRAME, "painted", 15, "shell", E15)
    flex = []
    for x in (TBX0 + 60, TBX1 - 80):
        for y in (-TBW / 2 + 20, TBW / 2 - 50):
            top_z = TZ - 18 + (y + 15) * tan_t - 3
            flex.append(_b(x + 13, x + 17, y + 2, y + 28, top_z - 62, top_z))
    add("Flexure leg strips (spring steel)", _comp(flex), C_STEEL, "metal", 15, "shell", E15)
    head = _b(FX1 + 20, TBX0 + 40, -90, 90, 640, 780)
    head = _fillet_try(head, head.edges(), [10.0, 6.0, 3.0])
    head += _yc(HX, -100, -88, HZ, 30)
    add("Eccentric head housing", head, C_CAST, "painted", 15, "shell", E15)
    pit = _tb(TBX0 - 10, TBX0 + 60, -15, 15, 760, 800) + _xc(TBX0 + 40, TBX0 + 70, 0, 780, 14)
    add("Pitman arm", pit, C_STEEL, "metal", 15, "shell", E15)
    es = _yc(HX, -250, -90, HZ, 12)
    add("Eccentric shaft", es, C_STEEL, "metal", 15, "shell", E15)
    hpul = Pos(HX, -250, HZ) * Rot(90, 0, 0) * Cylinder(hpr, 20)
    hpul = _fillet_try(hpul, hpul.edges(), [2.0, 1.0])
    hpul -= _yc(HX, -257, -243, HZ, hpr + 1) - _yc(HX, -258, -242, HZ, hpr - 8)
    for k in range(4):
        a = 2 * math.pi * k / 4 + math.pi / 4
        hpul -= _yc(HX + 34 * math.cos(a), -262, -238, HZ + 34 * math.sin(a), 10)
    add("Head pulley, 125 mm", hpul, C_STEEL, "metal", 15, "shell", E15)

    # ============================================================ 16 concentrate launder and lockable box
    E16 = (350, -350, 0)
    ly0, ly1 = -TBW / 2 - 130, -TBW / 2 - 30
    la = _b(TBX0 + 150, TBX1 + 40, ly0, ly1, 600, 660) - _b(TBX0 + 156, TBX1 + 34, ly0 + 6, ly1 - 6, 606, 661)
    la += _tb(TBX0 + 160, TBX0 + 190, -TBW / 2 - 100, -TBW / 2 - 60, 0, 600)
    la += _tb(TBX1, TBX1 + 30, -TBW / 2 - 100, -TBW / 2 - 60, 0, 600)
    add("Concentrate launder (galvanized)", la, C_GALV, "metal", 16, "shell", E16)
    bl = _b(TBX1 - 150, TBX1 + 40, ly0 - 2, ly1 + 2, 660, 668)
    bl = _fillet_try(bl, bl.edges().filter_by(Axis.Z), [4.0, 2.0])
    add("Concentrate box lid", bl, C_ACCENT, "painted", 16, "shell", E16)
    hasp = _b(TBX1 - 20, TBX1, ly0 - 5, ly0 - 2, 632, 668) + _yc(TBX1 - 10, ly0 - 8, ly0 - 2, 640, 5)
    add("Padlock hasp", hasp, C_STEEL, "metal", 16, "shell", E16)
    lock = _b(TBX1 - 26, TBX1 + 6, ly0 - 22, ly0 - 8, 600, 628)
    lock = _fillet_try(lock, lock.edges(), [4.0, 2.0])
    shackle = (_yc(TBX1 - 10, ly0 - 17, ly0 - 13, 634, 12) - _yc(TBX1 - 10, ly0 - 18, ly0 - 12, 634, 8)) \
        & _b(TBX1 - 30, TBX1 + 10, ly0 - 20, ly0 - 10, 628, 650)
    add("Padlock body", lock, C_BRASS, "metal", 16, "shell", E16)
    add("Padlock shackle", shackle, C_STEEL, "metal", 16, "shell", E16)

    # ============================================================ 19 bowl speed display
    E19 = (0, -300, 0)
    sd = _b(CX - 30, CX + 30, -FY - 30, -FY, RZ - 60, RZ)
    sd = _fillet_try(sd, sd.edges().filter_by(Axis.Y), [8.0, 5.0])
    sd = _fillet_try(sd, sd.faces().sort_by(Axis.Y)[0].edges(), [2.0, 1.0])
    add("Speed display head unit", sd, C_BLACK, "plastic", 19, "shell", E19)
    lcd = _b(CX - 22, CX + 22, -FY - 31, -FY - 29.5, RZ - 40, RZ - 10)
    add("Speed display screen", lcd, C_LCD, "screen", 19, "shell", E19)
    dig = _comp([_b(CX - 16 + 11 * k, CX - 8 + 11 * k, -FY - 31.6, -FY - 31, RZ - 34, RZ - 16) for k in range(3)])
    add("Speed display readout", dig, "#1B2A22", "paper", 19, "shell", E19)
    btn = _yc(CX, -FY - 33, -FY - 29, RZ - 50, 4)
    add("Speed display button", btn, C_ACCENT, "rubber", 19, "shell", E19)
    sens = _b(CX - 8, CX + 8, -70, -55, pz + 10, pz + 30)
    sens = _fillet_try(sens, sens.edges(), [2.0, 1.0])
    sens += _b(CX - 3, CX + 3, -80, -68, pz + 14, pz + 26)
    add("Speed sensor", sens, C_BLACK, "plastic", 19, "internal", E5)
    swire = _pipe([(CX, -80, pz + 20), (CX, -200, pz + 60), (CX, -FY + 10, RZ - 60), (CX, -FY - 15, RZ - 60)], 2.0)
    add("Speed sensor cable", swire, C_BLACK, "rubber", 19, "shell", E19)

    # ============================================================ context (not in the BOM, except the hose)
    gx0, gx1, gy0, gy1 = -1130.0, TBX1 + 110, -450.0, 480.0
    ground = _b(gx0, gx1, gy0, gy1, -40, 0)
    ground = _fillet_try(ground, ground.edges().filter_by(Axis.Z), [60.0, 30.0])
    ground = _fillet_try(ground, ground.faces().sort_by(Axis.Z)[-1].edges(), [8.0, 4.0])
    add("Ground patch (compacted earth)", ground, C_GROUND, "paper", None, "context", (0, 0, 0))
    th_ = _pipe([(CX, FY + 110, tz0 + 12), (CX, FY + 175, tz0 - 60), (CX + 40, gy1 - 40, 15), (CX + 120, gy1 + 10, 15)], 14)
    add("Tailings hose, 25 mm", th_, C_RUBBER, "rubber", 17, "context", (0, 0, 0))
    if with_rider:
        from context_parts import mannequin
        j, tx, tz = _rider_joints(pts, SEAT_X, 830.0)
        person = Pos(tx, 0, tz) * Rot(0, 0, 90) * mannequin(MQ_HEIGHT, "sit", **j)
        add("Operator, 1.70 m (clay mannequin, pedalling)", person, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:46s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:10.2f} cm3")
