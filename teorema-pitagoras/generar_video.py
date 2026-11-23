import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

FRAMES_DIR = "/workspace/frames"
FPS = 24
W, H = 12.8, 7.2

plt.rcParams["font.family"] = "DejaVu Sans"

BG = "#0f172a"
FG = "#e2e8f0"
DIM = "#94a3b8"
C_TRI = "#38bdf8"
C_A = "#f472b6"
C_B = "#facc15"
C_C = "#4ade80"

# Geometría del triángulo rectángulo (catetos 3 y 4, hipotenusa 5)
A = (0.0, 0.0)
B = (4.0, 0.0)
C = (0.0, 3.0)


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def seg(t, start, end):
    if end <= start:
        return 1.0 if t >= start else 0.0
    return ease((t - start) / (end - start))


def add(a, b, s=1.0):
    return (a[0] + b[0] * s, a[1] + b[1] * s)


def quad_side(P, Q, n, g):
    L = math.hypot(Q[0] - P[0], Q[1] - P[1])
    return [P, Q, add(Q, n, L * g), add(P, n, L * g)]


def draw_triangle(ax, alpha, t_draw):
    pts = [A, B, C]
    for i in range(3):
        g = seg(t_draw, 0.12 * i, 0.12 * i + 0.3)
        if g <= 0:
            continue
        P, Q = pts[i], pts[(i + 1) % 3]
        E = add(P, (Q[0] - P[0], Q[1] - P[1]), g)
        ax.plot([P[0], E[0]], [P[1], E[1]], color=C_TRI, lw=4,
                alpha=alpha, solid_capstyle="round", zorder=5)
    g = seg(t_draw, 0.36, 0.6)
    if g > 0:
        s = 0.38 * g
        ax.plot([s, s, 0], [0, s, s], color=C_TRI, lw=2,
                alpha=0.9 * alpha, zorder=6)


SCENES = [
    ("titulo", 4.0),
    ("triangulo", 9.0),
    ("cuadrados", 12.0),
    ("formula", 6.0),
    ("ejemplo", 12.0),
    ("cierre", 6.0),
]
TOTAL = sum(d for _, d in SCENES)


def render(scene, t, path):
    fig = plt.figure(figsize=(W, H), dpi=100)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-8.2, 10.2)
    ax.set_ylim(-5.6, 8.4)
    ax.axis("off")

    if scene == "titulo":
        a1 = seg(t, 0.05, 0.4)
        a2 = seg(t, 0.45, 0.8)
        ax.text(0.5, 0.56, "EL TEOREMA DE PITÁGORAS", transform=ax.transAxes,
                ha="center", va="center", fontsize=38, fontweight="bold",
                color=FG, alpha=a1)
        ax.text(0.5, 0.40, "una idea simple con un poder enorme", transform=ax.transAxes,
                ha="center", va="center", fontsize=19, color=DIM, alpha=a1)
        ax.text(0.5, 0.24, r"$a^2 + b^2 = c^2$", transform=ax.transAxes,
                ha="center", va="center", fontsize=34, color=C_TRI, alpha=a2)

    elif scene == "triangulo":
        alpha = seg(t, 0.0, 0.15)
        draw_triangle(ax, alpha, t)
        a = seg(t, 0.6, 0.85)
        ax.text(0.32, 1.5, "a", fontsize=24, color=C_A, fontweight="bold",
                ha="left", va="center", alpha=a)
        ax.text(1.9, 0.34, "b", fontsize=24, color=C_B, fontweight="bold",
                ha="center", va="center", alpha=a)
        ax.text(1.72, 1.44, "c", fontsize=24, color=C_C, fontweight="bold",
                ha="center", va="center", alpha=a)
        a2 = seg(t, 0.8, 1.0)
        ax.text(0.9, 2.35, "cateto", fontsize=15, color=C_A, ha="left", alpha=a2)
        ax.text(1.9, -0.75, "cateto", fontsize=15, color=C_B, ha="center", alpha=a2)
        ax.text(2.95, 2.35, "hipotenusa", fontsize=15, color=C_C, ha="left", alpha=a2)
        ax.text(0.5, 0.94, "Un triángulo rectángulo tiene un ángulo de 90°",
                transform=ax.transAxes, ha="center", fontsize=21, color=FG,
                alpha=seg(t, 0.0, 0.2))

    elif scene == "cuadrados":
        draw_triangle(ax, 0.9, 1.0)
        squares = [
            (A, C, (-1, 0), C_A, r"$a^2$", (-1.5, 1.5), 0.05, 0.32),
            (A, B, (0, -1), C_B, r"$b^2$", (2.0, -2.0), 0.30, 0.57),
            (B, C, (0.6, 0.8), C_C, r"$c^2$", (3.5, 3.5), 0.55, 0.88),
        ]
        for P, Q, n, col, lab, ctr, s0, s1 in squares:
            g = seg(t, s0, s1)
            if g <= 0:
                continue
            poly = Polygon(quad_side(P, Q, n, g), closed=True, facecolor=col,
                           alpha=0.28 * g, edgecolor=col, lw=2.5, zorder=2)
            ax.add_patch(poly)
            lg = seg(t, s1 - 0.12, s1 + 0.08)
            if lg > 0:
                ax.text(ctr[0], ctr[1], lab, fontsize=30, color=col,
                        fontweight="bold", ha="center", va="center",
                        alpha=lg, zorder=7)
        ax.text(0.5, 0.94, "Construimos un cuadrado sobre cada lado",
                transform=ax.transAxes, ha="center", fontsize=21, color=FG,
                alpha=seg(t, 0.0, 0.15))

    elif scene == "formula":
        draw_triangle(ax, 0.15 + seg(t, 0.0, 0.2) * 0.25, 1.0)
        squares = [
            (A, C, (-1, 0), C_A),
            (A, B, (0, -1), C_B),
            (B, C, (0.6, 0.8), C_C),
        ]
        fade = 0.5 * (1 - seg(t, 0.0, 0.25))
        for P, Q, n, col in squares:
            if fade <= 0:
                continue
            ax.add_patch(Polygon(quad_side(P, Q, n, 1.0), closed=True,
                                 facecolor=col, alpha=0.22 * fade,
                                 edgecolor=col, lw=2, zorder=2))
        a1 = seg(t, 0.15, 0.5)
        a2 = seg(t, 0.45, 0.8)
        ax.text(0.5, 0.54, r"$a^2 + b^2 = c^2$", transform=ax.transAxes,
                ha="center", va="center", fontsize=56, color=FG, alpha=a1)
        ax.text(0.5, 0.34,
                "El área de los dos cuadrados pequeños, sumada,\n"
                "es exactamente el área del cuadrado grande",
                transform=ax.transAxes, ha="center", va="center",
                fontsize=19, color=DIM, alpha=a2, linespacing=1.5)

    elif scene == "ejemplo":
        draw_triangle(ax, 0.9, 1.0)
        squares = [
            (A, C, (-1, 0), C_A, "9", 0.05, 0.30),
            (A, B, (0, -1), C_B, "16", 0.28, 0.53),
            (B, C, (0.6, 0.8), C_C, "25", 0.51, 0.76),
        ]
        for P, Q, n, col, num, s0, s1 in squares:
            g = seg(t, s0, s1)
            if g <= 0:
                continue
            ax.add_patch(Polygon(quad_side(P, Q, n, g), closed=True,
                                 facecolor=col, alpha=0.28 * g,
                                 edgecolor=col, lw=2.5, zorder=2))
            lg = seg(t, s1 - 0.10, s1 + 0.08)
            if lg > 0:
                L = math.hypot(Q[0] - P[0], Q[1] - P[1])
                nx, ny = n
                ctr = ((P[0] + Q[0]) / 2 + nx * L / 2,
                       (P[1] + Q[1]) / 2 + ny * L / 2)
                ax.text(ctr[0], ctr[1], num, fontsize=26, color=col,
                        fontweight="bold", ha="center", va="center",
                        alpha=lg, zorder=7)
        a = seg(t, 0.6, 0.8)
        ax.text(0.32, 1.5, "a = 3", fontsize=17, color=C_A, ha="left",
                va="center", alpha=a)
        ax.text(1.9, 0.34, "b = 4", fontsize=17, color=C_B, ha="center",
                va="center", alpha=a)
        ax.text(1.68, 1.5, "c = 5", fontsize=17, color=C_C, ha="center",
                va="center", alpha=a)
        a2 = seg(t, 0.78, 1.0)
        ax.text(0.5, 0.94, "Ejemplo 3 - 4 - 5", transform=ax.transAxes,
                ha="center", fontsize=21, color=FG, alpha=seg(t, 0.0, 0.15))
        ax.text(0.5, 0.08, "3² + 4² = 5²   →   9 + 16 = 25 ✓",
                transform=ax.transAxes, ha="center", fontsize=26,
                color=FG, alpha=a2)

    else:
        a1 = seg(t, 0.05, 0.4)
        a2 = seg(t, 0.35, 0.7)
        ax.text(0.5, 0.58, r"$a^2 + b^2 = c^2$", transform=ax.transAxes,
                ha="center", va="center", fontsize=52, color=C_TRI, alpha=a1)
        ax.text(0.5, 0.40, "Recuerda: solo vale para triángulos RECTÁNGULOS",
                transform=ax.transAxes, ha="center", fontsize=21, color=FG, alpha=a2)
        ax.text(0.5, 0.27, "Si conoces dos lados, ¡siempre puedes hallar el tercero!",
                transform=ax.transAxes, ha="center", fontsize=18, color=DIM, alpha=a2)

    fig.savefig(path, facecolor=BG)
    plt.close(fig)


def main():
    os.makedirs(FRAMES_DIR, exist_ok=True)
    i = 0
    for scene, dur in SCENES:
        n = int(round(dur * FPS))
        for k in range(n):
            render(scene, k / max(n - 1, 1), f"{FRAMES_DIR}/f_{i:05d}.png")
            i += 1
    print("frames:", i)


if __name__ == "__main__":
    main()
