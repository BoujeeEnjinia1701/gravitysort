"""GravitySort product model for Cycles renders (STANDARDS sections 12 and 24), TRL 3, kit 1.9.1.

Every product part is components(CHOSEN) from cad/src/model.py as it is: the D3 model of option A, the
constructable design of GVS-DDR-003 with the STEM fixes of 2026-10-25 (GVS-DEC-001 F1 to F5): the welded frame
of 25 x 25 x 1.5 mm tube with its weld beads, the braced 1.7 m post and the 560 mm header drum, the bowl, jacket,
spindle, bearings, brake, drive, guards, pedal station, MotionCore option, screen filter, the shaking table with
its head, bump stop and pitman, the concentrate box, the flush container and every bolt, nut, washer, pin and
screw. Only context is added: a heap of milled ore beside the hopper (site) and a 1.75 m mannequin standing on
the ground at the pedal end (scale). The site itself (wet mud, sky and sun) is the photoreal outdoor scene, with
ground level at model z = 0 (RENDER_VIEWS "args"); the ore heap reaches below it.

Groups: "shell" (frame, guards, tub, lid, hopper, water, table and everything outside), "internal" (the rotating
bowl group, spindle, bearings, brake, belts, gearbox and jackshaft: the detail view), "accessory" (the loose
flush container) and "context" (ore heap, mannequin). APPEARANCE AND DESIGN MODEL ARE THE SAME GEOMETRY; no
appearance deviation from model.py. CONCEPT, NOT FOR FABRICATION.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

import model as M  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402
from build123d import Cone, Pos, Rot  # noqa: E402

TITLE = "GravitySort: mercury-free gold concentrator with centrifugal bowl and shaking table"

_SITE = ["--scene=outdoor", "--ground=mud", "--ground-z=0", "--water=-8", "--sun=42,-20", "--lens=40"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 18, "az": -38,
     "args": _SITE,
     "note": "Site render on wet mud at a mining camp, from the front right and a little above (about 18 deg elevation): "
             "shaking table nearest, centrifuge with hopper and lid in the middle under the 60 L drum on its braced 1.7 m "
             "post, flush container on the ground in front, a heap of milled ore behind, and a 1.75 m person standing at "
             "the pedal end for scale"},
    {"name": "studio", "groups": ["shell", "internal", "accessory"], "explode": False, "el": 24, "az": -55,
     "note": "Studio render from the front right and above (about 24 deg elevation): the whole machine with every "
             "bolt and weld bead, pedal station at left, centrifuge and drum in the middle, shaking table at right"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): hopper and screen, lid, bowl, "
             "jacket and tub over the frame; spindle, brake and drive below; pedal station at left; water drum above; "
             "shaking table, head, bump stop, launder and concentrate box at right; flush container in front"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 22, "az": -40,
     "note": "Detail from the front right and above (about 22 deg elevation), without frame, guards or tub: bowl with "
             "riffle rings in its fluidization jacket, hub and bowl bolts, spindle, bearing units, brake disc and caliper, "
             "the V-belt from the gearbox pulley, and the jackshaft with its freewheel and table take-off pulley"},
]

INTERNAL_KEYS = ("Bowl liner", "Bowl shell", "Fluidization jacket", "Shaft flange hub", "bowl to hub", "Spacer bush",
                 "cast-in nut", "Spindle", "bearing unit", "Driven pulley", "Rotary union", "Brake flange", "Brake disc",
                 "disc to flange", "disc caliper", "Bowl belt", "Drive pulley", "Gearbox output shaft", "bevel gearbox",
                 "Jackshaft", "Freewheel", "take-off pulley", "Motor sprocket")


def _group(p):
    n = p["name"]
    if p.get("bom") == 23:
        return "accessory"
    if any(k in n for k in INTERNAL_KEYS):
        return "internal"
    return "shell"


def context():
    """A heap of milled ore behind the hopper (site, reaching below ground) and a mannequin at the pedal end."""
    out = []
    heap = Pos(-120, 820, -120) * Cone(520, 60, 420, align=None)
    out.append(part("Heap of milled ore (site)", break_edges(heap, 20), "sand", kind="context", group="context"))
    try:
        import context_parts
        man = Pos(-980, -520, 0) * Rot(0, 0, 150) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context":
            continue
        q = dict(p)
        q["group"] = _group(p)
        if p.get("bom") == 23:
            q["explode"] = (0, -600, 0)      # clears the table belt guard in the exploded render
        out.append(q)
    return out + context()


if __name__ == "__main__":
    ps = product_parts()
    from collections import Counter
    print(len(ps), "parts;", dict(Counter(p["group"] for p in ps)))
