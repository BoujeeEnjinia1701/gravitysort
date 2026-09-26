"""GravitySort sizing calculations, GVS-CAL-001 v0.2 (TRL 3, decisions of GVS-DDR-002 applied).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.
Geometry comes from cad/src/model.py (PARAMS, riffle_rings, frame_members) and costs from
bom/bom.csv. All inputs are stated assumptions for a paper design; nothing here is measured.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, riffle_rings, frame_members, bowl_radius  # noqa: E402

G = 9.81
RHO_W, MU_W = 1000.0, 1.0e-3          # water at about 20 °C
RHO_AU, RHO_Q = 19300.0, 2650.0       # gold, quartz
RHO_AIR = 1.2

# ---------------------------------------------------------------- assumptions
A = {
    "feed_kg_h": 200.0,          # R2 design feed rate, dry solids
    "solids_frac": 0.30,         # slurry solids by mass
    "shift_h": 8.0,
    "flush_interval_h": 2.0,
    "flush_min": 5.0,            # R13 target
    "fluid_l_min": 12.0,         # fluidization water, mid-range
    "rpm_ref": 730.0, "rpm_lo": 600.0, "rpm_hi": 850.0, "rpm_limit": 900.0,
    "cadence_lo": 55.0, "cadence_hi": 70.0, "cadence_sprint": 100.0,
    "r_ref": 0.100,              # reference radius for G (R3)
    # drivetrain efficiencies
    "eta_chain": 0.97, "eta_jack_bearings": 0.99, "eta_bevel": 0.93, "eta_vbelt": 0.94,
    # spindle drag
    "T_bearing_Nm": 0.03,        # each contact-sealed insert bearing
    "T_union_Nm": 0.10,          # 1/2 in rotary union face seal (no datasheet yet)
    "P_air_W": 1.0,              # windage and splash allowance
    # motor option (MotionCore reference geared hub)
    "eta_motor_ctrl": 0.70,      # motor and controller at about 60 W, light load
    "motor_n0_rpm": 250.0,       # no-load speed at full pack voltage (assumed, no datasheet)
    "motor_load_frac": 0.85,     # loaded speed as a fraction of no-load
    "motor_P_W": 250.0,
    # bed and film in the bowl
    "bed_depth_m": 0.012, "bed_fill": 0.60, "bed_solids_rho": 4000.0, "bed_solids_vf": 0.50,
    "bed_bulk_kg_l": 2.5,        # retained concentrate, wet bulk
    "film_m": 0.005,
    "flake_factor": 0.5,         # flaky gold settles at about half the sphere velocity
    # fluidization supply
    "tank_level_m": 1.45, "union_height_m": 0.15,
    "hose_len_m": 4.0, "hose_d_m": 0.019, "hose_f": 0.03,
    "K_fittings": 6.0, "fittings_d_m": 0.0127,   # union, rotameter, valve on a 1/2 in bore
    "Cd_hole": 0.62,
    "p_target_kPa": 10.0,        # proposed minimum net pressure at every ring
    # table
    "table_ratio_per_pass": 8.0, "table_passes": 2,
    "table_moving_kg": 17.0, "table_stroke_m": 0.015, "table_friction_W": 10.0,
    # rotor materials
    "rho_pu": 1150.0, "rho_gfrp": 1800.0, "gfrp_strength_MPa": 80.0, "pu_strength_MPa": 20.0,
    "rho_steel": 7850.0,
    # brake
    "brake_mu": 0.4, "brake_pad_N": 150.0, "brake_r_m": 0.070,
    "rotor_kg": 0.12, "steel_cp": 460.0,
    "drive_pulley_kg": 2.5,
    # gold balance (reference ore)
    "grade_g_t": 5.0, "oversize_loss": 0.05, "bowl_rec": 0.71, "table_rec": 0.93, "smelt_rec": 0.96,
    # budget
    "budget_usd": 455.0, "budget_previous_usd": 450.0,     # 350 to 450 (GVS-DDR-002, 2026-09-25); 455 approved by Amish 2026-09-26
    "sf_min_sprint": 10.0,       # R12 as reworded: minimum burst safety factor at the sprint speed
    "steel_E_GPa": 200.0, "steel_yield_MPa": 235.0,
}

rows = []   # results table (id, quantity, value, target, status)
out = []


def say(s=""):
    out.append(s)
    print(s)


def rpm2w(n):
    return n * 2 * math.pi / 60


def gees(n, r):
    return rpm2w(n) ** 2 * r / G


# ---------------------------------------------------------------- 1. speed and G (R3)
ratio_chain = P["chainring_t"] / P["freewheel_t"]
ratio_belt = P["drive_pulley_d"] / P["driven_pulley_d"]
ratio = ratio_chain * P["bevel_ratio"] * ratio_belt
say("1. Speed and G (R3)")
say(f"  drive ratio pedal to bowl {ratio_chain:.0f} x {P['bevel_ratio']:.0f} x {ratio_belt:.0f} = {ratio:.0f}:1")
for n in (A["rpm_lo"], A["rpm_ref"], A["rpm_hi"]):
    say(f"  {n:.0f} rpm: {gees(n, A['r_ref']):.1f} G at 100 mm, cadence {n / ratio:.1f} rpm")
n_for = lambda g: math.sqrt(g * G / A["r_ref"]) * 60 / (2 * math.pi)
say(f"  40 G needs {n_for(40):.0f} rpm, 60 G {n_for(60):.0f} rpm, 80 G {n_for(80):.0f} rpm at 100 mm")
say(f"  cadence 55 to 70 rpm gives {A['cadence_lo'] * ratio:.0f} to {A['cadence_hi'] * ratio:.0f} rpm "
    f"({gees(A['cadence_lo'] * ratio, A['r_ref']):.0f} to {gees(A['cadence_hi'] * ratio, A['r_ref']):.0f} G)")
rings = riffle_rings()
for i, (z, r, ri) in enumerate(rings, 1):
    say(f"  ring {i}: wall radius {r:.1f} mm, {gees(A['rpm_ref'], r / 1000):.0f} G at 730 rpm, "
        f"{gees(A['rpm_lo'], r / 1000):.0f} to {gees(A['rpm_hi'], r / 1000):.0f} G over 600 to 850 rpm")
lip_v = rpm2w(A["rpm_ref"]) * P["bowl_lip_d"] / 2000
say(f"  lip speed at 730 rpm {lip_v:.2f} m/s; bicycle computer at 1667 mm reads {A['rpm_ref'] * 1.667 * 60 / 1000:.1f} (= rpm/10)")
rows.append(("R3", "Bowl G at 100 mm over the speed range", f"{gees(600, .1):.0f} to {gees(850, .1):.0f} G (600 to 850 rpm); speed display item 19",
             "40 to 80 G, speed shown", "Met (paper)"))

# ---------------------------------------------------------------- 2. throughput (R2)
say("\n2. Throughput (R2)")
stops = int(A["shift_h"] / A["flush_interval_h"]) - 1
feed_h = A["shift_h"] - stops * A["flush_min"] / 60
day_t = A["feed_kg_h"] * feed_h / 1000
need = 1600 / feed_h
say(f"  {stops} mid-shift flush stops of {A['flush_min']:.0f} min; feed time {feed_h:.2f} h")
say(f"  at 200 kg/h: {day_t:.2f} t per shift; 1.6 t needs {need:.0f} kg/h or {1.6e3 / A['feed_kg_h'] + stops * A['flush_min'] / 60:.2f} h")
rows.append(("R2", "Ore per 8 h shift", f"200 kg/h; {day_t:.2f} t per shift with {stops} flush stops", "200 kg/h, 1.6 t per 8 h",
             f"At risk (needs {need:.0f} kg/h)"))

# ---------------------------------------------------------------- 3. water (R8)
say("\n3. Water (R8)")
ms = A["feed_kg_h"] / 3600
mw_sl = ms * (1 - A["solids_frac"]) / A["solids_frac"]
q_fl = A["fluid_l_min"] / 60000
q_slurry = mw_sl / RHO_W + ms / RHO_Q
water_m3h = (mw_sl / RHO_W + q_fl) * 3600
rho_slurry = 1 / (A["solids_frac"] / RHO_Q + (1 - A["solids_frac"]) / RHO_W)
say(f"  slurry water {mw_sl * 3.6:.3f} m3/h; fluidization {q_fl * 3600:.2f} m3/h; total {water_m3h:.2f} m3/h, {water_m3h * feed_h:.1f} m3 per shift")
say(f"  slurry {q_slurry * 3.6e6 / 1000:.3f} m3/h at {rho_slurry:.0f} kg/m3; flow over the lip {(q_slurry + q_fl) * 1000:.3f} L/s")
tank_min = 60 / (water_m3h * 1000 / 60)
say(f"  60 L header tank lasts {tank_min:.1f} min at full flow; lift from pond to tank top about 1.7 m: "
    f"{RHO_W * G * 1.7 * water_m3h / 3600:.1f} W hydraulic")
rows.append(("R8", "Water use at 200 kg/h", f"{water_m3h:.2f} m3/h", "1.5 m3/h or less", "Met (paper)"))

# ---------------------------------------------------------------- 4. settling and capture (R4 plausibility)
say("\n4. Settling in the bowl (R4 plausibility check)")


def v_settle(d, rho_p, a):
    """Terminal velocity (m/s) of a sphere in water under acceleration a (Schiller-Naumann drag)."""
    v = (rho_p - RHO_W) * a * d * d / (18 * MU_W)
    for _ in range(200):
        re = max(RHO_W * v * d / MU_W, 1e-9)
        cd = 24 / re * (1 + 0.15 * re ** 0.687)
        v_new = math.sqrt(4 * (rho_p - RHO_W) * a * d / (3 * cd * RHO_W))
        v = 0.5 * v + 0.5 * v_new
    return v


a_ref = rpm2w(A["rpm_ref"]) ** 2 * A["r_ref"]
slant = math.hypot(P["bowl_depth"], (P["bowl_lip_d"] - P["bowl_base_d"]) / 2) / 1000
r_mean = (P["bowl_lip_d"] + P["bowl_base_d"]) / 4000
q_mean = q_slurry + q_fl / 2
v_film = q_mean / (2 * math.pi * r_mean * A["film_m"])
t_transit = slant / v_film
say(f"  a = {a_ref:.0f} m/s2 ({a_ref / G:.1f} G) at 100 mm; wall length {slant * 1000:.0f} mm; film {A['film_m'] * 1000:.0f} mm")
say(f"  mean film velocity {v_film:.3f} m/s; transit {t_transit:.1f} s")
cap = {}
for name, d, rho, k in (("gold 20 um flake", 20e-6, RHO_AU, A["flake_factor"]), ("gold 38 um flake", 38e-6, RHO_AU, A["flake_factor"]),
                        ("gold 38 um sphere", 38e-6, RHO_AU, 1.0), ("gold 75 um flake", 75e-6, RHO_AU, A["flake_factor"]),
                        ("quartz 38 um", 38e-6, RHO_Q, 1.0), ("quartz 150 um", 150e-6, RHO_Q, 1.0)):
    v = v_settle(d, rho, a_ref) * k
    t = A["film_m"] / v
    cap[name] = t_transit / t
    say(f"  {name}: {v * 1000:.0f} mm/s at {a_ref / G:.0f} G, crosses the film in {t * 1000:.0f} ms, transit/settle ratio {t_transit / t:.0f}")
groove_area = sum(2 * math.pi * r / 1000 * (P["ring_pitch"] - P["ring_t"]) / 1000 for _, r, _ in rings)
v_fl = q_fl / groove_area
say(f"  fluidization upflow {v_fl * 1000:.1f} mm/s through {groove_area:.3f} m2 of groove; "
    f"{v_fl / (v_settle(38e-6, RHO_Q, a_ref)) * 100:.0f} % of the settling velocity of 38 um quartz")
rows.append(("R4", "Fine-gold recovery", f"settling ratio {cap['gold 20 um flake']:.0f} or more for 20 um flakes; overall 60 % assumed",
             "80 % / 50 % in bowl; 60 % overall", "Not verifiable at TRL 3 (at risk)"))

# ---------------------------------------------------------------- 5. fluidization jacket and supply
say("\n5. Fluidization jacket and supply (R4, R8)")
v_hose = q_fl / (math.pi * A["hose_d_m"] ** 2 / 4)
v_fit = q_fl / (math.pi * A["fittings_d_m"] ** 2 / 4)
dp_hose = A["hose_f"] * A["hose_len_m"] / A["hose_d_m"] * RHO_W * v_hose ** 2 / 2
dp_fit = A["K_fittings"] * RHO_W * v_fit ** 2 / 2
p_static = RHO_W * G * (A["tank_level_m"] - A["union_height_m"])
p_axis = p_static - dp_hose - dp_fit
v_half = q_fl / (math.pi * 0.0127 ** 2 / 4)
dp_half = A["hose_f"] * A["hose_len_m"] / 0.0127 * RHO_W * v_half ** 2 / 2
say(f"  header head {p_static / 1000:.1f} kPa; 3/4 in hose loss {dp_hose / 1000:.1f} kPa; fittings {dp_fit / 1000:.1f} kPa; "
    f"pressure at the union {p_axis / 1000:.1f} kPa")
say(f"  with 1/2 in hose the hose loss is {dp_half / 1000:.1f} kPa and the union pressure {(p_static - dp_half - dp_fit) / 1000:.1f} kPa")
rho_bed = A["bed_solids_vf"] * A["bed_solids_rho"] + (1 - A["bed_solids_vf"]) * RHO_W


def ring_dp(n, r, p0):
    """Net pressure (Pa) across a fluidization hole at wall radius r (m): jacket minus loaded bed and film."""
    w2 = rpm2w(n) ** 2
    hb, hf = A["bed_depth_m"], A["film_m"]
    p_j = p0 + RHO_W * w2 * r * r / 2
    p_b = w2 * (rho_bed * hb * (r - hb / 2) + rho_slurry * hf * (r - hb - hf / 2))
    return p_j - p_b


hole_a = math.pi * (P["fluid_hole_d"] / 1000) ** 2 / 4
flows = []
for i, (z, r, _) in enumerate(rings, 1):
    dp = ring_dp(A["rpm_ref"], r / 1000, p_axis)
    q1 = A["Cd_hole"] * hole_a * math.sqrt(2 * max(dp, 0) / RHO_W)
    flows.append(q1)
    say(f"  ring {i}: net {dp / 1000:.1f} kPa at 730 rpm (bed full), {ring_dp(A['rpm_lo'], r / 1000, p_axis) / 1000:.1f} kPa at 600 rpm, "
        f"{q1 * 60000:.3f} L/min per 1.0 mm hole")
n_holes = q_fl / (sum(flows) / len(flows))
say(f"  holes of 1.0 mm for 12 L/min: about {n_holes:.0f} ({n_holes / len(rings):.0f} per ring); "
    f"lowest to highest ring flow per hole {flows[0] / flows[-1]:.2f}")
dp_min_rel = min(ring_dp(A["rpm_lo"], r / 1000, 0) for _, r, _ in rings)
p_need = A["p_target_kPa"] * 1000 - dp_min_rel
say(f"  supply pressure at the union for {A['p_target_kPa']:.0f} kPa net at every ring and 600 rpm: {p_need / 1000:.1f} kPa "
    f"({p_need / RHO_W / G + A['union_height_m'] + (dp_hose + dp_fit) / RHO_W / G:.2f} m tank level)")

# ---------------------------------------------------------------- 6. power (R6, R7)
say("\n6. Power (R6, R7)")
m_through = ms + mw_sl + q_fl * RHO_W
eta_ped = A["eta_chain"] * A["eta_jack_bearings"] * A["eta_bevel"] * A["eta_vbelt"]


def bowl_power(n):
    w = rpm2w(n)
    v = w * P["bowl_lip_d"] / 2000
    p_slurry = m_through * v * v
    p_drag = (2 * A["T_bearing_Nm"] + A["T_union_Nm"]) * w + A["P_air_W"] * (n / A["rpm_ref"]) ** 3
    return p_slurry, p_drag


pw = {}
for n in (A["rpm_lo"], A["rpm_ref"], A["rpm_hi"], A["cadence_sprint"] * ratio):
    ps, pd = bowl_power(n)
    pw[n] = (ps, pd, (ps + pd) / eta_ped)
    say(f"  {n:.0f} rpm: slurry and water {ps:.1f} W, drag {pd:.1f} W, at the pedals {(ps + pd) / eta_ped:.1f} W")
say(f"  mass through the bowl {m_through:.3f} kg/s; drivetrain efficiency {eta_ped:.3f}")
p_ref = pw[A["rpm_ref"]][2]; p_hi = pw[A["rpm_hi"]][2]
torque_crank = p_ref / rpm2w(A["rpm_ref"] / ratio)
say(f"  crank torque at 61 rpm cadence {torque_crank:.1f} N m")
rows.append(("R6", "Pedal power at full throughput", f"{p_ref:.1f} W at 60 G; {p_hi:.1f} W at 80 G", "60 W or less at 55 to 70 rpm",
             "At risk (met at 60 G, not at 80 G)"))
e_day = p_ref / A["eta_motor_ctrl"] * A["shift_h"] / 1000
margin = A["motor_P_W"] / p_ref
ratio_motor = A["rpm_limit"] / (ratio_belt * P["bevel_ratio"] * A["motor_n0_rpm"])
n_loaded = A["motor_n0_rpm"] * A["motor_load_frac"] * ratio_motor * ratio_belt
say(f"  motor margin {margin:.1f} x at 60 G, {A['motor_P_W'] / p_hi:.1f} x at 80 G; pack energy {e_day:.2f} kWh per shift")
say(f"  motor chain step-up for 900 rpm at no-load: {ratio_motor:.2f}:1; loaded bowl speed about {n_loaded:.0f} rpm")
rows.append(("R7", "Motor power margin", f"{margin:.1f} x at 60 G ({A['motor_P_W'] / p_hi:.1f} x at 80 G)", "3 x or more", "Met (paper)"))

# ---------------------------------------------------------------- 7. mass balance (R5)
say("\n7. Mass balance (R5)")
groove_vol = sum(2 * math.pi * r / 1000 * (P["ring_pitch"] - P["ring_t"]) / 1000 * P["ring_depth"] / 1000 for _, r, _ in rings)
flush_kg = groove_vol * 1000 * A["bed_fill"] * A["bed_bulk_kg_l"]
flushes = int(A["shift_h"] / A["flush_interval_h"])
pull = flush_kg / (A["feed_kg_h"] * A["flush_interval_h"]) * 100
bowl_day = flush_kg * flushes
table_ratio = A["table_ratio_per_pass"] ** A["table_passes"]
say(f"  groove volume {groove_vol * 1000:.2f} L; at {A['bed_fill']:.0%} fill and {A['bed_bulk_kg_l']} kg/L: {flush_kg:.2f} kg per flush")
say(f"  mass pull {pull:.2f} %; {flushes} flushes: {bowl_day:.1f} kg per shift")
say(f"  100 g needs a table ratio of {bowl_day * 1000 / 100:.0f}:1; assumed {A['table_passes']} passes at "
    f"{A['table_ratio_per_pass']:.0f}:1 = {table_ratio:.0f}:1 gives {bowl_day * 1000 / table_ratio:.0f} g")
rows.append(("R5", "Concentrate for direct smelting", f"bowl pull {pull:.2f} %; {bowl_day:.1f} kg/day needs {bowl_day * 10:.0f}:1 on the table",
             "0.5 % or less; 100 g or less", "At risk (table ratio needs two passes)"))

# ---------------------------------------------------------------- 8. table drive
say("\n8. Shaking table drive")
tr = P["head_pulley_d"]
k_table = ratio_chain * P["take_off_d"] / tr
say(f"  strokes/min = cadence x {k_table:.2f}: {A['cadence_lo'] * k_table:.0f} to {A['cadence_hi'] * k_table:.0f} at 55 to 70 rpm; "
    f"240 to 300 needs {240 / k_table:.0f} to {300 / k_table:.0f} rpm")
f_t = 270 / 60
v_pk = 2 * math.pi * f_t * A["table_stroke_m"] / 2
p_table = 2 * 0.5 * A["table_moving_kg"] * v_pk ** 2 * f_t + A["table_friction_W"]
say(f"  270 strokes/min, {A['table_stroke_m'] * 1000:.0f} mm stroke: peak speed {v_pk:.2f} m/s, about {p_table:.0f} W at the head, "
    f"{p_table / (A['eta_chain'] * A['eta_vbelt']):.0f} W at the pedals")

# ---------------------------------------------------------------- 9. rotor safety (R12)
say("\n9. Rotor safety: inertia, burst, spindle, brake (R12)")
t_l, t_s, gap, jt = P["liner_t"] / 1000, P["shell_t"] / 1000, P["jacket_gap"] / 1000, P["jacket_t"] / 1000
alpha = math.atan(((P["bowl_lip_d"] - P["bowl_base_d"]) / 2) / P["bowl_depth"])


def shell_ring(offset, thick, rho, z_top=None):
    """Mass (kg) and inertia (kg m2) of a conical layer at a radial offset from the liner surface."""
    z0 = P["bowl_z0"]; z1 = z_top or z0 + P["bowl_depth"]
    n = 60; m = i = 0.0
    for k in range(n):
        z = z0 + (k + 0.5) * (z1 - z0) / n
        r = bowl_radius(z) / 1000 + offset
        dA = 2 * math.pi * r * (z1 - z0) / n / 1000 / math.cos(alpha)
        dm = rho * thick * dA
        m += dm; i += dm * r * r
    rb = P["bowl_base_d"] / 2000 + offset
    mb = rho * thick * math.pi * rb * rb
    return m + mb, i + mb * rb * rb / 2


jz1 = P["bowl_z0"] + P["bowl_depth"] - 30
parts_i = {
    "liner": shell_ring(t_l / 2, t_l, A["rho_pu"]),
    "shell": shell_ring(t_l + t_s / 2, t_s, A["rho_gfrp"]),
    "jacket": shell_ring(t_l + t_s + gap + jt / 2, jt, A["rho_gfrp"], jz1),
    "jacket water": shell_ring(t_l + t_s + gap / 2, gap, RHO_W, jz1),
}
ring_m = sum(A["rho_pu"] * 2 * math.pi * (r - P["ring_depth"] / 2) / 1000 * P["ring_depth"] / 1000 * P["ring_t"] / 1000 for _, r, _ in rings)
ring_i = sum(A["rho_pu"] * 2 * math.pi * (r / 1000) ** 3 * P["ring_depth"] / 1000 * P["ring_t"] / 1000 for _, r, _ in rings)
parts_i["rings"] = (ring_m, ring_i)
conc_i = sum(flush_kg / len(rings) * ((r - 6) / 1000) ** 2 for _, r, _ in rings)
parts_i["concentrate"] = (flush_kg, conc_i)
parts_i["hub and fittings"] = (0.5, 0.5 * 0.03 ** 2)
m_rot = sum(m for m, _ in parts_i.values()); I_rot = sum(i for _, i in parts_i.values())
I_drive = 0.5 * A["drive_pulley_kg"] * (P["drive_pulley_d"] / 2000) ** 2 / ratio_belt ** 2
I_tot = I_rot + I_drive
for k, (m, i) in parts_i.items():
    say(f"  {k}: {m:.2f} kg, {i * 1000:.2f} g m2")
say(f"  rotating bowl group {m_rot:.2f} kg, I = {I_rot:.4f} kg m2; drive side reflected {I_drive:.4f}; total {I_tot:.4f} kg m2")
ke = {n: 0.5 * I_tot * rpm2w(n) ** 2 for n in (A["rpm_ref"], A["rpm_hi"], A["rpm_limit"], A["cadence_sprint"] * ratio)}
for n, e in ke.items():
    say(f"  kinetic energy at {n:.0f} rpm: {e:.0f} J")

n_proof = 1.2 * A["rpm_limit"]; n_sprint = A["cadence_sprint"] * ratio
say(f"  burst checks at 1.2 x 900 = {n_proof:.0f} rpm and at a 100 rpm sprint cadence = {n_sprint:.0f} rpm")
r_jo = bowl_radius(jz1) / 1000 + t_l + t_s + gap
r_top = rings[-1][1] / 1000
sf = {}
for n in (n_proof, n_sprint):
    w2 = rpm2w(n) ** 2
    p_j = p_axis + RHO_W * w2 * r_jo ** 2 / 2
    s_j = p_j * r_jo / (jt * math.cos(alpha)) + A["rho_gfrp"] * w2 * (r_jo + jt / 2) ** 2
    p_in = w2 * (A["rho_pu"] * t_l * (r_top + t_l / 2) + rho_bed * A["bed_depth_m"] * r_top + rho_slurry * A["film_m"] * (r_top - A["bed_depth_m"]))
    r_s = r_top + t_l + t_s / 2
    s_s = p_in * r_s / (t_s * math.cos(alpha)) + A["rho_gfrp"] * w2 * r_s ** 2
    s_pu = A["rho_pu"] * w2 * (r_top + t_l) ** 2
    a_along = w2 * r_top * math.sin(alpha)
    w_lip = rho_bed * (P["ring_pitch"] - P["ring_t"]) / 1000 * A["bed_depth_m"] * a_along
    s_lip = w_lip * A["bed_depth_m"] / 2 / ((P["ring_t"] / 1000) ** 2 / 6)
    sf[n] = (A["gfrp_strength_MPa"] / (s_j / 1e6), A["gfrp_strength_MPa"] / (s_s / 1e6), A["pu_strength_MPa"] / (s_lip / 1e6))
    say(f"  {n:.0f} rpm: jacket water {p_j / 1000:.0f} kPa, jacket hoop {s_j / 1e6:.1f} MPa (SF {sf[n][0]:.0f}); "
        f"shell with jacket empty {p_in / 1000:.0f} kPa, hoop {s_s / 1e6:.1f} MPa (SF {sf[n][1]:.0f}); "
        f"liner free hoop {s_pu / 1e6:.2f} MPa; ring lip bending {s_lip / 1e6:.2f} MPa (SF {sf[n][2]:.0f})")
frag = 0.25 * (parts_i["liner"][0] + parts_i["shell"][0])
v_frag = rpm2w(n_sprint) * (P["bowl_lip_d"] / 2000 + t_l + t_s)
say(f"  quarter of liner and shell {frag:.2f} kg at {v_frag:.1f} m/s: {0.5 * frag * v_frag ** 2:.0f} J (containment by tub and lid not verified)")

# spindle bending and critical speed
d_sp = P["spindle_d"] / 1000
belt_pull = 300.0
overhang = (P["bearing_z"][0] + P["bearing_h"] / 2 - (P["pulley_z"] + 20)) / 1000
M = belt_pull * overhang
s_sp = 32 * M / (math.pi * d_sp ** 3)
I_sec = math.pi * d_sp ** 4 / 64
L_c = ((P["bowl_z0"] + P["bowl_depth"] / 2) - (P["bearing_z"][1] + P["bearing_h"])) / 1000
m_over = m_rot + 1.0
k_sp = 3 * 193e9 * I_sec / L_c ** 3
n_crit = math.sqrt(k_sp / m_over) * 60 / (2 * math.pi)
say(f"  spindle: belt pull {belt_pull:.0f} N at {overhang * 1000:.0f} mm overhang, {s_sp / 1e6:.0f} MPa bending; "
    f"bowl {L_c * 1000:.0f} mm above the upper bearing, first critical about {n_crit:.0f} rpm ({n_crit / n_sprint:.1f} x the sprint speed)")
unb = 0.05 * 0.1 * rpm2w(A["rpm_ref"]) ** 2
say(f"  50 g of uneven concentrate at 100 mm: {unb:.0f} N rotating load at 730 rpm")

# coast-down and brake
T_f = 2 * A["T_bearing_Nm"] + A["T_union_Nm"]
c_w = q_fl * RHO_W * (P["bowl_lip_d"] / 2000) ** 2          # water leaving at the lip: torque = c_w * omega
tau = I_tot / c_w
w0 = rpm2w(A["rpm_hi"])
t_coast = tau * math.log(1 + w0 * c_w / T_f)
t_coast_dry = I_tot * w0 / T_f
T_brake_max = 2 * A["brake_mu"] * A["brake_pad_N"] * A["brake_r_m"]
t_brake = I_tot * w0 / (T_brake_max + T_f)
T_15 = I_tot * w0 / 15 - T_f
dT = ke[A["rpm_hi"]] / (A["rotor_kg"] * A["steel_cp"])
say(f"  coast from 850 rpm: {t_coast:.0f} s with fluidization water running, {t_coast_dry:.0f} s with water off")
say(f"  disc brake at {A['brake_pad_N']:.0f} N pad force: {T_brake_max:.1f} N m, stop in {t_brake:.1f} s; "
    f"a 15 s stop needs only {max(T_15, 0):.2f} N m; rotor warms {dT:.1f} K per stop")
say(f"  pedal speed: 900 rpm at a cadence of {A['rpm_limit'] / ratio:.0f} rpm; gearing does not cap the pedal speed")
sf_min = min(sf[n_sprint])
say(f"  R12 as reworded (GVS-DDR-002): lowest burst safety factor at {n_sprint:.0f} rpm is {sf_min:.0f} "
    f"(required {A['sf_min_sprint']:.0f}); speed display fitted; brake stop {t_brake:.1f} s")
ok12 = sf_min >= A["sf_min_sprint"] and t_brake <= 15
rows.append(("R12", "Guards, speed limit, stop time", f"brake stop {t_brake:.1f} s (coast {t_coast:.0f} s); motor capped by ratio and MotionCore; "
             f"pedal: SF {sf_min:.0f} at {n_sprint:.0f} rpm, speed display", "guarded; motor 900 rpm or less; pedal SF 10 or more at sprint speed with display; stop within 15 s",
             "Met (paper); containment not verified" if ok12 else "Not met"))

# ---------------------------------------------------------------- 10. mass and size (R11)
say("\n10. Mass and size (R11)")
tube_m = sum(l for _, l in frame_members()) / 1000
kg_m = (P["tube"] ** 2 - (P["tube"] - 2 * P["tube_wall"]) ** 2) * 1e-6 * A["rho_steel"]
kg_m_old = (30 ** 2 - 26 ** 2) * 1e-6 * A["rho_steel"]      # TRL 3 v0.1: 30 x 30 x 2 mm
tub_kg = 950 * P["tub_t"] / 1000 * (math.pi * P["tub_d"] / 1000 * (P["tub_z"][1] - P["tub_z"][0]) / 1000 + math.pi * (P["tub_d"] / 2000) ** 2)
lid_kg = 950 * P["lid_t"] / 1000 * math.pi * (P["tub_d"] / 2000 + 0.008) ** 2
bowl_dry = m_rot - parts_i["jacket water"][0] - parts_i["concentrate"][0]
loads = {
    "1 Base frame with spindle, bearings, brake, union": {"frame tube": tube_m * kg_m, "spindle": 1.6, "bearing units": 2.0,
                                                        "driven pulley": 0.4, "brake": 0.5, "rotary union": 0.5, "speed display": 0.1},
    "2 Drive and pedal station": {"jackshaft and bearings": 2.6, "bevel gearbox": 3.0, "drive pulley": A["drive_pulley_kg"],
                                  "sprockets, chains, take-off pulley": 1.8, "belts": 0.4, "guards": 2.0,
                                  "pedal station": 2.7 * kg_m + 2.5},
    "3 Bowl, jacket, tub, lid, hopper": {"bowl and jacket (dry)": bowl_dry, "splash tub": tub_kg, "lid guard": lid_kg,
                                         "hopper, screen, feed pipe": 2.5, "launder": 0.5},
    "4 Table deck": {"plywood": 1.0 * 0.45 * 0.018 * 600, "HDPE facing": 1.0 * 0.45 * 0.003 * 950, "riffles and feed box": 1.1},
    "5 Table stand, head, tray": {"legs and stretchers": 5.6 * 0.8 + 2 * 0.95 * kg_m, "head box": 1.87, "head post": 0.64 * kg_m,
                                  "eccentric, pulley, pitman": 2.0, "launder and tray": 4.5},
    "6 Water tank and hoses": {"60 L drum": 3.0, "valve, rotameter, hoses": 2.0},
}
tot = 0.0; heaviest = 0.0
for name, items in loads.items():
    m = sum(items.values()); tot += m; heaviest = max(heaviest, m)
    say(f"  load {name}: {m:.1f} kg")
tot += 2.0
say(f"  hardware 2.0 kg; total {tot:.1f} kg; heaviest load {heaviest:.1f} kg; frame tube {tube_m:.2f} m at {kg_m:.2f} kg/m")
tube_other = 2.7 + 2 * 0.95 + 0.64          # pedal outrigger, table stretchers, table head post (m)
saved = (tube_m + tube_other) * (kg_m_old - kg_m)
say(f"  25 x 25 x 1.5 mm tube at {kg_m:.2f} kg/m against 30 x 30 x 2 mm at {kg_m_old:.2f} kg/m saves {saved:.1f} kg "
    f"({tube_m:.2f} m frame, {tube_other:.2f} m pedal outrigger, table stretchers and head post); total was {tot + saved:.1f} kg")
# frame member check: spindle bearing member, 600 mm span, carries belt pull and the rotating group
S_t, t_w = P["tube"], P["tube_wall"]
I_t = (S_t ** 4 - (S_t - 2 * t_w) ** 4) / 12          # mm4
Z_t = I_t / (S_t / 2)
span = 2 * P["frame_y"]
F_mem = 300.0 + (m_rot + 3.0) * G + 29.0             # belt pull, rotor and spindle weight, unbalance
M_mem = F_mem * span / 4                              # N mm, central point load, simply supported
s_mem = M_mem / Z_t
d_mem = F_mem * span ** 3 / (48 * A["steel_E_GPa"] * 1e3 * I_t)
say(f"  spindle bearing member {S_t:.0f} x {S_t:.0f} x {t_w} mm over {span:.0f} mm: {F_mem:.0f} N central load, "
    f"{s_mem:.0f} MPa bending (SF {A['steel_yield_MPa'] / s_mem:.1f} on {A['steel_yield_MPa']:.0f} MPa), deflection {d_mem:.2f} mm (pinned ends, upper bound)")
try:
    from model import assemblies
    bb = assemblies()["gravitysort-assembly"].bounding_box()
    size = f"{bb.size.X / 1000:.2f} x {bb.size.Y / 1000:.2f} x {bb.size.Z / 1000:.2f} m"
except Exception as e:  # pragma: no cover
    size = f"(model not built: {e})"
say(f"  overall size {size}")
st = "Met (paper)" if tot <= 80 and heaviest <= 30 else ("Not met" if tot > 80 else "At risk")
rows.append(("R11", "Transport mass", f"{tot:.0f} kg total in 6 loads, heaviest {heaviest:.0f} kg", "80 kg or less; loads 30 kg or less", st))

# ---------------------------------------------------------------- 11. cost (R9)
say("\n11. Cost (R9)")
total = 0.0; excl = 0.0
with open(ROOT / "bom/bom.csv", newline="") as f:
    for r in csv.DictReader(f):
        c = float(r["qty"]) * float(r["unit_cost_usd"])
        total += c
        if r["unit_cost_usd"] in ("", None):
            raise SystemExit("unpriced BOM line")
say(f"  BOM total ${total:.0f} (MotionCore $335 and battery excluded)")
say(f"  against ${A['budget_usd']:.0f}: {total - A['budget_usd']:+.0f} ({(total / A['budget_usd'] - 1) * 100:+.1f} %); "
    f"against the former ${A['budget_previous_usd']:.0f}: {total - A['budget_previous_usd']:+.0f}")
rows.append(("R9", "Parts cost", f"${total:.0f}", f"${A['budget_usd']:.0f} or less", "Met (paper)" if total <= A["budget_usd"] else
             f"Not met (${total - A['budget_usd']:.0f} over)"))

# ---------------------------------------------------------------- 12. gold balance
say("\n12. Gold balance (reference ore, estimates)")
au = A["grade_g_t"] * A["feed_kg_h"] * A["shift_h"] / 1000
s1 = au * (1 - A["oversize_loss"]); s2 = s1 * A["bowl_rec"]; s3 = s2 * A["table_rec"]; s4 = s3 * A["smelt_rec"]
say(f"  gold in {au:.1f} g; screened {s1:.1f}; bowl {s2:.1f}; table {s3:.1f}; smelted {s4:.1f} g; overall {s4 / au * 100:.0f} %")
say(f"  losses: oversize {au - s1:.1f}, bowl tailings {s1 - s2:.1f}, table tailings {s2 - s3:.1f}, slag {s3 - s4:.1f} g")

# ---------------------------------------------------------------- design-review requirements
rows += [
    ("R1", "No mercury", "no amalgamation step in the flowsheet", "no mercury at any step", "Met (design review)"),
    ("R10", "Local workshop build", "welding, drill press, printed mold; set-screw inserts and taper bush, no lathe", "no lathe", "Met (design review); casting route unproven"),
    ("R13", "Quick, secure clean-up", "toolless lid clamps; flush into lockable container; lockable tray", "5 min, no tools", "Met (paper); time not verified"),
    ("R14", "Liner life", "no wear data for this PU on quartz", "500 h; replace in 30 min", "Not verifiable at TRL 3"),
]
order = {f"R{i}": i for i in range(1, 15)}
rows.sort(key=lambda r: order[r[0]])
with open(Path(__file__).with_name("results.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "quantity", "value", "target", "status"])
    w.writerows(rows)
say("\nResults")
for r in rows:
    say(f"  {r[0]:>4}  {r[4]:<45} {r[2]}")
