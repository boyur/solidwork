#!/usr/bin/env python3
"""Generate a simple 2D toy-tank silhouette as DXF (for SolidWorks sketch
import) and an SVG preview.

Geometry is one closed polyline (outer silhouette, arcs encoded as bulges)
plus four circles (road wheels). Units: millimetres. Overall size 36 x 19 mm —
fits the face of a 40 mm cube; scale freely in SolidWorks.
"""

import math

# Outer silhouette, counter-clockwise. Each entry: (x, y, bulge)
# where bulge applies to the segment from this vertex to the next.
B90 = math.tan(math.radians(90 / 4))  # 90-degree arc
B180 = 1.0                            # 180-degree arc

OUTLINE = [
    (5.0, 0.0, 0),       # track, flat bottom
    (31.0, 0.0, B180),   # right end of track -> semicircle up
    (29.0, 10.0, 0),     # short flat on top of track
    (29.0, 13.0, 0),     # hull right side (vertex at top)
    (24.0, 13.0, 0),     # hull top, right part
    (24.0, 14.5, 0),     # turret right side, below barrel
    (36.0, 14.5, 0),     # barrel bottom
    (36.0, 16.2, 0),     # barrel muzzle
    (24.0, 16.2, 0),     # barrel top
    (24.0, 17.5, B90),   # turret right side -> rounded corner
    (22.5, 19.0, 0),     # turret top
    (13.5, 19.0, B90),   # rounded corner
    (12.0, 17.5, 0),     # turret left side
    (12.0, 13.0, 0),     # turret left bottom
    (7.0, 13.0, 0),      # hull top, left part
    (7.0, 10.0, 0),      # hull left side
    (5.0, 10.0, B180),   # left end of track -> semicircle down, closes path
]

WHEELS = [((8.0, 5.0), 2.5), ((15.0, 5.0), 2.5),
          ((22.0, 5.0), 2.5), ((29.0, 5.0), 2.5)]


def dxf() -> str:
    out = ["0", "SECTION", "2", "ENTITIES"]
    out += ["0", "POLYLINE", "8", "0", "66", "1", "70", "1"]
    for x, y, b in OUTLINE:
        out += ["0", "VERTEX", "8", "0", "10", f"{x}", "20", f"{y}"]
        if b:
            out += ["42", f"{b:.12f}"]
    out += ["0", "SEQEND"]
    for (cx, cy), r in WHEELS:
        out += ["0", "CIRCLE", "8", "0",
                "10", f"{cx}", "20", f"{cy}", "40", f"{r}"]
    out += ["0", "ENDSEC", "0", "EOF"]
    return "\n".join(out) + "\n"


def svg() -> str:
    # SVG y-axis points down, so mirror: Y = height - y. CCW bulge arcs
    # become sweep=0 in mirrored coordinates.
    h = 19.0

    def pt(x, y):
        return f"{x},{h - y}"

    d = [f"M {pt(*OUTLINE[0][:2])}"]
    n = len(OUTLINE)
    for i, (x, y, b) in enumerate(OUTLINE):
        nx, ny, _ = OUTLINE[(i + 1) % n]
        if b:
            theta = 4 * math.atan(b)
            chord = math.hypot(nx - x, ny - y)
            r = chord / (2 * math.sin(theta / 2))
            large = 1 if theta > math.pi else 0
            d.append(f"A {r:.4f} {r:.4f} 0 {large} 0 {pt(nx, ny)}")
        else:
            d.append(f"L {pt(nx, ny)}")
    d.append("Z")
    circles = "\n  ".join(
        f'<circle cx="{cx}" cy="{h - cy}" r="{r}" fill="white" '
        f'stroke="black" stroke-width="0.4"/>'
        for (cx, cy), r in WHEELS)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 40 23"
     width="800" height="460">
  <path d="{' '.join(d)}" fill="#cccccc" stroke="black" stroke-width="0.4"/>
  {circles}
</svg>
'''


if __name__ == "__main__":
    import pathlib
    here = pathlib.Path(__file__).parent
    (here / "toy_tank.dxf").write_text(dxf())
    (here / "toy_tank_preview.svg").write_text(svg())
    print("written: toy_tank.dxf, toy_tank_preview.svg")
