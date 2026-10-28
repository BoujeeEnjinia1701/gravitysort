"""GravitySort STEM check calculations (GVS-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv, which the STM document's claims table follows. Each row is a first-order
screen of one claim. The sizing itself is in the calculation note (GVS-CAL-001, docs/04-calcs/sizing.py), which
this script imports (it builds the model, so it takes about a minute) so that rows on the TRL 3 design close
against the same numbers. Options B and C (GVS-OPT-001) are screened with their own first-order figures below.
"""
import contextlib
import io
import math
import sys

sys.path.insert(0, ".kit")
from stem_check import Check, G, WITHIN, PLAUSIBLE, FIX, limits  # noqa: E402,F401

sys.path.insert(0, "docs/04-calcs")
with contextlib.redirect_stdout(io.StringIO()):
    import sizing as CAL  # noqa: E402  GVS-CAL-001, reads cad/src/model.py

P, A = CAL.P, CAL.A
c = Check()

# ------------------------------------------------------------------ option A: physics
g60 = CAL.gees(730, 0.100)
c.order_of_magnitude("S1", "The bowl gives about 60 G at the 100 mm reference radius at 730 rpm", "Physics", "Mechanics and statics",
                     claimed=60.0, estimate=g60, unit="G", law="Centripetal acceleration a = omega^2 r", closed_by="GVS-CAL-001 section 2")
c.claim("S2", "Fine gold reaches the bowl wall before it leaves: a 20 um gold flake crosses the 5 mm film well within the transit time",
        "Physics", "Fluid mechanics", "Terminal velocity in the centrifugal field with Schiller and Naumann drag; flake at half the sphere velocity",
        round(CAL.cap["gold 20 um flake"], 0), 1.0, "transit/settle ratio", rule="above", closed_by="GVS-CAL-001 section 5")
c.cited("S3", "The fluidized bed in the riffle rings keeps fine gold (80 % of 75 to 1,000 um, 50 % of 38 to 75 um; about 71 % of screened gold) while the bed is flushed every 2 h",
        "Physics", "Fluid mechanics",
        f"Fluidized centrifugal concentrators recover very fine gold over a wide size range (Veiga and Gunson 2020). The 2.7 mm/s upflow is about the minimum fluidization velocity of 75 um quartz at 60 G ({CAL.umf['quartz 75 um'] * 1000:.1f} mm/s, Wen and Yu) and well below that of coarser or denser grains ({CAL.umf['pyrite 150 um'] * 1000:.0f} mm/s for 150 um pyrite), so most of the bed is not fully fluidized; commercial bowls use 10 to 30 L/min at 35 to 100 kPa (iCON i150) against 12 L/min at about 10 kPa here; saturation by heavy minerals in the feed is not calculable",
        "Settling check passes (S2); retention needs a test with characterized or spiked ore (PR-004, TRL 4)", PLAUSIBLE, closed_by="")
net_mid = min(CAL.ring_dp(600, r / 1000, CAL.p_axis, z / 1000) for z, r, _ in CAL.rings)
c.order_of_magnitude("S4", "The 1.7 m header post gives the proposed 10 kPa net at every ring at 600 rpm with the tank half full, without a pump",
                     "Physics", "Fluid mechanics", claimed=10.0, estimate=net_mid / 1000, unit="kPa", factor=1.1,
                     law="Static head less hose, fittings and filter losses (Darcy-Weisbach, K factors), less the climb from the union to the ring (rho g dz), plus rho omega^2 r^2 / 2 in the jacket. v0.8 left out the climb (4.5 to 5.6 kPa) and had 6.0 kPa: fixed by 3/4 in valve and rotameter",
                     closed_by="GVS-DEC-001 F6; GVS-CAL-001 section 6")
c.claim("S5", "Water still enters every ring with the tank nearly empty and the filter at its cleaning point", "Physics", "Fluid mechanics",
        "Lowest net ring pressure at 600 rpm, tank 50 mm above its floor, filter K 6", round(CAL.net_dirty / 1000, 2), 0.0, "kPa", rule="above",
        closed_by="GVS-CAL-001 section 6; GVS-DEC-001 F2")
c.order_of_magnitude("S6", "Bringing the slurry and water to lip speed takes about 27 W at 730 rpm", "Physics", "Thermodynamics",
                     claimed=27.0, estimate=CAL.m_through * (CAL.rpm2w(730) * P["bowl_lip_d"] / 2000) ** 2, unit="W",
                     law="Power = m v^2 at the lip: half leaves as kinetic energy, half is lost in slip in the film (an upper bound); bowl and table never run together",
                     closed_by="GVS-CAL-001 section 7")
sf_min = min(CAL.sf[CAL.n_sprint])
c.claim("S7", "Bowl, jacket and rings keep a burst safety factor of at least 10 at 1,200 rpm (a sprinting rider)", "Physics", "Strength of materials",
        "Thin-wall hoop stress from jacket water pressure and self-weight; GFRP 80 MPa, PU 20 MPa (typical)", round(sf_min, 1), A["sf_min_sprint"], "safety factor",
        rule="above", closed_by="GVS-CAL-001 section 10")
c.cited("S8", "The spindle's first critical speed is well above the highest reachable bowl speed (1.25 x 1,200 rpm)", "Physics", "Acoustics and vibration",
        f"Cantilever 3EI/L^3 of the 25 x 2 mm tube gives {CAL.n_crit:.0f} rpm on rigid bearings; with the compliance of the 25 x 25 x 1.5 members the bearings hang from, magnified by the 210 mm overhang over the 165 mm bearing span, {CAL.n_crit_lo:.0f} rpm (member ends pinned) to {CAL.n_crit_hi:.0f} rpm (fixed)",
        "Above 900 rpm, the limit, in every case; against 1,500 rpm only if the members act nearly fixed. Tap test on the first frame at TRL 4 (GVS-DEC-001 O4)", PLAUSIBLE, closed_by="")
c.claim("S9", "The disc brake stops the bowl within the 15 s of PR-012", "Physics", "Mechanics and statics",
        "t = I omega / (T_brake + T_drag); bicycle disc, mu 0.4, 150 N per pad at 70 mm", round(CAL.t_brake, 2), 15.0, "s", closed_by="GVS-CAL-001 section 10")
c.cited("S10", "The 6 mm HDPE tub and 10 mm lid contain a fragment of the bowl thrown off at 900 to 1,200 rpm", "Physics", "Mechanics and statics",
        f"Oblique impact: normal share {CAL.f_n:.2f} of {0.5 * CAL.frag * (CAL.rpm2w(CAL.n_sprint) * CAL.r1) ** 2:.0f} J gives {CAL.contain[CAL.n_sprint]:.0f} J at 1,200 rpm and {CAL.contain[A['rpm_limit']]:.0f} J at 900 rpm into the wall; "
        f"plugging energy of the wall {CAL.e_flat:.0f} J face first, {CAL.e_edge:.0f} J edge first (dishing not counted); a quarter of the whole bowl group (review's bounding case) puts {CAL.e_all:.0f} J into the wall",
        "Not shown edge first, nor for the bounding case. Fix proposed: a 3 mm steel band (it breaks PR-011, so it goes to Amish, GVS-DEC-001 O2), or an impact test before any spin test", FIX, closed_by="")
c.claim("S11", "With a full tank the machine stands on a 10 degree slope in any direction", "Physics", "Mechanics and statics",
        "Tipping about the narrowest base (600 mm) with the frame-borne mass at 0.55 m and a full 64 kg tank on the post", round(CAL.th_now, 1), A["tip_slope_deg"],
        "degrees", rule="above", closed_by="GVS-CAL-001 section 11; GVS-DEC-001 2026-10-03")
c.claim("S12", "The spindle members carry the belt pull, rotor weight and unbalance with a safety factor of at least 1.5 on yield", "Physics", "Strength of materials",
        "Central point load on a pinned 600 mm span of 25 x 25 x 1.5 tube, S235", round(CAL.s_mem, 0), round(A["steel_yield_MPa"] / 1.5, 0), "MPa",
        closed_by="GVS-CAL-001 section 11")
c.claim("S13", "The tank post above the braces does not yield at the side push that tips the machine", "Physics", "Strength of materials",
        "Cantilever bending of 25 x 25 x 1.5 tube above the brace node", round(CAL.s_post, 0), round(A["steel_yield_MPa"] / 1.5, 0), "MPa", closed_by="GVS-CAL-001 section 11")
asym = CAL.bump[A["stop_start_mm"]]["ratio"]
c.claim("S14", "The rubber bump stop makes the table stroke asymmetric: the deck stops sharply at the far end and turns smoothly at the head end", "Physics",
        "Acoustics and vibration", "Impact of the 17 kg deck on a bonded rubber buffer (shape factor), against the harmonic turn at the head end",
        round(asym, 2), 2.0, "deceleration ratio", rule="above", closed_by="GVS-CAL-001 section 9")
c.cited("S15", "The shaking table reduces about 5.3 kg of bowl concentrate to 100 g or less in two passes (53:1)", "Physics", "Mechanics and statics",
        "Shaking tables reach concentration ratios of 28.8 to 170.9 (mean 66.7) at the MICA plant in Migori, Kenya (Mitchell et al. 2026); a 1,000 x 450 mm table on a heavy-mineral concentrate is not proven",
        "Two passes at 8:1 give 64:1 on paper (PR-005 at risk); test at TRL 4", PLAUSIBLE, closed_by="")
c.claim("S16", "The bump stop buffer works within its rating at the largest setting", "Engineering and technology", "Standards practice",
        "Peak buffer force at the 6 mm setting against the buffer's rated compression load (the BOM said 600 N; now 800 N, as GVS-CAL-001 section 9 chose)",
        round(CAL.bump[6.0]["F"], 0), 800.0 / 1.25, "N", closed_by="GVS-DEC-001 F3")
# ------------------------------------------------------------------ option A: mathematics
c.order_of_magnitude("S17", "A 61 rpm cadence turns the bowl at about 730 rpm through 48T/12T, 1:1 and 300/100", "Mathematics", "Units and dimensional analysis",
                     claimed=730.0, estimate=61 * CAL.ratio, unit="rpm", law="Product of the stage ratios", closed_by="GVS-CAL-001 section 2")
c.order_of_magnitude("S18", "A bicycle computer set to 1,667 mm reads bowl rpm divided by 10", "Mathematics", "Units and dimensional analysis",
                     claimed=73.0, estimate=730 * 1.667 * 60 / 1000, unit="km/h at 730 rpm", law="Speed = rpm x wheel size x 60 / 1000", closed_by="GVS-CAL-001 section 2")
c.balance("S19", "Water use is 1.19 m3/h: slurry water at 30 % solids plus 12 L/min of fluidization", "Mathematics", "Orders of magnitude",
          inputs={"PR-008 limit": 1.5}, outputs={"slurry water": CAL.mw_sl * 3.6, "fluidization": CAL.q_fl * 3600}, unit="m3/h",
          law="Mass balance of water", closed_by="GVS-CAL-001 section 4")
c.order_of_magnitude("S20", "The 60 L header drum holds 60 L as drawn", "Mathematics", "Units and dimensional analysis",
                     claimed=60.0, estimate=CAL.tank_l, unit="L", factor=1.1, law="Volume of the drawn drum (was 400 mm tall: 45 L)", closed_by="GVS-DEC-001 F1")
overall = (1 - A["oversize_loss"]) * A["bowl_rec"] * A["table_rec"] * A["smelt_rec"]
c.order_of_magnitude("S21", "The gold balance is consistent: 7.75 g in per shift on 5 g/t ore (1.55 t of feed), about 60 % smelted as the product of the assumed stage recoveries (the recoveries themselves are S3 and S15)", "Mathematics", "Statistics and uncertainty",
                     claimed=0.60, estimate=CAL.s4 / CAL.au, unit="fraction", factor=1.05,
                     law=f"Product of assumed stage recoveries ({overall:.3f}); gold in = grade x feed time (was the full 8 h: 8.0 g)", closed_by="GVS-DEC-001 F4; GVS-CAL-001 section 13")
c.order_of_magnitude("S22", "Each flush yields about 1.33 kg of concentrate, a mass pull of 0.33 %", "Mathematics", "Orders of magnitude",
                     claimed=1.33, estimate=CAL.flush_kg, unit="kg", law="Groove volume x 60 % fill x 2.5 kg/L wet bulk", closed_by="GVS-CAL-001 section 8")
# ------------------------------------------------------------------ option A: engineering
c.cited("S23", "With the motor the bowl cannot exceed 900 rpm", "Engineering and technology", "Control",
        "The 1.2:1 step-up is chosen from an assumed 250 rpm no-load motor speed (no datasheet), so the kinematic cap holds only if the motor's real no-load speed at full pack voltage is 250 rpm or less; MotionCore's own speed limit is the second cap",
        "To confirm against the motor datasheet when bought (GVS-DEC-001, to confirm item 10)", PLAUSIBLE, closed_by="")
c.cited("S24", "The fluidization water is clean enough for 1.0 mm holes: a screen filter stops grains that could block them", "Engineering and technology",
        "Standards practice", "Fluidization water must be clean (Veiga and Gunson 2020). The 120 mesh screen stops grains over 0.125 mm, an eighth of the hole size; silt finer than that and biofilm still pass, and the right ratio for silty pond water is not sourced here",
        "Flow through every ring after the filter to check at TRL 4 (BLD first checks)", PLAUSIBLE, closed_by="GVS-DEC-001 F2 (filter fitted)")
c.cited("S25", "A local workshop builds every part without a lathe; the liner is cast in a printed mold", "Engineering and technology", "Manufacturing tolerances",
        "Set-screw insert bearings, a taper bush and a welded nipple avoid turning (GVS-DDR-003); casting a Shore 85A PU liner on a six-segment printed core is common practice in PU shops but untried here",
        "Casting route to try at TRL 4 (PR-010)", PLAUSIBLE, closed_by="")
c.claim("S26", "A rider supplies 48 W at 60 G for sessions of about an hour, taking turns (the bowl and table never run together)", "Biology", "Human physiology and biomechanics",
        "Sustained pedalling by an average adult about 75 W (kit limit); at 80 G the 62.8 W is near it (PR-006 at risk)", round(CAL.p_ref, 1), limits.HUMAN_SUSTAINED_W, "W",
                     closed_by="GVS-CAL-001 section 7")
# ------------------------------------------------------------------ option A: chemistry and biology
c.cited("S27", "Direct smelting of the table concentrate with borax recovers the gold with no mercury", "Chemistry", "Inorganic",
        "Gold melts at 1,064 C; borax fluxes oxide and silicate gangue into a slag. Benguet miners smelt gravity concentrates with borax (Appel and Na-Oy 2012); the US EPA cites concentrates of about 50 to 100 g. A sulfide-rich (pyrite, arsenopyrite) concentrate can carry gold into a matte and fume arsenic, so it may need the sulfides removed or roasted first",
        "Depends on the partner's ore; smelting is outside the machine (RSK H10)", PLAUSIBLE, closed_by="")
c.cited("S28", "Mercury in old tailings would be concentrated by the bowl, so the machine must never process mercury-contaminated material", "Chemistry",
        "Environmental and atmospheric chemistry", "Liquid mercury (13.5 g/cm3) and amalgam are denser than quartz and report to any gravity concentrate",
        "A hazard, not a performance claim: kept as a safety rule in PRC, RSK and the README", WITHIN, closed_by="GVS-RSK-001")
c.cited("S29", "The cast PU liner lasts 500 h or more on quartz feed", "Chemistry", "Materials and polymer chemistry",
        "Elastomer and ceramic wear linings are used in commercial centrifugal concentrator bowls (a moulded rubber insert lasted 1.5 to 2 times the ceramic tiles at Detour Gold; Canadian Mining Journal 2014); life of this cast PU on this feed is unknown",
        "Wear data needed (PR-014, TRL 4)", PLAUSIBLE, closed_by="")
c.cited("S30", "Settling ponds and flooded pits near the machine can breed mosquitoes", "Biology", "Epidemiology",
        "Malaria transmission is linked to mining sites, where pits and ponds hold standing water (studies of mining workers in Muara Enim, Indonesia, Scientific Reports 2023, and of a malaria outbreak at illegal gold mining sites in French Guiana)",
        "A site risk: pond fencing, covering or draining with the partner (RSK H7)", WITHIN, closed_by="GVS-RSK-001")
c.cited("S31", "Heavy-mineral concentrates can carry arsenic (arsenopyrite) and lead; gloves and hand washing control the exposure at clean-up (smelter fume is the smelting step's hazard, RSK H10)", "Biology", "Toxicology",
        "Arsenopyrite is a common gold-bearing sulfide; arsenic is acutely and chronically toxic (WHO arsenic fact sheet)", "Safety rule in PRC and RSK", WITHIN,
        closed_by="GVS-RSK-001")

c.claim("S32", "The GFRP shell does not buckle under the full jacket's pressure with the bowl empty and the holes blocked, at 1,200 rpm", "Physics", "Strength of materials",
        "Windenburg-Trilling short-cylinder buckling of the 4 mm shell between the riffle rings (38 mm pitch), E = 7 GPa hand-laid GFRP, liner ignored (independent review's missing case)",
        round(CAL.p_ext / 1000, 0), round(CAL.p_cr / 1000 / 3, 0), "kPa", closed_by="GVS-CAL-001 section 10")
c.cited("S33", "A full tank on the 1.7 m post does not resonate with the table drive", "Physics", "Acoustics and vibration",
        f"Post above the brace node as a cantilever under the 64 kg tank: about {CAL.f_post:.1f} Hz, against the table at 4.0 to 5.0 Hz and the harmonics of the bump stop impacts (independent review); with the brace node raised to 1.6 m about 7.5 Hz",
        "Near resonance. Fix proposed: raise the brace node to 1.6 m (about +0.5 kg, which takes PR-011 over 100 kg) or run the table with the drum drained; to Amish (GVS-DEC-001 O3)", FIX, closed_by="")

# ------------------------------------------------------------------ option B: diaphragm jig (first-order figures, GVS-OPT-001)
bed_a = (0.300 - 0.004) ** 2                      # screen area, m2
dia_a = 0.190 ** 2 + 0.5 * (0.216 ** 2 - 0.190 ** 2)   # plate plus half the free annulus, m2
stroke = 0.012
w_stroke = dia_a * stroke / bed_a
c.claim("B1", "Option B: the 12 mm diaphragm stroke lifts the water over the ragging bed by at least 5 mm each pulse", "Physics", "Fluid mechanics",
        "Displaced volume = effective diaphragm area x stroke, spread over the screen area", round(w_stroke * 1000, 1), 5.0, "mm", rule="above",
        closed_by="GVS-OPT-001 (model: 190 mm plate in a 216 mm free opening)")
p_bed = 0.040 * 0.6 * 7850 * G                    # steel shot bed, 40 mm at 60 % packing, Pa
f_jig = 60 * 4 / 60                               # 240 strokes/min at a 60 rpm cadence, Hz
p_jig = 2 * p_bed * dia_a * stroke * f_jig / 0.839
c.order_of_magnitude("B2", "Option B: the pedal drives the jig with about 15 W", "Physics", "Thermodynamics", claimed=15.0, estimate=p_jig, unit="W",
                     law="Work to lift the bed pressure over the displaced volume, twice for losses, at 240 strokes/min", closed_by="GVS-OPT-001")
c.cited("B3", "Option B holds free gold coarser than about 0.1 mm but loses much of the finer gold", "Physics", "Fluid mechanics",
        "Jigs are not efficient for fine gold particles and need narrow size fractions (Veiga and Gunson 2020)", "Within known science; scored against UR-003 in OPT",
        WITHIN, closed_by="GVS-OPT-001")
q_hutch = 0.006 * bed_a * 3600                    # 6 mm/s upflow over the bed, m3/h
c.order_of_magnitude("B4", "Option B uses about 2.3 m3/h of water (hutch water at about 6 mm/s plus slurry water)", "Mathematics", "Orders of magnitude",
                     claimed=2.3, estimate=q_hutch + CAL.mw_sl * 3.6, unit="m3/h", law="Hutch upflow over the bed area plus slurry water; jigs need large amounts of water (Veiga and Gunson 2020)",
                     closed_by="GVS-OPT-001")
# ------------------------------------------------------------------ option C: sluice and pans
c.cited("C1", "Option C holds gold coarser than about 0.1 mm; recovery falls below 20 % for gold finer than 100 um", "Physics", "Fluid mechanics",
        "Sluice recovery drops to less than 20 % for grains finer than 100 um (Mitchell et al. 2026); good recovery of 105 to 212 um gold with expanded metal riffles (Poling and Hamilton, UBC pilot study)",
        "Within known science; scored against UR-003 in OPT", WITHIN, closed_by="GVS-OPT-001")
q_sl = A["feed_kg_h"] * (1 - 0.10) / 0.10 / 1000  # at 10 % solids, m3/h
c.order_of_magnitude("C2", "Option C uses about 2 m3/h of water running at about 10 % solids", "Mathematics", "Orders of magnitude", claimed=2.0, estimate=q_sl,
                     unit="m3/h", law="Water at 10 % solids by mass for 200 kg/h of solids; large sluices use far more (Veiga and Gunson 2020)", closed_by="GVS-OPT-001")
c.cited("C3", "Option C's concentrate (about 1 to 2 % of the feed, 15 to 30 kg per shift) is panned by hand to a smeltable 100 g", "Biology", "Ergonomics",
        "Sluices concentrate weakly (mean ratio 2.5 at Migori; Mitchell et al. 2026); panning tens of kilograms a day is hours of stooped work",
        "Plausible on paper; the labour is scored in OPT", PLAUSIBLE, closed_by="GVS-OPT-001 (not carried forward)")

if __name__ == "__main__":
    c.write()
