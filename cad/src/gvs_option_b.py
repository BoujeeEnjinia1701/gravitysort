"""GravitySort option B at detail level D3 (kit 1.9, STANDARDS section 24): diaphragm jig and shaking table.

Working principle: a rubber diaphragm under the jig hutch is pushed up and down 12 mm about 300 times a minute by an
eccentric on the pedal jackshaft, so water pulses up through a ragging bed of steel shot on a punched screen; dense
grains (gold, heavy minerals) work down through the bed into the hutch and are drawn off at the spigot, light
gangue overflows the lip. The hutch concentrate is cleaned on the same shaking table as option A, from the same
pedal drive.

Shared with option A (same parts and fixings, from gvs_option_a.option_a with keep): the base frame without the
spindle, tub and tank members, the pedal station, jackshaft, pillow blocks, freewheel and take-off, and the whole
shaking table group. New here: two bearers across the top side rails, the hutch (screen box, pyramid, collar,
flanges), diaphragm, clamp ring and plates, connecting rod, eccentric, spigot and water valves, screen, ragging,
tailings chute and a 60 L drum on its own cradle. Axes as model.py. CONCEPT OPTION, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Plane, Pos, Rot, Sketch, Rectangle, RectangleRounded, Circle, extrude, loft, Cylinder  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402
from gvs_parts import Holes, bolt, screw, cut_holes, bead, box, cyl, tube_box  # noqa: E402

JIG = dict(
    xc=-250.0, half=150.0, wall=2.0,          # hutch centred on the jackshaft, 300 x 300 screen box
    z_flange=725.0, flange_t=6.0, box_h=200.0, lip_drop=30.0,
    z_bottom=545.0, bottom_half=110.0,         # pyramid down to a 220 mm square collar (diaphragm sized for a 5.7 mm water stroke, STM B1)
    collar_h=40.0, ring_t=4.0, dia_t=3.0, plate_half=95.0, ring_half=150.0, opening_half=108.0,
    stroke=12.0, ecc_r=22.0, rod_w=25.0, rod_t=8.0,
    screen_z=851.0, bed_t=40.0,
    bearer_x=(-415.0, -85.0), drum_x=260.0, drum_bearers=(120.0, 400.0),
)


def option_b():
    import model as M
    from gvs_option_a import option_a
    P = M.PARAMS; D = M.derived(P)
    S = P["tube"]; FY, RZ = P["frame_y"], P["rail_z"]
    JX, DZ = P["jack_x"], P["drive_z"]
    J = JIG
    out = option_a(with_bom=False, keep=lambda tags: bool(tags & {"core", "table"}))
    for q in out:
        q["bom"] = None
    new = []
    H = Holes()

    def add(name, shape, mat, kind="made"):
        new.append(part(name, shape, mat, kind=kind, bom=None, group="shell"))

    xc, hf, wt = J["xc"], J["half"], J["wall"]
    zf, ft = J["z_flange"], J["flange_t"]
    zb0 = zf + ft                                  # bottom of the screen box walls
    zb1 = zb0 + J["box_h"]
    # ------------------------------------------------------------------ bearers across the top side rails, bolted
    for xb in J["bearer_x"]:
        add(f"Jig bearer at x {xb:.0f}, 25 x 25 x 1.5 tube", tube_box(xb - S / 2, xb + S / 2, -FY, FY, RZ, RZ + S), "painted_steel")
        for y in (-FY + S / 2, FY - S / 2):
            new.extend(bolt(8, 2 * S, (xb, y, RZ + S), (0, 0, -1), H, bom=None, label=", jig bearer to top side rail"))
    # ------------------------------------------------------------------ hutch: flange plate, screen box walls, pyramid, collar, flange ring
    fl = box(xc - hf - 30, xc + hf + 30, -hf - 30, hf + 30, zf, zf + ft) - box(xc - hf + 2, xc + hf - 2, -hf + 2, hf - 2, zf - 1, zf + ft + 1)
    add("Hutch flange plate, 6 mm", break_edges(fl, 0.8), "galvanised")
    for xb in J["bearer_x"]:
        for y in (-hf - 15, hf + 15):
            new.extend(bolt(8, ft + S, (xb, y, zf + ft), (0, 0, -1), H, bom=None, label=", hutch flange to bearer"))
    walls = [("front", box(xc - hf, xc + hf, -hf, -hf + wt, zb0, zb1)), ("back", box(xc - hf, xc + hf, hf - wt, hf, zb0, zb1)),
             ("feed end", box(xc - hf, xc - hf + wt, -hf + wt, hf - wt, zb0, zb1)),
             ("overflow end", box(xc + hf - wt, xc + hf, -hf + wt, hf - wt, zb0, zb1 - J["lip_drop"]))]
    for nm, w in walls:
        add(f"Screen box wall, {nm}, 2 mm galvanised", break_edges(w, 0.5), "galvanised")
    wb = [bead((xc - hf, -hf, zb0), (1, 0, 0), 2 * hf, (0, -1, 0), (0, 0, 1), 3.0),
          bead((xc - hf, hf, zb0), (1, 0, 0), 2 * hf, (0, 1, 0), (0, 0, 1), 3.0),
          bead((xc - hf, -hf, zb0), (0, 1, 0), 2 * hf, (-1, 0, 0), (0, 0, 1), 3.0),
          bead((xc + hf, -hf, zb0), (0, 1, 0), 2 * hf, (1, 0, 0), (0, 0, 1), 3.0)]
    for i, w in enumerate(wb):
        new.append(part(f"Weld, screen box wall {i + 1} to flange plate", w, "galvanised", kind="weld"))
    for sg in (-1, 1):
        led = box(xc - hf + wt, xc + hf - wt, sg * (hf - wt) - (15 if sg > 0 else 0), sg * (hf - wt) + (0 if sg > 0 else 15), J["screen_z"] - 3, J["screen_z"])
        add(f"Screen ledge, {'front' if sg < 0 else 'back'}, 15 x 3 flat bar", break_edges(led, 0.5), "galvanised")
    zbot, bh = J["z_bottom"], J["bottom_half"]
    outer = loft([Pos(xc, 0, zbot) * Rectangle(2 * bh, 2 * bh), Pos(xc, 0, zf) * Rectangle(2 * hf, 2 * hf)])
    inner = loft([Pos(xc, 0, zbot - 0.01) * Rectangle(2 * bh - 2 * wt * 1.1, 2 * bh - 2 * wt * 1.1),
                  Pos(xc, 0, zf + 0.01) * Rectangle(2 * hf - 2 * wt * 1.1, 2 * hf - 2 * wt * 1.1)])
    add("Hutch pyramid, 2 mm galvanised, welded", outer - inner, "galvanised")
    zc0 = zbot - J["collar_h"]
    collar = box(xc - bh, xc + bh, -bh, bh, zc0, zbot) - box(xc - bh + wt, xc + bh - wt, -bh + wt, bh - wt, zc0 - 1, zbot + 1)
    add("Hutch collar, 220 mm square, 2 mm", collar, "galvanised")
    rt, dt = J["ring_t"], J["dia_t"]
    zr0 = zc0 - rt
    rh, oh = J["ring_half"], J["opening_half"]
    ring = box(xc - rh, xc + rh, -rh, rh, zr0, zc0) - box(xc - oh, xc + oh, -oh, oh, zr0 - 1, zc0 + 1)
    add("Hutch bottom flange ring, 4 mm", break_edges(ring, 0.5), "galvanised")
    new.append(part("Weld, collar to bottom flange ring", bead((xc - bh, -bh, zc0), (1, 0, 0), 2 * bh, (0, -1, 0), (0, 0, 1), 3.0), "galvanised", kind="weld"))
    zd0 = zr0 - dt
    dia = box(xc - rh, xc + rh, -rh, rh, zd0, zr0)
    add("Diaphragm, 3 mm EPDM sheet", break_edges(dia, 0.5), "epdm", kind="bought")
    zc_0 = zd0 - rt
    cring = box(xc - rh, xc + rh, -rh, rh, zc_0, zd0) - box(xc - oh, xc + oh, -oh, oh, zc_0 - 1, zd0 + 1)
    add("Diaphragm clamp ring, 4 mm", break_edges(cring, 0.5), "galvanised")
    for x, y in ((-129, -129), (-60, -129), (60, -129), (129, -129), (-129, 0), (129, 0), (-129, 129), (-60, 129), (60, 129), (129, 129)):
        new.extend(bolt(6, rt + dt + rt, (xc + x, y, zc0), (0, 0, -1), H, bom=None, label=", diaphragm flange"))
    ph = J["plate_half"]
    tp = box(xc - ph, xc + ph, -ph, ph, zr0, zc0)
    bp = box(xc - ph, xc + ph, -ph, ph, zc_0, zd0)
    add("Diaphragm top plate, 4 mm", break_edges(tp, 0.5), "galvanised")
    add("Diaphragm bottom plate, 4 mm", break_edges(bp, 0.5), "galvanised")
    for x, y in ((-75, -75), (75, -75), (-75, 75), (75, 75)):
        new.extend(bolt(6, rt + dt + rt, (xc + x, y, zc0), (0, 0, -1), H, bom=None, label=", diaphragm plates"))
    # clevis lugs under the bottom plate, pin along y
    zp = zc_0 - 20.0
    for sg in (-1, 1):
        lug = box(xc - 20, xc + 20, sg * 5 - (6 if sg < 0 else 0), sg * 5 + (6 if sg > 0 else 0), zc_0 - 34, zc_0) - Plane(origin=(xc, -20, zp), x_dir=(1, 0, 0), z_dir=(0, 1, 0)) * Cylinder(5.0, 40, align=None)
        add(f"Clevis lug, {'front' if sg < 0 else 'back'}, 6 mm", break_edges(lug, 0.5), "galvanised")
        new.append(part(f"Weld, clevis lug {'front' if sg < 0 else 'back'} to bottom plate",
                        bead((xc - 20, sg * 11, zc_0), (1, 0, 0), 40, (0, sg, 0), (0, 0, -1), 3.0), "galvanised", kind="weld"))
    # ------------------------------------------------------------------ drive: eccentric on the jackshaft, connecting rod, clevis pin
    e = J["stroke"] / 2
    jb = M._cyly(JX, DZ, -2000, 2000, 10)
    ecc = break_edges(M._cyly(JX, DZ + e, -12, 12, J["ecc_r"]), 1.0) - jb
    add("Jig eccentric, 44 mm disc, 6 mm throw", ecc, "mild_steel")
    eye = M._cyly(JX, DZ + e, -8, 8, J["ecc_r"] + 10) - M._cyly(JX, DZ + e, -9, 9, J["ecc_r"] + 0.5)
    boss = M._cyly(xc, zp, -4, 4, 12)
    rod = eye + M._bar((JX, 0, DZ + e + J["ecc_r"] + 4), (xc, 0, zp), J["rod_w"], J["rod_t"], normal=(0, 1, 0)) + boss
    rod = rod - M._cyly(xc, zp, -5, 5, 5)
    add("Connecting rod, 25 x 8 flat bar, bushed eye", rod, "mild_steel")
    cpin = Plane(origin=(xc, -11, zp), x_dir=(1, 0, 0), z_dir=(0, -1, 0)) * cp.clevis_pin(10, 22)
    new.append(part("Clevis pin 10 x 22 (ISO 2341), rod to diaphragm", cpin, "zinc_plated", kind="fastener"))
    new.append(part("Split pin (ISO 1234), rod pin", Pos(xc, -11 + 22 + 10, zp) * cp.split_pin(10), "zinc_plated", kind="fastener"))
    # ------------------------------------------------------------------ screen, ragging bed, tailings chute
    sk = Sketch() + RectangleRounded(2 * hf - 2 * wt - 1, 2 * hf - 2 * wt - 1, 2)
    for a in range(12):
        for b in range(12):
            sk -= Pos(-hf + 22 + a * 23, -hf + 22 + b * 23) * Circle(2.0)
    scr = Pos(xc, 0, J["screen_z"]) * extrude(sk, 2.0)
    add("Jig screen, 2 mm punched stainless, 4 mm holes", scr, "stainless")
    bed = box(xc - hf + wt + 1, xc + hf - wt - 1, -hf + wt + 1, hf - wt - 1, J["screen_z"] + 2, J["screen_z"] + 2 + J["bed_t"])
    add("Ragging bed, steel shot 3 to 5 mm, 40 mm deep", break_edges(bed, 1.0), "mild_steel", kind="bought")
    zl = zb1 - J["lip_drop"]
    ch = Plane(origin=(xc + hf, 0, zl - 42), x_dir=(0, 1, 0), z_dir=(1, 0, 0)) * cp.bent_channel_sheet(200, 40, 1.5, 160)
    add("Tailings chute, 1.5 mm galvanised", ch, "galvanised")
    new.append(part("Weld, tailings chute to overflow wall", bead((xc + hf, -100, zl - 42), (0, 1, 0), 200, (0, 0, -1), (1, 0, 0), 2.5), "galvanised", kind="weld"))
    # ------------------------------------------------------------------ spigot and hutch water
    zs = zc0 + 20
    nip = Plane(origin=(xc, -bh, zs), x_dir=(1, 0, 0), z_dir=(0, -1, 0)) * cp.round_tube(26.9, 3.2, 50)
    add("Spigot nipple, 3/4 in steel pipe", nip, "galvanised", kind="bought")
    sv = break_edges(box(xc - 15, xc + 15, -bh - 80, -bh - 50, zs - 15, zs + 15), 2.0) + box(xc - 4, xc + 4, -bh - 72, -bh - 58, zs + 15, zs + 60)
    add("Spigot ball valve, 3/4 in", sv, "brass", kind="bought")
    zw = 600.0
    hw = bh + (hf - bh) * (zw - zbot) / (zf - zbot)
    wn = Plane(origin=(xc, hw - 12, zw), x_dir=(1, 0, 0), z_dir=(0, 1, 0)) * cp.round_tube(26.9, 3.2, 140 - hw + 12)
    wn = wn - outer
    add("Hutch water nipple, 3/4 in steel pipe", wn, "galvanised", kind="bought")
    wv = break_edges(box(xc - 15, xc + 15, 140, 170, zw - 15, zw + 15), 2.0) + box(xc - 4, xc + 4, 148, 162, zw + 15, zw + 60)
    add("Hutch water valve, 3/4 in", wv, "brass", kind="bought")
    # ------------------------------------------------------------------ 60 L drum on a cradle plate and two bearers
    dx = J["drum_x"]
    for xb in J["drum_bearers"]:
        add(f"Drum bearer at x {xb:.0f}, 25 x 25 x 1.5 tube", tube_box(xb - S / 2, xb + S / 2, -FY, FY, RZ, RZ + S), "painted_steel")
        for y in (-FY + S / 2, FY - S / 2):
            new.extend(bolt(8, 2 * S, (xb, y, RZ + S), (0, 0, -1), H, bom=None, label=", drum bearer to top side rail"))
    zc = RZ + S
    add("Drum cradle plate, 300 x 300 x 6", break_edges(box(dx - 150, dx + 150, -150, 150, zc, zc + 6), 0.8), "painted_steel")
    for xb in J["drum_bearers"]:
        for y in (-145.0, 145.0):
            new.extend(bolt(8, 6 + S, (xb, y, zc + 6), (0, 0, -1), H, bom=None, label=", cradle to drum bearer"))
    td0 = zc + 6
    drum = cyl(dx, 0, td0, td0 + 560, 190) - cyl(dx, 0, td0 + 4, td0 + 556, 186)
    for zr in (td0 + 150, td0 + 400):
        drum = drum + (cyl(dx, 0, zr, zr + 12, 193) - cyl(dx, 0, zr - 1, zr + 13, 189))
    add("Header drum, 60 L HDPE", drum, "pe_tank_white", kind="bought")
    valve = break_edges(box(dx - 15, dx + 15, 190, 220, td0 + 15, td0 + 45), 2.0) + box(dx - 4, dx + 4, 198, 212, td0 + 45, td0 + 95)
    add("Ball valve, 3/4 in, drum", valve, "brass", kind="bought")
    hose = cp.rope([(dx, 205, td0 + 15), (dx, 205, 650), (xc + 60, 205, 650), (xc + 60, 205, zw), (xc + 15, 205, zw), (xc, 198, zw), (xc, 170 + 13.5, zw)], 27.0)
    add("Hose, 3/4 in, drum to hutch", hose, "hdpe_black", kind="bought")

    allp = out + new
    cut_holes(allp, H)
    return allp
