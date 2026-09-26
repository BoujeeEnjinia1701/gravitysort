"""GravitySort parametric model (build123d), TRL 3 (frame in 25 x 25 x 1.5 mm tube per GVS-DDR-002).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, and prints the main envelopes.

Massing-plus detail: correct interfaces and main dimensions (bowl, riffle rings and
fluidization jacket, spindle with bearings, brake rotor and rotary union, drive train,
splash tub, table and water tank), not fabrication detail. PRELIMINARY, NOT FOR FABRICATION.

Axes: X along the machine (pedal station at -X, shaking table at +X), Y front (-Y) to
back (+Y), Z up from the ground. Units mm. The centrifuge axis is at (bowl_x, 0).
docs/04-calcs/sizing.py (GVS-CAL-001) imports PARAMS, riffle_rings() and frame_members()
so that the calculation note and the geometry use the same numbers.
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Base frame (item 1): 25 x 25 x 1.5 mm mild steel square tube (GVS-DDR-002, was 30 x 30 x 2)
    "frame_x0": -450.0, "frame_x1": 450.0, "frame_y": 300.0, "rail_z": 700.0, "tube": 25.0, "tube_wall": 1.5,
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
    "union_z": (120.0, 180.0), "union_d": 56.0,
    # Spindle and bearings (item 5)
    "spindle_d": 25.0, "bearing_z": (280.0, 430.0), "bearing_d": 90.0, "bearing_h": 40.0,
    "driven_pulley_d": 100.0, "pulley_z": 190.0,
    # Bowl brake (item 18): 160 mm bicycle disc rotor and mechanical caliper on the spindle
    "brake_rotor_d": 160.0, "brake_z": 360.0,
    # Splash tub (item 6) and lid guard (item 7)
    "tub_d": 430.0, "tub_z": (470.0, 790.0), "tub_t": 6.0, "lid_t": 10.0, "lid_hole_d": 60.0,
    # Hopper and screen (item 2)
    "hopper_z": (960.0, 1180.0), "hopper_top_d": 340.0, "screen_d": 360.0, "feed_pipe_d": 44.0,
    # Drive (items 8 to 10)
    "pedal_x": -800.0, "drive_z": 330.0, "jack_x": -250.0,
    "chainring_t": 48, "freewheel_t": 12, "bevel_ratio": 1.0, "drive_pulley_d": 300.0,
    "take_off_d": 140.0, "head_pulley_d": 125.0,
    # Water header tank (item 13)
    "tank_x": -330.0, "tank_y": 180.0, "tank_d": 380.0, "tank_z": (1250.0, 1650.0),
    # Shaking table (items 14 to 16)
    "table_x0": 620.0, "table_l": 1000.0, "table_w": 450.0, "table_z": 820.0, "table_tilt": 3.0,
    "head_x": 560.0, "head_z": 710.0,
}


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _cyl(x, y, z0, z1, r):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _cone(x, y, z0, z1, r0, r1):
    from build123d import Cone, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cone(r0, r1, z1 - z0)


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


def frame_members(p=PARAMS):
    """(name, length mm) of every frame tube in the base frame, including the tank post."""
    lx = p["frame_x1"] - p["frame_x0"]; ly = 2 * p["frame_y"]
    m = [("leg", p["rail_z"])] * 4 + [("top rail X", lx)] * 2 + [("top rail Y", ly)] * 2
    m += [("low stretcher", lx)] * 2
    m += [("tub cross member", ly)] * 2 + [("spindle bearing member", ly), ("jackshaft member", ly),
                                           ("motor member", ly), ("tank post member", ly)]
    m += [("tank post", p["tank_z"][0] - p["rail_z"])]
    return m


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item, explode_offset)."""
    from build123d import Cylinder, Box, Pos, Rot
    b, c = _box, _cyl
    FX0, FX1, FY, RZ, S = p["frame_x0"], p["frame_x1"], p["frame_y"], p["rail_z"], p["tube"]
    CX = p["bowl_x"]; CY = 0.0
    JX, DZ, PX = p["jack_x"], p["drive_z"], p["pedal_x"]

    # 1 Base frame
    frame = None
    for x in (FX0, FX1 - S):
        for y in (-FY, FY - S):
            leg = b(x, x + S, y, y + S, 0, RZ)
            frame = leg if frame is None else frame + leg
    frame += b(FX0, FX1, -FY, -FY + S, RZ - S, RZ) + b(FX0, FX1, FY - S, FY, RZ - S, RZ)
    frame += b(FX0, FX0 + S, -FY, FY, RZ - S, RZ) + b(FX1 - S, FX1, -FY, FY, RZ - S, RZ)
    frame += b(FX0, FX1, -FY, -FY + S, 90, 90 + S) + b(FX0, FX1, FY - S, FY, 90, 90 + S)
    tz0 = p["tub_z"][0]
    for x in (CX - 165, CX + 135):
        frame += b(x, x + S, -FY, FY, tz0 - S, tz0)
    h = S / 2
    frame += b(CX - h, CX + h, -FY, FY, 280 - S, 280)
    frame += b(JX - h, JX + h, -FY, FY, 280 - S, 280)
    frame += b(-100 - h, -100 + h, -FY, FY, 265 - S, 265)
    frame += b(-330 - h, -330 + h, -FY, FY, RZ - S, RZ)

    # 2 Feed hopper, screen and feed pipe
    hz0, hz1 = p["hopper_z"]; hr = p["hopper_top_d"] / 2
    hopper = _cone(CX, CY, hz0, hz1, 70, hr) - _cone(CX, CY, hz0 + 3, hz1 + 3, 62, hr - 8)
    fr = p["feed_pipe_d"] / 2
    hopper += c(CX, CY, 760, hz0, fr) - c(CX, CY, 750, hz0 + 1, fr - 6)
    hopper += b(CX - 12, CX + 12, -FY, -FY + 24, RZ, 1000) + b(CX - 12, CX + 12, -FY, CY - 76, 976, 1000)
    screen = c(CX, CY, hz1, hz1 + 6, p["screen_d"] / 2)

    # 3 Bowl: GFRP shell, PU liner and four riffle rings with fluidization holes (holes not modelled)
    z0 = p["bowl_z0"]; z1 = z0 + p["bowl_depth"]
    r0, r1 = p["bowl_base_d"] / 2, p["bowl_lip_d"] / 2
    t = p["liner_t"] + p["shell_t"]
    bowl = _cone(CX, CY, z0 - t, z1, r0 + t, r1 + t) - _cone(CX, CY, z0, z1 + 1, r0, r1 + 0.01)
    for z, r, ri in riffle_rings(p):
        bowl += c(CX, CY, z, z + p["ring_t"], r + 2) - c(CX, CY, z - 1, z + p["ring_t"] + 1, ri)
    bowl += c(CX, CY, z0 - t - 40, z0 - t, 30)                                   # hub

    # 4 Fluidization jacket (rotates with the bowl) and rotary union at the spindle foot
    g, jt = p["jacket_gap"], p["jacket_t"]
    jz0, jz1 = z0 - t - g, z1 - 30
    rin0, rin1 = r0 + t, bowl_radius(jz1, p) + t
    jacket = _cone(CX, CY, jz0 - jt, jz1, rin0 + g + jt, rin1 + g + jt) - \
        _cone(CX, CY, jz0, jz1 + 1, rin0 + g, rin1 + g + 0.01)
    uz0, uz1 = p["union_z"]
    union = c(CX, CY, uz0, uz1, p["union_d"] / 2)

    # 5 Spindle, bearing units and driven pulley
    sr = p["spindle_d"] / 2
    spindle = c(CX, CY, uz1, jz0 - jt, sr)
    for bz in p["bearing_z"]:
        spindle += c(CX, CY, bz, bz + p["bearing_h"], p["bearing_d"] / 2)
    pz = p["pulley_z"]
    spindle += c(CX, CY, pz, pz + 40, p["driven_pulley_d"] / 2)

    # 18 Bowl brake: disc rotor and caliper on a bracket from the spindle bearing member
    bz = p["brake_z"]; br = p["brake_rotor_d"] / 2
    brake = c(CX, CY, bz, bz + 3, br) + b(CX + br - 25, CX + br + 15, -30, 30, bz - 15, bz + 20)
    brake += b(CX + br - 5, CX + br + 15, -15, 15, 280, bz - 15)

    # 6 Splash tub with tailings outlet and launder toward the back (+Y)
    TR = p["tub_d"] / 2; tz1 = p["tub_z"][1]; tt = p["tub_t"]
    tub = (c(CX, CY, tz0, tz1, TR) - c(CX, CY, tz0 + tt + 2, tz1 + 1, TR - tt)) - c(CX, CY, tz0 - 1, tz0 + 9, 50)
    tub += b(CX - 40, CX + 40, TR - 20, FY + 120, tz0 - 10, tz0 + 40) - \
        b(CX - 34, CX + 34, TR - 10, FY + 121, tz0 - 4, tz0 + 41)

    # 7 Lid guard
    lid = c(CX, CY, tz1, tz1 + p["lid_t"], TR + 8) - c(CX, CY, tz1 - 1, tz1 + p["lid_t"] + 1, p["lid_hole_d"] / 2)

    # 8 Pedal station
    pedal = b(PX - 20, FX0, -20, 20, 250, 280) + b(PX - 180, FX0, -20, 20, 90, 120)
    pedal += b(PX - 180, PX - 150, -20, 20, 0, 780) + b(PX - 260, PX - 80, -90, 90, 780, 830)
    pedal += b(PX - 20, PX + 20, -20, 20, 0, 350) + b(PX - 200, PX + 20, -150, 150, 0, 20)
    ring_r = 100.0                                   # 48T, 12.7 mm pitch: about 97 mm pitch radius
    pedal += Pos(PX, 60, DZ) * Rot(90, 0, 0) * Cylinder(ring_r, 6)
    pedal += b(PX - 10, PX + 10, 76, 88, DZ - 170, DZ) + b(PX - 50, PX + 50, 88, 138, DZ - 178, DZ - 164)
    pedal += b(PX - 10, PX + 10, -88, -76, DZ, DZ + 170) + b(PX - 50, PX + 50, -138, -88, DZ + 164, DZ + 178)

    # 9 Jackshaft, freewheel, chain, bevel gearbox, drive pulley, motor sprocket, table take-off
    jack = Pos(JX, 5, DZ) * Rot(90, 0, 0) * Cylinder(10, 550)
    jack += Pos(JX, 60, DZ) * Rot(90, 0, 0) * Cylinder(25, 8)
    jack += b(PX, JX, 56, 64, DZ + ring_r - 6, DZ + ring_r + 2) + b(PX, JX, 56, 64, DZ - 30, DZ - 22)
    jack += b(JX - 50, JX + 50, -40, 40, 280, 380)
    dr = p["drive_pulley_d"] / 2
    jack += c(JX, 0, 190, 280, 12) + c(JX, 0, 190, 230, dr)
    jack += Pos(JX, 220, DZ) * Rot(90, 0, 0) * Cylinder(35, 8)
    jack += b(JX, -100, 216, 224, DZ + 30, DZ + 38) + b(JX, -100, 216, 224, DZ - 38, DZ - 30)
    jack += Pos(JX, -250, DZ) * Rot(90, 0, 0) * Cylinder(p["take_off_d"] / 2, 20)

    # 10 Belts: bowl belt (horizontal) and table belt (inclined; slack unless tensioned)
    belt = b(JX, CX, dr - 12, dr + 2, 200, 220) + b(JX, CX, -dr - 2, -dr + 12, 200, 220)
    HX, HZ = p["head_x"], p["head_z"]
    dx, dz = HX - JX, HZ - DZ
    ang = math.degrees(math.atan2(dz, dx))
    belt += Pos((JX + HX) / 2, -250, (DZ + HZ) / 2 + 70) * Rot(0, -ang, 0) * Box(math.hypot(dx, dz), 20, 8)

    # 11 Guards over the bowl belt and pulleys and the chain
    guard = b(JX - dr - 15, CX + 70, -dr - 20, dr + 20, 175, 245) - \
        b(JX - dr - 9, CX + 64, -dr - 14, dr + 14, 181, 239)
    guard += b(PX - 115, JX + 45, 40, 80, 215, 445) - b(PX - 109, JX + 39, 44, 76, 221, 439)

    # 12 MotionCore module (243 x 168 x 66 mm, MTC-PRC-001) and reference 250 W geared hub motor
    motor = Pos(-100, 220, DZ) * Rot(90, 0, 0) * Cylinder(80, 60)
    motor += b(-130, -70, 190, 250, 265, 275)
    mcore = b(-420, -177, 120, 288, RZ - S - 66, RZ - S)

    # 13 Water header tank on a post, valve, flow meter and hose to the rotary union
    TX, TY = p["tank_x"], p["tank_y"]; tk0, tk1 = p["tank_z"]
    tank = c(TX, TY, tk0, tk1, p["tank_d"] / 2)
    water = b(TX - 10, TX + 10, TY - 200, TY - 180, 140, tk0) + b(TX - 25, TX + 25, TY - 215, TY - 165, 1050, 1150)
    water += b(TX, CX - 20, -20, 0, 140, 160) + b(TX - 10, TX + 10, -20, TY - 180, 140, 160)

    # 14 Shaking table deck with riffles, tilted toward the front (-Y)
    TBX0 = p["table_x0"]; TBX1 = TBX0 + p["table_l"]; TBW = p["table_w"]; TZ = p["table_z"]
    deck = b(TBX0, TBX1, -TBW / 2, TBW / 2, TZ - 18, TZ)
    for i in range(9):
        y = -TBW / 2 + 60 + i * 38
        deck += b(TBX0 + 60 + i * 30, TBX1 - 40, y, y + 6, TZ, TZ + 8)
    deck += b(TBX0, TBX0 + 180, TBW / 2 - 90, TBW / 2, TZ, TZ + 70)
    deck = Pos(0, 0, TZ) * Rot(p["table_tilt"], 0, 0) * Pos(0, 0, -TZ) * deck

    # 15 Table stand (flexure legs) and head motion
    tan_t = math.tan(math.radians(p["table_tilt"]))
    tstand = None
    for x in (TBX0 + 60, TBX1 - 80):
        for y in (-TBW / 2 + 20, TBW / 2 - 50):
            top = TZ - 18 + (y + 15) * tan_t - 3      # stop short of the deck underside (flexure mount)
            leg = b(x, x + 30, y, y + 30, 0, top)
            tstand = leg if tstand is None else tstand + leg
    # stretchers in the frame tube (25 x 25 x 1.5, GVS-DDR-002)
    tstand += b(TBX0 + 60, TBX1 - 50, -TBW / 2 + 20, -TBW / 2 + 20 + S, 150, 150 + S)
    tstand += b(TBX0 + 60, TBX1 - 50, TBW / 2 - 20 - S, TBW / 2 - 20, 150, 150 + S)
    tstand += b(FX1 + 20, TBX0 + 40, -90, 90, 640, 780) + b(TBX0 - 10, TBX0 + 60, -15, 15, 760, 800)
    tstand += b(FX1 + 60, FX1 + 60 + S, -80, 80, 0, 640) + b(FX1 + 30, FX1 + 120, -120, 120, 0, 20)
    tstand += Pos(HX, -170, HZ) * Rot(90, 0, 0) * Cylinder(12, 160)
    tstand += Pos(HX, -250, HZ) * Rot(90, 0, 0) * Cylinder(p["head_pulley_d"] / 2, 20)

    # 16 Concentrate launder and lockable tray
    tray = b(TBX0 + 150, TBX1 + 40, -TBW / 2 - 130, -TBW / 2 - 30, 600, 660) - \
        b(TBX0 + 156, TBX1 + 34, -TBW / 2 - 124, -TBW / 2 - 36, 606, 661)
    tray += b(TBX0 + 160, TBX0 + 190, -TBW / 2 - 100, -TBW / 2 - 60, 0, 600)
    tray += b(TBX1, TBX1 + 30, -TBW / 2 - 100, -TBW / 2 - 60, 0, 600)

    # 19 Bowl speed display: bicycle computer on the frame, magnet sensor at the spindle pulley
    speedo = b(CX - 30, CX + 30, -FY - 30, -FY, RZ - 60, RZ) + b(CX - 8, CX + 8, -70, -55, pz + 10, pz + 30)

    return [
        ("Base frame, welded steel tube", frame, "#4B5563", 1, (0, 0, -250)),
        ("Feed hopper, 2 mm screen, feed pipe", hopper, "#D97706", 2, (0, 0, 520)),
        ("Screen", screen, "#92400E", None, (0, 0, 620)),
        ("Centrifugal bowl with riffle rings", bowl, "#0F766E", 3, (0, 0, 360)),
        ("Fluidization jacket and rotary union", jacket, "#5EEAD4", 4, (0, 0, 250)),
        ("Rotary union", union, "#5EEAD4", None, (0, 0, -300)),
        ("Spindle, bearings and pulley", spindle, "#9CA3AF", 5, (0, 0, -150)),
        ("Splash tub and tailings outlet", tub, "#60A5FA", 6, (0, -150, 50)),
        ("Bowl lid guard", lid, "#1F2937", 7, (0, 0, 440)),
        ("Pedal station (seat, crank, chainring)", pedal, "#374151", 8, (-250, 0, -550)),
        ("Jackshaft, gearbox, chains, pulleys", jack, "#78716C", 9, (-100, -150, -300)),
        ("Drive belts (bowl and table)", belt, "#111827", 10, (0, -250, -450)),
        ("Belt and chain guards", guard, "#FACC15", 11, (0, -450, -420)),
        ("MotionCore module", mcore, "#15803D", 12, (150, -230, 260)),
        ("Reference hub motor", motor, "#166534", None, (0, 350, -250)),
        ("Water header tank, valve, flow meter", tank, "#38BDF8", 13, (0, 250, 380)),
        ("Water line", water, "#0EA5E9", None, (0, 250, 380)),
        ("Shaking table deck with riffles", deck, "#E5E7EB", 14, (300, 0, 330)),
        ("Table stand and head motion", tstand, "#6B7280", 15, (300, 0, 0)),
        ("Concentrate launder and lockable tray", tray, "#B45309", 16, (300, -300, 0)),
        ("Bowl brake", brake, "#DC2626", 18, (250, 0, -150)),
        ("Speed display", speedo, "#7C3AED", 19, (0, -250, 150)),
    ]


def assemblies(parts=None):
    """Named compounds for export: the whole machine, the rotating bowl group and the table deck."""
    import copy
    from build123d import Compound
    parts = parts or build_parts()
    # Sub-assemblies take copies: a build123d shape can have only one parent compound.
    by = {n: copy.copy(s) for n, s, *_ in parts}
    return {
        "gravitysort-assembly": Compound(children=[s for _, s, *_ in parts]),
        "gravitysort-bowl": Compound(children=[by["Centrifugal bowl with riffle rings"],
                                               by["Fluidization jacket and rotary union"]]),
        "gravitysort-table-deck": Compound(children=[by["Shaking table deck with riffles"]]),
    }


if __name__ == "__main__":
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    for name, shape in assemblies().items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    for z, r, ri in riffle_rings():
        print(f"riffle ring at z {z:.0f} mm: wall radius {r:.1f} mm, lip radius {ri:.1f} mm")
    print(f"frame tube {sum(l for _, l in frame_members()) / 1000:.2f} m")
