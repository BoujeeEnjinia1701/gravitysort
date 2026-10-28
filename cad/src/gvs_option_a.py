"""GravitySort option A at detail level D3 (kit 1.9, STANDARDS section 24): the current design.

Fluidized centrifugal bowl and shaking table on one pedal drive, exactly as build_components() in model.py
(the build plan, drawings and calculations use that function), but with every part its own solid:

- the welded frame, outrigger, table base, stop bracket, hopper support, motor cradle and caliper bracket as
  real 25 x 25 x 1.5 mm square hollow sections, 6 mm plates and fillet weld beads (cad_parts.weld_fillet);
- every bolt, nut and washer at its joint (cad_parts.hex_bolt_set) with its hole drilled through the parts;
  screws into tapped holes, cast-in nuts and timber; the pitman's clevis pin and split pin;
- bought parts (bearing units, pillow blocks, gearbox, union, filter, drum, MotionCore module with its board and
  connectors) at catalogue envelope with their bores and features; edges broken where a real part has them.

Every made or bought part of option A carries its bom/bom.csv line. Each part dict also carries "tags", the
sub-assemblies it belongs to, which option B reuses (the frame, pedal drive, jackshaft and the table).
PRELIMINARY, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Plane, Pos, Rot, Cylinder, Compound  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402
from gvs_parts import (Holes, bolt, screw, cut_holes, tube_box, tube_between, bead, end_welds, box, cyl, vpulley)  # noqa: E402

PAINT = "painted_steel"
EXPLODE = None


def _ex(bom):
    import model as M
    return M.EXPLODE_BOM.get(21 if bom == 22 else bom, (0, 0, 0))


class Builder:
    def __init__(self):
        self.parts = []
        self.holes = Holes()
        self._nh = 0

    def add(self, name, shape, mat, kind="made", bom=None, tags=("core",), explode=None, color=None):
        ex = explode if explode is not None else (_ex(bom) if bom else (0, 0, 0))
        p = part(name, shape, mat, kind=kind, bom=bom, group="shell", explode=ex, color=color)
        p["tags"] = set(tags)
        self.parts.append(p)
        return p

    def fasteners(self, plist, tags=("core",)):
        for p in plist:
            p["tags"] = set(tags)
            self.parts.append(p)
        for i in range(self._nh, len(self.holes.items)):        # the holes these fasteners need carry their tags
            self.holes.items[i] = (self.holes.items[i][0], self.holes.items[i][1], set(tags))
        self._nh = len(self.holes.items)

    def welds(self, solids, name, bom=1, tags=("core",), mat=PAINT):
        for i, s in enumerate(solids):
            self.add(f"Weld, {name}" + (f" {i + 1}" if len(solids) > 1 else ""), s, mat, kind="weld", bom=bom, tags=tags)


def frame_member_list(P, D):
    """(name, box, tags) of every tube in the welded base frame, as build_components() places them."""
    S = P["tube"]; FX0, FX1, FY, RZ = P["frame_x0"], P["frame_x1"], P["frame_y"], P["rail_z"]
    LZ, LT, MT, MZ, TB = P["low_rail_z"], D["low_top"], D["mem_top"], P["mid_z"], D["top_bot"]
    TX, TY = P["tank_x"], P["tank_y"]; tk0 = P["tank_z"][0]; hz = P["head_member_z"]
    m = []
    for x, xs in ((FX0, "pedal end"), (FX1 - S, "table end")):
        for y, ys in ((-FY, "front"), (FY - S, "back")):
            m.append((f"Frame leg, {ys} {xs}", (x, x + S, y, y + S, 0, RZ), ("core",)))
    for y, ys in ((-FY, "front"), (FY - S, "back")):
        m.append((f"Top side rail, {ys}", (FX0 + S, FX1 - S, y, y + S, RZ - S, RZ), ("core",)))
        m.append((f"Lower side rail, {ys}", (FX0 + S, FX1 - S, y, y + S, LZ, LT), ("core",)))
    m.append(("Top end rail, pedal end", (FX0, FX0 + S, -FY + S, FY - S, RZ - S, RZ), ("core",)))
    m.append(("Top end rail, table end", (FX1 - S, FX1, -FY + S, FY - S, RZ - S, RZ), ("core",)))
    m.append(("Low end member, pedal end", (FX0, FX0 + S, -FY + S, FY - S, P["end_low_z"], P["end_low_z"] + S), ("core",)))
    m.append(("Head member, table end", (FX1 - S, FX1, -FY + S, FY - S, hz, hz + S), ("core",)))
    for i, xc in enumerate(D["gbx_members"]):
        m.append((f"Gearbox member {i + 1}", (xc - S / 2, xc + S / 2, -FY, FY, LT, MT), ("core",)))
    for i, xc in enumerate(D["sp_members"]):
        m.append((f"Spindle member {i + 1}", (xc - S / 2, xc + S / 2, -FY, FY, LT, MT), ("centrifuge",)))
        m.append((f"Tub member {i + 1}", (xc - S / 2, xc + S / 2, -FY, FY, MZ, MZ + S), ("centrifuge",)))
        for y, ys in ((-FY, "front"), (FY - S, "back")):
            m.append((f"Drop post {i + 1}, {ys}", (xc - S / 2, xc + S / 2, y, y + S, MZ + S, TB), ("centrifuge",)))
    m.append(("Tank post member", (TX - S / 2, TX + S / 2, -FY + S, FY - S, RZ - S, RZ), ("water",)))
    m.append(("End post, pedal end", (FX0, FX0 + S, -S / 2, S / 2, P["end_low_z"] + S, RZ - S), ("core",)))
    m.append(("Tank post", (TX - S / 2, TX + S / 2, TY - S / 2, TY + S / 2, RZ, tk0 - 5), ("water",)))
    return m


def joint_welds(members, receivers, leg=3.0):
    """Fillet beads round every tube end that butts onto a face of another member or plate.
    members: [(name, box, tags)]; receivers: same plus plates. Returns [(name, [solids], tags)]."""
    out = []
    for name, b, tags in members:
        d = [b[1] - b[0], b[3] - b[2], b[5] - b[4]]
        k = max(range(3), key=lambda i: d[i])
        others = [i for i in range(3) if i != k]
        a1, a2 = d[others[0]], d[others[1]]
        for end, sgn in ((b[2 * k], 1), (b[2 * k + 1], -1)):
            for rn, rb, rtags in receivers:
                if rn == name:
                    continue
                face = rb[2 * k + 1] if sgn > 0 else rb[2 * k]
                if abs(face - end) > 1e-6:
                    continue
                if not all(rb[2 * i] - 1e-6 <= b[2 * i] and b[2 * i + 1] <= rb[2 * i + 1] + 1e-6 for i in others):
                    continue
                c = [0.0, 0.0, 0.0]; c[k] = end
                for i in others:
                    c[i] = (b[2 * i] + b[2 * i + 1]) / 2
                u = [0.0, 0.0, 0.0]; u[k] = float(sgn)
                fb = list(rb)
                beads = end_welds(tuple(c), tuple(u), a1, tuple(fb), leg=leg, b=a2)
                if beads:
                    out.append((f"{name} to {rn}", beads, tags))
                break
    return out


def option_a(p=None, with_bom=True, keep=None):
    """Option A part dicts. keep(tags) -> bool selects sub-assemblies (option B reuses the frame, pedal drive,
    jackshaft and table); only the holes of the fasteners kept are drilled."""
    import model as M
    P = p or M.PARAMS
    D = M.derived(P)
    C = M.build_components(P)
    B = Builder()
    S, PT = P["tube"], P["plate_t"]
    FX0, FX1, FY, RZ = P["frame_x0"], P["frame_x1"], P["frame_y"], P["rail_z"]
    LZ, LT, MT, MZ, TB = P["low_rail_z"], D["low_top"], D["mem_top"], P["mid_z"], D["top_bot"]
    CX, CY = P["bowl_x"], 0.0
    JX, DZ, PX, BZ = P["jack_x"], P["drive_z"], P["pedal_x"], P["bb_z"]
    TX, TY = P["tank_x"], P["tank_y"]; tk0 = P["tank_z"][0]
    bn = (lambda n: n) if with_bom else (lambda n: None)
    H = B.holes

    # ------------------------------------------------------------------ 1 base frame: tubes, plates, welds
    members = frame_member_list(P, D)
    for name, b, tags in members:
        B.add(name + ", 25 x 25 x 1.5 tube", tube_box(*b, wall=P["tube_wall"]), PAINT, bom=bn(1), tags=tags)
    # tank post braces: the same tube, mitred onto the post and the top side rails
    post_col = box(TX - S / 2, TX + S / 2, TY - S / 2, TY + S / 2, RZ, tk0 - 5)
    first_full = None
    for i, (a_, e_) in enumerate(M.brace_ends(P)):
        d_ = [e_[j] - a_[j] for j in range(3)]
        n_ = (-d_[1], d_[0], 0.0)
        nn = math.hypot(n_[0], n_[1]); n_ = (n_[0] / nn, n_[1] / nn, 0.0)
        br = tube_between(a_, e_, S, P["tube_wall"], x_dir=n_, extend=30.0)
        rail = box(FX0 + S, FX1 - S, -FY if e_[1] < 0 else FY - S, -FY + S if e_[1] < 0 else FY, RZ - S, RZ)
        br = br - box(TX - S / 2, TX + S / 2, TY - S / 2, TY + S / 2, RZ, tk0 + 200) - rail
        br = br - box(-2000, 2000, -2000, 2000, RZ - 400, RZ - S)
        br = max(br.solids(), key=lambda q: q.volume)
        uu = [d_[j] / math.sqrt(sum(v * v for v in d_)) for j in range(3)]
        full = M._bar(tuple(a_[j] - 40 * uu[j] for j in range(3)), e_, S, S, normal=n_)
        if first_full is None:
            first_full = full
        else:
            br = max((br - first_full).solids(), key=lambda q: q.volume)     # mitred against the first brace
        B.add(f"Tank post brace {'front' if e_[1] < 0 else 'back'}, 25 x 25 x 1.5 tube", br, PAINT, bom=bn(1), tags=("water",))
    # bearing plates (6 mm in the BOM text; 5 mm in the model) with the spindle hole
    x0, x1 = D["sp_members"][0] - S / 2, D["sp_members"][1] + S / 2
    bplates = []
    for nm, zt in (("lower", LT), ("upper", MZ)):
        pl = box(x0, x1, -65, 65, zt - 5, zt) - cyl(CX, CY, zt - 6, zt + 1, 20)
        B.add(f"Bearing plate, {nm}", break_edges(pl, 0.8), PAINT, bom=bn(1), tags=("centrifuge",))
        bplates.append((f"Bearing plate, {nm}", (x0, x1, -65, 65, zt - 5, zt), ("centrifuge",)))
        beads = []
        for xc in D["sp_members"]:
            for sg in (-1, 1):
                beads.append(bead((xc - S / 2, sg * 65, zt), (1, 0, 0), S, (0, sg, 0), (0, 0, -1), 3.0))
        B.welds(beads, f"bearing plate {nm} to spindle members" if nm == "lower" else "bearing plate upper to tub members", bom=bn(1), tags=("centrifuge",))
    # tank cradle plate and gussets
    cr = box(TX - 125, TX + 125, TY - 125, TY + 125, tk0 - 5, tk0)
    B.add("Tank cradle plate, 250 x 250 x 5", break_edges(cr, 0.8), PAINT, bom=bn(1), tags=("water",))
    for s_ in (1, -1):
        yb = TY + s_ * S / 2
        g = M._prism([(yb, RZ), (yb + s_ * 70, RZ), (yb, RZ + 70)], "x", TX - 3, TX + 3)
        B.add(f"Tank post foot gusset {'back' if s_ > 0 else 'front'}", g, PAINT, bom=bn(1), tags=("water",))
        xb = TX + s_ * S / 2
        g = M._prism([(xb, tk0 - 5), (xb + s_ * 90, tk0 - 5), (xb, tk0 - 95)], "y", TY - 3, TY + 3)
        B.add(f"Tank cradle gusset {'table side' if s_ > 0 else 'pedal side'}", g, PAINT, bom=bn(1), tags=("water",))
    receivers = members + bplates + [("Tank cradle plate", (TX - 125, TX + 125, TY - 125, TY + 125, tk0 - 5, tk0), ("water",))]
    # crossing welds: the gearbox and spindle members sit on the lower side rails
    for name, b, tags in members:
        if name.startswith(("Gearbox member", "Spindle member")):
            beads = []
            for yr in ((-FY, -FY + S), (FY - S, FY)):
                for sg, xf in ((-1, b[0]), (1, b[1])):
                    beads.append(bead((xf, yr[0], LT), (0, 1, 0), S, (sg, 0, 0), (0, 0, 1), 3.0))
            B.welds(beads, f"{name.lower()} on the lower side rails", bom=bn(1), tags=tags)

    # ------------------------------------------------------------------ 8 pedal outrigger (welded) and its end plates
    xe = FX0 - 6
    sx = PX - 172.5
    o_members = [
        ("Outrigger seat cross foot", (PX - 185, PX - 160, -200, 200, 0, S)),
        ("Outrigger spine, rear", (PX - 160, PX - S / 2, -S / 2, S / 2, 0, S)),
        ("Outrigger pedal cross foot", (PX - S / 2, PX + S / 2, -150, 150, 0, S)),
        ("Outrigger spine, front", (PX + S / 2, xe, -S / 2, S / 2, 0, S)),
        ("Outrigger pedal post", (PX - S / 2, PX + S / 2, -S / 2, S / 2, S, BZ - 20)),
        ("Outrigger top arm", (sx + 16, xe, -S / 2, S / 2, 600, 600 + S)),
    ]
    for nm, b in o_members:
        B.add(nm + ", 25 x 25 x 1.5 tube", tube_box(*b), PAINT, bom=bn(8), tags=("core",))
    seat_tube = Pos(sx, 0, S) * cp.round_tube(32, 2, 700 - S)
    B.add("Outrigger seat tube, 32 x 2 round tube", seat_tube, PAINT, bom=bn(8), tags=("core",))
    bb_shell = M._cyly(PX, BZ, -34, 34, 20) - M._cyly(PX, BZ, -35, 35, 17)
    B.add("Bottom bracket shell (cut from a scrap bicycle frame)", bb_shell, "mild_steel", bom=bn(8), tags=("core",))
    ep_lo = (xe, FX0, -40, 40, 0, P["end_low_z"] + S + 10)
    ep_hi = (xe, FX0, -40, 40, 580, 645)
    for nm, b in (("lower", ep_lo), ("upper", ep_hi)):
        B.add(f"Outrigger end plate, {nm}, 6 mm", break_edges(box(*b), 0.8), PAINT, bom=bn(8), tags=("core",))
    o_recv = [(n, b, ("core",)) for n, b in o_members] + [("Outrigger end plate lower", ep_lo, ("core",)),
                                                          ("Outrigger end plate upper", ep_hi, ("core",))]
    for nm, beads, tags in joint_welds([(n, b, ("core",)) for n, b in o_members], o_recv):
        B.welds(beads, nm.lower(), bom=bn(8), tags=("core",))
    # seat tube on the seat foot: a ring of short beads at the foot of the tube
    B.welds([bead((sx - 16, -6, S), (0, 1, 0), 12, (-1, 0, 0), (0, 0, 1), 3.0),
             bead((sx + 16, -6, S), (0, 1, 0), 12, (1, 0, 0), (0, 0, 1), 3.0)], "seat tube on the seat cross foot", bom=bn(8))
    # end plates bolt to the low end member and the end post (four M8)
    for y in (-25.0, 25.0):
        B.fasteners(bolt(8, 6 + S, (xe, y, P["end_low_z"] + S / 2), (1, 0, 0), H, bom=bn(17), label=", outrigger to frame"))
    for z in (588.0, 637.0):
        B.fasteners(bolt(8, 6 + S, (xe, 0.0, z), (1, 0, 0), H, bom=bn(17), label=", outrigger to frame"))
    seat_post = C["seat"].shape.solids()
    B.add("Seat post, 27.2 mm (bicycle)", Pos(sx, 0, 650) * cp.round_bar(27.2, P["seat_z"] - 650, 1.0), "aluminium", kind="bought", bom=bn(8))
    saddle = break_edges(M._box(sx - 90, sx + 80, -85, 85, P["seat_z"], P["seat_z"] + 50), 8.0)
    B.add("Saddle (bicycle)", saddle, "matte_black", kind="bought", bom=bn(8))
    B.add("Crankset, 48T chainring and pedals (bicycle)", C["crankset"].shape, "mild_steel", kind="bought", bom=bn(8))

    # ------------------------------------------------------------------ 9 jackshaft, pillow blocks, gearbox, wheels, chain
    jack_bore = M._cyly(JX, DZ, -2000, 2000, 10)
    for i, s in enumerate(sorted(C["pillow_blocks"].shape.solids(), key=lambda q: q.center().Y)):
        B.add(f"Jackshaft pillow block {i + 1}, UCP204 class", s - jack_bore, "cast_aluminium", kind="bought", bom=bn(9))
    for y in P["pillow_y"]:
        for xs in (-47.5, 47.5):
            B.fasteners(bolt(10, 13 + S, (JX + xs, y, MT + 13), (0, 0, -1), H, bom=bn(17), label=", pillow block"))
    gfoot = box(JX - 50, JX + 50, -40, 40, MT, MT + 10)
    gbody = box(JX - 32, JX + 32, -40, 40, MT + 10, MT + 70)
    gbox = break_edges(gfoot, 1.0) + break_edges(gbody, 4.0) + M._cyly(JX, DZ, -42, 42, 22)
    gbox = gbox - jack_bore - M._cyl(JX, 0, MT - 1, MT + 30, 12)
    B.add("Right-angle bevel gearbox, 1:1", gbox, "cast_aluminium", kind="bought", bom=bn(9), tags=("centrifuge",))
    for xs in (-42.5, 42.5):
        for ys in (-30.0, 30.0):
            B.fasteners(bolt(8, 10 + S, (JX + xs, ys, MT + 10), (0, 0, -1), H, bom=bn(17), label=", gearbox foot"), tags=("centrifuge",))
    B.add("Jackshaft, 20 mm bright steel", Pos(0, P["belt_y"] - 20, 0) * Pos(JX, 0, DZ) * Rot(-90, 0, 0) *
          cp.round_bar(20, P["motor_chain_y"] + 16.5 - (P["belt_y"] - 20)), "mild_steel", bom=bn(9))
    fw = M._cyly(JX, DZ, P["chain_y"] - 3, P["chain_y"] + 3, D["chain_r"][1]) - jack_bore
    B.add("Freewheel, 12T (bicycle)", fw, "mild_steel", kind="bought", bom=bn(9))
    mspr = M._cyly(JX, DZ, P["motor_chain_y"] - 2, P["motor_chain_y"] + 2, D["motor_spr_r"][0]) - jack_bore
    B.add("Motor sprocket on the jackshaft", mspr, "mild_steel", kind="bought", bom=bn(9), tags=("motor",))
    tko = Plane(origin=(JX, P["belt_y"], DZ), x_dir=(1, 0, 0), z_dir=(0, 1, 0)) * vpulley(P["take_off_d"], 20, 20, spokes=5)
    B.add("Table take-off pulley, 140 mm A-section", tko, "cast_aluminium", kind="bought", bom=bn(9))
    pz = P["pulley_z"]
    B.add("Drive pulley, 300 mm A-section", Pos(JX, 0, pz + 20) * vpulley(P["drive_pulley_d"], 40, 24, spokes=6), "cast_aluminium", kind="bought", bom=bn(9), tags=("centrifuge",))
    B.add("Gearbox output shaft, 24 mm", Pos(JX, 0, pz) * cp.round_bar(24, MT - pz), "mild_steel", kind="bought", bom=bn(9), tags=("centrifuge",))
    cr_r = D["chain_r"][0]
    B.add("Pedal chain, 1/2 in pitch", M._band((PX, BZ, cr_r), (JX, DZ, D["chain_r"][1]), "y", P["chain_y"] - 4, P["chain_y"] + 4, 0.5, 6.0),
          "mild_steel", kind="bought", bom=bn(9))

    # ------------------------------------------------------------------ 5 spindle, bearing units, driven pulley; 4 union
    B.add("Spindle, 25 x 2 mm stainless tube with welded 1/2 in nipple", C["spindle"].shape, "stainless", bom=bn(5), tags=("centrifuge",))
    for i, s in enumerate(sorted(C["bearings"].shape.solids(), key=lambda q: q.center().Z)):
        B.add(f"Spindle bearing unit {'lower' if i == 0 else 'upper'}, UCF205 class", s, "cast_aluminium", kind="bought", bom=bn(5), tags=("centrifuge",))
    for zt in (LT - 5, MZ - 5):
        for xs in (-35, 35):
            for ys in (-35, 35):
                B.fasteners(bolt(10, 5 + 14, (CX + xs, ys, zt + 5), (0, 0, -1), H, bom=bn(17), label=", bearing unit"), tags=("centrifuge",))
    B.add("Driven pulley, 100 mm A-section on a taper bush", Pos(CX, CY, P["pulley_z"] + 20) * vpulley(P["driven_pulley_d"], 40, P["spindle_d"]),
          "cast_aluminium", kind="bought", bom=bn(5), tags=("centrifuge",))
    uz0, uz1 = P["union_z"]
    union = break_edges(M._cyl(CX, CY, uz0 + 8, uz1, P["union_d"] / 2), 2.0) + break_edges(M._cyl(CX, CY, uz0, uz0 + 8, 20), 1.0)
    B.add("Rotary union, 1/2 in, single passage", union, "brass", kind="bought", bom=bn(4), tags=("centrifuge",))

    # ------------------------------------------------------------------ 18 brake, flange, caliper, bracket
    bz, brr = P["brake_z"], P["brake_rotor_d"] / 2
    B.add("Brake flange on a 25 mm shaft collar, welded", C["brake_flange"].shape, "mild_steel", bom=bn(18), tags=("centrifuge",))
    rotor = M._cyl(CX, CY, bz, bz + 3, brr) - M._cyl(CX, CY, bz - 1, bz + 4, 17)
    for k in range(6):
        a = math.radians(30 + 60 * k)
        rotor = rotor - M._cyl(CX + 50 * math.cos(a), 50 * math.sin(a), bz - 1, bz + 4, 9)
    B.add("Brake disc, 160 mm (bicycle, 6-bolt)", rotor, "stainless", kind="bought", bom=bn(18), tags=("centrifuge",))
    for k in range(6):
        a = math.radians(60 * k)
        B.fasteners(screw(5, 6, (CX + 22 * math.cos(a), 22 * math.sin(a), bz + 3), (0, 0, -1), H, bom=bn(18), washer=False,
                          hole_d=5.0, label=", disc to flange"), tags=("centrifuge",))
    cal = C["caliper"].shape
    B.add("Mechanical disc caliper (bicycle)", cal, "cast_aluminium", kind="bought", bom=bn(18), tags=("centrifuge",))
    xb = D["sp_members"][1]
    bplate = box(xb - S / 2, CX + 91, -30, 30, MT, MT + PT)
    bup = box(CX + 85, CX + 91, -30, 30, MT + PT, bz + 20)
    B.add("Caliper bracket base plate, 6 mm", break_edges(bplate, 0.8), PAINT, bom=bn(18), tags=("centrifuge",))
    B.add("Caliper bracket upright, 6 mm", break_edges(bup, 0.8), PAINT, bom=bn(18), tags=("centrifuge",))
    B.welds([bead((CX + 85, -30, MT + PT), (0, 1, 0), 60, (-1, 0, 0), (0, 0, 1), 3.0)], "caliper bracket upright to base", bom=bn(18), tags=("centrifuge",))
    for ys in (-20.0, 20.0):
        B.fasteners(bolt(8, PT + S + 5, (xb, ys, MT + PT), (0, 0, -1), H, bom=bn(17), label=", caliper bracket"), tags=("centrifuge",))
        B.fasteners(bolt(6, 6 + 35, (CX + 91, ys * 0.9, bz + 14), (-1, 0, 0), H, bom=bn(18), label=", caliper"), tags=("centrifuge",))

    # ------------------------------------------------------------------ 10, 11 bowl belt, guards, speed sensor
    pz = P["pulley_z"]
    dr = P["drive_pulley_d"] / 2
    bb_ = M._band((JX, 0, dr), (CX, 0, P["driven_pulley_d"] / 2), "z", pz + 20 - 6.5, pz + 20 + 6.5, -11.5, 0.0)
    B.add("Bowl belt, A-section link V-belt", bb_, "rubber_belt", kind="bought", bom=bn(10), tags=("centrifuge",))
    gz0, gz1 = pz - 10, pz + 50
    dr = P["drive_pulley_d"] / 2
    gx_0, gx_1 = JX - dr - 8, CX + P["driven_pulley_d"] / 2 + 8
    gy = dr + 8
    guard = box(gx_0, gx_1, -gy, gy, gz0, gz1) - box(gx_0 + 1.2, gx_1 - 1.2, -gy + 1.2, gy - 1.2, gz0 + 1.2, gz1 - 1.2)
    guard -= M._cyl(JX, 0, gz1 - 3, gz1 + 1, 20) + M._cyl(CX, 0, gz1 - 3, gz1 + 1, 20) + M._cyl(CX, 0, gz0 - 1, gz0 + 3, 16)
    B.add("Bowl belt guard, 1.2 mm perforated sheet box", guard, "galvanised", bom=bn(11), tags=("centrifuge",))
    for xc in (D["gbx_members"][0], D["sp_members"][0]):
        for y in (-140.0, 140.0):
            sg = 1 if y > 0 else -1
            strap = box(xc - 12.5, xc + 12.5, y - 1.5, y + 1.5, gz1, LT - 3)
            ya, yb4 = (y - 1.5, y + 25.0) if sg > 0 else (y - 25.0, y + 1.5)
            tab = box(xc - 12.5, xc + 12.5, ya, yb4, LT - 3, LT)
            B.add(f"Belt guard hanger {'front' if sg < 0 else 'back'} at x {xc:.0f}, 3 mm strip and tab", strap + tab, "galvanised", bom=bn(11), tags=("centrifuge",))
            B.fasteners(bolt(6, S + 3, (xc, y + sg * 12.0, MT), (0, 0, -1), H, bom=bn(17), label=", belt guard hanger"), tags=("centrifuge",))
    sensor = break_edges(M._box(CX - 8, CX + 8, -76, -60, gz1 - 17.2, gz1 - 1.2), 1.5)
    B.add("Speed sensor (bicycle computer)", sensor, "matte_black", kind="bought", bom=bn(19), tags=("centrifuge",))
    B.add("Pedal chain case, 1.2 mm sheet", C["chain_case"].shape, "galvanised", bom=bn(11))

    # ------------------------------------------------------------------ 6 tub, standpipe, tailings pipe; 4 bolts
    TR = P["tub_d"] / 2; tz0, tz1 = P["tub_z"]; tt = P["tub_t"]
    B.add("Splash tub, cut HDPE drum 430 mm", C["tub"].shape, "hdpe_natural", bom=bn(6), tags=("centrifuge",))
    sz0, sz1 = P["standpipe_z"]
    spipe = M._cyl(CX, CY, sz0, sz1, P["standpipe_d"] / 2) - M._cyl(CX, CY, sz0 - 1, sz1 + 1, P["standpipe_d"] / 2 - 3)
    B.add("Standpipe, 63 mm PVC", spipe, "hdpe_black", bom=bn(6), tags=("centrifuge",))
    B.add("Floor grommet, rubber, 63 mm pipe", C["standpipe"].shape - spipe, "epdm", kind="bought", bom=bn(6), tags=("centrifuge",))
    ty, tr_ = P["tail_pipe_z"], P["tail_pipe_d"] / 2
    tpipe = M._cyly(CX, ty, 200, 440, tr_) - M._cyly(CX, ty, 199, 441, tr_ - 3)
    B.add("Tailings pipe, 75 mm PVC", tpipe, "hdpe_black", bom=bn(6), tags=("centrifuge",))
    B.add("Wall grommet, rubber, 75 mm pipe", C["tail_pipe"].shape - tpipe, "epdm", kind="bought", bom=bn(6), tags=("centrifuge",))
    for xc in D["sp_members"]:
        for y in (-150.0, 150.0):
            B.fasteners(bolt(8, tt + S, (xc, y, tz0 + tt), (0, 0, -1), H, bom=bn(17), label=", tub to tub member"), tags=("centrifuge",))

    # ------------------------------------------------------------------ 3 bowl, 4 jacket and hub, bolts, spacers, nuts
    z0 = P["bowl_z0"]; lt = P["liner_t"]
    liner = C["liner"].shape
    for k in (1, 3, 5, 7):
        a = math.pi / 4 * k
        liner = liner - Pos(CX + 30 * math.cos(a), 30 * math.sin(a), z0 - lt) * cp._hex(10, 5.0)
    B.add("Bowl liner, cast polyurethane Shore 85A", liner, "hdpe_recycled", bom=bn(3), tags=("centrifuge",), color="#C2711D")
    B.add("Bowl shell, 4 mm hand-laid GFRP", C["shell"].shape, "hdpe_natural", bom=bn(3), tags=("centrifuge",), color="#0F766E")
    B.add("Fluidization jacket, 4 mm GFRP", C["jacket"].shape, "hdpe_natural", bom=bn(4), tags=("centrifuge",), color="#5EEAD4")
    B.add("Shaft flange hub, 25 mm bore", C["hub"].shape, "mild_steel", kind="bought", bom=bn(4), tags=("centrifuge",))
    z0 = P["bowl_z0"]; lt = P["liner_t"]
    fb = D["flange_bot"]
    for k in (1, 3, 5, 7):
        a = math.pi / 4 * k
        x, y = CX + 30 * math.cos(a), 30 * math.sin(a)
        L = (z0 - lt + 5) - fb
        blt = Plane(origin=(x, y, fb), x_dir=(1, 0, 0), z_dir=(0, 0, -1)) * cp.hex_bolt(6, L)
        B.add(f"M6 x {L:.0f} hex screw (ISO 4017), stainless, bowl to hub {k // 2 + 1}", blt, "stainless", kind="fastener", bom=bn(17), tags=("centrifuge",))
        sp = Pos(x, y, D["jacket_in"]) * cp.bush(12, 6.4, D["shell_bot"] - D["jacket_in"])
        B.add(f"Spacer bush 12 x 6.4 x 12, stainless {k // 2 + 1}", sp, "stainless", kind="fastener", bom=bn(17), tags=("centrifuge",))
        nut = Pos(x, y, z0 - lt) * (cp._hex(10, 5.0) - Pos(0, 0, 2.5) * Cylinder(3, 5.0))
        B.add(f"M6 cast-in nut, stainless {k // 2 + 1}", nut, "stainless", kind="fastener", bom=bn(3), tags=("centrifuge",))

    # ------------------------------------------------------------------ 7 lid and clamps (M5 to the tub wall)
    B.add("Lid guard, 10 mm HDPE disc", C["lid"].shape, "hdpe_black", bom=bn(7), tags=("centrifuge",))
    for i, (s, ang) in enumerate(zip(C["clamps"].shape.solids(), (-45.0, -135.0))):
        B.add(f"Over-centre lid clamp {i + 1}{', with the interlock pin' if i == 0 else ''}", s, "stainless", kind="bought", bom=bn(7), tags=("centrifuge",))
        a = math.radians(ang)
        for z in (tz1 - 35, tz1 - 15):
            o = (CX + (TR + 22) * math.cos(a), (TR + 22) * math.sin(a), z)
            B.fasteners(bolt(5, 22 + tt, o, (-math.cos(a), -math.sin(a), 0), H, mat="stainless", bom=bn(7), label=", lid clamp"), tags=("centrifuge",))

    # ------------------------------------------------------------------ 2 hopper, screen, support (bolted foot)
    B.add("Feed hopper cone and 44 mm feed pipe, welded", C["hopper"].shape, PAINT, bom=bn(2), tags=("centrifuge",))
    B.add("Screen, 2 mm punched stainless in a flat bar rim", C["screen"].shape, "stainless", bom=bn(2), tags=("centrifuge",))
    hz0, hz1 = P["hopper_z"]; hr0, hr1 = P["hopper_bot_d"] / 2, P["hopper_top_d"] / 2
    rz = P["hopper_ring_z"]; rr = hr0 + (hr1 - hr0) * (rz - hz0) / (hz1 - hz0)
    foot = (CX - 37.5, CX + 37.5, -FY, -FY + S, RZ, RZ + PT)
    hpost = (CX - S / 2, CX + S / 2, -FY, -FY + S, RZ + PT, rz)
    arm = (CX - S / 2, CX + S / 2, -FY + S, -rr - 12, rz - S, rz)
    ring = M._cyl(CX, CY, rz - PT, rz, rr + 20) - M._cyl(CX, CY, rz - PT - 1, rz + 1, rr)
    B.add("Hopper post foot plate, 6 mm", break_edges(box(*foot), 0.8), PAINT, bom=bn(2), tags=("centrifuge",))
    B.add("Hopper post, 25 x 25 x 1.5 tube", tube_box(*hpost), PAINT, bom=bn(2), tags=("centrifuge",))
    B.add("Hopper arm, 25 x 25 x 1.5 tube", tube_box(*arm) - M._cyl(CX, CY, rz - S - 1, rz + 1, rr + 20), PAINT, bom=bn(2), tags=("centrifuge",))
    B.add("Hopper ring, 6 mm", ring, PAINT, bom=bn(2), tags=("centrifuge",))
    for nm, beads, tags in joint_welds([("Hopper post", hpost, ("centrifuge",)), ("Hopper arm", arm, ("centrifuge",))],
                                       [("Hopper post foot", foot, ("centrifuge",)), ("Hopper post", hpost, ("centrifuge",))]):
        B.welds(beads, nm.lower(), bom=bn(2), tags=("centrifuge",))
    for xs in (-25.0, 25.0):
        B.fasteners(bolt(6, PT + S, (CX + xs, -FY + S / 2, RZ + PT), (0, 0, -1), H, bom=bn(17), label=", hopper foot"), tags=("centrifuge",))

    # ------------------------------------------------------------------ 13 water: drum, valve, rotameter, filter, hose
    tdr = P["tank_d"] / 2; tz1_ = P["tank_z"][1]
    drum = M._cyl(TX, TY, tk0, tz1_, tdr) - M._cyl(TX, TY, tk0 + 4, tz1_ - 4, tdr - 4)
    for zr in (tk0 + 150, tk0 + 400):
        drum = drum + (M._cyl(TX, TY, zr, zr + 12, tdr + 3) - M._cyl(TX, TY, zr - 1, zr + 13, tdr - 1))
    drum = drum + M._cyl(TX + 110, TY, tz1_, tz1_ + 12, 30) - M._cyl(TX + 110, TY, tz1_ - 5, tz1_ + 13, 22)
    B.add("Header drum, 60 L HDPE, about 380 x 560", drum, "pe_tank_white", kind="bought", bom=bn(13), tags=("water",))
    yv = TY + tdr
    valve = break_edges(M._box(TX - 15, TX + 15, yv, yv + 30, tk0 + 15, tk0 + 45), 2.0) + M._box(TX - 4, TX + 4, yv + 8, yv + 22, tk0 + 45, tk0 + 95)
    B.add("Ball valve, 3/4 in, with lever", valve, "brass", kind="bought", bom=bn(13), tags=("water",))
    yb_ = FY + 5
    bracket = M._box(TX - 20, TX + 20, FY, yb_, RZ - S, RZ + 130)
    B.add("Rotameter bracket, 5 mm plate", break_edges(bracket, 0.8), PAINT, bom=bn(13), tags=("water",))
    B.welds([bead((TX + sg * 20, FY, RZ - S), (0, 0, 1), S, (sg, 0, 0), (0, 1, 0), 3.0) for sg in (-1, 1)], "rotameter bracket to back top rail", bom=bn(13), tags=("water",))
    meter = break_edges(M._box(TX - 15, TX + 15, yb_, yb_ + 30, 720, 820), 2.0)
    B.add("Rotameter, 2 to 20 L/min", meter, "polycarbonate", kind="bought", bom=bn(13), tags=("water",))
    sz0_, sz1_ = P["strainer_z"]; yh = C["strainer"].shape.center().Y
    hx = lambda z0_, z1_: Pos(TX, yh, z0_) * cp._hex(40, z1_ - z0_)  # noqa: E731
    filt = hx(sz0_, sz0_ + 14) + hx(sz1_ - 14, sz1_) + M._cyl(TX, yh, sz0_ + 14, sz1_ - 14, 20) + M._cyl(TX, yh, sz0_ + 40, sz1_ - 30, 23)
    filt = filt + M._cylx(yh, sz0_ + 25, TX - 40, TX - 18, 6)
    B.add("Screen filter, 3/4 in, 120 mesh stainless screen, flush valve", filt, "polycarbonate", kind="bought", bom=bn(13), tags=("water",))
    B.add("Hose, 3/4 in, tank to rotary union", C["hose"].shape, "hdpe_black", kind="bought", bom=bn(13), tags=("water",), color="#0369A1")

    # ------------------------------------------------------------------ 19 display, 18 lever
    B.add("Speed display (bicycle computer) on its bracket", C["display"].shape, "matte_black", kind="bought", bom=bn(19), tags=("centrifuge",))
    B.add("Brake lever with parking latch", C["brake_lever"].shape, "cast_aluminium", kind="bought", bom=bn(18), tags=("centrifuge",))

    # ------------------------------------------------------------------ 20 motor option: cradle (bolted), motor, chain, guard; 12 MotionCore
    MX, MZ_ = P["motor_x"], P["motor_z"]; my0, my1 = P["motor_y"]
    cy1 = 392
    cplate = box(MX - 65, MX + 65, FY - S, cy1, LT, LT + PT)
    B.add("Motor cradle base plate, 6 mm", break_edges(cplate, 0.8), PAINT, bom=bn(20), tags=("motor",))
    for nm, (ya, yb2) in (("inner", (my0 - 6, my0)), ("outer", (382, 388))):
        dro = box(MX - 30, MX + 30, ya, yb2, LT + PT, MZ_ + 14) - M._cyly(MX, MZ_, ya - 1, yb2 + 1, 6) - box(MX - 6, MX + 6, ya - 1, yb2 + 1, MZ_, MZ_ + 20)
        B.add(f"Motor dropout, {nm}, 6 mm", dro, PAINT, bom=bn(20), tags=("motor",))
        B.welds([bead((MX - 30, ya, LT + PT), (1, 0, 0), 60, (0, -1, 0), (0, 0, 1), 3.0),
                 bead((MX - 30, yb2, LT + PT), (1, 0, 0), 60, (0, 1, 0), (0, 0, 1), 3.0)], f"motor dropout {nm} to base plate", bom=bn(20), tags=("motor",))
    for xs in (-45.0, 45.0):
        B.fasteners(bolt(8, PT + S, (MX + xs, FY - S / 2, LT + PT), (0, 0, -1), H, bom=bn(17), label=", motor cradle"), tags=("motor",))
    B.add("Reference hub motor with sprocket (MotionCore)", C["motor"].shape, "aluminium", kind="bought", bom=bn(12), tags=("motor",), color="#166534")
    mch = M._band((JX, DZ, D["motor_spr_r"][0]), (MX, MZ_, D["motor_spr_r"][1]), "y", P["motor_chain_y"] - 4, P["motor_chain_y"] + 4, 0.5, 6.0)
    B.add("Motor chain, 1/2 in pitch", mch, "mild_steel", kind="bought", bom=bn(12), tags=("motor",))
    B.add("Motor chain guard, 1.2 mm sheet", C["motor_guard"].shape, "galvanised", bom=bn(20), tags=("motor",))
    ex0, ex1, ey0, ey1, ez0, ez1 = -420, -177, 120, 288, TB - 66, TB
    encl = box(ex0, ex1, ey0, ey1, ez0, ez1 - 4) - box(ex0 + 3, ex1 - 3, ey0 + 3, ey1 - 3, ez0 + 3, ez1)
    B.add("MotionCore enclosure, 3 mm ABS", break_edges(encl, 1.0), "matte_black", kind="bought", bom=bn(12), tags=("motor",))
    B.add("MotionCore enclosure lid", break_edges(box(ex0, ex1, ey0, ey1, ez1 - 4, ez1), 1.0), "matte_black", kind="bought", bom=bn(12), tags=("motor",))
    pcb = box(ex0 + 10, ex1 - 10, ey0 + 10, ey1 - 10, ez0 + 13, ez0 + 14.6)
    for hx_, hy_ in ((ex0 + 16, ey0 + 16), (ex1 - 16, ey0 + 16), (ex0 + 16, ey1 - 16), (ex1 - 16, ey1 - 16)):
        pcb = pcb - M._cyl(hx_, hy_, ez0 + 12, ez0 + 16, 1.6)
    B.add("MotionCore controller board (PCB)", pcb, "hdpe_recycled", kind="bought", bom=bn(12), tags=("motor",), color="#14532D")
    for j, (bx_, by_) in enumerate(((ex0 + 16, ey0 + 16), (ex1 - 16, ey0 + 16), (ex0 + 16, ey1 - 16), (ex1 - 16, ey1 - 16))):
        B.fasteners([part(f"Board spacer M3 x 10, {j + 1}", Pos(bx_, by_, ez0 + 3) * cp.bush(6, 3, 10), "brass", kind="fastener", bom=bn(12))], tags=("motor",))
    for j, (w, l, h) in enumerate(((20, 12, 10), (20, 12, 10), (30, 15, 12), (12, 10, 8))):
        cx0 = ex0 + 40 + j * 45
        con = break_edges(box(cx0, cx0 + w, ey0 + 12, ey0 + 12 + l, ez0 + 14.6, ez0 + 14.6 + h), 0.5)
        B.add(f"Board connector {j + 1} (screw terminal)", con, "safety_yellow" if j < 3 else "matte_black", kind="bought", bom=bn(12), tags=("motor",))
    for j in range(3):
        gx = ex0 + 60 + j * 60
        gland = Plane(origin=(gx, ey0, ez0 + 30), x_dir=(1, 0, 0), z_dir=(0, -1, 0)) * (cp._hex(19, 6) + Pos(0, 0, 6) * Cylinder(7, 8))
        B.add(f"Cable gland M16 {j + 1}", gland, "matte_black", kind="bought", bom=bn(12), tags=("motor",))

    # ------------------------------------------------------------------ 14 to 16 shaking table
    P_ = P
    TBX0 = P["table_x0"]; TBX1 = TBX0 + P["table_l"]; TBW = P["table_w"]; TZ = P["table_z"]
    tilt = P["table_tilt"]
    rot = lambda s: Pos(0, 0, TZ) * Rot(tilt, 0, 0) * Pos(0, 0, -TZ) * s  # noqa: E731
    deck_board = M._box(TBX0, TBX1, -TBW / 2, TBW / 2, TZ - 18, TZ)
    B.add("Table deck, 18 mm marine plywood", rot(deck_board), "plywood", bom=bn(14), tags=("table",))
    B.add("Table deck facing, 3 mm HDPE", rot(break_edges(M._box(TBX0, TBX1, -TBW / 2, TBW / 2, TZ, TZ + 3), 0.8)), "hdpe_natural", bom=bn(14), tags=("table",))
    for i in range(9):
        y = -TBW / 2 + 60 + i * 38
        rf = break_edges(M._box(TBX0 + 60 + i * 30, TBX1 - 40, y, y + 6, TZ + 3, TZ + 11), 0.8)
        B.add(f"Table riffle {i + 1}, 6 x 8 HDPE strip", rot(rf), "hdpe_natural", bom=bn(14), tags=("table",))
    fbx = M._box(TBX0, TBX0 + 180, TBW / 2 - 90, TBW / 2, TZ + 3, TZ + 73) - M._box(TBX0 + 4, TBX0 + 176, TBW / 2 - 86, TBW / 2 - 4, TZ + 6, TZ + 74)
    B.add("Table feed box, 4 mm HDPE", rot(fbx), "hdpe_natural", bom=bn(14), tags=("table",))
    ls_ = P["pin_slot"]
    slot = M._cyly(TBX0 + 25, TZ - 30, -15, 15, 6) + M._cyly(TBX0 + 25 + ls_, TZ - 30, -15, 15, 6) + M._box(TBX0 + 25, TBX0 + 25 + ls_, -15, 15, TZ - 36, TZ - 24)
    for y0_, nm in ((-14, "front"), (8, "back")):
        ch = M._box(TBX0 + 5, TBX0 + 45, y0_, y0_ + 6, TZ - 40, TZ - 18) - slot
        B.add(f"Pitman cheek, {nm}, 6 mm with the pin slot", rot(break_edges(ch, 0.5)), PAINT, bom=bn(14), tags=("table",))
    B.add("Wash water pipe, 40 mm PVC, drilled", C["wash_pipe"].shape, "hdpe_black", bom=bn(14), tags=("table",))
    # table base (welded) and flexure legs with angle cleats
    fy, fw, ft = P["flex_y"], P["flex_w"], P["flex_t"]
    bx0, bx1 = P["flex_x"][0] - 40, P["flex_x"][1] + 40
    t_mem = [(f"Table base rail, {'front' if y < 0 else 'back'}", (bx0, bx1, y - S / 2, y + S / 2, 0, S), ("table",)) for y in (-fy, fy)]
    t_mem += [(f"Table base cross tube, {'head' if x == bx0 else 'far'} end", (x, x + S, -fy + S / 2, fy - S / 2, 0, S), ("table",)) for x in (bx0, bx1 - S)]
    for nm, b, tg in t_mem:
        B.add(nm + ", 25 x 25 x 1.5 tube", tube_box(*b), PAINT, bom=bn(15), tags=tg)
    for nm, beads, tg in joint_welds(t_mem, t_mem):
        B.welds(beads, nm.lower(), bom=bn(15), tags=("table",))
    under = rot(M._box(TBX0 - 200, TBX1 + 200, -TBW, TBW, -500, TZ - 18))
    for x in P["flex_x"]:
        for y in (-fy, fy):
            leg = M._box(x - ft / 2, x + ft / 2, y - fw / 2, y + fw / 2, S, TZ + 50) & under
            B.add(f"Flexure leg at x {x:.0f}, {'front' if y < 0 else 'back'}, 18 mm marine plywood", break_edges(leg, 1.5), "plywood", bom=bn(15), tags=("table",))
            cb = M._box(x + ft / 2, x + ft / 2 + 40, y - fw / 2, y + fw / 2, S, S + 4) + M._box(x + ft / 2, x + ft / 2 + 4, y - fw / 2, y + fw / 2, S + 4, S + 40)
            B.add(f"Leg cleat, base, x {x:.0f} {'front' if y < 0 else 'back'}, 40 x 40 x 4 angle", cb, PAINT, bom=bn(15), tags=("table",))
            ct = M._box(x + ft / 2, x + ft / 2 + 40, y - fw / 2, y + fw / 2, TZ - 22, TZ - 18) + M._box(x + ft / 2, x + ft / 2 + 4, y - fw / 2, y + fw / 2, TZ - 58, TZ - 22)
            B.add(f"Leg cleat, deck, x {x:.0f} {'front' if y < 0 else 'back'}, 40 x 40 x 4 angle", rot(ct), PAINT, bom=bn(15), tags=("table",))
            ry0, ry1 = y - S / 2, y + S / 2
            xo = min(x + ft / 2 + 40, bx1)                    # outer side: to the end of the rail
            xi = min(x + ft / 2 + 40, bx1 - S - 3)            # inner side: stops short of the far cross tube
            sgo = -1 if y < 0 else 1
            B.welds([bead((x + ft / 2, ry0 if y < 0 else ry1, S), (1, 0, 0), xo - x - ft / 2, (0, sgo, 0), (0, 0, -1), 3.0),
                     bead((x + ft / 2, ry1 if y < 0 else ry0, S), (1, 0, 0), xi - x - ft / 2, (0, -sgo, 0), (0, 0, -1), 3.0)],
                    f"base cleat at x {x:.0f} {'front' if y < 0 else 'back'} to base rail", bom=bn(15), tags=("table",))
            for dy in (-20.0, 20.0):
                B.fasteners(bolt(8, ft + 4, (x - ft / 2, y + dy, S + 22), (1, 0, 0), H, bom=bn(17), label=", leg to base cleat"), tags=("table",))
                bl = bolt(8, ft + 4, (x - ft / 2, y + dy, TZ - 40), (1, 0, 0), H, bom=bn(17), label=", leg to deck cleat")
                for q in bl:
                    q["shape"] = rot(q["shape"])
                H.items[-1] = (rot(H.items[-1][0]), H.items[-1][1])
                B.fasteners(bl, tags=("table",))
                cs = screw(6, 16, (x + ft / 2 + 30, y + dy, TZ - 22), (0, 0, 1), H, bom=bn(17), kind="coach", label=", deck cleat to deck")
                for q in cs:
                    q["shape"] = rot(q["shape"])
                H.items[-1] = (rot(H.items[-1][0]), H.items[-1][1])
                B.fasteners(cs, tags=("table",))
    # head: plate bolted to the frame end, shelf, gussets (welded), two pillow blocks, head shaft, eccentric, pulley
    HX, HZ = P["head_x"], P["head_z"]; ph = P["pillow_h"]; hz = P["head_member_z"]
    sh_top = HZ - ph
    hplate = M._box(FX1, FX1 + PT, -310, 65, hz - 5, RZ + 5)
    shelf = M._box(FX1 + PT, HX + 80, -310, 65, sh_top - PT, sh_top) - M._box(HX - 60, HX + 70, -250, 0, sh_top - PT - 1, sh_top + 1) \
        - M._box(HX - 60, HX + 70, -250, 30, sh_top - PT - 1, sh_top + 1)
    B.add("Table head plate, 6 mm", break_edges(hplate, 0.8), PAINT, bom=bn(15), tags=("table",))
    B.add("Table head shelf, 6 mm", shelf, PAINT, bom=bn(15), tags=("table",))
    for y in (-200, 59):
        g = M._prism([(FX1 + PT, sh_top - PT), (FX1 + PT + 90, sh_top - PT), (FX1 + PT, sh_top - PT - 90)], "y", y - 3, y + 3)
        B.add(f"Table head gusset at y {y}", g, PAINT, bom=bn(15), tags=("table",))
    hb = []
    for ya, yb3 in ((-310, -203), (-197, 56), (62, 65)):
        hb.append(bead((FX1 + PT, ya, sh_top - PT), (0, 1, 0), yb3 - ya, (0, 0, -1), (1, 0, 0), 3.0))
    hb.append(bead((FX1 + PT, -310, sh_top), (0, 1, 0), 375, (0, 0, 1), (1, 0, 0), 3.0))
    B.welds(hb, "table head shelf to plate", bom=bn(15), tags=("table",))
    for y in (-240.0, -20.0):
        for z in (hz + S / 2, RZ - S / 2):
            B.fasteners(bolt(8, PT + S, (FX1 + PT, y, z), (-1, 0, 0), H, bom=bn(17), label=", head plate to frame"), tags=("table",))
    head_bore = M._cyly(HX, HZ, -2000, 2000, 10)
    for i, s in enumerate(sorted(C["head_bearings"].shape.solids(), key=lambda q: q.center().Y)):
        B.add(f"Head shaft pillow block {i + 1}, UCP204 class", s - head_bore, "cast_aluminium", kind="bought", bom=bn(15), tags=("table",))
    for y in (-290.0, 40.0):
        for xs in (-47.5, 47.5):
            B.fasteners(bolt(10, 13 + PT, (HX + xs, y, sh_top + 13), (0, 0, -1), H, bom=bn(17), label=", head pillow block"), tags=("table",))
    e = P["eccentric"]
    B.add("Head shaft, 20 mm bright steel", Pos(HX, P["belt_y"] - 15, HZ) * Rot(-90, 0, 0) * cp.round_bar(20, 64 - (P["belt_y"] - 15)), "mild_steel", bom=bn(15), tags=("table",))
    hp = Plane(origin=(HX, P["belt_y"], HZ), x_dir=(1, 0, 0), z_dir=(0, 1, 0)) * vpulley(P["head_pulley_d"], 20, 20, spokes=5)
    B.add("Head pulley, 125 mm A-section", hp, "cast_aluminium", kind="bought", bom=bn(15), tags=("table",))
    B.add("Eccentric disc, 60 mm, 7.5 mm throw", break_edges(M._cyly(HX + e, HZ, -12, 12, 30), 1.0) - head_bore, "mild_steel", bom=bn(15), tags=("table",))
    # bump stop bracket (welded), buffer, stud and lock nuts, striker with coach screws
    sy, szs, bd, bl_ = P["stop_y"], P["stop_z"], P["buffer_d"], P["buffer_l"]
    xs_ = TBX0 + PT; xb_ = xs_ + bl_; xn = xb_ + 6.5; xu = xn + PT
    sfoot = (FX1 - S, FX1 - S + 40, sy - 33, sy + 33, RZ, RZ + PT)
    sarm = (FX1 - S, xu, sy - S / 2, sy + S / 2, RZ + PT, RZ + PT + S)
    supr = M._box(xn, xu, sy - 20, sy + 20, RZ + PT + S, szs + 30) - M._cylx(sy, szs, xn - 1, xu + 1, 4.5)
    B.add("Stop bracket foot, 6 mm", break_edges(box(*sfoot), 0.8), PAINT, bom=bn(21), tags=("table",))
    B.add("Stop bracket arm, 25 x 25 x 1.5 tube", tube_box(*sarm), PAINT, bom=bn(21), tags=("table",))
    B.add("Stop bracket upright, 6 mm", break_edges(supr, 0.8), PAINT, bom=bn(21), tags=("table",))
    B.welds([bead((FX1 - S, sy - S / 2, RZ + PT), (1, 0, 0), 40, (0, -1, 0), (0, 0, 1), 3.0),
             bead((FX1 - S, sy + S / 2, RZ + PT), (1, 0, 0), 40, (0, 1, 0), (0, 0, 1), 3.0),
             bead((xn, sy - S / 2, RZ + PT + S), (0, 1, 0), S, (-1, 0, 0), (0, 0, 1), 3.0)], "stop bracket", bom=bn(21), tags=("table",))
    for ys in (sy - 25.0, sy + 25.0):
        B.fasteners(bolt(8, PT + S, (FX1 - S / 2, ys, RZ + PT), (0, 0, -1), H, bom=bn(22), label=", stop foot"), tags=("table",))
    stud = M._cylx(sy, szs, xs_ + bl_ - 10, xu + 22, 4)
    B.add("Rubber buffer 40 x 30, 55 Shore A, M8 insert", M._cylx(sy, szs, xs_, xb_, bd / 2) - stud, "epdm", kind="bought", bom=bn(22), tags=("table",))
    B.add("M8 x 45 threaded rod, stainless (buffer stud)", stud, "stainless", kind="fastener", bom=bn(22), tags=("table",))
    for nm, xa in (("inner", xb_), ("outer", xu)):
        nut = Plane(origin=(xa, sy, szs), x_dir=(0, 1, 0), z_dir=(1, 0, 0)) * (cp._hex(13, 6.5) - Pos(0, 0, 3.25) * Cylinder(4, 6.5))
        B.add(f"M8 lock nut, {nm}, stainless", nut, "stainless", kind="fastener", bom=bn(22), tags=("table",))
    zb = TZ - 18
    stk = M._box(TBX0, TBX0 + 40, sy - 20, sy + 20, zb - PT, zb) + M._box(TBX0, TBX0 + PT, sy - 20, sy + 20, zb - 70, zb - PT)
    B.add("Striker angle, 6 mm, under the deck", rot(stk), PAINT, bom=bn(21), tags=("table",))
    for dy in (-10.0, 10.0):
        cs = screw(6, 20, (TBX0 + 26, sy + dy, zb - PT), (0, 0, 1), H, bom=bn(22), kind="coach", label=", striker to deck")
        for q in cs:
            q["shape"] = rot(q["shape"])
        H.items[-1] = (rot(H.items[-1][0]), H.items[-1][1])
        B.fasteners(cs, tags=("table",))
    # pitman: eye on the eccentric, bar, boss with the pin bore; clevis pin and split pin in the deck cheeks
    tr = math.radians(tilt)
    pin = (TBX0 + 25, -(-30) * math.sin(tr), TZ - 30 * math.cos(tr))
    eye = M._cyly(HX + e, HZ, -10, 10, 42) - M._cyly(HX + e, HZ, -11, 11, 30.5)
    boss = rot(M._cyly(TBX0 + 25, TZ - 30, -6, 6, 11))
    pit = eye + M._bar((HX + e + 36, 0, HZ + 20), pin, 22, 12, normal=(0, 1, 0)) + boss - rot(M._cyly(TBX0 + 25, TZ - 30, -7, 7, 6))
    B.add("Pitman arm with bronze-bushed eye", pit, "mild_steel", bom=bn(15), tags=("table",))
    cpin = Plane(origin=(TBX0 + 25, -14, TZ - 30), x_dir=(1, 0, 0), z_dir=(0, -1, 0)) * cp.clevis_pin(12, 28)
    B.add("Clevis pin 12 x 28 (ISO 2341), pitman to deck", rot(cpin), "zinc_plated", kind="fastener", bom=bn(15), tags=("table",))
    B.add("Split pin 3.2 (ISO 1234), pitman pin", rot(Pos(TBX0 + 25, 26, TZ - 30) * cp.split_pin(12)), "zinc_plated", kind="fastener", bom=bn(15), tags=("table",))
    B.add("Table belt tensioner (idler on a latched arm)", C["tensioner"].shape, "galvanised", bom=bn(15), tags=("table",))
    cA, cB = (JX, DZ, P["take_off_d"] / 2), (HX, HZ, P["head_pulley_d"] / 2)
    tbelt = M._band(cA, cB, "y", P["belt_y"] - 6.5, P["belt_y"] + 6.5, -11.5, 0.0)
    B.add("Table belt, A-section V-belt", tbelt, "rubber_belt", kind="bought", bom=bn(10), tags=("table",))
    B.add("Table belt guard, 1.2 mm perforated sheet", C["table_guard"].shape, "galvanised", bom=bn(11), tags=("table",))
    lx0, lx1 = TBX0 + 150, TBX1 - 40
    llegs = [(x, x + 25, -262.5, -237.5, 0, 640) for x in (lx0 + 20, lx1 - 45)]
    trough = C["launder"].shape
    for lb in llegs:
        trough = trough - box(*lb)
    B.add("Tailings launder trough, 1.5 mm sheet", max(trough.solids(), key=lambda q: q.volume), "galvanised", bom=bn(16), tags=("table",))
    kx0, kx1 = TBX1 - 25, TBX1 + 95
    klegs = [(x, x + 25, y, y + 25, 0, 640) for x in (kx0 + 10, kx1 - 35) for y in (-215, 20)]
    kbox = C["conc_box"].shape
    for lb in klegs:
        kbox = kbox - box(*lb)
    B.add("Concentrate box, 1.5 mm sheet, with hinge strip", max(kbox.solids(), key=lambda q: q.volume), "galvanised", bom=bn(16), tags=("table",))
    for i, lb in enumerate(llegs + klegs):
        nm = f"Launder leg {i + 1}" if i < 2 else f"Concentrate box leg {i - 1}"
        B.add(nm + ", 25 x 25 x 1.5 tube", tube_box(*lb), PAINT, bom=bn(16), tags=("table",))
        B.welds([bead((lb[0], lb[2], 640), (0, 1, 0), 25, (-1, 0, 0), (0, 0, -1), 3.0),
                 bead((lb[1], lb[2], 640), (0, 1, 0), 25, (1, 0, 0), (0, 0, -1), 3.0)], nm.lower() + " to its trough or box", bom=bn(16), tags=("table",))
    B.add("Concentrate box lid, 2 mm sheet", break_edges(box(kx0, kx1 - 3, -230, 60, 760, 762), 0.5), "galvanised", bom=bn(16), tags=("table",))
    cxh = (kx0 + kx1) / 2
    staple = box(cxh - 15, cxh + 15, -233, -230, 715, 745) + box(cxh - 4, cxh + 4, -245, -233, 726, 734)
    strap = box(cxh - 18, cxh + 18, -241, -237, 720, 762) + box(cxh - 18, cxh + 18, -241, -215, 762, 765) - box(cxh - 6, cxh + 6, -242, -236, 724, 736)
    B.add("Concentrate box hasp staple", staple, "zinc_plated", kind="bought", bom=bn(16), tags=("table",))
    B.add("Concentrate box hasp strap", strap, "zinc_plated", kind="bought", bom=bn(16), tags=("table",))

    # ------------------------------------------------------------------ 23 flush container with a padlock hasp (loose)
    B.add("Flush container, 10 L HDPE pail and lid", C["flush_box"].shape, "hdpe_natural", kind="bought", bom=bn(23), tags=("centrifuge",))
    B.add("Flush container hasp staple, riveted", C["flush_staple"].shape, "zinc_plated", kind="bought", bom=bn(23), tags=("centrifuge",))
    B.add("Flush container hasp strap, riveted", C["flush_hasp"].shape, "zinc_plated", kind="bought", bom=bn(23), tags=("centrifuge",))

    # ------------------------------------------------------------------ frame welds (every tube end on a face)
    for nm, beads, tags in joint_welds(members, receivers):
        if nm.startswith("Tank post to"):
            continue        # the post's foot and head are welded through their gussets (not drawn as beads)
        B.welds(beads, nm.lower(), bom=bn(1), tags=tags)

    if keep is not None:
        B.parts = [q for q in B.parts if keep(q["tags"])]
        H.items = [h for h in H.items if len(h) < 3 or keep(h[2])]
    cut_holes(B.parts, H)
    return B.parts
