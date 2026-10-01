"""GravitySort general arrangement drawing GVS-DWG-001 (Rev P4, constructable design GVS-DDR-003 with the table bump stop).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/GVS-DWG-001.svg, .pdf and .png from the parametric model.
The concept blueprint keeps GVS-DWG-010 (media/concept-blueprint).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assemblies, build_parts  # noqa: E402

parts = build_parts()
asm = assemblies(parts)["gravitysort-assembly"]
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="GravitySort", title="General arrangement, gravity concentrator", dwg_no="GVS-DWG-001",
          rev="P4", author="Amish Chadha", date="2026-10-01", concept=True,
          material="Frame 25 x 25 x 1.5 steel tube; bowl PU on GFRP; tub HDPE. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the TRL 3 model (GVS-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Frame 25 x 25 x 1.5 tube; mass 77 kg (GVS-DDR-002)", "2026-09-25", "AC"),
                     ("P3", "Constructable design; mass 96 kg (GVS-DDR-003)", "2026-10-01", "AC"),
                     ("P4", "Table bump stop added; mass 97 kg (GVS-DDR-003 A2)", "2026-10-01", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 37, 140, 74, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions and interfaces (mm)", [
    "Overall 2780 x 790 x 1650; about 97 kg in 6 loads (est.)",
    f"Frame {P['frame_x1'] - P['frame_x0']:.0f} x {2 * P['frame_y']:.0f} x {P['rail_z']:.0f}, {P['tube']:.0f} x {P['tube']:.0f} x {P['tube_wall']} tube",
    f"Bowl lip {P['bowl_lip_d']:.0f}, base {P['bowl_base_d']:.0f}, depth {P['bowl_depth']:.0f}; 4 rings, pitch {P['ring_pitch']:.0f}",
    f"Liner {P['liner_t']:.0f} PU on {P['shell_t']:.0f} GFRP; jacket gap {P['jacket_gap']:.0f}; about 89 holes 1.0",
    f"Spindle {P['spindle_d']:.0f} x {P['spindle_wall']:.0f} stainless tube, 2 x UCF205; 1/2 in union",
    "Drive 48T/12T chain, 1:1 bevel, 300/100 belt = 12:1",
    "730 rpm (60 G at r 100) at 61 rpm cadence; limit 900 rpm",
    f"Brake: {P['brake_rotor_d']:.0f} disc, parking latch, lid pin interlock",
    f"Tub {P['tub_d']:.0f} HDPE, lid {P['lid_t']:.0f} HDPE; tank 60 L on 1250 post",
    f"Table {P['table_l']:.0f} x {P['table_w']:.0f}, tilt {P['table_tilt']:.0f} deg; head pulley {P['head_pulley_d']:.0f}",
    "Table bump stop: 40 x 30 rubber buffer, set 3 (2 to 6) in",
    "Motor option on a cradle at the back, step-up 1.2:1",
    "Making sketches GVS-DWG-101 to 121 (GVS-BLD-001)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=122, width=140)
s.save(ROOT / "cad/drawings/GVS-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/GVS-DWG-001.svg, .pdf, .png")
