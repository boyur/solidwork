#!/usr/bin/env python3
"""Генератор 2D-силуэта самолёта (единый замкнутый контур).

Контур — объединение фюзеляжа, крыла и стабилизатора в один
многоугольник. Размеры в мм: длина 120, размах 140.

Запуск:  python3 generate_silhouette_2d.py
Результат:
  airplane_silhouette.dxf — для импорта в эскиз SolidWorks
  airplane_silhouette.svg — для просмотра / лазера / гравировки
"""

# Точки 117.109, 4.156 — пересечение задней кромки стабилизатора
# (118,0)-(112,-28) с сужением фюзеляжа (110,-7)-(120,-3);
# 32.8, 67, 97 — пересечения кромок крыла и стабилизатора
# с бортом фюзеляжа (z = ±7).
OUTLINE = [
    (0, -3), (8, -7), (32.8, -7),            # нос и борт до крыла
    (40, -70), (58, -70), (67, -7),          # крыло (низ)
    (97, -7), (100, -28), (112, -28),        # борт и стабилизатор (низ)
    (117.109, -4.156), (120, -3),            # сужение хвоста
    (120, 3), (117.109, 4.156),              # хвост
    (112, 28), (100, 28), (97, 7),           # стабилизатор (верх)
    (67, 7), (58, 70), (40, 70), (32.8, 7),  # крыло (верх)
    (8, 7), (0, 3),                          # борт и нос
]


def write_dxf(path, pts):
    """Минимальный DXF R12 с одной замкнутой полилинией."""
    lines = ["0", "SECTION", "2", "ENTITIES",
             "0", "POLYLINE", "8", "0", "66", "1", "70", "1"]
    for x, y in pts:
        lines += ["0", "VERTEX", "8", "0",
                  "10", f"{x:.4f}", "20", f"{y:.4f}"]
    lines += ["0", "SEQEND", "0", "ENDSEC", "0", "EOF"]
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def write_svg(path, pts):
    d = "M " + " L ".join(f"{x:.3f},{-y:.3f}" for x, y in pts) + " Z"
    with open(path, "w") as f:
        f.write(
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'viewBox="-5 -75 130 150" width="130mm" height="150mm">\n'
            f'  <path d="{d}" fill="#4f8fd9" stroke="#1b3a5c" '
            'stroke-width="0.5"/>\n</svg>\n')


if __name__ == "__main__":
    write_dxf("airplane_silhouette.dxf", OUTLINE)
    write_svg("airplane_silhouette.svg", OUTLINE)
    print(f"Записаны airplane_silhouette.dxf и .svg: {len(OUTLINE)} точек")
