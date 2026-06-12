#!/usr/bin/env python3
"""Генератор STL-файлов фигурки самолёта для 3D-печати.

Создаёт две модели (размеры в мм, длина 120, размах крыла 140):
  airplane_flat.stl     — максимально простая плоская пластина-силуэт
                          толщиной 4 мм, печатается лёжа без поддержек
  airplane_figurine.stl — объёмная фигурка (фюзеляж, крыло, хвост,
                          кабина) высотой 34 мм, тоже без поддержек

Запуск:  python3 generate_airplane_stl.py
"""
import struct


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def newell_normal(poly):
    nx = ny = nz = 0.0
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        nx += (p[1] - q[1]) * (p[2] + q[2])
        ny += (p[2] - q[2]) * (p[0] + q[0])
        nz += (p[0] - q[0]) * (p[1] + q[1])
    return (nx, ny, nz)


def prism(base, d):
    """Треугольники призмы: выпуклый плоский многоугольник base,
    выдавленный вдоль вектора d."""
    if dot(newell_normal(base), d) < 0:
        base = base[::-1]
    top = [add(p, d) for p in base]
    tris = []
    for i in range(1, len(base) - 1):
        tris.append((top[0], top[i], top[i + 1]))
        tris.append((base[0], base[i + 1], base[i]))
    m = len(base)
    for i in range(m):
        a, b = base[i], base[(i + 1) % m]
        a2, b2 = top[i], top[(i + 1) % m]
        tris.append((a, b, b2))
        tris.append((a, b2, a2))
    return tris


def in_xy(poly2d, z):
    return [(x, y, z) for x, y in poly2d]


def in_xz(poly2d, y):
    return [(x, y, z) for x, z in poly2d]


# Профиль фюзеляжа сбоку (X — вдоль, Y — вверх), плоское дно на Y=0
FUSELAGE = [(10, 0), (105, 0), (120, 5), (120, 14),
            (75, 16), (25, 16), (0, 11), (0, 5)]
# Крыло в плане (X — вдоль, Z — вбок), размах 140
WING = [(32, 0), (40, -70), (58, -70), (68, 0), (58, 70), (40, 70)]
# Горизонтальный стабилизатор в плане, размах 56
STABILIZER = [(96, 0), (100, -28), (112, -28), (118, 0), (112, 28), (100, 28)]
# Киль сбоку
FIN = [(100, 13), (118, 13), (118, 34), (110, 34)]
# Кабина сбоку
CANOPY = [(30, 15), (50, 15), (46, 24), (36, 24)]

# Фюзеляж плоской версии: вид в плане, ширина 14
FLAT_BODY = [(0, -3), (8, -7), (110, -7), (120, -3),
             (120, 3), (110, 7), (8, 7), (0, 3)]


def build_figurine():
    tris = []
    tris += prism(in_xy(FUSELAGE, -8), (0, 0, 16))   # фюзеляж, ширина 16
    tris += prism(in_xz(WING, 0), (0, 5, 0))         # крыло, толщина 5
    tris += prism(in_xz(STABILIZER, 0), (0, 5, 0))   # стабилизатор, толщина 5
    tris += prism(in_xy(FIN, -2), (0, 0, 4))         # киль, толщина 4
    tris += prism(in_xy(CANOPY, -5), (0, 0, 10))     # кабина, ширина 10
    return tris


def build_flat():
    """Плоский силуэт самолёта толщиной 4 мм."""
    tris = []
    tris += prism(in_xz(FLAT_BODY, 0), (0, 4, 0))    # фюзеляж
    tris += prism(in_xz(WING, 0), (0, 4, 0))         # крыло
    tris += prism(in_xz(STABILIZER, 0), (0, 4, 0))   # стабилизатор
    return tris


def write_stl(path, tris):
    with open(path, "wb") as f:
        f.write(b"airplane figurine, mm".ljust(80, b"\0"))
        f.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            n = cross(sub(b, a), sub(c, a))
            length = dot(n, n) ** 0.5 or 1.0
            n = (n[0] / length, n[1] / length, n[2] / length)
            f.write(struct.pack("<3f", *n))
            for v in (a, b, c):
                f.write(struct.pack("<3f", *(float(x) for x in v)))
            f.write(struct.pack("<H", 0))


if __name__ == "__main__":
    for path, tris in (("airplane_flat.stl", build_flat()),
                       ("airplane_figurine.stl", build_figurine())):
        write_stl(path, tris)
        print(f"Записан {path}: {len(tris)} треугольников")
