#!/usr/bin/env python3
"""Generate a simple 2D toy-tank silhouette as DXF (for SolidWorks sketch
import) and an SVG preview.

Geometry is one closed polyline, straight segments only: rhomboid track
(pointed ends), hull, square turret, barrel. Units: millimetres. Overall
size 38 x 19 mm — fits the face of a 40 mm cube; scale freely in SolidWorks.
"""

import math

# Outer silhouette, counter-clockwise. Each entry: (x, y, bulge)
# where bulge applies to the segment from this vertex to the next.
OUTLINE = [
    (5.0, 0.0, 0),       # track, flat bottom
    (31.0, 0.0, 0),      # slant up to the right track point
    (36.0, 5.0, 0),      # track right point, slant back up
    (31.0, 10.0, 0),     # track top, right flat
    (29.0, 10.0, 0),     # hull right side
    (29.0, 13.0, 0),     # hull top, right part
    (24.0, 13.0, 0),     # turret right side, below barrel
    (24.0, 14.5, 0),     # barrel bottom
    (38.0, 14.5, 0),     # barrel muzzle
    (38.0, 16.2, 0),     # barrel top
    (24.0, 16.2, 0),     # turret right side, above barrel
    (24.0, 19.0, 0),     # turret top
    (12.0, 19.0, 0),     # turret left side
    (12.0, 13.0, 0),     # hull top, left part
    (7.0, 13.0, 0),      # hull left side
    (7.0, 10.0, 0),      # track top, left flat
    (5.0, 10.0, 0),      # slant down to the left track point
    (0.0, 5.0, 0),       # track left point, slant down closes path
]

WHEELS = []


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
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 42 23"
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
