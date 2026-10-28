"""GravitySort option C at detail level D3 (kit 1.9, STANDARDS section 24): carpeted sluice and gold pans.

Working principle: slurry runs in a thin film down a galvanised sluice inclined at about 1 in 12, over ribbed
rubber matting held down by expanded metal riffle panels; dense grains settle behind the strands and in the
matting. A punched plate over the head box screens the feed. At clean-up the panels are lifted, the matting is
washed into a tub and the concentrate is panned by hand. No power, no moving parts.

Axes: X along the sluice (head box at x = 0, tail toward +X), Y across, Z up from the ground (z = 0). The
sluice parts are built in the sluice's own frame (floor top at z = 1.5, x from 0 to 2,400) and tilted onto
two timber trestles. A 60 L drum on a timber stand feeds the head box. CONCEPT OPTION, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Plane, Pos, Rot, Sketch, Rectangle, RectangleRounded, Circle, extrude, Cone, Cylinder  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402
from gvs_parts import Holes, bolt, screw, cut_holes, bead, box, cyl  # noqa: E402

L, W, HW, T = 2400.0, 300.0, 150.0, 1.5        # sluice length, width, wall height, sheet
SLOPE = math.degrees(math.atan(1 / 12))        # about 4.8 degrees
ZH = 760.0                                     # head end: underside of the floor above the ground
X_RIF = 400.0                                  # riffles start after the head box
N_PAN = 4


def _tf():
    """Sluice frame to world: tilt about the head end (tail goes down)."""
    return lambda s: Pos(0, 0, ZH) * Rot(0, SLOPE, 0) * s


def _world(x, z):
    a = math.radians(SLOPE)
    return x * math.cos(a) + z * math.sin(a), ZH - x * math.sin(a) + z * math.cos(a)


def option_c():
    tf = _tf()
    out = []
    H = Holes()

    def add(name, shape, mat, kind="made", sl=True):
        out.append(part(name, tf(shape) if sl else shape, mat, kind=kind, bom=None, group="shell"))

    # ------------------------------------------------------------------ sluice body: folded U channel and head plate
    ch = Plane(origin=(0, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0)) * cp.bent_channel_sheet(W, HW, T, L)
    add("Sluice channel, 1.5 mm galvanised sheet folded to a U, 2400 x 300 x 150", ch, "galvanised")
    head = break_edges(box(0, T, -W / 2 + T, W / 2 - T, T, HW), 0.4)
    add("Sluice head plate, 1.5 mm galvanised", head, "galvanised")
    out.append(part("Weld, head plate to floor", tf(bead((T, -W / 2 + T, T), (0, 1, 0), W - 2 * T, (1, 0, 0), (0, 0, 1), 2.5)), "galvanised", kind="weld"))
    for sg in (-1, 1):
        out.append(part(f"Weld, head plate to {'front' if sg < 0 else 'back'} wall",
                        tf(bead((T, sg * (W / 2 - T), T + 3), (0, 0, 1), HW - T - 3, (1, 0, 0), (0, -sg, 0), 2.5)), "galvanised", kind="weld"))

    # ------------------------------------------------------------------ matting and expanded metal riffles
    plen = (L - X_RIF) / N_PAN
    wi = W - 2 * T
    for i in range(N_PAN):
        x0 = X_RIF + i * plen
        sk = Sketch() + Pos(plen / 2, 0) * Rectangle(plen - 1, wi - 1)
        for k in range(int(plen // 25) - 1):
            sk -= Pos(18 + k * 25, 0) * Rectangle(8, wi - 30)
        base = Pos(x0 + plen / 2, 0, T) * extrude(Rectangle(plen - 1, wi - 1), 4.0)
        add(f"Ribbed rubber matting section {i + 1}, 10 mm", base + Pos(x0, 0, T + 4) * extrude(sk, 6.0), "epdm", kind="bought")
        sk2 = Sketch() + Pos(plen / 2, 0) * RectangleRounded(plen - 1, wi - 1, 4)
        for a in range(int((plen - 30) // 34)):
            for b in range(int((wi - 30) // 22)):
                sk2 -= Pos(25 + a * 34, -wi / 2 + 22 + b * 22) * RectangleRounded(24, 12, 3)
        em = Pos(x0, 0, T + 10) * extrude(sk2, 8.0)
        add(f"Expanded metal riffle panel {i + 1}, 8 mm deep, galvanised", em, "galvanised")
    # side hold-down angles, bolted through the walls
    for sg, nm in ((-1, "front"), (1, "back")):
        if sg < 0:
            pl = Plane(origin=(X_RIF, -W / 2 + T, T + 18), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
        else:
            pl = Plane(origin=(L, W / 2 - T, T + 18), x_dir=(0, -1, 0), z_dir=(-1, 0, 0))
        ang = pl * cp.angle(25, 25, 3, L - X_RIF)
        add(f"Hold-down angle, {nm}, 25 x 25 x 3 galvanised", ang, "galvanised")
        for k in range(6):
            x = X_RIF + 100 + k * (L - X_RIF - 200) / 5
            bl = bolt(6, T + 3, (x, sg * W / 2, T + 18 + 14), (0, -sg, 0), H, mat="galvanised", bom=None, label=", hold-down angle")
            for q in bl:
                q["shape"] = tf(q["shape"])
            H.items[-1] = (tf(H.items[-1][0]), H.items[-1][1])
            out += bl

    # ------------------------------------------------------------------ head box screen (punched plate grizzly) on two cross angles
    for nm in ("upstream", "downstream"):
        if nm == "upstream":
            pl = Plane(origin=(0.0, W / 2 + 20, HW), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
            xa = 0.0
        else:
            pl = Plane(origin=(380.0, -W / 2 - 20, HW), x_dir=(-1, 0, 0), z_dir=(0, 1, 0))
            xa = 355.0
        ang = pl * cp.angle(25, 25, 3, W + 40)
        add(f"Screen cross angle, {nm}, 25 x 25 x 3", ang, "galvanised")
        for sg in (-1, 1):
            out.append(part(f"Weld, screen cross angle {nm} to {'front' if sg < 0 else 'back'} wall",
                            tf(bead((xa, sg * W / 2, HW), (1, 0, 0), 25, (0, sg, 0), (0, 0, -1), 2.5)), "galvanised", kind="weld"))
    sk = Sketch() + Pos(0, 0) * RectangleRounded(368, W + 40, 4)
    for a in range(10):
        for b in range(8):
            sk -= Pos(-162 + a * 36, -140 + b * 40) * Circle(4.0)
    scr = Pos(190, 0, HW + 3) * extrude(sk, 2.0)
    add("Punched plate screen, 2 mm galvanised, 8 mm holes", scr, "galvanised")
    for xa in (14.0, 366.0):
        for yb in (-W / 2 - 10, W / 2 + 10):
            bl = bolt(6, 2 + 3, (xa, yb, HW + 5), (0, 0, -1), H, mat="galvanised", bom=None, label=", screen to cross angle")
            for q in bl:
                q["shape"] = tf(q["shape"])
            H.items[-1] = (tf(H.items[-1][0]), H.items[-1][1])
            out += bl

    # ------------------------------------------------------------------ two timber trestles (posts, crossbar, tie, cleats)
    for xs, nm in ((300.0, "head"), (2050.0, "tail")):
        xw, zw = _world(xs + 25, 0.0)           # downstream edge of the crossbar under the floor
        ztop = zw
        cb = box(xw - 50, xw, -260, 260, ztop - 75, ztop)
        out.append(part(f"Trestle crossbar, {nm}, 50 x 75 hardwood", break_edges(cb, 2.0), "hardwood", kind="made"))
        for y in (-210.0, 210.0):
            post = box(xw - 50, xw, y - 25, y + 25, 0, ztop - 75)
            out.append(part(f"Trestle post, {nm}, {'front' if y < 0 else 'back'}, 50 x 50 hardwood", break_edges(post, 2.0), "hardwood"))
            out += screw(8, 100, (xw - 25, y, ztop), (0, 0, -1), H, mat="galvanised", bom=None, kind="coach", label=", crossbar to post")
        tie = box(xw, xw + 25, -260, 260, 150, 225)
        out.append(part(f"Trestle tie rail, {nm}, 25 x 75 hardwood", break_edges(tie, 2.0), "hardwood"))
        for y in (-210.0, 210.0):
            out += bolt(8, 25 + 50, (xw + 25, y, 187.5), (-1, 0, 0), H, mat="galvanised", bom=None, label=", tie to post")
        for y, nm2 in ((-W / 2 - 40, "front"), (W / 2, "back")):
            cl = box(xw - 50, xw, y, y + 40, ztop, ztop + 40)
            out.append(part(f"Trestle cleat, {nm}, {nm2}, 50 x 40 hardwood", break_edges(cl, 2.0), "hardwood"))
            out += screw(6, 70, (xw - 25, y + 20, ztop + 40), (0, 0, -1), H, mat="galvanised", bom=None, kind="coach", label=", cleat to crossbar")

    # ------------------------------------------------------------------ water: 60 L drum on a timber stand, valve, hose
    DX, DY, DZ0 = -650.0, 0.0, 1150.0
    for x in (DX - 170, DX + 120):
        for y in (-170.0, 120.0):
            out.append(part(f"Drum stand leg at x {x:.0f} y {y:.0f}, 50 x 50 hardwood", break_edges(box(x, x + 50, y, y + 50, 0, DZ0 - 18), 2.0), "hardwood"))
    top = box(DX - 200, DX + 200, -200, 200, DZ0 - 18, DZ0)
    out.append(part("Drum stand top, 18 mm marine plywood", break_edges(top, 1.5), "plywood"))
    for x in (DX - 145, DX + 145):
        for y in (-145.0, 145.0):
            out += screw(6, 60, (x, y, DZ0), (0, 0, -1), H, mat="galvanised", bom=None, kind="coach", label=", stand top to leg")
    for z, nm in ((300.0, "lower"), (800.0, "upper")):
        for y in (-170.0, 170.0):
            br = box(DX - 170, DX + 170, (y - 25) if y < 0 else (y), (y) if y < 0 else (y + 25), z, z + 75)
            out.append(part(f"Drum stand rail, {nm}, {'front' if y < 0 else 'back'}, 25 x 75 hardwood", break_edges(br, 2.0), "hardwood"))
            for x in (DX - 145, DX + 145):
                yy = (y - 25) if y < 0 else (y + 25)
                out += bolt(8, 25 + 50, (x, yy, z + 37.5), (0, 1 if y < 0 else -1, 0), H, mat="galvanised", bom=None, label=", stand rail")
    tdr, th = 190.0, 560.0
    drum = cyl(DX, DY, DZ0, DZ0 + th, tdr) - cyl(DX, DY, DZ0 + 4, DZ0 + th - 4, tdr - 4)
    for zr in (DZ0 + 150, DZ0 + 400):
        drum = drum + (cyl(DX, DY, zr, zr + 12, tdr + 3) - cyl(DX, DY, zr - 1, zr + 13, tdr - 1))
    out.append(part("Header drum, 60 L HDPE", drum, "pe_tank_white", kind="bought"))
    valve = break_edges(box(DX + tdr, DX + tdr + 30, -15, 15, DZ0 + 15, DZ0 + 45), 2.0) + box(DX + tdr + 8, DX + tdr + 22, -4, 4, DZ0 + 45, DZ0 + 95)
    out.append(part("Ball valve, 3/4 in", valve, "brass", kind="bought"))
    xh, zh = _world(150.0, HW + 60)
    hose = cp.rope([(DX + tdr + 30, 0, DZ0 + 30), (DX + tdr + 120, 0, DZ0 + 30), (-150, 0, zh + 120), (xh - 60, 0, zh + 60), (xh, 0, zh)], 27.0)
    out.append(part("Hose, 3/4 in, drum to head box", hose, "hdpe_black", kind="bought", color="#0369A1"))

    # ------------------------------------------------------------------ clean-up: wash tub, lockable concentrate bucket, two gold pans
    tub = cyl(400, -800, 0, 300, 250) - cyl(400, -800, 4, 301, 246)
    out.append(part("Clean-up tub, 60 L HDPE", break_edges(tub, 1.0), "hdpe_black", kind="bought"))
    bx, by = 950.0, -700.0
    pail = cyl(bx, by, 0, 280, 125) - cyl(bx, by, 2, 281, 123)
    lid = cyl(bx, by, 280, 288, 129) + (cyl(bx, by, 260, 280, 129) - cyl(bx, by, 259, 281, 125))
    out.append(part("Concentrate bucket, 10 L HDPE pail and lid", pail + lid, "hdpe_natural", kind="bought"))
    yw = by - 125
    staple = box(bx - 15, bx + 15, yw - 3, yw, 180, 225) + box(bx - 4, bx + 4, yw - 15, yw - 3, 196, 208)
    flap = box(bx - 18, bx + 18, yw - 8, yw - 4, 185, 288) + box(bx - 18, bx + 18, yw - 8, yw + 60, 288, 291) - box(bx - 6, bx + 6, yw - 9, yw - 3, 192, 212)
    out.append(part("Bucket hasp staple, riveted", staple, "zinc_plated", kind="bought"))
    out.append(part("Bucket hasp strap, riveted", flap, "zinc_plated", kind="bought"))
    for i, (px, py) in enumerate(((1450.0, -750.0), (1950.0, -750.0))):
        outer = Pos(px, py, 0) * Cone(100, 200, 80, align=None)
        inner = Pos(px, py, 2.5) * Cone(97.5, 197.5, 80, align=None)
        pan = outer - inner + (Pos(px, py, 75) * (Cylinder(206, 5, align=None) - Cylinder(197, 5, align=None)))
        for k in range(3):
            zr = 30 + 12 * k
            ri = 97.5 + 100 * (zr - 2.5) / 80
            pan = pan + Pos(px, py, zr) * (Cylinder(ri + 0.5, 3, align=None) - Cylinder(ri - 3, 3, align=None))
        out.append(part(f"Gold pan {i + 1}, 400 mm, HDPE with riffles", pan, "hdpe_black", kind="bought"))

    cut_holes(out, H)
    return out
