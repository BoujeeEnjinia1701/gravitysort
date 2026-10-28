"""GravitySort repo-specific CAD helpers for the kit 1.9 detailed model (STANDARDS section 24).

These sit beside .kit/cad_parts.py and are candidates for a future kit release (see docs/REVIEW.md):

    tube_box()      a square hollow section (cad_parts.shs) filling an axis-aligned box, along its long side
    tube_between()  a square hollow section between two points, with a chosen face direction
    bead()          a cad_parts.weld_fillet bead along any edge, legs on any two perpendicular faces
    end_welds()     fillet beads round the end of a square tube that butts onto a flat face
    bolt()          a cad_parts.hex_bolt_set placed along any axis, with the hole it needs
    screw()         a bolt with no nut (tapped hole, cast-in insert or timber), with its hole
    cut_holes()     drill every recorded hole through the made and bought parts it passes through

All sizes in millimetres. Axes as model.py: X along the machine, Y front (-Y) to back (+Y), Z up.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Plane, Pos, Vector  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402

AXES = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}


def _v(a):
    return Vector(*a)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _perp(u):
    """A global axis perpendicular to u (for the x direction of a plane whose z is u)."""
    for c in ((0, 0, 1), (0, 1, 0), (1, 0, 0)):
        if abs(sum(i * j for i, j in zip(c, u))) < 0.9:
            x = _cross(c, u)
            n = math.sqrt(sum(i * i for i in x))
            return tuple(i / n for i in x)
    raise ValueError(u)


def tube_box(x0, x1, y0, y1, z0, z1, wall=1.5):
    """Square (or rectangular) hollow section filling the box, running along its longest side."""
    d = {"x": x1 - x0, "y": y1 - y0, "z": z1 - z0}
    ax = max(d, key=d.get)
    w, h = [d[k] for k in "xyz" if k != ax]
    L = d[ax]
    if ax == "z":
        pl = Plane(origin=((x0 + x1) / 2, (y0 + y1) / 2, z0), x_dir=(1, 0, 0), z_dir=(0, 0, 1))
    elif ax == "x":
        pl = Plane(origin=(x0, (y0 + y1) / 2, (z0 + z1) / 2), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
        w, h = d["y"], d["z"]
    else:
        pl = Plane(origin=((x0 + x1) / 2, y0, (z0 + z1) / 2), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
        w, h = d["x"], d["z"]
    return pl * cp.rhs(w, h, wall, L)


def tube_between(a, b, size=25.0, wall=1.5, x_dir=None, extend=0.0):
    """Square hollow section from point a to point b (centre line), extended by `extend` at both ends."""
    a, b = _v(a), _v(b)
    d = (b - a)
    L = d.length
    u = d.normalized()
    xd = x_dir if x_dir is not None else _perp((u.X, u.Y, u.Z))
    pl = Plane(origin=a - u * extend, x_dir=xd, z_dir=u)
    return pl * cp.shs(size, wall, L + 2 * extend)


def bead(start, e, length, d1, d2, leg=3.0):
    """Fillet weld bead from `start` along unit vector e for `length`, its legs along d1 and d2 (unit vectors,
    perpendicular to e and to each other): d1 lies on the first face, d2 on the second."""
    b = cp.weld_fillet(length, leg)               # along +X, legs along +Y and +Z
    y = _cross(d2, e)
    if all(abs(i - j) < 1e-6 for i, j in zip(y, d1)):
        return Plane(origin=start, x_dir=e, z_dir=d2) * b
    s2 = tuple(s + ei * length for s, ei in zip(start, e))
    return Plane(origin=s2, x_dir=tuple(-i for i in e), z_dir=d2) * b


def end_welds(c, u, a, face_box, leg=3.0, b=None, sides=None):
    """Fillet beads round the end of an a x b tube (b defaults to a) whose end centre c sits on a flat face of the
    box face_box = (x0, x1, y0, y1, z0, z1); u points from that face along the tube. A bead is laid on a side only
    where the face carries it (the strip the bead stands on lies inside the face). Returns a list of solids."""
    b = b or a
    u = tuple(float(i) for i in u)
    out = []
    k = [i for i in range(3) if abs(u[i]) > 0.5][0]
    others = [i for i in range(3) if i != k]
    half = {others[0]: a / 2, others[1]: b / 2}
    lo = (face_box[0], face_box[2], face_box[4]); hi = (face_box[1], face_box[3], face_box[5])
    for ax in others:
        for sg in (-1, 1):
            if sides is not None and (ax, sg) not in sides:
                continue
            s = [0.0, 0.0, 0.0]; s[ax] = sg
            o = [i for i in others if i != ax][0]
            e = [0.0, 0.0, 0.0]; e[o] = 1.0
            ok = True
            for q in (-1, 1):
                p = list(c)
                p[ax] += sg * (half[ax] + leg)
                p[o] += q * half[o]
                if not all(lo[i] - 0.01 <= p[i] <= hi[i] + 0.01 for i in others):
                    ok = False
            if not ok:
                continue
            st = list(c); st[ax] += sg * half[ax]; st[o] -= half[o]
            out.append(bead(tuple(st), tuple(e), 2 * half[o], tuple(s), u, leg))
    return out


class Holes:
    """Holes recorded as fasteners are placed, then drilled through the parts they pass through."""

    def __init__(self):
        self.items = []

    def add(self, solid, only=None):
        self.items.append((solid, only))


def _loc(origin, n):
    """Plane at origin whose +Z points against the insertion direction n (the head side)."""
    z = tuple(-i for i in n)
    return Plane(origin=origin, x_dir=_perp(z), z_dir=z)


def bolt(d, grip, origin, n, holes, mat="zinc_plated", bom=17, group="shell", explode=(0, 0, 0), label="", only=None,
         clearance=1.0):
    """ISO 4017 bolt, two ISO 7089 washers and an ISO 4032 nut clamping a joint `grip` thick. `origin` is the centre
    of the hole on the head-side face; n is the unit insertion direction (head side to nut side). Records a
    clearance hole (d + clearance) through the grip. Returns part dicts."""
    pl = _loc(origin, n)
    out = [part(f"{nm}{label}", pl * shp, mat, kind="fastener", bom=bom, group=group, explode=explode)
           for nm, shp in cp.hex_bolt_set(int(d), grip)]
    hole = pl * (Pos(0, 0, -grip / 2) * Cylinder(d / 2 + clearance / 2, grip + 0.4))
    holes.add(hole, only)
    return out


def screw(d, length, origin, n, holes, mat="zinc_plated", bom=17, group="shell", explode=(0, 0, 0), label="", kind="hex",
          hole_d=None, washer=True, only=None):
    """A screw with no nut: ISO 4017 hex screw into a tapped hole or insert, or a DIN 571 coach screw into timber
    ("coach"). origin is the hole centre on the head-side face; the shank runs `length` along n. Records a hole of
    hole_d (default d, the tap or pilot size) over the shank."""
    pl = _loc(origin, n)
    h = cp.ISO[int(d)][4] if washer else 0.0
    if kind == "coach":
        shp = cp.coach_screw(int(d), length)
        nm = f"M{d} x {length:.0f} coach screw (DIN 571)"
    else:
        shp = cp.hex_bolt(int(d), length)
        nm = f"M{d} x {length:.0f} hex screw (ISO 4017)"
    out = [part(f"{nm}{label}", pl * Pos(0, 0, h) * shp, mat, kind="fastener", bom=bom, group=group, explode=explode)]
    if washer:
        out.append(part(f"M{d} washer (ISO 7089){label}", pl * cp.washer(int(d)), mat, kind="fastener", bom=bom, group=group,
                        explode=explode))
    hd = hole_d if hole_d is not None else d
    holes.add(pl * (Pos(0, 0, -(length - h) / 2 - 0.1) * Cylinder(hd / 2, length - h + 0.4)), only)
    return out


def cut_holes(parts, holes):
    """Subtract every recorded hole from the made and bought parts whose bounding box it meets (or only from the
    parts whose name contains one of the strings in `only`)."""
    for item in holes.items:
        solid, only = item[0], item[1]
        hb = solid.bounding_box()
        for p in parts:
            if p["kind"] not in ("made", "bought"):
                continue
            if only is not None and not any(s in p["name"] for s in only):
                continue
            pb = p["shape"].bounding_box()
            if (pb.max.X < hb.min.X or hb.max.X < pb.min.X or pb.max.Y < hb.min.Y or hb.max.Y < pb.min.Y
                    or pb.max.Z < hb.min.Z or hb.max.Z < pb.min.Z):
                continue
            try:
                inter = (p["shape"] & solid).volume
            except Exception:
                inter = 1.0
            if inter > 1e-3:
                p["shape"] = p["shape"] - solid
    return parts


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def cyl(x, y, z0, z1, r):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def vpulley(d, w, bore, groove_w=14.0, groove_depth=12.0, spokes=0, spoke_r=None):
    """V-belt pulley along +Z centred on z = 0: rim diameter d, width w, one groove groove_w wide and groove_depth
    deep (the belt band built with the same groove sits in it without touching), bore, optional lightening holes."""
    body = Cylinder(d / 2, w)
    ring = Cylinder(d / 2 + 1, groove_w) - Cylinder(d / 2 - groove_depth, groove_w)
    out = body - ring - Cylinder(bore / 2, w * 2)
    if spokes:
        r_h = spoke_r or (bore / 2 + (d / 2 - groove_depth - bore / 2) / 2)
        hr = (d / 2 - groove_depth - bore / 2) * 0.28
        for k in range(spokes):
            a = 2 * math.pi * k / spokes
            out = out - Pos(r_h * math.cos(a), r_h * math.sin(a), 0) * Cylinder(hr, w * 2)
    return out
