"""GravitySort parametric model (build123d), TRL 3, constructable design (GVS-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL into cad/step and cad/stl, prints the
                                       main envelopes and the constructability checks
    python cad/src/model.py --check    prints the constructability checks only

Every component is modelled as it is made or bought: tube members butt between the members they
weld to, plates carry the bearings, the hopper drops into a ring, the outrigger bolts to the frame
end, and so on (GVS-DDR-003 lists each change from the concept). Tube is modelled solid; its
mass is taken from the cut lengths in frame_members(). Still not fabrication detail: no
tolerances, weld sizes or thread callouts. PRELIMINARY, NOT FOR FABRICATION.

Axes: X along the machine (pedal station at -X, shaking table at +X), Y front (-Y) to back (+Y),
Z up from the ground. Units mm. The centrifuge axis is at (bowl_x, 0).
docs/04-calcs/sizing.py (GVS-CAL-001) imports PARAMS, riffle_rings(), frame_members(),
outrigger_members(), stand_members() and plate_list() so the calculation note and the geometry
use the same numbers. cad/src/build_plan_media.py draws the build plan from build_components().
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Base frame (item 1): 25 x 25 x 1.5 mm mild steel square tube (GVS-DDR-002)
    "frame_x0": -450.0, "frame_x1": 450.0, "frame_y": 300.0, "rail_z": 700.0, "tube": 25.0, "tube_wall": 1.5,
    "low_rail_z": 255.0,          # bottom of the lower side rails (the members sit on top of them)
    "mid_z": 445.0,               # bottom of the tub members, hung from the top rails by drop posts
    "end_low_z": 90.0,            # bottom of the low end member at the pedal end
    "head_member_z": 600.0,       # bottom of the head member at the table end
    "plate_t": 6.0,               # bearing plates, cradle, brackets
    # Centrifuge axis and bowl (item 3): cast PU liner on a GFRP shell
    "bowl_x": 100.0,
    "bowl_lip_d": 220.0, "bowl_base_d": 130.0, "bowl_depth": 180.0,   # inner (liner) surface
    "bowl_z0": 560.0,                                                  # inside floor of the bowl
    "liner_t": 8.0, "shell_t": 4.0,
    "rings": 4, "ring_first": 50.0, "ring_pitch": 38.0,                # ring height above the floor, pitch
    "ring_t": 6.0, "ring_depth": 12.0,                                 # axial thickness, radial depth of groove
    "fluid_hole_d": 1.0,
    # Fluidization jacket (item 4): GFRP, rotates with the bowl; rotary union at the spindle foot
    "jacket_gap": 12.0, "jacket_t": 4.0,
    "union_z": (114.0, 164.0), "union_d": 56.0,
    "hub_flange_d": 80.0, "hub_flange_t": 12.0, "hub_boss_d": 44.0, "hub_boss_h": 15.0, "hub_pcd": 60.0,
    # Spindle and bearings (item 5): 25 x 2 mm stainless tube (water passes up its bore)
    "spindle_d": 25.0, "spindle_wall": 2.0,
    "bearing_z": (235.0, 400.0), "bearing_d": 90.0, "bearing_h": 40.0, "bearing_flange": 95.0,
    "driven_pulley_d": 100.0, "pulley_z": 180.0,
    # Bowl brake (item 18): 160 mm bicycle disc rotor and mechanical caliper on the spindle
    "brake_rotor_d": 160.0, "brake_z": 360.0,
    # Splash tub (item 6) and lid guard (item 7)
    "tub_d": 430.0, "tub_z": (470.0, 790.0), "tub_t": 6.0, "lid_t": 10.0, "lid_hole_d": 60.0,
    "standpipe_d": 63.0, "standpipe_z": (445.0, 495.0), "tail_pipe_d": 75.0, "tail_pipe_z": 534.0,
    # Hopper and screen (item 2)
    "hopper_z": (960.0, 1180.0), "hopper_top_d": 340.0, "hopper_bot_d": 140.0, "screen_d": 360.0,
    "feed_pipe_d": 44.0, "feed_pipe_end": 815.0, "hopper_ring_z": 1000.0,
    # Drive (items 8 to 10)
    "pedal_x": -800.0, "bb_z": 438.0, "drive_z": 338.0, "jack_x": -250.0,
    "chainring_t": 48, "freewheel_t": 12, "bevel_ratio": 1.0, "drive_pulley_d": 300.0,
    "take_off_d": 140.0, "head_pulley_d": 125.0,
    "chain_y": 60.0, "belt_y": -330.0, "motor_chain_y": 373.5,
    "pillow_y": (-230.0, 250.0), "pillow_h": 33.0,
    "seat_z": 910.0,
    # Motor option (item 12): reference hub motor on a cradle on the back lower rail
    "motor_x": -85.0, "motor_z": 376.0, "motor_y": (306.0, 366.0), "motor_r": 80.0,
    # Water header tank (item 13)
    "tank_x": -330.0, "tank_y": 180.0, "tank_d": 380.0, "tank_z": (1250.0, 1650.0),
    # Shaking table (items 14 to 16)
    "table_x0": 620.0, "table_l": 1000.0, "table_w": 450.0, "table_z": 820.0, "table_tilt": 3.0,
    "head_x": 560.0, "head_z": 710.0, "eccentric": 7.5,
    "flex_x": (680.0, 1540.0), "flex_y": 135.0, "flex_w": 80.0, "flex_t": 18.0,
    # Table bump stop (items 21 and 22, GVS-DDR-003 A2): rubber buffer on an M8 stud in a bracket bolted on the
    # frame's table-end top rail, striking an angle under the deck's back edge at the end of the forward stroke.
    # The model is drawn at the zero setting (buffer just touching at full forward travel); the working setting
    # turns the stud 3 mm toward the deck. The pitman pin works in a slot with 8 mm of lost motion.
    "stop_y": 205.0, "stop_z": 762.0, "buffer_d": 40.0, "buffer_l": 30.0, "pin_slot": 8.0,
}

STEEL = 7850.0          # kg/m3


@dataclass
class Comp:
    name: str
    shape: object
    color: str
    bom: int
    explode: tuple = (0, 0, 0)


# ------------------------------------------------------------------ primitives
def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _cyl(x, y, z0, z1, r):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _cyly(x, z, y0, y1, r):
    from build123d import Cylinder, Pos, Rot
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def _cylx(y, z, x0, x1, r):
    from build123d import Cylinder, Pos, Rot
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def _cone(x, y, z0, z1, r0, r1):
    from build123d import Cone, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cone(r0, r1, z1 - z0)


def _rod(a, b, r):
    """Round bar or hose from point a to point b."""
    from build123d import Cylinder, Location, Vector, Plane
    a, b = Vector(*a), Vector(*b)
    d = b - a
    pl = Plane(origin=(a + b) / 2, z_dir=d.normalized())
    return pl * Cylinder(r, d.length)


def _bar(a, b, w, t, normal=(0, 1, 0)):
    """Flat bar from a to b (centre line), width w across, thickness t along `normal`."""
    from build123d import Box, Plane, Vector
    a, b = Vector(*a), Vector(*b)
    d = b - a
    n = Vector(*normal)
    x = d.normalized()
    z = n - x * n.dot(x)
    pl = Plane(origin=(a + b) / 2, x_dir=x, z_dir=z.normalized())
    return pl * Box(d.length, w, t)


def _prism(pts, axis, a0, a1):
    """Prism from a 2D polygon. axis 'y': pts are (x, z), extruded from y=a0 to a1; 'z': (x, y); 'x': (y, z)."""
    from build123d import Face, Vector, Wire, extrude
    if axis == "y":
        v = [Vector(p[0], a0, p[1]) for p in pts]; d = (0, 1, 0)
    elif axis == "z":
        v = [Vector(p[0], p[1], a0) for p in pts]; d = (0, 0, 1)
    else:
        v = [Vector(a0, p[0], p[1]) for p in pts]; d = (1, 0, 0)
    return extrude(Face(Wire.make_polygon(v, close=True)), amount=a1 - a0, dir=d)


def _hull_pts(circles, n=72):
    """Convex hull (counter-clockwise) of circles [(cx, cy, r), ...] sampled at n points each."""
    pts = []
    for cx, cy, r in circles:
        for k in range(n):
            t = 2 * math.pi * k / n
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    pts = sorted(set((round(x, 4), round(y, 4)) for x, y in pts))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def _hull(circles, axis, a0, a1):
    return _prism(_hull_pts(circles), axis, a0, a1)


def _band(c1, c2, axis, a0, a1, r_in, r_out):
    """A belt or chain round two pulleys: c = (cx, cy, r). Inner radius r + r_in, outer r + r_out."""
    o = _hull([(c1[0], c1[1], c1[2] + r_out), (c2[0], c2[1], c2[2] + r_out)], axis, a0, a1)
    i = _hull([(c1[0], c1[1], c1[2] + r_in), (c2[0], c2[1], c2[2] + r_in)], axis, a0 - 1, a1 + 1)
    return o - i


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


# ------------------------------------------------------------------ helpers shared with the calculations
def bowl_radius(z, p=PARAMS):
    """Inner (liner surface) radius of the bowl at height z."""
    r0, r1 = p["bowl_base_d"] / 2, p["bowl_lip_d"] / 2
    return r0 + (r1 - r0) * (z - p["bowl_z0"]) / p["bowl_depth"]


def riffle_rings(p=PARAMS):
    """List of (z, wall radius, lip inner radius) for each riffle ring, in mm."""
    out = []
    for i in range(p["rings"]):
        z = p["bowl_z0"] + p["ring_first"] + i * p["ring_pitch"]
        r = bowl_radius(z, p)
        out.append((z, r, r - p["ring_depth"]))
    return out


def derived(p=PARAMS):
    S = p["tube"]
    d = {}
    d["low_top"] = p["low_rail_z"] + S                 # top of the lower side rails
    d["mem_top"] = d["low_top"] + S                    # top of the members that sit on them
    d["mid_top"] = p["mid_z"] + S                      # top of the tub members (the tub floor)
    d["top_bot"] = p["rail_z"] - S                     # underside of the top rails
    d["gbx_members"] = (p["jack_x"] - 47.5, p["jack_x"] + 47.5)     # centres, under the pillow block bolts
    d["sp_members"] = (p["bowl_x"] - 62.5, p["bowl_x"] + 62.5)      # spindle and tub member centres
    t = p["liner_t"] + p["shell_t"]
    d["shell_bot"] = p["bowl_z0"] - t
    d["jacket_in"] = d["shell_bot"] - p["jacket_gap"]  # top face of the jacket floor
    d["jacket_bot"] = d["jacket_in"] - p["jacket_t"]
    d["flange_bot"] = d["jacket_bot"] - p["hub_flange_t"]
    d["boss_bot"] = d["flange_bot"] - p["hub_boss_h"]
    d["chain_r"] = (100.0, 25.0)                       # 48T and 12T pitch radii, 12.7 mm pitch (about)
    d["motor_spr_r"] = (35.0, 42.0)                    # jackshaft and motor sprockets (1.2:1 step-up)
    return d


def frame_members(p=PARAMS):
    """(name, cut length mm) of every tube in the welded base frame."""
    S = p["tube"]; FY = p["frame_y"]
    lx = p["frame_x1"] - p["frame_x0"] - 2 * S          # side rails between the legs
    ly = 2 * FY - 2 * S                                  # cross members between the side rails
    D = derived(p)
    m = [("leg", p["rail_z"])] * 4
    m += [("top side rail", lx)] * 2 + [("lower side rail", lx)] * 2
    m += [("top end rail", ly)] * 2
    m += [("low end member (pedal end)", ly), ("head member (table end)", ly)]
    m += [("gearbox member", 2 * FY)] * 2 + [("spindle member", 2 * FY)] * 2
    m += [("tub member", 2 * FY)] * 2
    m += [("drop post", D["top_bot"] - D["mid_top"])] * 4
    m += [("tank post member", ly)]
    m += [("end post", D["top_bot"] - (p["end_low_z"] + S))]
    m += [("tank post", p["tank_z"][0] - p["rail_z"] - 5)]
    return m


def outrigger_members(p=PARAMS):
    """(name, cut length mm) of the square tube in the pedal outrigger (the seat post is round tube)."""
    PX = p["pedal_x"]
    return [("spine", (p["frame_x0"] - 6) - (PX - 185)), ("seat cross foot", 400.0), ("pedal cross foot", 300.0),
            ("pedal post", p["bb_z"] - 20 - 25), ("top arm", (p["frame_x0"] - 6) - (PX - 160))]


def stand_members(p=PARAMS):
    """(name, cut length mm) of the square tube in the table base."""
    x0, x1 = p["flex_x"][0] - 40, p["flex_x"][1] + 40
    return [("base rail", x1 - x0)] * 2 + [("base cross tube", 2 * p["flex_y"] - p["tube"])] * 2


def plate_list(p=PARAMS):
    """(name, kg) of the steel plate parts (not tube), from their modelled volume or plate size."""
    C = build_components(p)
    vol = lambda *ks: sum(C[k].shape.volume for k in ks) * 1e-9 * STEEL  # noqa: E731
    rr = p["hopper_bot_d"] / 2 + (p["hopper_top_d"] - p["hopper_bot_d"]) / 2 * (p["hopper_ring_z"] - p["hopper_z"][0]) / (p["hopper_z"][1] - p["hopper_z"][0])
    ring = math.pi * ((rr + 20) ** 2 - rr ** 2) * p["plate_t"] * 1e-9 * STEEL + 75 * 25 * p["plate_t"] * 1e-9 * STEEL
    return [("Bearing plates (2)", vol("bearing_plates")), ("Tank cradle and gussets", vol("tank_cradle")),
            ("Outrigger end plates", vol("outrigger_plates")), ("Head plate, shelf and gussets", vol("head")),
            ("Caliper bracket and brake flange", vol("caliper_bracket", "brake_flange")),
            ("Hopper ring and post foot", ring), ("Motor cradle (motor option)", vol("motor_cradle")),
            ("Stop bracket plates", stop_plates_kg(p)), ("Striker angle", vol("striker"))]


def stop_bracket_members(p=PARAMS):
    """(name, cut length mm) of the square tube in the table bump stop bracket (the arm)."""
    return [("stop arm", p["table_x0"] + 2 * p["plate_t"] + p["buffer_l"] + 6.5 - (p["frame_x1"] - p["tube"]))]


def stop_plates_kg(p=PARAMS):
    """Mass (kg) of the two 6 mm plates of the stop bracket: foot 40 x 66 and upright 40 x 61."""
    return (40 * 66 + 40 * 61) * p["plate_t"] * 1e-9 * STEEL


# ------------------------------------------------------------------ the components
def build_components(p=PARAMS):
    """Every component of the constructable design, by key, in build order."""
    from build123d import Pos, Rot
    b, c = _box, _cyl
    D = derived(p)
    S, PT = p["tube"], p["plate_t"]
    FX0, FX1, FY, RZ = p["frame_x0"], p["frame_x1"], p["frame_y"], p["rail_z"]
    LZ, LT, MT, MZ, TB = p["low_rail_z"], D["low_top"], D["mem_top"], p["mid_z"], D["top_bot"]
    CX, CY = p["bowl_x"], 0.0
    JX, DZ, PX, BZ = p["jack_x"], p["drive_z"], p["pedal_x"], p["bb_z"]
    C = {}

    def add(key, name, shape, color, bom, explode=(0, 0, 0)):
        C[key] = Comp(name, shape, color, bom, explode)

    # ---------------------------------------------------------------- 1 base frame (welded)
    legs = [b(x, x + S, y, y + S, 0, RZ) for x in (FX0, FX1 - S) for y in (-FY, FY - S)]
    rails = []
    for y in (-FY, FY - S):
        rails += [b(FX0 + S, FX1 - S, y, y + S, RZ - S, RZ), b(FX0 + S, FX1 - S, y, y + S, LZ, LT)]
    rails += [b(FX0, FX0 + S, -FY + S, FY - S, RZ - S, RZ), b(FX1 - S, FX1, -FY + S, FY - S, RZ - S, RZ)]
    rails += [b(FX0, FX0 + S, -FY + S, FY - S, p["end_low_z"], p["end_low_z"] + S)]
    hz = p["head_member_z"]
    rails += [b(FX1 - S, FX1, -FY + S, FY - S, hz, hz + S)]
    members = []
    for xc in D["gbx_members"] + D["sp_members"]:
        members.append(b(xc - S / 2, xc + S / 2, -FY, FY, LT, MT))          # on top of the lower rails
    for xc in D["sp_members"]:
        members.append(b(xc - S / 2, xc + S / 2, -FY, FY, MZ, MZ + S))      # tub members
        for y in (-FY, FY - S):
            members.append(b(xc - S / 2, xc + S / 2, y, y + S, MZ + S, TB))  # drop posts
    TX, TY = p["tank_x"], p["tank_y"]
    members.append(b(TX - S / 2, TX + S / 2, -FY + S, FY - S, RZ - S, RZ))   # tank post member
    members.append(b(FX0, FX0 + S, -S / 2, S / 2, p["end_low_z"] + S, RZ - S))  # end post
    tk0 = p["tank_z"][0]
    members.append(b(TX - S / 2, TX + S / 2, TY - S / 2, TY + S / 2, RZ, tk0 - 5))   # tank post
    frame = _fuse(legs + rails + members)
    add("frame", "Base frame, welded", frame, "#4B5563", 1, (0, 0, -300))

    # bearing plates, welded under the spindle members and under the tub members
    x0, x1 = D["sp_members"][0] - S / 2, D["sp_members"][1] + S / 2
    hole = lambda z0, z1: c(CX, CY, z0 - 1, z1 + 1, 20)  # noqa: E731
    lp = b(x0, x1, -65, 65, LT - 5, LT) - hole(LT - 5, LT)
    up = b(x0, x1, -65, 65, MZ - 5, MZ) - hole(MZ - 5, MZ)
    add("bearing_plates", "Bearing plates (2), welded", lp + up, "#6B7280", 1)

    # tank cradle: plate on the tank post, two gussets each way
    cr = b(TX - 125, TX + 125, TY - 125, TY + 125, tk0 - 5, tk0)          # 5 mm plate
    g = []
    for s_ in (1, -1):
        yb = TY + s_ * S / 2
        g.append(_prism([(yb, RZ), (yb + s_ * 70, RZ), (yb, RZ + 70)], "x", TX - 3, TX + 3))
        xb = TX + s_ * S / 2
        g.append(_prism([(xb, tk0 - 5), (xb + s_ * 90, tk0 - 5), (xb, tk0 - 95)], "y", TY - 3, TY + 3))
    add("tank_cradle", "Tank cradle and gussets, welded", _fuse([cr] + g), "#6B7280", 1)

    # ---------------------------------------------------------------- 8 pedal outrigger (welded, bolts to the frame end)
    xe = FX0 - 6                                         # face of the end plates
    spine = b(PX - 185, xe, -S / 2, S / 2, 0, S)
    seat_foot = b(PX - 185, PX - 160, -200, 200, 0, S)
    ped_foot = b(PX - S / 2, PX + S / 2, -150, 150, 0, S)
    ped_post = b(PX - S / 2, PX + S / 2, -S / 2, S / 2, S, BZ - 20)
    sx = PX - 172.5
    seat_tube = c(sx, 0, S, 700, 16) - c(sx, 0, 300, 701, 14)
    top_arm = b(sx + 16, xe, -S / 2, S / 2, 600, 600 + S)
    bb_shell = _cyly(PX, BZ, -34, 34, 20) - _cyly(PX, BZ, -35, 35, 17)
    out = _fuse([spine, seat_foot, ped_foot, ped_post, seat_tube, top_arm, bb_shell])
    add("outrigger", "Pedal outrigger, welded", out, "#374151", 8, (-300, 0, 0))
    ep = b(xe, FX0, -40, 40, 0, p["end_low_z"] + S + 10) + b(xe, FX0, -40, 40, 580, 645)
    add("outrigger_plates", "Outrigger end plates", ep, "#374151", 8, (-300, 0, 0))
    seat = c(sx, 0, 650, p["seat_z"], 13.6) + b(sx - 90, sx + 80, -85, 85, p["seat_z"], p["seat_z"] + 50)
    add("seat", "Seat and seat post (bicycle)", seat, "#111827", 8, (0, 0, 250))
    cr_r = D["chain_r"][0]
    crank = _cyly(PX, BZ, -70, 70, 8) + _cyly(PX, BZ, -34, -24, 17) + _cyly(PX, BZ, 24, 34, 17)
    crank += Pos(PX, 60, BZ) * Rot(90, 0, 0) * __import__("build123d").Cylinder(cr_r, 6)
    crank += b(PX - 10, PX + 10, 76, 88, BZ - 170, BZ) + b(PX - 50, PX + 50, 88, 138, BZ - 178, BZ - 164)
    crank += b(PX - 10, PX + 10, -88, -76, BZ, BZ + 170) + b(PX - 50, PX + 50, -138, -88, BZ + 164, BZ + 178)
    add("crankset", "Crankset, 48T chainring and pedals", crank, "#1F2937", 8, (0, -200, 0))

    # ---------------------------------------------------------------- 9 jackshaft, gearbox, sprockets, pulleys
    gx0, gx1 = D["gbx_members"]
    ph = p["pillow_h"]
    pb = []
    for y in p["pillow_y"]:
        pb.append(b(JX - 63.5, JX + 63.5, y - 19, y + 19, MT, MT + 13) + b(JX - 22, JX + 22, y - 15, y + 15, MT + 13, DZ)
                  + _cyly(JX, DZ, y - 15, y + 15, 30))
    add("pillow_blocks", "Jackshaft bearings (2 pillow blocks)", _fuse(pb), "#57534E", 9, (0, 0, 120))
    gbox = b(JX - 50, JX + 50, -40, 40, MT, MT + 70)
    add("gearbox", "Right-angle gearbox, 1:1", gbox, "#78716C", 9, (0, 0, 150))
    ytop = p["motor_chain_y"] + 16.5
    jack = _cyly(JX, DZ, p["belt_y"] - 20, ytop, 10)
    add("jackshaft", "Jackshaft, 20 mm", jack, "#A8A29E", 9, (0, 0, 220))
    fw = _cyly(JX, DZ, p["chain_y"] - 3, p["chain_y"] + 3, D["chain_r"][1])
    mspr = _cyly(JX, DZ, p["motor_chain_y"] - 2, p["motor_chain_y"] + 2, D["motor_spr_r"][0])
    tko = _cyly(JX, DZ, p["belt_y"] - 10, p["belt_y"] + 10, p["take_off_d"] / 2)
    add("jack_wheels", "Freewheel, motor sprocket, table take-off pulley", fw + mspr + tko, "#57534E", 9, (0, 0, 220))
    pz = p["pulley_z"]
    dr = p["drive_pulley_d"] / 2
    dpul = c(JX, 0, pz, pz + 40, dr) + c(JX, 0, pz + 40, MT, 12)
    add("drive_pulley", "Gearbox output shaft and 300 mm drive pulley", dpul, "#57534E", 9, (0, 0, -150))
    chain = _band((PX, BZ, cr_r), (JX, DZ, D["chain_r"][1]), "y", p["chain_y"] - 4, p["chain_y"] + 4, -3, 5)
    add("pedal_chain", "Pedal chain", chain, "#111827", 9, (0, -120, 0))

    # ---------------------------------------------------------------- 5 spindle, bearings, driven pulley, union
    sr = p["spindle_d"] / 2
    uz0, uz1 = p["union_z"]
    sp = c(CX, CY, uz1, D["jacket_in"], sr) - c(CX, CY, uz1 - 1, D["jacket_in"] + 1, sr - p["spindle_wall"])
    add("spindle", "Spindle, 25 x 2 mm stainless tube", sp, "#D6D3D1", 5, (0, 0, 450))
    bf, bh = p["bearing_flange"], p["bearing_h"]
    brg = []
    for z0_, top in ((p["bearing_z"][0], LT - 5), (p["bearing_z"][1], MZ - 5)):
        brg.append(b(CX - bf / 2, CX + bf / 2, -bf / 2, bf / 2, top - 14, top) + c(CX, CY, z0_, top - 14, 32)
                   - c(CX, CY, z0_ - 1, top + 1, sr))
    add("bearings", "Spindle bearings (2 flanged units)", _fuse(brg), "#57534E", 5, (0, 0, -120))
    dp = c(CX, CY, pz, pz + 40, p["driven_pulley_d"] / 2) - c(CX, CY, pz - 1, pz + 41, sr)
    add("driven_pulley", "100 mm driven pulley on a taper bush", dp, "#57534E", 5, (0, 0, -120))
    un = c(CX, CY, uz0, uz1, p["union_d"] / 2)
    add("union", "Rotary union, 1/2 in", un, "#B45309", 4, (0, 0, -150))

    # ---------------------------------------------------------------- 18 brake
    bz = p["brake_z"]; br = p["brake_rotor_d"] / 2
    flange = c(CX, CY, bz - 23, bz - 3, 20) + c(CX, CY, bz - 3, bz, 28) - c(CX, CY, bz - 24, bz + 1, sr)
    add("brake_flange", "Brake flange on a shaft collar", flange, "#9CA3AF", 18)
    rotor = c(CX, CY, bz, bz + 3, br) - c(CX, CY, bz - 1, bz + 4, 22)
    add("rotor", "160 mm brake disc", rotor, "#DC2626", 18, (0, 0, 100))
    cal = b(CX + 50, CX + 85, -30, 30, bz - 15, bz + 20) - b(CX + 49, CX + 82, -31, 31, bz - 3, bz + 6)
    add("caliper", "Mechanical disc caliper", cal, "#991B1B", 18, (120, 0, 0))
    xb = D["sp_members"][1]
    brk = b(xb - S / 2, CX + 91, -30, 30, MT, MT + PT) + b(CX + 85, CX + 91, -30, 30, MT + PT, bz + 20)
    add("caliper_bracket", "Caliper bracket", brk, "#6B7280", 18, (120, 0, 0))

    # ---------------------------------------------------------------- 10/11 belt, guards
    bowl_belt = _band((JX, 0, dr), (CX, 0, p["driven_pulley_d"] / 2), "z", pz + 12, pz + 28, -9, 0)
    add("bowl_belt", "Bowl belt (A-section link V-belt)", bowl_belt, "#111827", 10, (0, 0, -100))
    gz0, gz1 = pz - 10, pz + 50                          # guard box 170 to 230
    gx_0, gx_1 = JX - dr - 8, CX + p["driven_pulley_d"] / 2 + 8
    gy = dr + 8
    guard = b(gx_0, gx_1, -gy, gy, gz0, gz1) - b(gx_0 + 2, gx_1 - 2, -gy + 2, gy - 2, gz0 + 2, gz1 - 2)
    guard -= c(JX, 0, gz1 - 3, gz1 + 1, 20) + c(CX, 0, gz1 - 3, gz1 + 1, 20) + c(CX, 0, gz0 - 1, gz0 + 3, 16)
    straps = [b(xc - 12.5, xc + 12.5, y - 1.5, y + 1.5, gz1, LT) for xc in (D["gbx_members"][0], D["sp_members"][0]) for y in (-140, 140)]
    add("belt_guard", "Bowl belt guard and hangers", guard + _fuse(straps), "#CA8A04", 11, (0, 0, -200))
    sensor = b(CX - 8, CX + 8, -76, -60, gz1 - 18, gz1 - 2)
    add("sensor", "Speed sensor (bicycle computer)", sensor, "#7C3AED", 19)
    ccase_o = _hull([(PX, BZ, cr_r + 14), (JX, DZ, D["chain_r"][1] + 14)], "y", 44, 74)
    ccase_i = _hull([(PX, BZ, cr_r + 12), (JX, DZ, D["chain_r"][1] + 12)], "y", 46, 72)
    xm = D["gbx_members"][0]
    ccase_o -= b(xm - 40, xm + 30, 0, 100, 0, MT)                        # flat bottom where it sits on the gearbox member
    ccase_i -= b(xm - 42, xm + 32, 0, 100, 0, MT + 2)
    ccase = ccase_o - ccase_i - _cyly(PX, BZ, 40, 80, 14) - _cyly(JX, DZ, 40, 80, 14)
    ccase += b(PX - S / 2, PX + S / 2, S / 2, 44, BZ - 105, BZ - 80)        # tab to the pedal post
    add("chain_case", "Pedal chain case", ccase, "#CA8A04", 11, (0, -150, 0))

    # ---------------------------------------------------------------- 6 splash tub, standpipe, tailings pipe
    TR = p["tub_d"] / 2; tz0, tz1 = p["tub_z"]; tt = p["tub_t"]
    ty = p["tail_pipe_z"]; tr_ = p["tail_pipe_d"] / 2
    tub = c(CX, CY, tz0, tz1, TR) - c(CX, CY, tz0 + tt, tz1 + 1, TR - tt)
    tub -= c(CX, CY, tz0 - 1, tz0 + tt + 1, 38)
    tub -= _cyly(CX, ty, 0, TR + 10, 49)
    add("tub", "Splash tub, cut HDPE drum", tub, "#60A5FA", 6, (0, 0, 380))
    sz0, sz1 = p["standpipe_z"]
    spipe = c(CX, CY, sz0, sz1, p["standpipe_d"] / 2) - c(CX, CY, sz0 - 1, sz1 + 1, p["standpipe_d"] / 2 - 3)
    ri_ = p["standpipe_d"] / 2
    grom1 = (c(CX, CY, tz0 - 2, tz0 + tt + 2, 38) + c(CX, CY, tz0 - 2, tz0, 44) + c(CX, CY, tz0 + tt, tz0 + tt + 2, 44)) \
        - c(CX, CY, tz0 - 3, tz0 + tt + 3, ri_)
    add("standpipe", "Standpipe and floor grommet", spipe + grom1, "#1D4ED8", 6, (0, 0, 300))
    ywall = math.sqrt(TR ** 2 - 0) - tt
    tpipe = _cyly(CX, ty, 200, 440, tr_) - _cyly(CX, ty, 199, 441, tr_ - 3)
    yi = math.sqrt((TR - tt) ** 2 - 55 ** 2)            # inner wall face at the lip edge
    grom2 = _cyly(CX, ty, yi, TR, 49) + _cyly(CX, ty, yi - 3, yi, 55) + _cyly(CX, ty, TR, TR + 3, 55)
    grom2 -= _cyly(CX, ty, yi - 4, TR + 4, tr_)
    add("tail_pipe", "Tailings pipe and wall grommet", tpipe + grom2, "#1D4ED8", 6, (0, 250, 0))
    tbolts = [c(xc, y, tz0 - S - 6, tz0 + tt + 6, 4) for xc in D["sp_members"] for y in (-150, 150)]
    add("tub_bolts", "Tub bolts (4 x M8)", _fuse(tbolts), "#111827", 17)
    C["tub"].shape = C["tub"].shape - _fuse(tbolts)

    # ---------------------------------------------------------------- 3 bowl: GFRP shell and cast PU liner
    z0 = p["bowl_z0"]; z1 = z0 + p["bowl_depth"]
    r0, r1 = p["bowl_base_d"] / 2, p["bowl_lip_d"] / 2
    lt, st = p["liner_t"], p["shell_t"]
    void = _cone(CX, CY, z0, z1 + 1, r0, r1 + (r1 - r0) / p["bowl_depth"])
    liner_out = _cone(CX, CY, z0 - lt, z1, r0 + lt, r1 + lt)
    liner = liner_out - void
    for z, r, ri in riffle_rings(p):
        liner += c(CX, CY, z, z + p["ring_t"], r + 2) - c(CX, CY, z - 1, z + p["ring_t"] + 1, ri)
    nuts = [c(CX + 30 * math.cos(a), 30 * math.sin(a), z0 - lt, z0 - lt + 5, 5) for a in (math.pi / 4 * k for k in (1, 3, 5, 7))]
    add("liner", "Bowl liner, cast polyurethane", liner, "#D97706", 3, (0, 0, 520))
    shell = _cone(CX, CY, z0 - lt - st, z1, r0 + lt + st, r1 + lt + st) - liner_out
    add("shell", "Bowl shell, GFRP", shell, "#0F766E", 3, (0, 0, 420))

    # ---------------------------------------------------------------- 4 fluidization jacket and hub
    g, jt = p["jacket_gap"], p["jacket_t"]
    jz0 = D["jacket_in"]; jz1 = z1 - 30
    ro = lambda z: bowl_radius(z, p) + lt + st          # noqa: E731  shell outer radius
    j_in = _cone(CX, CY, jz0, jz1, ro(D["shell_bot"]) + g, ro(jz1) + g)
    j_out = _cone(CX, CY, jz0 - jt, jz1, ro(D["shell_bot"]) + g + jt, ro(jz1) + g + jt)
    jacket = j_out - j_in
    ring = c(CX, CY, jz1 - 4, jz1, ro(jz1) + g + 0.5) - _cone(CX, CY, z0 - lt - st, z1, r0 + lt + st, r1 + lt + st)
    jacket = jacket + ring - c(CX, CY, jz0 - jt - 1, jz0 + 1, sr)
    add("jacket", "Fluidization jacket, GFRP", jacket, "#5EEAD4", 4, (0, 0, 320))
    fb = D["flange_bot"]
    hub = c(CX, CY, fb, D["jacket_bot"], p["hub_flange_d"] / 2) + c(CX, CY, D["boss_bot"], fb, p["hub_boss_d"] / 2)
    hub -= c(CX, CY, D["boss_bot"] - 1, D["jacket_bot"] + 1, sr)
    add("hub", "Shaft flange hub, 25 mm bore", hub, "#57534E", 4, (0, 0, 220))
    bolts = []
    for a in (math.pi / 4 * k for k in (1, 3, 5, 7)):
        x, y = CX + 30 * math.cos(a), 30 * math.sin(a)
        bolts.append(c(x, y, fb - 4, z0 - lt + 5, 3) + c(x, y, fb - 4, fb, 5))
        bolts.append(c(x, y, jz0, D["shell_bot"], 6) - c(x, y, jz0 - 1, D["shell_bot"] + 1, 3.2))
    bolts += nuts
    holes = _fuse([c(CX + 30 * math.cos(a), 30 * math.sin(a), fb - 5, z0 - lt + 5, 3) for a in (math.pi / 4 * k for k in (1, 3, 5, 7))])
    for k in ("hub", "jacket", "shell"):
        C[k].shape = C[k].shape - holes
    C["liner"].shape = C["liner"].shape - _fuse(nuts) - holes
    add("bowl_bolts", "Bowl bolts, spacers and cast-in nuts", _fuse(bolts), "#111827", 17)

    # ---------------------------------------------------------------- 7 lid guard and clamps
    lid = c(CX, CY, tz1, tz1 + p["lid_t"], TR + 8) - c(CX, CY, tz1 - 1, tz1 + p["lid_t"] + 1, p["lid_hole_d"] / 2)
    add("lid", "Lid guard, 10 mm HDPE", lid, "#1F2937", 7, (0, 0, 350))
    cl = []
    for ang in (-45.0, -135.0):
        a = math.radians(ang)
        body = b(TR, TR + 22, -12, 12, tz1 - 45, tz1 - 5) + b(TR - 10, TR + 22, -12, 12, tz1 + p["lid_t"], tz1 + p["lid_t"] + 6) \
            + b(TR + 12, TR + 22, -12, 12, tz1 - 5, tz1 + p["lid_t"])
        cl.append(Pos(CX, CY, 0) * Rot(0, 0, ang) * body)
    add("clamps", "Over-centre lid clamps (2), one with the interlock pin", _fuse(cl), "#0F766E", 7, (0, -150, 0))

    # ---------------------------------------------------------------- 2 hopper, screen, support
    hz0, hz1 = p["hopper_z"]; hr0, hr1 = p["hopper_bot_d"] / 2, p["hopper_top_d"] / 2
    fr = p["feed_pipe_d"] / 2
    hop = _cone(CX, CY, hz0, hz1, hr0, hr1) - _cone(CX, CY, hz0 + 2, hz1 + 0.01, hr0 - 2, hr1 - 2 + 2 * (hr1 - hr0) / (hz1 - hz0) * 0.01)
    hop += c(CX, CY, p["feed_pipe_end"], hz0, fr)
    hop -= c(CX, CY, p["feed_pipe_end"] - 1, hz0 + 3, fr - 6)
    add("hopper", "Feed hopper and feed pipe", hop, "#D97706", 2, (0, 0, 420))
    scr = c(CX, CY, hz1, hz1 + 6, p["screen_d"] / 2) - c(CX, CY, hz1 - 1, hz1 + 7, p["screen_d"] / 2 - 10)
    scr += c(CX, CY, hz1 + 2, hz1 + 3, p["screen_d"] / 2 - 9)
    add("screen", "2 mm screen in its frame", scr, "#92400E", 2, (0, 0, 520))
    rz = p["hopper_ring_z"]
    rr = hr0 + (hr1 - hr0) * (rz - hz0) / (hz1 - hz0)
    post = b(CX - 37.5, CX + 37.5, -FY, -FY + S, RZ, RZ + PT) + b(CX - S / 2, CX + S / 2, -FY, -FY + S, RZ + PT, rz)
    post += b(CX - S / 2, CX + S / 2, -FY + S, -rr - 12, rz - S, rz)
    post += c(CX, CY, rz - PT, rz, rr + 20) - c(CX, CY, rz - PT - 1, rz + 1, rr)
    add("hopper_post", "Hopper support: post, arm and ring", post, "#6B7280", 2, (0, -250, 0))

    # ---------------------------------------------------------------- 13 water: tank, valve, rotameter, hose
    tank = c(TX, TY, tk0, p["tank_z"][1], p["tank_d"] / 2)
    add("tank", "60 L header tank", tank, "#38BDF8", 13, (0, 0, 300))
    yv = TY + p["tank_d"] / 2                            # valve on the back of the drum, near its bottom
    valve = b(TX - 15, TX + 15, yv, yv + 30, tk0 + 15, tk0 + 45)
    yb = FY + 5                                          # rotameter on a bracket on the back top rail
    meter = b(TX - 20, TX + 20, FY, yb, RZ - S, RZ + 130) + b(TX - 15, TX + 15, yb, yb + 30, 720, 820)
    add("valve_meter", "Ball valve, rotameter and its bracket", valve + meter, "#0EA5E9", 13, (0, 150, 0))
    hr = 13.5
    yh = yb + 15
    path = [(TX, yv + 15, tk0 + 15), (TX, yv + 15, 840), (TX, yh, 840), (TX, yh, 820), None, (TX, yh, 720), (TX, yh, 140),
            (TX, 0, 140), (CX - p["union_d"] / 2, 0, 140)]
    hose = []
    for a_, b_ in zip(path[:-1], path[1:]):
        if a_ is None or b_ is None:
            continue
        hose.append(_rod(a_, b_, hr))
    for pt in (path[1], path[2], path[6], path[7]):
        hose.append(__import__("build123d").Pos(*pt) * __import__("build123d").Sphere(hr))
    add("hose", "3/4 in hose to the rotary union", _fuse(hose), "#0369A1", 13, (0, 200, 0))

    # ---------------------------------------------------------------- 19 speed display, brake lever
    disp = b(FX0 - 30, FX0 - 6, -130, -70, RZ - 60, RZ - 10) + b(FX0 - 6, FX0, -112, -88, RZ - 35, RZ)   # faces the rider
    add("display", "Speed display (bicycle computer) on its bracket", disp, "#7C3AED", 19)
    lever = b(FX0 - 25, FX0, 70, 120, RZ - 30, RZ) + b(FX0 - 25, FX0 - 15, 105, 120, RZ, RZ + 90)
    add("brake_lever", "Brake lever with parking latch", lever, "#991B1B", 18)

    # ---------------------------------------------------------------- 12 motor option: cradle, hub motor, chain, guard, module
    MX, MZ_ = p["motor_x"], p["motor_z"]
    my0, my1 = p["motor_y"]
    cy0, cy1 = my0 - 6, 392
    cradle = b(MX - 65, MX + 65, FY - S, cy1, LT, LT + PT)
    cradle += b(MX - 30, MX + 30, my0 - 6, my0, LT + PT, MZ_ + 14) + b(MX - 30, MX + 30, 382, 388, LT + PT, MZ_ + 14)
    cradle -= _cyly(MX, MZ_, my0 - 7, 389, 6)
    cradle -= b(MX - 6, MX + 6, my0 - 7, 389, MZ_, MZ_ + 20)            # slots open upward
    add("motor_cradle", "Motor cradle (motor option)", cradle, "#6B7280", 12, (0, 200, 0))
    mr = p["motor_r"]
    motor = _cyly(MX, MZ_, my0, my1, mr) + _cyly(MX, MZ_, my1, 370.5, 25) + _cyly(MX, MZ_, my0 - 12, 395, 6)
    motor += _cyly(MX, MZ_, 371.5, 375.5, D["motor_spr_r"][1])
    add("motor", "Reference hub motor with sprocket (motor option)", motor, "#166534", 12, (0, 250, 0))
    mch = _band((JX, DZ, D["motor_spr_r"][0]), (MX, MZ_, D["motor_spr_r"][1]), "y", p["motor_chain_y"] - 4, p["motor_chain_y"] + 4, -3, 5)
    add("motor_chain", "Motor chain (motor option)", mch, "#111827", 12, (0, 150, 0))
    mg = _hull([(JX, DZ, D["motor_spr_r"][0] + 16), (MX, MZ_, D["motor_spr_r"][1] + 16)], "y", 398, 400)
    rim_o = _hull([(JX, DZ, D["motor_spr_r"][0] + 16), (MX, MZ_, D["motor_spr_r"][1] + 16)], "y", 362, 398)
    rim_i = _hull([(JX, DZ, D["motor_spr_r"][0] + 14), (MX, MZ_, D["motor_spr_r"][1] + 14)], "y", 361, 399)
    rim = (rim_o - rim_i) & b(JX - 80, MX - mr - 8, 350, 400, 0, 2000)
    mg += rim + c(MX, 389, MZ_ - 50, MZ_ - 40, 0.1)
    mg += _cyly(MX - 20, MZ_ - 45, 388, 398, 5) + _cyly(MX + 20, MZ_ - 45, 388, 398, 5)
    add("motor_guard", "Motor chain guard (motor option)", mg, "#CA8A04", 12, (0, 150, 0))
    mcore = b(-420, -177, 120, 288, TB - 66, TB)
    add("mcore", "MotionCore module", mcore, "#15803D", 12, (0, 0, -150))

    # ---------------------------------------------------------------- 14 to 16 shaking table
    TBX0 = p["table_x0"]; TBX1 = TBX0 + p["table_l"]; TBW = p["table_w"]; TZ = p["table_z"]
    tilt = p["table_tilt"]
    rot = lambda s: Pos(0, 0, TZ) * Rot(tilt, 0, 0) * Pos(0, 0, -TZ) * s  # noqa: E731
    deck = b(TBX0, TBX1, -TBW / 2, TBW / 2, TZ - 18, TZ) + b(TBX0, TBX1, -TBW / 2, TBW / 2, TZ, TZ + 3)
    for i in range(9):
        y = -TBW / 2 + 60 + i * 38
        deck += b(TBX0 + 60 + i * 30, TBX1 - 40, y, y + 6, TZ + 3, TZ + 11)
    fbx = b(TBX0, TBX0 + 180, TBW / 2 - 90, TBW / 2, TZ + 3, TZ + 73) - b(TBX0 + 4, TBX0 + 176, TBW / 2 - 86, TBW / 2 - 4, TZ + 6, TZ + 74)
    deck += fbx
    for y0_ in (-14, 8):                                                 # pitman bracket cheeks under the head end
        deck += b(TBX0 + 5, TBX0 + 45, y0_, y0_ + 6, TZ - 40, TZ - 18)
    ls_ = p["pin_slot"]                                                  # pin slot: 8 mm of lost motion toward the far end
    deck -= _cyly(TBX0 + 25, TZ - 30, -15, 15, 6) + _cyly(TBX0 + 25 + ls_, TZ - 30, -15, 15, 6) \
        + b(TBX0 + 25, TBX0 + 25 + ls_, -15, 15, TZ - 36, TZ - 24)
    add("deck", "Shaking table deck", rot(deck), "#E7E5E4", 14, (0, 0, 300))
    wash = _cylx(TBW / 2 - 25, TZ + 23, TBX0 + 190, TBX1 - 40, 20) - _cylx(TBW / 2 - 25, TZ + 23, TBX0 + 189, TBX1 - 39, 18)
    add("wash_pipe", "Wash water pipe", rot(wash), "#0EA5E9", 14, (0, 0, 380))

    # table base and flexure legs
    fy, fw, ft = p["flex_y"], p["flex_w"], p["flex_t"]
    bx0, bx1 = p["flex_x"][0] - 40, p["flex_x"][1] + 40
    base = _fuse([b(bx0, bx1, y - S / 2, y + S / 2, 0, S) for y in (-fy, fy)]
                 + [b(x, x + S, -fy + S / 2, fy - S / 2, 0, S) for x in (bx0, bx1 - S)])
    add("table_base", "Table base, welded", base, "#6B7280", 15, (0, 0, -150))
    under = rot(b(TBX0 - 200, TBX1 + 200, -TBW, TBW, -500, TZ - 18))
    legs_ = []
    clts = []
    for x in p["flex_x"]:
        for y in (-fy, fy):
            leg = b(x - ft / 2, x + ft / 2, y - fw / 2, y + fw / 2, S, TZ + 50) & under
            legs_.append(leg)
            clts.append(b(x + ft / 2, x + ft / 2 + 40, y - fw / 2, y + fw / 2, S, S + 4) + b(x + ft / 2, x + ft / 2 + 4, y - fw / 2, y + fw / 2, S + 4, S + 40))
            tc = b(x + ft / 2, x + ft / 2 + 40, y - fw / 2, y + fw / 2, TZ - 22, TZ - 18) + b(x + ft / 2, x + ft / 2 + 4, y - fw / 2, y + fw / 2, TZ - 58, TZ - 22)
            clts.append(rot(tc))
    add("flex_legs", "Flexure legs (4), plywood", _fuse(legs_), "#A16207", 15, (0, 0, 200))
    add("cleats", "Leg cleats (8), steel angle", _fuse(clts), "#374151", 15)

    # head: plate bolted to the frame end, shelf, two pillow blocks, head shaft, eccentric, pulley, pitman
    HX, HZ = p["head_x"], p["head_z"]
    sh_top = HZ - ph
    head = b(FX1, FX1 + PT, -310, 65, hz - 5, RZ + 5)
    head += b(FX1 + PT, HX + 80, -310, 65, sh_top - PT, sh_top) - b(HX - 60, HX + 70, -250, 0, sh_top - PT - 1, sh_top + 1) \
        - b(HX - 60, HX + 70, -250, 30, sh_top - PT - 1, sh_top + 1)      # slot for the pitman eye, lightening cut-out
    for y in (-200, 50):
        head += _prism([(FX1 + PT, sh_top - PT), (FX1 + PT + 90, sh_top - PT), (FX1 + PT, sh_top - PT - 90)], "y", y - 3, y + 3)
    add("head", "Table head plate and shelf", head, "#6B7280", 15, (200, 0, 0))
    hpb = []
    for y in (-290.0, 40.0):
        hpb.append(b(HX - 63.5, HX + 63.5, y - 19, y + 19, sh_top, sh_top + 13) + b(HX - 22, HX + 22, y - 15, y + 15, sh_top + 13, HZ)
                   + _cyly(HX, HZ, y - 15, y + 15, 30))
    add("head_bearings", "Head shaft bearings (2 pillow blocks)", _fuse(hpb), "#57534E", 15, (0, 0, 150))
    e = p["eccentric"]
    hsh = _cyly(HX, HZ, p["belt_y"] - 15, 64, 10) + _cyly(HX, HZ, p["belt_y"] - 10, p["belt_y"] + 10, p["head_pulley_d"] / 2)
    hsh += _cyly(HX + e, HZ, -12, 12, 30)
    add("head_shaft", "Head shaft, eccentric and 125 mm pulley", hsh, "#57534E", 15, (0, 0, 220))
    # bump stop (21, 22): bracket on the table-end top rail, M8 stud, rubber buffer, striker angle under the deck
    sy, sz, bd, bl = p["stop_y"], p["stop_z"], p["buffer_d"], p["buffer_l"]
    xs = TBX0 + PT                                       # strike face of the striker (deck at full forward travel)
    xb = xs + bl                                         # back of the buffer
    xn = xb + 6.5                                        # inner lock nut, then the upright
    xu = xn + PT
    foot = b(FX1 - S, FX1 - S + 40, sy - 33, sy + 33, RZ, RZ + PT)
    arm = b(FX1 - S, xu, sy - S / 2, sy + S / 2, RZ + PT, RZ + PT + S)
    upr = b(xn, xu, sy - 20, sy + 20, RZ + PT + S, sz + 30) - _cylx(sy, sz, xn - 1, xu + 1, 4.5)
    add("stop_bracket", "Bump stop bracket (arm, foot and upright)", foot + arm + upr, "#6B7280", 21, (0, 200, 0))
    buf = _cylx(sy, sz, xs, xb, bd / 2)
    stud = _cylx(sy, sz, xs + bl - 10, xu + 22, 4)
    nuts = [_cylx(sy, sz, xb, xn, 7.5), _cylx(sy, sz, xu, xu + 6.5, 7.5)]
    add("bump_stop", "Rubber buffer 40 x 30 on an M8 stud with lock nuts", _fuse([buf, stud] + nuts), "#111827", 22, (0, 200, 0))
    # striker: 6 mm angle, 40 wide, screwed under the deck's head end at the back edge (deck coordinates, then tilted)
    zb = TZ - 18
    stk = b(TBX0, TBX0 + 40, sy - 20, sy + 20, zb - PT, zb) + b(TBX0, TBX0 + PT, sy - 20, sy + 20, zb - 70, zb - PT)
    add("striker", "Striker angle under the deck", rot(stk), "#374151", 21, (0, 0, 300))
    # pitman: eye round the eccentric to the pin in the deck bracket
    tr = math.radians(tilt)
    pin = (TBX0 + 25, -(-30) * math.sin(tr), TZ - 30 * math.cos(tr))     # bracket pin, on the deck centre line
    eye = _cyly(HX + e, HZ, -10, 10, 42) - _cyly(HX + e, HZ, -11, 11, 30.5)
    pit = eye + _bar((HX + e + 36, 0, HZ + 20), pin, 22, 12, normal=(0, 1, 0)) + rot(_cyly(TBX0 + 25, TZ - 30, -14, 14, 6))
    add("pitman", "Pitman arm", pit, "#B45309", 15, (0, -150, 0))
    # tensioner on the table belt (top run), pivot on the front top rail
    by = p["belt_y"]
    cA, cB = (JX, DZ, p["take_off_d"] / 2), (HX, HZ, p["head_pulley_d"] / 2)
    dx, dz = cB[0] - cA[0], cB[1] - cA[1]
    L = math.hypot(dx, dz); ang = math.atan2(dz, dx); beta = math.asin((cA[2] - cB[2]) / L)
    nx, nz = -math.sin(ang + beta), math.cos(ang + beta)        # outward normal of the top run
    tA = (cA[0] + cA[2] * nx, cA[1] + cA[2] * nz)
    tB = (cB[0] + cB[2] * nx, cB[1] + cB[2] * nz)
    xi = 120.0
    ti = (xi, tA[1] + (tB[1] - tA[1]) * (xi - tA[0]) / (tB[0] - tA[0]))
    ic = (ti[0] + nx * 30.05, ti[1] + nz * 30.05)
    pv = (-20.0, RZ - 12.5)
    tens = _cyly(ic[0], ic[1], by - 8, by + 8, 30) + _cyly(ic[0], ic[1], by - 13, by + 8, 6)
    tens += _bar((pv[0], by - 16, pv[1]), (ic[0], by - 16, ic[1]), 24, 6, normal=(0, 1, 0))
    tens += _bar((pv[0], by - 16, pv[1]), (pv[0] - 40, by - 16, pv[1] + 130), 20, 6, normal=(0, 1, 0))
    tens += _cyly(pv[0], pv[1], by - 19, -FY - 6, 6) + b(pv[0] - 30, pv[0] + 60, -FY - 6, -FY, RZ - S, RZ)
    add("tensioner", "Table belt tensioner", tens, "#0F766E", 15, (0, -150, 0))
    tbelt = _band(cA, cB, "y", by - 8, by + 8, -9, 0)
    add("table_belt", "Table belt (A-section V-belt)", tbelt, "#111827", 10, (0, -120, 0))
    tg = _hull([(cA[0], cA[1], cA[2] + 22), (cB[0], cB[1], cB[2] + 22), (ic[0], ic[1], 52)], "y", -354, -352)
    tr_o = _hull([(cA[0], cA[1], cA[2] + 22), (cB[0], cB[1], cB[2] + 22), (ic[0], ic[1], 52)], "y", -352, -312)
    tr_i = _hull([(cA[0], cA[1], cA[2] + 20), (cB[0], cB[1], cB[2] + 20), (ic[0], ic[1], 50)], "y", -353, -311)
    tg += (tr_o - tr_i) - _hull([(pv[0], pv[1], 22), (ic[0], ic[1], 22)], "y", -352, -311) \
        - _hull([(pv[0], pv[1], 22), (pv[0] - 40, pv[1] + 130, 22)], "y", -352, -311)
    add("table_guard", "Table belt guard", tg, "#CA8A04", 11, (0, -200, 0))

    # 16 tailings launder (front) and concentrate box (far end)
    lx0, lx1 = TBX0 + 150, TBX1 - 40
    lau = b(lx0, lx1, -300, -200, 640, 700) - b(lx0 + 3, lx1 - 3, -297, -203, 643, 701)
    lau -= b(lx0 - 1, lx0 + 3, -270, -230, 650, 701)
    lau += b(lx0 - 60, lx0 + 3, -270, -230, 640, 643) + b(lx0 - 60, lx0 + 3, -273, -270, 640, 660) + b(lx0 - 60, lx0 + 3, -230, -227, 640, 660)
    for x in (lx0 + 20, lx1 - 45):
        lau += b(x, x + 25, -262.5, -237.5, 0, 640)
    add("launder", "Tailings launder on legs", lau, "#B45309", 16, (0, -250, 0))
    kx0, kx1 = TBX1 - 25, TBX1 + 95
    box = b(kx0, kx1, -230, 60, 640, 760) - b(kx0 + 3, kx1 - 3, -227, 57, 643, 761)
    box += b(kx1 - 3, kx1 + 1, -230, 60, 760, 763)          # hinge strip for the lid on the far edge
    for x in (kx0 + 10, kx1 - 35):
        for y in (-215, 20):
            box += b(x, x + 25, y, y + 25, 0, 640)
    add("conc_box", "Lockable concentrate box on legs", box, "#92400E", 16, (300, 0, 0))
    return C


def build_parts(p=PARAMS):
    """(name, shape, colour, bom_item, explode_offset) per BOM item, for the concept media and GA."""
    from build123d import Compound
    C = build_components(p)
    names = {1: "Base frame, welded steel tube", 2: "Feed hopper, screen and support", 3: "Centrifugal bowl (liner and shell)",
             4: "Fluidization jacket, hub and rotary union", 5: "Spindle, bearings and pulley", 6: "Splash tub, standpipe, tailings pipe",
             7: "Bowl lid guard and clamps", 8: "Pedal station (outrigger, seat, crank)", 9: "Jackshaft, gearbox, chain, pulleys",
             10: "Drive belts (bowl and table)", 11: "Belt and chain guards", 12: "MotionCore module and motor option",
             13: "Water header tank, valve, flow meter, hose", 14: "Shaking table deck with riffles", 15: "Table stand, head and tensioner",
             16: "Tailings launder and concentrate box", 17: "Hardware", 18: "Bowl brake", 19: "Speed display",
             21: "Table bump stop (21, 22)"}
    cols = {1: "#4B5563", 2: "#D97706", 3: "#0F766E", 4: "#5EEAD4", 5: "#9CA3AF", 6: "#60A5FA", 7: "#1F2937", 8: "#374151",
            9: "#78716C", 10: "#111827", 11: "#FACC15", 12: "#15803D", 13: "#38BDF8", 14: "#E5E7EB", 15: "#6B7280",
            16: "#B45309", 17: "#111827", 18: "#DC2626", 19: "#7C3AED", 21: "#374151"}
    ex = {1: (0, 0, -250), 2: (0, 0, 520), 3: (0, 0, 380), 4: (0, 0, 250), 5: (0, 0, -150), 6: (0, -150, 80), 7: (0, 0, 460),
          8: (-250, 0, -550), 9: (-100, -150, -300), 10: (0, -250, -450), 11: (0, -450, -420), 12: (150, 230, 260),
          13: (0, 250, 380), 14: (300, 0, 330), 15: (300, 0, 0), 16: (300, -300, 0), 17: (0, 0, 0), 18: (250, 0, -150),
          19: (0, -250, 150), 21: (300, 250, 330)}
    groups = {}
    for k, comp in C.items():
        groups.setdefault(21 if comp.bom == 22 else comp.bom, []).append(comp.shape)
    out = []
    for n in sorted(groups):
        if n == 17:
            continue
        out.append((names[n], Compound(children=groups[n]), cols[n], n, ex[n]))
    return out


def assemblies(parts=None):
    """Named compounds for export: the whole machine, the rotating bowl group and the table deck."""
    import copy
    from build123d import Compound
    C = build_components()
    return {
        "gravitysort-assembly": Compound(children=[copy.copy(c.shape) for c in C.values()]),
        "gravitysort-bowl": Compound(children=[copy.copy(C[k].shape) for k in ("liner", "shell", "jacket", "hub", "bowl_bolts")]),
        "gravitysort-table-deck": Compound(children=[copy.copy(C["deck"].shape), copy.copy(C["wash_pipe"].shape)]),
    }


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch, and pairs that must stay apart by a clearance (mm).
    Returns (description, overlap volume mm3, gap mm, expectation, ok) rows."""
    C = build_components(p)
    S = lambda *ks: _fuse([C[k].shape for k in ks])  # noqa: E731
    P_ = p
    xn0 = p["table_x0"] + p["plate_t"] + p["buffer_l"]      # back of the buffer: the inner lock nut starts here
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        if expect == "touch":
            ok = v < 1e-2 and gp < 0.05
        elif expect == "fit":
            ok = v < 1e-2 and gp <= 1.0
        else:
            ok = v < 1e-2 and gp >= expect - 1e-6
        rows.append((desc, v, gp, expect, ok))

    T = "touch"
    # frame and plates
    chk("Bearing plates welded under the spindle and tub members", S("bearing_plates"), S("frame"), T)
    chk("Tank cradle on the tank post", S("tank_cradle"), S("frame"), T)
    # outrigger
    chk("Outrigger end plates on the outrigger", S("outrigger_plates"), S("outrigger"), T)
    chk("Outrigger end plates on the frame end", S("outrigger_plates"), S("frame"), T)
    chk("Outrigger clear of the frame (only the plates touch)", S("outrigger"), S("frame"), 3.0)
    chk("Seat post in the seat tube (sliding fit)", S("seat"), S("outrigger"), "fit")
    chk("Crankset in the bottom bracket shell", S("crankset"), S("outrigger"), T)
    chk("Crankset clear of the chain case", S("crankset") - S("pedal_chain"), S("chain_case"), 1.5)
    # drive
    chk("Pillow blocks on the gearbox members", S("pillow_blocks"), S("frame"), T)
    chk("Gearbox on the gearbox members", S("gearbox"), S("frame"), T)
    chk("Pedal chain clear of the frame", S("pedal_chain"), S("frame"), 4.0)
    chk("Pedal chain clear of the outrigger", S("pedal_chain"), S("outrigger", "outrigger_plates"), 5.0)
    chk("Pedal chain clear of the gearbox", S("pedal_chain"), S("gearbox", "pillow_blocks"), 5.0)
    chk("Chain case sits on the gearbox member", S("chain_case"), S("frame"), T)
    chk("Chain case tab on the pedal post", S("chain_case"), S("outrigger"), T)
    chk("Chain case clear of the gearbox", S("chain_case"), S("gearbox"), 2.0)
    chk("Chain case clear of the pedal chain", S("chain_case"), S("pedal_chain"), 1.5)
    chk("Chain case clear of the outrigger plates and seat", S("chain_case"), S("outrigger_plates", "seat"), 5.0)
    chk("Drive pulley clear of the frame", S("drive_pulley"), S("frame"), 5.0)
    chk("Take-off pulley and freewheel clear of the frame", S("jack_wheels"), S("frame"), 5.0)
    chk("Jackshaft clear of the frame", S("jackshaft"), S("frame"), 5.0)
    chk("Bowl belt clear of the frame", S("bowl_belt"), S("frame", "bearing_plates"), 5.0)
    chk("Belt guard hangers on the members", S("belt_guard"), S("frame"), T)
    chk("Belt guard clear of the pulleys and belt", S("belt_guard"), S("drive_pulley", "driven_pulley", "bowl_belt"), 3.0)
    chk("Belt guard clear of the spindle and union", S("belt_guard"), S("spindle", "union"), 2.0)
    chk("Belt guard clear of the lower bearing", S("belt_guard"), S("bearings"), 3.0)
    chk("Speed sensor under the guard top", S("sensor"), S("belt_guard"), T)
    chk("Speed sensor clear of the driven pulley", S("sensor"), S("driven_pulley"), 5.0)
    chk("Speed display and brake lever on the end top rail", S("display", "brake_lever"), S("frame"), T)
    chk("Speed display and brake lever clear of the outrigger", S("display", "brake_lever"), S("outrigger", "outrigger_plates", "seat"), 10.0)
    # spindle
    chk("Bearings bolted under the bearing plates", S("bearings"), S("bearing_plates"), T)
    chk("Spindle clear of the bearing plates (holes)", S("spindle"), S("bearing_plates"), 5.0)
    chk("Spindle clear of the frame", S("spindle"), S("frame"), 10.0)
    chk("Driven pulley clear of the lower bearing", S("driven_pulley"), S("bearings"), 5.0)
    chk("Rotary union on the spindle foot", S("union"), S("spindle"), T)
    chk("Brake flange on the spindle", S("brake_flange"), S("spindle"), T)
    chk("Brake disc on its flange", S("rotor"), S("brake_flange"), T)
    chk("Brake disc clear of the frame and plates", S("rotor"), S("frame", "bearing_plates", "bearings"), 10.0)
    chk("Brake disc runs in the caliper slot", S("rotor"), S("caliper"), 1.5)
    chk("Caliper on its bracket", S("caliper"), S("caliper_bracket"), T)
    chk("Caliper bracket on the spindle member", S("caliper_bracket"), S("frame"), T)
    chk("Caliper bracket clear of the disc", S("caliper_bracket"), S("rotor"), 3.0)
    chk("Caliper clear of the upper bearing", S("caliper", "caliper_bracket"), S("bearings"), 5.0)
    # tub and bowl
    chk("Tub floor on the tub members", S("tub"), S("frame"), T)
    chk("Tub wall clear of the drop posts", S("tub") - _box(-500, 500, -500, 500, 0, 480), S("frame"), 10.0)
    chk("Standpipe on the upper bearing plate", S("standpipe"), S("bearing_plates"), T)
    chk("Standpipe grommet in the tub floor", S("standpipe"), S("tub"), T)
    chk("Spindle clear of the standpipe", S("spindle"), S("standpipe"), 10.0)
    chk("Tailings pipe grommet in the tub wall", S("tail_pipe"), S("tub"), T)
    chk("Tailings pipe clear of the frame", S("tail_pipe"), S("frame"), 3.0)
    chk("Hub on the spindle", S("hub"), S("spindle"), T)
    chk("Hub flange against the jacket floor", S("hub"), S("jacket"), T)
    chk("Hub clear of the standpipe", S("hub"), S("standpipe"), 8.0)
    chk("Jacket clear of the standpipe and tub", S("jacket"), S("standpipe", "tub"), 8.0)
    chk("Jacket closing ring on the shell", S("jacket"), S("shell"), T)
    chk("Liner cast into the shell", S("liner"), S("shell"), T)
    chk("Bowl bolts, spacers and cast-in nuts in place", S("bowl_bolts"), S("jacket", "shell", "hub", "liner"), T)
    chk("Bowl lip clear of the tub wall", S("shell", "liner", "jacket"), S("tub"), 50.0)
    chk("Lid on the tub rim", S("lid"), S("tub"), T)
    chk("Lid clamps on the tub and over the lid", S("clamps"), S("tub", "lid"), T)
    chk("Bowl clear of the lid", S("shell", "liner"), S("lid"), 30.0)
    chk("Tub clear of the motor (motor option)", S("tub"), S("motor"), 8.0)
    # hopper
    chk("Hopper post on the front top rail", S("hopper_post"), S("frame"), T)
    chk("Hopper cone sits in the ring", S("hopper"), S("hopper_post"), T)
    chk("Screen on the hopper rim", S("screen"), S("hopper"), T)
    chk("Feed pipe clear of the lid (lid lifts off)", S("hopper"), S("lid"), 10.0)
    chk("Hopper post clear of the lid and clamps", S("hopper_post"), S("lid", "clamps", "tub"), 30.0)
    # water
    chk("Tank on its cradle", S("tank"), S("tank_cradle"), T)
    chk("Tank clear of the hopper", S("tank"), S("hopper", "screen"), 50.0)
    chk("Valve on the tank", S("valve_meter"), S("tank"), T)
    chk("Rotameter bracket on the back top rail", S("valve_meter"), S("frame"), T)
    chk("Hose into the valve and rotameter", S("hose"), S("valve_meter"), T)
    chk("Hose to the rotary union", S("hose"), S("union"), T)
    chk("Hose clear of the frame", S("hose"), S("frame"), 3.0)
    chk("Hose clear of the guard and drive", S("hose"), S("belt_guard", "drive_pulley", "motor", "motor_cradle", "mcore"), 3.0)
    chk("MotionCore module under the top rails", S("mcore"), S("frame"), T)
    # motor option
    chk("Motor cradle on the back lower rail", S("motor_cradle"), S("frame"), T)
    chk("Motor in its dropouts", S("motor"), S("motor_cradle"), T)
    chk("Motor clear of the frame", S("motor"), S("frame"), 8.0)
    chk("Motor chain clear of the frame and cradle", S("motor_chain"), S("frame", "motor_cradle"), 4.0)
    chk("Motor chain clear of the hub shell", S("motor_chain"), _cyly(PARAMS["motor_x"], PARAMS["motor_z"], 306, 366, 80), 2.0)
    chk("Motor chain guard on its spacers at the dropout", S("motor_guard"), S("motor_cradle"), T)
    chk("Motor chain guard clear of the chain and motor", S("motor_guard"), S("motor_chain", "motor", "jackshaft", "jack_wheels"), 3.0)
    # table
    chk("Flexure legs on the table base", S("flex_legs"), S("table_base"), T)
    chk("Flexure legs under the deck", S("flex_legs"), S("deck"), T)
    chk("Cleats on the legs", S("cleats"), S("flex_legs"), T)
    chk("Cleats on the base and deck", S("cleats"), S("table_base", "deck"), T)
    chk("Head plate on the frame end", S("head"), S("frame"), T)
    chk("Head bearings on the shelf", S("head_bearings"), S("head"), T)
    chk("Pitman eye clear of the shelf", S("pitman"), S("head"), 3.0)
    chk("Pitman pin at the pulling end of its slot in the deck cheeks", S("pitman"), S("deck"), T)
    chk("Pitman eye on the eccentric (running fit)", S("pitman"), S("head_shaft"), "fit")
    chk("Deck clear of the head and frame (stroke 15 mm)", S("deck"), S("head", "head_bearings", "head_shaft", "frame"), 15.0)
    chk("Deck clear of the launder and box", S("deck", "wash_pipe"), S("launder", "conc_box"), 15.0)
    # bump stop (GVS-DDR-003 A2); the model is at full forward travel, so the head end of the stroke is 15 mm toward -X
    from build123d import Pos
    back = lambda sh: Pos(-15, 0, 0) * sh  # noqa: E731
    chk("Stop bracket foot on the table-end top rail", S("stop_bracket"), S("frame"), T)
    chk("Stop bracket clear of the head plate, bearings and shaft", S("stop_bracket"), S("head", "head_bearings", "head_shaft"), 10.0)
    chk("Buffer stud held in the upright by its lock nuts", S("bump_stop"), S("stop_bracket"), T)
    chk("Striker angle under the deck", S("striker"), S("deck"), T)
    chk("Striker on the buffer at full forward travel (zero setting)", S("striker"), S("bump_stop"), T)
    chk("Striker 15 mm off the buffer at the head end of the stroke", back(S("striker")), S("bump_stop"), 14.99)
    chk("Striker clear of the stop arm at full forward travel", S("striker"), S("stop_bracket"), 8.0)
    chk("Striker clear of the stop arm at the head end of the stroke", back(S("striker")), S("stop_bracket"), 8.0)
    chk("Deck clear of the stop bracket and buffer", S("deck", "wash_pipe"), S("stop_bracket", "bump_stop"), 15.0)
    chk("Deck clear of the stop at the head end of the stroke", back(S("deck", "wash_pipe")), S("stop_bracket", "bump_stop"), 15.0)
    chk("Stop clear of the flexure legs and cleats", S("stop_bracket", "bump_stop", "striker"), S("flex_legs", "cleats"), 10.0)
    chk("Stop clear of the pitman and table belt guard", S("stop_bracket", "bump_stop", "striker"), S("pitman", "table_guard", "table_belt"), 20.0)
    others = [k for k in C if k not in ("stop_bracket", "bump_stop")]
    chk("Room for a 13 mm spanner on the lock nuts from the back", _box(xn0 - 8, xn0 + 30, 214, 330, P_["stop_z"] - 16, P_["stop_z"] + 16),
        S(*others), 2.0)
    chk("Launder clear of the legs and base", S("launder"), S("flex_legs", "table_base", "cleats"), 10.0)
    chk("Box clear of the legs and base", S("conc_box"), S("flex_legs", "table_base", "cleats", "launder"), 10.0)
    chk("Table belt clear of the frame and head", S("table_belt"), S("frame", "head", "launder"), 5.0)
    chk("Tensioner idler on the belt", S("tensioner"), S("table_belt"), "fit")
    chk("Tensioner pivot bracket on the front top rail", S("tensioner"), S("frame"), T)
    chk("Table guard clear of the belt, pulleys and tensioner", S("table_guard"), S("table_belt", "tensioner", "jack_wheels", "head_shaft"), 2.0)
    chk("Table guard clear of the frame and head", S("table_guard"), S("frame", "head"), 2.0)
    chk("Table guard clear of the jackshaft end", S("table_guard"), S("jackshaft"), 1.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = exp if isinstance(exp, str) else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:62s} overlap {v:9.2f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    for name, shape in assemblies().items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.5)
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    for z, r, ri in riffle_rings():
        print(f"riffle ring at z {z:.0f} mm: wall radius {r:.1f} mm, lip radius {ri:.1f} mm")
    print(f"frame tube {sum(l for _, l in frame_members()) / 1000:.2f} m")
    print_checks()
