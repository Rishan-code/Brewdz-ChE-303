"""
BrewDz Particle Engineering Pvt. Ltd. — ChE 303 Slide Visuals Generator
Generates 3 publication-grade, 300-DPI PNG + SVG engineering flowcharts & schematics
for Part 2: The Industrial Coffee Making Process (3-Slide Presentation Deck).
"""

import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

# Ensure output directory exists
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "slide_visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# BrewDz Brand Palette
C_BG       = "#FAF6F0"   # Warm cream paper background
C_CARD     = "#FFFFFF"   # Pure white card surface
C_ESPRESSO = "#2C1810"   # Deep espresso dark text/borders
C_CREMA    = "#D4A373"   # Warm crema gold accent
C_ROAST    = "#8A5A2B"   # Medium roast brown
C_LIGHT_BR = "#F2E6D8"   # Soft tan fill
C_GREEN    = "#137333"   # Engineering green (PROD / Pass)
C_GREEN_BG = "#E6F4EA"   # Soft green fill
C_RUST     = "#C2571A"   # Alert rust / Recycle / Heat
C_RUST_BG  = "#FCE8E6"   # Soft rust fill
C_BLUE     = "#1A5F7A"   # Industrial blue (Instant / Water / Chilled)
C_BLUE_BG  = "#E3F2F8"   # Soft blue fill
C_MUTED    = "#6B5B53"   # Muted secondary text
C_BORDER   = "#D8CBB8"   # Soft card border

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = C_BORDER


def draw_box(ax, x, y, w, h, title, subtitle="", facecolor=C_CARD, edgecolor=C_ESPRESSO,
             title_color=C_ESPRESSO, sub_color=C_MUTED, lw=1.6, title_fs=9.5, sub_fs=7.5,
             radius=0.012, zorder=3, title_y=0.68, sub_y=0.30):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.004,rounding_size={radius}",
        facecolor=facecolor, edgecolor=edgecolor, linewidth=lw, zorder=zorder
    )
    ax.add_patch(box)
    if subtitle:
        ax.text(x + w / 2, y + h * title_y, title, ha="center", va="center",
                fontsize=title_fs, fontweight="bold", color=title_color, zorder=zorder + 1)
        ax.text(x + w / 2, y + h * sub_y, subtitle, ha="center", va="center",
                fontsize=sub_fs, color=sub_color, zorder=zorder + 1, linespacing=1.28)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center",
                fontsize=title_fs, fontweight="bold", color=title_color, zorder=zorder + 1)


def draw_arrow(ax, x1, y1, x2, y2, color=C_ESPRESSO, lw=1.8, style="-|>", rad=0.0, ls="-", zorder=4):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=13,
        color=color, linewidth=lw, linestyle=ls,
        connectionstyle=f"arc3,rad={rad}", zorder=zorder
    )
    ax.add_patch(arr)


def setup_canvas(title, subtitle):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)  # Full-bleed 16:9 HD widescreen
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Top Title Banner
    header = Rectangle((0, 0.895), 1, 0.105, facecolor=C_ESPRESSO, edgecolor="none", zorder=1)
    ax.add_patch(header)
    accent = Rectangle((0, 0.888), 1, 0.007, facecolor=C_CREMA, edgecolor="none", zorder=2)
    ax.add_patch(accent)

    ax.text(0.025, 0.957, title, ha="left", va="center",
            fontsize=15.5, fontweight="bold", color="#FFFFFF", zorder=3)
    ax.text(0.025, 0.918, subtitle, ha="left", va="center",
            fontsize=10.0, color=C_CREMA, zorder=3)
    ax.text(0.975, 0.946, "BrewDz Particle Engineering · ChE 303", ha="right", va="center",
            fontsize=10.0, fontweight="bold", color="#E8D8C8", zorder=3)
    return fig, ax


# =============================================================================
# SLIDE 1 VISUAL: UPSTREAM FLOWSHEET + ROASTING + ANGLE OF NIP GEOMETRY
# =============================================================================
def generate_slide1():
    fig, ax = setup_canvas(
        "SLIDE 1 · Upstream Processing & BrewDz Comminution Core",
        "From Green Bean Conditioning & Pyrolysis Roasting to Controlled Double-Roll Fracture & Closed-Loop Screening"
    )

    # --- TOP PANEL: END-TO-END UPSTREAM FLOWCHART ---
    panel_top = FancyBboxPatch((0.02, 0.555), 0.96, 0.308,
                               boxstyle="round,pad=0.005,rounding_size=0.015",
                               facecolor=C_CARD, edgecolor=C_BORDER, linewidth=1.3, zorder=1)
    ax.add_patch(panel_top)
    ax.text(0.035, 0.840, "A. UPSTREAM PROCESS FLOWCHART (COMMON TO BOTH GROUND & INSTANT COFFEE)",
            fontsize=10.5, fontweight="bold", color=C_ROAST, ha="left", va="center", zorder=2)

    steps = [
        ("1. Green Beans", "10–12% Moisture\nρ_b = 680 kg/m³", C_LIGHT_BR, C_ESPRESSO),
        ("2. Cleaning &\nDe-Stoning", "Air Elutriation\nu_t = 8–12 m/s", C_BLUE_BG, C_BLUE),
        ("3. Thermal\nRoaster", "200–240°C\nFirst Crack (+70%)", C_RUST_BG, C_RUST),
        ("4. Chilled Air\nQuench", "< 30°C (< 60 s)\nLocks Volatiles", C_BLUE_BG, C_BLUE),
        ("5. BrewDz\nRoller Mill", "T < 28°C · 1.18 kW\nGap s = 0.50 mm", C_LIGHT_BR, C_ESPRESSO),
        ("6. Multi-Deck\nScreen", "Closed-Loop\n3-Cut Split", C_GREEN_BG, C_GREEN),
    ]

    xs = [0.035, 0.190, 0.345, 0.500, 0.655, 0.810]
    bw, bh, by = 0.130, 0.130, 0.640
    for i, (t, s, fc, ec) in enumerate(steps):
        draw_box(ax, xs[i], by, bw, bh, t, s, facecolor=fc, edgecolor=ec,
                 title_color=ec if ec != C_ESPRESSO else C_ESPRESSO,
                 title_fs=9.6, sub_fs=8.0, lw=1.8)
        if i < len(steps) - 1:
            draw_arrow(ax, xs[i] + bw + 0.005, by + bh / 2, xs[i + 1] - 0.005, by + bh / 2, color=C_ROAST, lw=2.2)

    # Recycle loop from Screen (step 6) back to Roller Mill (step 5)
    ax.plot([0.875, 0.875, 0.720, 0.720], [0.774, 0.815, 0.815, 0.782],
            color=C_RUST, lw=2.2, linestyle="--", zorder=4)
    draw_arrow(ax, 0.720, 0.790, 0.720, 0.774, color=C_RUST, lw=2.2)
    ax.text(0.798, 0.828, "OVERSIZE RECYCLE (23.0 kg/h, >1093 µm)",
            ha="center", va="center", fontsize=8.2, fontweight="bold", color=C_RUST,
            bbox=dict(boxstyle="round,pad=0.22", facecolor=C_RUST_BG, edgecolor=C_RUST, lw=0.9), zorder=5)

    # Screen split outputs downward arrows
    draw_arrow(ax, 0.842, 0.635, 0.775, 0.600, color=C_GREEN, lw=2.2)
    draw_arrow(ax, 0.902, 0.635, 0.902, 0.600, color=C_BLUE, lw=2.2)
    ax.text(0.685, 0.582, "PROD: 41.8 kg/h (600–1100 µm -> Ground)", ha="center", va="center",
            fontsize=7.8, fontweight="bold", color=C_GREEN,
            bbox=dict(boxstyle="round,pad=0.22", facecolor=C_GREEN_BG, edgecolor=C_GREEN, lw=0.9), zorder=5)
    ax.text(0.890, 0.582, "FINE: 55.2 kg/h (<597 µm -> Instant)", ha="center", va="center",
            fontsize=7.8, fontweight="bold", color=C_BLUE,
            bbox=dict(boxstyle="round,pad=0.22", facecolor=C_BLUE_BG, edgecolor=C_BLUE, lw=0.9), zorder=5)

    # --- BOTTOM LEFT PANEL: ROASTING CELLULAR TRANSFORMATION ---
    panel_bl = FancyBboxPatch((0.02, 0.025), 0.465, 0.500,
                              boxstyle="round,pad=0.005,rounding_size=0.015",
                              facecolor=C_CARD, edgecolor=C_BORDER, linewidth=1.3, zorder=1)
    ax.add_patch(panel_bl)
    ax.text(0.035, 0.502, "B. ROASTING PHYSICS: BEAN EXPANSION & POROSITY",
            fontsize=10.5, fontweight="bold", color=C_RUST, ha="left", va="center", zorder=2)

    # Green bean visual (equal-aspect circle via inset or scaled ellipse)
    ax_roast = fig.add_axes([0.03, 0.145, 0.445, 0.335])
    ax_roast.set_facecolor(C_CARD)
    ax_roast.set_aspect("equal")
    ax_roast.set_xlim(0, 6.0)
    ax_roast.set_ylim(0, 2.8)
    ax_roast.axis("off")

    # Green bean
    gb_c = (1.15, 1.80)
    ax_roast.add_patch(Circle(gb_c, 0.62, facecolor="#8CA67B", edgecolor="#465E38", lw=2.4, zorder=3))
    ax_roast.plot([gb_c[0], gb_c[0]], [gb_c[1] - 0.50, gb_c[1] + 0.50], color="#465E38", lw=1.8, zorder=4)
    ax_roast.text(gb_c[0], 0.92, "Green Bean (Raw)", ha="center", va="center", fontsize=10.0, fontweight="bold", color="#3A522D")
    ax_roast.text(gb_c[0], 0.70, "• Dense matrix (680 kg/m³)\n• Moisture: 10–12 wt%\n• Tough, rubbery cellulose",
                  ha="center", va="top", fontsize=8.5, color=C_MUTED, linespacing=1.38)

    # Thermal arrow
    draw_arrow(ax_roast, 2.00, 1.80, 3.35, 1.80, color=C_RUST, lw=3.0)
    ax_roast.text(2.68, 2.25, "200 – 240°C\nMaillard & Pyrolysis", ha="center", va="center",
                  fontsize=8.8, fontweight="bold", color=C_RUST)
    ax_roast.text(2.68, 1.40, "P_int = 15–25 atm\n'First Crack'", ha="center", va="center",
                  fontsize=8.2, color=C_MUTED)

    # Roasted bean (larger + cellular micro-pores)
    rb_c = (4.55, 1.80)
    ax_roast.add_patch(Circle(rb_c, 0.85, facecolor="#5C3317", edgecolor=C_ESPRESSO, lw=2.6, zorder=3))
    np.random.seed(42)
    for _ in range(32):
        ang = np.random.uniform(0, 2 * np.pi)
        rad = np.random.uniform(0.10, 0.70)
        px = rb_c[0] + rad * np.cos(ang)
        py = rb_c[1] + rad * np.sin(ang)
        ax_roast.add_patch(Circle((px, py), 0.065, facecolor="#D4A373", edgecolor="none", alpha=0.78, zorder=4))
    ax_roast.text(rb_c[0], 0.76, "Roasted Bean (+70% Vol)", ha="center", va="center", fontsize=10.0, fontweight="bold", color=C_ESPRESSO)
    ax_roast.text(rb_c[0], 0.56, "• Porous honeycomb (20–40 µm)\n• Bulk density: 400 kg/m³\n• Brittle -> ideal for roll crushing",
                  ha="center", va="top", fontsize=8.5, color=C_MUTED, linespacing=1.38)

    # Bottom kinetics bar inside BL panel (clean 2-line wrap)
    k_box = FancyBboxPatch((0.038, 0.045), 0.429, 0.085,
                           boxstyle="round,pad=0.004,rounding_size=0.010",
                           facecolor=C_LIGHT_BR, edgecolor=C_CREMA, lw=1.2, zorder=2)
    ax.add_patch(k_box)
    ax.text(0.252, 0.088,
            "Roasting Thermal Sequence:\n[25–130°C] Moisture Flash  ->  [130–170°C] Maillard Aroma  ->  [205°C] Pyrolysis  ->  [<30°C] Air Quench",
            ha="center", va="center", fontsize=8.0, fontweight="bold", color=C_ESPRESSO, linespacing=1.45, zorder=3)

    # --- BOTTOM RIGHT PANEL: DOUBLE ROLL CRUSHER & ANGLE OF NIP ---
    panel_br = FancyBboxPatch((0.50, 0.025), 0.480, 0.500,
                              boxstyle="round,pad=0.005,rounding_size=0.015",
                              facecolor=C_CARD, edgecolor=C_BORDER, linewidth=1.3, zorder=1)
    ax.add_patch(panel_br)
    ax.text(0.515, 0.502, "C. DOUBLE ROLL CRUSHER: ANGLE OF NIP & BOND'S LAW",
            fontsize=10.5, fontweight="bold", color=C_ESPRESSO, ha="left", va="center", zorder=2)

    # Equal-aspect inset cleanly bounded on left side of BR panel (x = 0.510 to 0.735)
    ax_inset = fig.add_axes([0.510, 0.115, 0.228, 0.355])
    ax_inset.set_facecolor(C_CARD)
    ax_inset.set_aspect("equal")
    ax_inset.set_xlim(-2.55, 2.55)
    ax_inset.set_ylim(-1.85, 2.35)
    ax_inset.axis("off")

    R = 1.10
    gap = 0.22
    cx_l = -(R + gap / 2)
    cx_r = +(R + gap / 2)

    for cx, sign in [(cx_l, 1), (cx_r, -1)]:
        ax_inset.add_patch(Circle((cx, 0), R, facecolor="#CBD5E1", edgecolor=C_ESPRESSO, lw=2.2, zorder=2))
        ax_inset.add_patch(Circle((cx, 0), R * 0.54, facecolor=C_BLUE_BG, edgecolor=C_BLUE, lw=1.3, ls="--", zorder=3))
        ax_inset.text(cx, 0, "Chilled\nRoll", ha="center", va="center", fontsize=7.5, fontweight="bold", color=C_BLUE, zorder=4)
        if sign == 1:
            draw_arrow(ax_inset, cx - 0.48, 0.65, cx + 0.45, 0.70, color=C_ESPRESSO, lw=1.6, rad=-0.35)
        else:
            draw_arrow(ax_inset, cx + 0.48, 0.65, cx - 0.45, 0.70, color=C_ESPRESSO, lw=1.6, rad=0.35)

    rp = 0.34
    yp = math.sqrt((R + rp) ** 2 - (R + gap / 2) ** 2)
    ax_inset.add_patch(Circle((0, yp), rp, facecolor="#6F3E1D", edgecolor=C_ESPRESSO, lw=2.0, zorder=5))
    ax_inset.text(0, yp + 0.56, "Feed Bean (Dp = 10.75 mm)", ha="center", va="center",
                  fontsize=8.2, fontweight="bold", color=C_ESPRESSO)

    ax_inset.plot([cx_l, 0, cx_r], [0, yp, 0], color=C_RUST, lw=1.5, ls=":", zorder=4)
    ax_inset.plot([0, 0], [-1.35, yp + 0.35], color=C_MUTED, lw=1.0, ls="--", zorder=1)

    ax_inset.annotate("", xy=(-gap / 2, -0.95), xytext=(gap / 2, -0.95),
                      arrowprops=dict(arrowstyle="<->", color=C_ESPRESSO, lw=1.4))
    ax_inset.text(0, -1.28, "Gap s = 0.50 mm", ha="center", va="center", fontsize=8.0, fontweight="bold", color=C_ESPRESSO)
    ax_inset.text(0, -1.65, "Crushed Output (dp < 2.09 mm)", ha="center", va="center", fontsize=8.0, fontweight="bold", color=C_GREEN)
    ax_inset.text(0, yp - 0.60, "α = 29.8°", ha="center", va="center", fontsize=8.4, fontweight="bold", color=C_RUST,
                  bbox=dict(boxstyle="round,pad=0.18", facecolor="#FFF5F0", edgecolor=C_RUST, lw=0.9), zorder=6)

    # Right side equations & verification cards inside BR panel (x = 0.748 to 0.964)
    eq_box1 = FancyBboxPatch((0.748, 0.275), 0.216, 0.195,
                             boxstyle="round,pad=0.004,rounding_size=0.010",
                             facecolor=C_GREEN_BG, edgecolor=C_GREEN, lw=1.4, zorder=2)
    ax.add_patch(eq_box1)
    ax.text(0.856, 0.445, "Angle of Nip Verification", ha="center", va="center", fontsize=9.2, fontweight="bold", color=C_GREEN)
    ax.text(0.856, 0.388, r"$\cos(\alpha/2) = \frac{D_R + s}{D_R + D_p}$", ha="center", va="center", fontsize=11.0, color=C_ESPRESSO)
    ax.text(0.856, 0.318, "α = 29.8° ≤ 35.5° (μ = 0.32)\n✓ ZERO-SLIP GRIPPING PASS",
            ha="center", va="center", fontsize=8.0, fontweight="bold", color=C_GREEN, linespacing=1.4)

    eq_box2 = FancyBboxPatch((0.748, 0.055), 0.216, 0.195,
                             boxstyle="round,pad=0.004,rounding_size=0.010",
                             facecolor=C_LIGHT_BR, edgecolor=C_ROAST, lw=1.4, zorder=2)
    ax.add_patch(eq_box2)
    ax.text(0.856, 0.225, "Bond's Comminution Law", ha="center", va="center", fontsize=9.2, fontweight="bold", color=C_ROAST)
    ax.text(0.856, 0.168, r"$P = 10 W_i \dot{m}\left(\frac{1}{\sqrt{d_{80,2}}} - \frac{1}{\sqrt{d_{80,1}}}\right)$",
            ha="center", va="center", fontsize=9.2, color=C_ESPRESSO)
    ax.text(0.856, 0.098, "Wi = 12.5 kWh/t · Load = 250 kg/h\nPower = 1.175 kW (Verified)",
            ha="center", va="center", fontsize=8.0, fontweight="bold", color=C_ESPRESSO, linespacing=1.4)

    # Clean footer note under inset rolls
    ax.text(0.624, 0.068, "Pure compression holds T < 28°C &\ncuts ultra-fine dust (<100 µm) by >60%.",
            ha="center", va="center", fontsize=8.0, fontweight="bold", color=C_MUTED, linespacing=1.35)

    for ext in ["png", "svg"]:
        path = os.path.join(OUT_DIR, f"slide1_upstream_comminution.{ext}")
        fig.savefig(path, dpi=300, facecolor=C_BG)
    plt.close(fig)
    print("Saved slide1_upstream_comminution.png & .svg")


# =============================================================================
# SLIDE 2 VISUAL: ROUTE A (ERGUN PACKED BED) vs ROUTE B (PERCOLATION BATTERY)
# =============================================================================
def generate_slide2():
    fig, ax = setup_canvas(
        "SLIDE 2 · Process Divergence: Route A (Ground) vs. Route B (Instant Extraction)",
        "Packed-Bed Fluid Hydraulics (Ergun Equation) vs. Industrial Counter-Current Pressurized Leaching Battery (14 bar)"
    )

    # --- LEFT HALF: ROUTE A (GROUND COFFEE & ERGUN HYDRAULICS) ---
    panel_l = FancyBboxPatch((0.02, 0.025), 0.465, 0.840,
                             boxstyle="round,pad=0.005,rounding_size=0.015",
                             facecolor=C_CARD, edgecolor=C_GREEN, linewidth=1.8, zorder=1)
    ax.add_patch(panel_l)
    ax.text(0.036, 0.840, "ROUTE A · GROUND COFFEE (R&G) — STOPS AT PACKAGING",
            fontsize=10.5, fontweight="bold", color=C_GREEN, ha="left", va="center", zorder=2)
    ax.text(0.036, 0.810, "Consumer extracts in brew basket  ->  Packed-Bed Fluid Mechanics governs cup quality",
            fontsize=8.4, color=C_MUTED, ha="left", va="center", zorder=2)

    # Ergun equation banner
    erg_box = FancyBboxPatch((0.036, 0.695), 0.433, 0.095,
                             boxstyle="round,pad=0.004,rounding_size=0.010",
                             facecolor=C_LIGHT_BR, edgecolor=C_CREMA, lw=1.3, zorder=2)
    ax.add_patch(erg_box)
    ax.text(0.252, 0.758, r"$\frac{\Delta P}{L} = 150\,\frac{(1-\epsilon)^2}{\epsilon^3}\,\frac{\mu\,u_0}{d_p^2} \;+\; 1.75\,\frac{1-\epsilon}{\epsilon^3}\,\frac{\rho\,u_0^2}{d_p}$",
            ha="center", va="center", fontsize=12.0, color=C_ESPRESSO, zorder=3)
    ax.text(0.252, 0.713, "Viscous resistance ∝ 1 / dp²  ->  50 µm fines exert 144× higher resistance than 600 µm grains!",
            ha="center", va="center", fontsize=7.9, fontweight="bold", color=C_RUST, zorder=3)

    # Sub-box 1: Conventional Bad Bed
    bad_box = FancyBboxPatch((0.036, 0.295), 0.208, 0.378,
                             boxstyle="round,pad=0.004,rounding_size=0.012",
                             facecolor="#FFF8F6", edgecolor=C_RUST, lw=1.5, zorder=2)
    ax.add_patch(bad_box)
    ax.text(0.140, 0.650, "Conventional Grinder", ha="center", va="center", fontsize=9.4, fontweight="bold", color=C_RUST)
    ax.text(0.140, 0.624, "Broad Bimodal PSD (Unscreened)", ha="center", va="center", fontsize=7.6, color=C_MUTED)

    bed_l = Rectangle((0.060, 0.390), 0.160, 0.205, facecolor="#F5ECE6", edgecolor=C_ESPRESSO, lw=1.5, zorder=3)
    ax.add_patch(bed_l)
    np.random.seed(7)
    for (bx, by, br) in [(0.088, 0.545, 0.016), (0.140, 0.555, 0.018), (0.188, 0.525, 0.015),
                         (0.105, 0.482, 0.017), (0.178, 0.455, 0.016), (0.135, 0.435, 0.014)]:
        ax.add_patch(Circle((bx, by), br, facecolor="#6E4223", edgecolor=C_ESPRESSO, lw=0.8, zorder=4))
    for fx in np.linspace(0.066, 0.214, 24):
        for fy in [0.396, 0.405, 0.413]:
            ax.add_patch(Circle((fx + np.random.uniform(-0.002, 0.002), fy), 0.0032,
                                facecolor=C_RUST, edgecolor="none", zorder=5))
    ax.plot([0.145, 0.153, 0.139, 0.155], [0.595, 0.525, 0.460, 0.390], color="#D93025", lw=2.4, zorder=6)
    draw_arrow(ax, 0.155, 0.412, 0.155, 0.382, color="#D93025", lw=2.0)
    ax.text(0.140, 0.346, "Filter Blinding & Channeling\n• Boulders -> Sour Under-Extract\n• Fines -> Bitter Astringent",
            ha="center", va="center", fontsize=7.6, fontweight="bold", color=C_RUST, linespacing=1.32)

    # Sub-box 2: BrewDz Screened Uniform Bed
    good_box = FancyBboxPatch((0.261, 0.295), 0.208, 0.378,
                              boxstyle="round,pad=0.004,rounding_size=0.012",
                              facecolor="#F4FBF6", edgecolor=C_GREEN, lw=1.5, zorder=2)
    ax.add_patch(good_box)
    ax.text(0.365, 0.650, "BrewDz PROD Powder", ha="center", va="center", fontsize=9.4, fontweight="bold", color=C_GREEN)
    ax.text(0.365, 0.624, "Narrow Cut (600 – 1100 µm)", ha="center", va="center", fontsize=7.6, color=C_MUTED)

    bed_r = Rectangle((0.285, 0.390), 0.160, 0.205, facecolor="#EDF7F0", edgecolor=C_ESPRESSO, lw=1.5, zorder=3)
    ax.add_patch(bed_r)
    for row_i, py in enumerate(np.linspace(0.412, 0.572, 5)):
        offset = 0.010 if row_i % 2 == 1 else 0.0
        for px in np.linspace(0.302, 0.420, 5):
            ax.add_patch(Circle((px + offset, py), 0.010, facecolor="#7A4B2A", edgecolor=C_ESPRESSO, lw=0.7, zorder=4))
    for sx in [0.312, 0.365, 0.418]:
        draw_arrow(ax, sx, 0.596, sx, 0.382, color=C_BLUE, lw=1.7, ls="-", zorder=6)
    ax.text(0.365, 0.346, "Uniform Laminar Flow\n• 0.00% Boulders (>1590 µm)\n• Even, Balanced Extraction",
            ha="center", va="center", fontsize=7.6, fontweight="bold", color=C_GREEN, linespacing=1.32)

    # Packaging flow at bottom of Route A
    draw_box(ax, 0.036, 0.148, 0.196, 0.112, "Degassing Silo", "CO2 Release (5–10 L/kg)\nN2 Blanket (4–24 h)",
             facecolor=C_LIGHT_BR, edgecolor=C_ROAST, title_fs=9.2, sub_fs=7.9)
    draw_arrow(ax, 0.236, 0.204, 0.270, 0.204, color=C_GREEN, lw=2.2)
    draw_box(ax, 0.273, 0.148, 0.196, 0.112, "MAP Foil Packaging", "N2 Flush (<0.5% O2)\n1-Way Silicone Valve",
             facecolor=C_GREEN_BG, edgecolor=C_GREEN, title_color=C_GREEN, title_fs=9.2, sub_fs=7.9)

    ax.text(0.252, 0.078, "✓ Route A Output: 41.8 kg/h Premium Specialty Ground Coffee\nPackaged directly after comminution & screening — Zero further processing",
            ha="center", va="center", fontsize=8.4, fontweight="bold", color=C_GREEN,
            bbox=dict(boxstyle="round,pad=0.38", facecolor=C_GREEN_BG, edgecolor=C_GREEN, lw=1.1), linespacing=1.4)

    # --- RIGHT HALF: ROUTE B (INSTANT COFFEE PERCOLATION BATTERY) ---
    panel_r = FancyBboxPatch((0.505, 0.025), 0.475, 0.840,
                             boxstyle="round,pad=0.005,rounding_size=0.015",
                             facecolor=C_CARD, edgecolor=C_BLUE, linewidth=1.8, zorder=1)
    ax.add_patch(panel_r)
    ax.text(0.522, 0.840, "ROUTE B · INSTANT COFFEE — INDUSTRIAL LEACHING BATTERY",
            fontsize=10.5, fontweight="bold", color=C_BLUE, ha="left", va="center", zorder=2)
    ax.text(0.522, 0.810, "Factory performs pressurized multi-stage counter-current solid-liquid extraction",
            fontsize=8.4, color=C_MUTED, ha="left", va="center", zorder=2)

    # Feed Callout Badge (BrewDz FINE stream)
    draw_box(ax, 0.522, 0.695, 0.440, 0.095,
             "Feed: BrewDz FINE Stream (55.2 kg/h, dp < 597 µm)",
             "Mass Transfer:  N_A = k_L·a·(C_s − C_b)   |   a = 6(1 − ε)/dp  ->  +200% Extraction Rate!",
             facecolor=C_BLUE_BG, edgecolor=C_BLUE, title_color=C_BLUE, title_fs=9.4, sub_fs=8.0)

    # 6-Column Counter-Current Percolation Battery
    ax.text(0.742, 0.665, "6-Column Counter-Current Pressurized Percolation Battery (P = 14 bar)",
            ha="center", va="center", fontsize=9.2, fontweight="bold", color=C_ESPRESSO)

    z1 = FancyBboxPatch((0.522, 0.355), 0.214, 0.288,
                        boxstyle="round,pad=0.003,rounding_size=0.010",
                        facecolor="#EDF7FC", edgecolor=C_BLUE, lw=1.2, ls="--", zorder=2)
    ax.add_patch(z1)
    ax.text(0.629, 0.622, "ZONE 1: ATMOSPHERIC", ha="center", va="center", fontsize=8.4, fontweight="bold", color=C_BLUE)
    ax.text(0.629, 0.597, "100 – 120°C (Fresh Grounds)", ha="center", va="center", fontsize=7.5, color=C_MUTED)

    z2 = FancyBboxPatch((0.748, 0.355), 0.214, 0.288,
                        boxstyle="round,pad=0.003,rounding_size=0.010",
                        facecolor="#FFF3EE", edgecolor=C_RUST, lw=1.2, ls="--", zorder=2)
    ax.add_patch(z2)
    ax.text(0.855, 0.622, "ZONE 2: THERMAL HYDROLYSIS", ha="center", va="center", fontsize=8.4, fontweight="bold", color=C_RUST)
    ax.text(0.855, 0.597, "160 – 180°C · 14 bar (Spent)", ha="center", va="center", fontsize=7.5, color=C_MUTED)

    col_xs = [0.540, 0.608, 0.676, 0.766, 0.834, 0.902]
    col_w, col_h, col_y = 0.046, 0.165, 0.415
    for idx, cx in enumerate(col_xs):
        is_hot = idx >= 3
        fc = "#D4A373" if not is_hot else "#A8643A"
        ec = C_BLUE if not is_hot else C_RUST
        ax.add_patch(FancyBboxPatch((cx, col_y), col_w, col_h,
                                    boxstyle="round,pad=0.002,rounding_size=0.008",
                                    facecolor=fc, edgecolor=ec, lw=1.8, zorder=3))
        ax.text(cx + col_w / 2, col_y + col_h / 2, f"C{idx+1}", ha="center", va="center",
                fontsize=9.2, fontweight="bold", color="#FFFFFF", zorder=4)
        if idx > 0:
            prev_x = col_xs[idx - 1]
            draw_arrow(ax, cx - 0.002, col_y + col_h * 0.5, prev_x + col_w + 0.002, col_y + col_h * 0.5,
                       color=C_RUST if idx >= 3 else C_BLUE, lw=1.9)

    draw_arrow(ax, 0.972, 0.498, 0.950, 0.498, color=C_RUST, lw=2.4)
    ax.text(0.905, 0.380, "Superheated Water IN\n(180°C, 14 bar)", ha="center", va="center",
            fontsize=7.5, fontweight="bold", color=C_RUST)

    draw_arrow(ax, 0.538, 0.498, 0.512, 0.498, color=C_BLUE, lw=2.4)
    ax.text(0.592, 0.380, "Rich Extract OUT\n(15 wt% Solids -> Slide 3)", ha="center", va="center",
            fontsize=7.5, fontweight="bold", color=C_BLUE)

    # Yield Breakthrough Cards
    draw_box(ax, 0.522, 0.155, 0.208, 0.170,
             "Stage 1 Yield: 20 – 25%",
             "Extracts freely soluble:\n• Caffeine & Trigonelline\n• Sucrose & Organic Acids\n• Primary Aroma Volatiles",
             facecolor=C_BLUE_BG, edgecolor=C_BLUE, title_color=C_BLUE, title_fs=9.2, sub_fs=7.8,
             title_y=0.80, sub_y=0.38)

    draw_arrow(ax, 0.733, 0.240, 0.752, 0.240, color=C_RUST, lw=2.4)

    draw_box(ax, 0.754, 0.155, 0.208, 0.170,
             "Total Yield: 45 – 50%!",
             "Thermal Hydrolysis cleaves:\n• Insoluble Galactomannans\n• Arabinogalactan Cell Walls\n-> Soluble Oligosaccharides",
             facecolor=C_RUST_BG, edgecolor=C_RUST, title_color=C_RUST, title_fs=9.2, sub_fs=7.8,
             title_y=0.80, sub_y=0.38)

    ax.text(0.742, 0.078, "✓ Breakthrough: Thermal hydrolysis doubles solid recovery (25% -> 48%)\nValorizing 100% of BrewDz's FINE stream into profitable instant coffee!",
            ha="center", va="center", fontsize=8.3, fontweight="bold", color=C_BLUE,
            bbox=dict(boxstyle="round,pad=0.38", facecolor=C_BLUE_BG, edgecolor=C_BLUE, lw=1.1), linespacing=1.4)

    for ext in ["png", "svg"]:
        path = os.path.join(OUT_DIR, f"slide2_process_divergence.{ext}")
        fig.savefig(path, dpi=300, facecolor=C_BG)
    plt.close(fig)
    print("Saved slide2_process_divergence.png & .svg")


# =============================================================================
# SLIDE 3 VISUAL: DEHYDRATION + AGGLOMERATION + ASPEN ZERO-WASTE MASS BALANCE
# =============================================================================
def generate_slide3():
    fig, ax = setup_canvas(
        "SLIDE 3 · Instant Coffee Dehydration, Agglomeration & Zero-Waste Balance",
        "Extract Concentration, Spray vs. Freeze Drying, Capillary Instantization & Validated Aspen Plus Circuit Closure"
    )

    # --- TOP PANEL: DOWNSTREAM INSTANT COFFEE REFINEMENT & DEHYDRATION ---
    panel_t = FancyBboxPatch((0.02, 0.405), 0.96, 0.462,
                             boxstyle="round,pad=0.005,rounding_size=0.015",
                             facecolor=C_CARD, edgecolor=C_BORDER, linewidth=1.3, zorder=1)
    ax.add_patch(panel_t)
    ax.text(0.035, 0.844, "A. INSTANT COFFEE DOWNSTREAM REFINEMENT, DEHYDRATION & AGGLOMERATION",
            fontsize=10.5, fontweight="bold", color=C_BLUE, ha="left", va="center", zorder=2)

    # Left-to-right pre-drying chain
    draw_box(ax, 0.035, 0.625, 0.115, 0.130, "Rich Extract", "15 wt% Solids\nFrom Battery",
             facecolor=C_BLUE_BG, edgecolor=C_BLUE, title_color=C_BLUE, title_fs=9.3, sub_fs=7.8)
    draw_arrow(ax, 0.153, 0.690, 0.178, 0.690, color=C_ESPRESSO, lw=2.0)

    draw_box(ax, 0.181, 0.625, 0.125, 0.130, "Aroma Stripper", "Vacuum Flash\n60°C · 0.3 bar",
             facecolor=C_GREEN_BG, edgecolor=C_GREEN, title_color=C_GREEN, title_fs=9.3, sub_fs=7.8)
    draw_arrow(ax, 0.309, 0.690, 0.334, 0.690, color=C_ESPRESSO, lw=2.0)

    draw_box(ax, 0.337, 0.625, 0.115, 0.130, "Centrifuge", "Disc-Stack\n7,000×g (>50µm)",
             facecolor=C_LIGHT_BR, edgecolor=C_ROAST, title_color=C_ROAST, title_fs=9.3, sub_fs=7.8)
    draw_arrow(ax, 0.455, 0.690, 0.480, 0.690, color=C_ESPRESSO, lw=2.0)

    draw_box(ax, 0.483, 0.625, 0.125, 0.130, "3-Effect Evap.", "Falling Film Vac.\n15% -> 40% TS",
             facecolor=C_BLUE_BG, edgecolor=C_BLUE, title_color=C_BLUE, title_fs=9.3, sub_fs=7.8)

    # Aroma bypass line
    ax.plot([0.243, 0.243, 0.628, 0.628], [0.758, 0.804, 0.804, 0.695],
            color=C_GREEN, lw=2.0, linestyle="--", zorder=4)
    draw_arrow(ax, 0.628, 0.720, 0.628, 0.692, color=C_GREEN, lw=2.0)
    ax.text(0.436, 0.816, "Volatile Top-Note Aromas Captured (4°C N2) & Re-Injected Before Drying",
            ha="center", va="center", fontsize=8.0, fontweight="bold", color=C_GREEN,
            bbox=dict(boxstyle="round,pad=0.20", facecolor=C_GREEN_BG, edgecolor=C_GREEN, lw=0.9), zorder=5)

    # Branch from Evaporator to Spray Drying & Freeze Drying
    ax.plot([0.610, 0.642], [0.690, 0.690], color=C_ESPRESSO, lw=2.0, zorder=3)
    draw_arrow(ax, 0.642, 0.690, 0.666, 0.740, color=C_RUST, lw=2.0)
    draw_arrow(ax, 0.642, 0.690, 0.666, 0.515, color=C_BLUE, lw=2.0)

    # Branch 1: Spray Drying + Steam Agglomeration
    draw_box(ax, 0.668, 0.665, 0.145, 0.145,
             "1. SPRAY DRYING",
             "220°C Air · 100 bar\nHollow Spheres (100 µm)\nFast · Low CapEx",
             facecolor=C_RUST_BG, edgecolor=C_RUST, title_color=C_RUST, title_fs=9.2, sub_fs=7.8,
             title_y=0.77, sub_y=0.35)
    draw_arrow(ax, 0.816, 0.738, 0.838, 0.738, color=C_RUST, lw=2.0)
    draw_box(ax, 0.840, 0.665, 0.128, 0.145,
             "Agglomeration",
             "105°C Steam Sinter\nPorous 1.5–2.0 mm\nDissolves < 3 s!",
             facecolor=C_LIGHT_BR, edgecolor=C_ESPRESSO, title_color=C_ESPRESSO, title_fs=9.2, sub_fs=7.8,
             title_y=0.77, sub_y=0.35)

    # Branch 2: Freeze Drying (Lyophilization) — cleanly wrapped 3-line subtitle
    draw_box(ax, 0.668, 0.435, 0.300, 0.185,
             "2. FREEZE DRYING (LYOPHILIZATION — PREMIUM)",
             "• N2 Pre-Foaming -> Belt Freeze (-45°C) -> Granulate\n"
             "• Deep Vacuum Sublimation (0.2 mbar < 6.11 mbar Triple Pt.)\n"
             "• ΔH_sub = 2838 kJ/kg · 100% Aroma · Golden Glass Crystals",
             facecolor=C_BLUE_BG, edgecolor=C_BLUE, title_color=C_BLUE, title_fs=9.0, sub_fs=7.8,
             title_y=0.82, sub_y=0.38)

    # Agglomeration Washburn physics callout box (cleanly separated from equation box)
    wash_box = FancyBboxPatch((0.035, 0.435), 0.573, 0.155,
                              boxstyle="round,pad=0.004,rounding_size=0.010",
                              facecolor="#FFFBF5", edgecolor=C_CREMA, lw=1.4, zorder=2)
    ax.add_patch(wash_box)
    ax.text(0.050, 0.564, "WHY AGGLOMERATION MATTERS (WASHBURN CAPILLARY PHYSICS):",
            ha="left", va="center", fontsize=8.8, fontweight="bold", color=C_ROAST)
    ax.text(0.050, 0.495,
            "• Raw spray-dried dust (50–100 µm) forms floating\n"
            "  hydrophobic clumps ('fish-eyes') in hot water.\n"
            "• Steam liquid bridges sinter dust into porous clusters\n"
            "  that pull water inward via rapid capillary suction.",
            ha="left", va="center", fontsize=7.9, color=C_ESPRESSO, linespacing=1.32)
    ax.text(0.592, 0.498, r"$L^2 = \frac{\gamma\,r_{\mathrm{pore}}\cos\theta}{2\mu}\,t$",
            ha="right", va="center", fontsize=12.0, color=C_ESPRESSO,
            bbox=dict(boxstyle="round,pad=0.30", facecolor=C_LIGHT_BR, edgecolor=C_ROAST, lw=1.0))

    # --- BOTTOM PANEL: ASPEN PLUS VALIDATED ZERO-WASTE MASS BALANCE ---
    panel_b = FancyBboxPatch((0.02, 0.025), 0.96, 0.355,
                             boxstyle="round,pad=0.005,rounding_size=0.015",
                             facecolor=C_CARD, edgecolor=C_GREEN, linewidth=1.8, zorder=1)
    ax.add_patch(panel_b)
    ax.text(0.035, 0.356, "B. BREWDZ CLOSED-LOOP ZERO-WASTE SYNTHESIS (ASPEN PLUS V14 VALIDATED MASS BALANCE)",
            fontsize=10.5, fontweight="bold", color=C_GREEN, ha="left", va="center", zorder=2)

    by = 0.138
    bh = 0.115
    draw_box(ax, 0.035, by, 0.115, bh, "RAW FEED", "100.0 kg/h\n97 Solids + 3 H2O",
             facecolor=C_LIGHT_BR, edgecolor=C_ESPRESSO, title_fs=9.3, sub_fs=7.9)
    draw_arrow(ax, 0.153, by + bh / 2, 0.185, by + bh / 2, color=C_ESPRESSO, lw=2.2)

    draw_box(ax, 0.188, by, 0.115, bh, "ROASTER", "210°C · 1.01 bar\nFlashes 3 kg/h H2O",
             facecolor=C_RUST_BG, edgecolor=C_RUST, title_color=C_RUST, title_fs=9.3, sub_fs=7.9)
    draw_arrow(ax, 0.306, by + bh / 2, 0.343, by + bh / 2, color=C_ESPRESSO, lw=2.2)
    ax.text(0.324, by + bh / 2 + 0.026, "97.0\nkg/h", ha="center", va="center", fontsize=7.8, fontweight="bold", color=C_ESPRESSO)

    draw_box(ax, 0.346, by, 0.100, bh, "MIXER", "Fresh +\nRecycle",
             facecolor=C_LIGHT_BR, edgecolor=C_ROAST, title_color=C_ROAST, title_fs=9.3, sub_fs=7.9)
    draw_arrow(ax, 0.449, by + bh / 2, 0.486, by + bh / 2, color=C_ESPRESSO, lw=2.2)
    ax.text(0.467, by + bh / 2 + 0.026, "120.0\nkg/h", ha="center", va="center", fontsize=7.8, fontweight="bold", color=C_ESPRESSO)

    draw_box(ax, 0.489, by, 0.115, bh, "CRUSHER", "Double Roll Mill\ndp < 2087 µm",
             facecolor=C_LIGHT_BR, edgecolor=C_ESPRESSO, title_fs=9.3, sub_fs=7.9)
    draw_arrow(ax, 0.607, by + bh / 2, 0.637, by + bh / 2, color=C_ESPRESSO, lw=2.2)

    draw_box(ax, 0.640, by, 0.105, bh, "SCREEN", "Multi-Deck\nVibrating Sieve",
             facecolor=C_GREEN_BG, edgecolor=C_GREEN, title_color=C_GREEN, title_fs=9.3, sub_fs=7.9)

    # Recycle stream loop
    ax.plot([0.692, 0.692, 0.396, 0.396], [by + bh + 0.005, 0.305, 0.305, by + bh + 0.012],
            color=C_RUST, lw=2.3, linestyle="--", zorder=4)
    draw_arrow(ax, 0.396, 0.278, 0.396, by + bh + 0.005, color=C_RUST, lw=2.3)
    ax.text(0.544, 0.319, "OVERSIZE RECYCLE: 23.0 kg/h (R/F = 0.24, 1093–2087 µm) -> 100% RECOVERED",
            ha="center", va="center", fontsize=8.2, fontweight="bold", color=C_RUST,
            bbox=dict(boxstyle="round,pad=0.22", facecolor=C_RUST_BG, edgecolor=C_RUST, lw=0.9), zorder=5)

    # Dual Product Exits
    draw_arrow(ax, 0.748, by + bh * 0.72, 0.785, 0.268, color=C_GREEN, lw=2.5)
    draw_arrow(ax, 0.748, by + bh * 0.28, 0.785, 0.145, color=C_BLUE, lw=2.5)

    draw_box(ax, 0.788, 0.220, 0.178, 0.098,
             "PROD: 41.8 kg/h (43%)",
             "600–1100 µm · 0% Boulders\n-> Route A: Ground Coffee",
             facecolor=C_GREEN_BG, edgecolor=C_GREEN, title_color=C_GREEN, title_fs=9.0, sub_fs=7.8, lw=1.9)

    draw_box(ax, 0.788, 0.095, 0.178, 0.098,
             "FINE: 55.2 kg/h (57%)",
             "< 597 µm · High Surface Area\n-> Route B: Instant Coffee",
             facecolor=C_BLUE_BG, edgecolor=C_BLUE, title_color=C_BLUE, title_fs=9.0, sub_fs=7.8, lw=1.9)

    # Bottom Summary Ribbon centered cleanly inside bottom panel
    ax.text(0.50, 0.056,
            "MASS BALANCE CLOSURE:   97.0 kg/h Dry Roasted Feed  =  41.8 kg/h (PROD) + 55.2 kg/h (FINE)   |   100% VALORIZATION · ZERO SOLID WASTE",
            ha="center", va="center", fontsize=8.4, fontweight="bold", color="#FFFFFF",
            bbox=dict(boxstyle="round,pad=0.35", facecolor=C_ESPRESSO, edgecolor=C_CREMA, lw=1.3), zorder=5)

    for ext in ["png", "svg"]:
        path = os.path.join(OUT_DIR, f"slide3_dehydration_mass_balance.{ext}")
        fig.savefig(path, dpi=300, facecolor=C_BG)
    plt.close(fig)
    print("Saved slide3_dehydration_mass_balance.png & .svg")


if __name__ == "__main__":
    generate_slide1()
    generate_slide2()
    generate_slide3()
    print(f"All 3 high-resolution slide visuals generated in: {OUT_DIR}")
