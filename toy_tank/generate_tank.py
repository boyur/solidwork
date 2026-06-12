#!/usr/bin/env python3
"""Generate a detailed 2D toy-tank silhouette as DXF (for SolidWorks sketch
import) and an SVG preview.

Straight segments only, two closed polylines: the outer silhouette (rhomboid
track, sloped hull, trapezoid turret, cupola, barrel with muzzle brake) and
an inner track contour that becomes a recessed band when embossed.
Units: millimetres. Overall size 38 x 19.8 mm — fits the face of a 40 mm
cube; scale freely in SolidWorks.
"""

# Closed contours as lists of (x, y) vertices. The first is the outer
# silhouette (counter-clockwise); the second is the inner track band,
# which SolidWorks treats as a hole when extruding the whole sketch.
SILHOUETTE = [
    (5.0, 0.0),      # track, flat bottom
    (31.0, 0.0),     # slant up to the right track point
    (36.0, 5.0),     # track right point
    (31.0, 10.0),    # track top, right flat
    (30.5, 10.0),    # glacis (sloped front armour)
    (28.5, 13.5),    # hull top, right part
    (23.5, 13.5),    # turret front slope, lower part
    (23.05, 14.8),   # barrel bottom
    (35.5, 14.8),    # muzzle brake, bottom step
    (35.5, 14.4),    # muzzle brake bottom
    (38.0, 14.4),    # muzzle brake face
    (38.0, 16.8),    # muzzle brake top
    (35.5, 16.8),    # muzzle brake, top step
    (35.5, 16.4),    # barrel top
    (22.49, 16.4),   # turret front slope, upper part
    (22.0, 17.8),    # turret roof, right part
    (19.5, 17.8),    # cupola right wall
    (19.5, 19.6),    # cupola top
    (15.0, 19.6),    # cupola left wall
    (15.0, 17.8),    # turret roof, left part
    (13.5, 17.8),    # turret rear slope
    (12.0, 13.5),    # hull top, left part
    (9.0, 13.5),     # rear armour slope
    (7.0, 10.0),     # track top, left flat
    (5.0, 10.0),     # slant down to the left track point
    (0.0, 5.0),      # track left point, slant down closes path
]

TRACK_BAND = [
    (7.0, 2.5),
    (28.5, 2.5),
    (31.0, 5.0),
    (28.5, 7.5),
    (7.0, 7.5),
    (4.5, 5.0),
]

CONTOURS = [SILHOUETTE, TRACK_BAND]


def dxf() -> str:
    out = ["0", "SECTION", "2", "ENTITIES"]
    for contour in CONTOURS:
        out += ["0", "POLYLINE", "8", "0", "66", "1", "70", "1"]
        for x, y in contour:
            out += ["0", "VERTEX", "8", "0", "10", f"{x}", "20", f"{y}"]
        out += ["0", "SEQEND"]
    out += ["0", "ENDSEC", "0", "EOF"]
    return "\n".join(out) + "\n"


def svg() -> str:
    # SVG y-axis points down, so mirror: Y = height - y.
    h = 19.8

    def path(contour):
        pts = " L ".join(f"{x},{h - y}" for x, y in contour)
        return f"M {pts} Z"

    d = " ".join(path(c) for c in CONTOURS)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 42 24"
     width="840" height="480">
  <path d="{d}" fill="#cccccc" fill-rule="evenodd"
        stroke="black" stroke-width="0.4"/>
</svg>
'''


if __name__ == "__main__":
    import pathlib
    here = pathlib.Path(__file__).parent
    (here / "toy_tank.dxf").write_text(dxf())
    (here / "toy_tank_preview.svg").write_text(svg())
    print("written: toy_tank.dxf, toy_tank_preview.svg")
