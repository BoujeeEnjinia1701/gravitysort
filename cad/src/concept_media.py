"""GravitySort concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the machine (pedal station at -X, shaking table at +X), Y front (-Y) to back (+Y),
Z up from the ground. Units mm. Geometry comes from cad/src/model.py, so the media match the
STEP files and drawing GVS-DWG-001. Numbers are printed by docs/04-calcs/sizing.py (GVS-CAL-001).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from concept import Part, render_all  # noqa: E402
from model import build_parts  # noqa: E402

parts = [Part(n, shape, colour, bom, ex) for n, shape, colour, bom, ex in build_parts()]

render_all(
    parts, project="GravitySort", title="Gravity concentrator concept", dwg_no="GVS-DWG-010", date="2026-10-01", rev="P3",
    key_figures=["Bowl 220 mm lip; 60 G at 730 rpm (40 to 80 G)",
                 "Feed 200 kg/h ore below 2 mm; 1.55 t per shift (est.)",
                 "Water 1.19 m3/h, recirculated; needs a pump (est.)",
                 "48 W at the pedals at 60 G; or 250 W motor (est.)",
                 "Disc brake; lid opens only with the brake set",
                 "Table 1000 x 450 mm; rubber bump stop",
                 "No mercury anywhere in the flowsheet",
                 "2.78 x 0.79 x 1.65 m, about 97 kg (est.)"],
    cut_exclude=("Water header tank, valve, flow meter, hose", "Belt and chain guards", "Speed display", "MotionCore module and motor option",
                 "Table stand, head and tensioner", "Table bump stop (21, 22)", "Tailings launder and concentrate box", "Shaking table deck with riffles"),
    flow={"title": "gold balance for one 8 h shift, 1.6 t of ore at 5 g/t (all values are estimates, GVS-CAL-001)",
          "unit": "g Au",
          "stages": [("Ore feed, milled", 8.0), ("Screened slurry", 7.6), ("Bowl concentrate", 5.4),
                     ("Table concentrate", 5.0), ("Smelted gold (borax)", 4.8)],
          "losses": [(0, "Oversize to regrind", 0.4), (1, "Bowl tailings", 2.2),
                     (2, "Table tailings, re-run", 0.4), (3, "Slag, re-smelt", 0.2)]},
)
