"""
BrewDz Particle Engineering Pvt. Ltd. — ChE 303 Part 2 Slide Visuals
Generates 3 clean, audience-friendly, math-free 16:9 (300 DPI) infographics & flowcharts
explaining:
  Slide 1: Why Coffee Making & Types of Coffee Beans (Arabica vs. Robusta vs. Liberica/Excelsa)
  Slide 2: General Coffee Making Procedure (Farm Cherry -> Green Bean -> Roast -> Grind)
  Slide 3: Ground Coffee vs. Instant Coffee (How They Differ + Spray vs. Freeze Drying)
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Ellipse

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "slide_visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# Warm Coffee Infographic Palette
C_BG       = "#FAF6F0"   # Warm cream canvas
C_CARD     = "#FFFFFF"   # Clean white card
C_ESPRESSO = "#2C1810"   # Deep espresso brown
C_CREMA    = "#D4A373"   # Golden crema accent
C_ROAST    = "#8A5A2B"   # Medium roast brown
C_TAN      = "#F3E8DC"   # Soft warm beige
C_GREEN    = "#1B6B3A"   # Fresh leaf / Arabica green
C_GREEN_BG = "#E8F5EE"   # Soft mint green
C_RUST     = "#B84A1A"   # Warm roast / Robusta terracotta
C_RUST_BG  = "#FCECE6"   # Soft terracotta tint
C_BLUE     = "#1D5B79"   # Cool blue (Instant / Freeze)
C_BLUE_BG  = "#E6F2F8"   # Soft blue tint
C_GOLD     = "#9A6B16"   # Premium gold
C_GOLD_BG  = "#FDF6E3"   # Soft gold tint
C_MUTED    = "#6B5B53"   # Secondary body text
C_BORDER   = "#DECDBB"   # Soft card outline

plt.rcParams["font.family"] = "DejaVu Sans"


def draw_card(ax, x, y, w, h, facecolor=C_CARD, edgecolor=C_BORDER, lw=1.4, radius=0.015, zorder=2):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0.004,rounding_size={radius}",
                       facecolor=facecolor, edgecolor=edgecolor, linewidth=lw, zorder=zorder)
    ax.add_patch(p)
    return p


def draw_box(ax, x, y, w, h, title, subtitle="", facecolor=C_CARD, edgecolor=C_ESPRESSO,
             title_color=C_ESPRESSO, sub_color=C_MUTED, lw=1.6, title_fs=10.0, sub_fs=8.2,
             radius=0.012, zorder=3, title_y=0.68, sub_y=0.30):
    draw_card(ax, x, y, w, h, facecolor=facecolor, edgecolor=edgecolor, lw=lw, radius=radius, zorder=zorder)
    if subtitle:
        ax.text(x + w / 2, y + h * title_y, title, ha="center", va="center",
                fontsize=title_fs, fontweight="bold", color=title_color, zorder=zorder + 1)
        ax.text(x + w / 2, y + h * sub_y, subtitle, ha="center", va="center",
                fontsize=sub_fs, color=sub_color, zorder=zorder + 1, linespacing=1.32)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center",
                fontsize=title_fs, fontweight="bold", color=title_color, zorder=zorder + 1)


def draw_arrow(ax, x1, y1, x2, y2, color=C_ROAST, lw=2.2, style="-|>", rad=0.0, ls="-", zorder=4):
    arr = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=15,
                          color=color, linewidth=lw, linestyle=ls,
                          connectionstyle=f"arc3,rad={rad}", zorder=zorder)
    ax.add_patch(arr)


def draw_bean_icon(ax, cx, cy, rx, ry, angle_deg, fill_color, edge_color, crease="s", zorder=5):
    bean = Ellipse((cx, cy), rx * 2, ry * 2, angle=angle_deg,
                   facecolor=fill_color, edgecolor=edge_color, lw=2.0, zorder=zorder)
    ax.add_patch(bean)
    # Center crease line
    t = np.linspace(-0.72, 0.72, 30)
    if crease == "s":
        lx = 0.18 * rx * np.sin(t * np.pi)
    else:
        lx = np.zeros_like(t)
    ly = t * ry
    ang = np.radians(angle_deg)
    xr = cx + lx * np.cos(ang) - ly * np.sin(ang)
    yr = cy + lx * np.sin(ang) + ly * np.cos(ang)
    ax.plot(xr, yr, color=edge_color, lw=2.0, solid_capstyle="round", zorder=zorder + 1)


def setup_canvas(title, subtitle, slide_tag):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Espresso header banner
    ax.add_patch(Rectangle((0, 0.892), 1, 0.108, facecolor=C_ESPRESSO, edgecolor="none", zorder=1))
    ax.add_patch(Rectangle((0, 0.884), 1, 0.008, facecolor=C_CREMA, edgecolor="none", zorder=2))

    ax.text(0.028, 0.956, title, ha="left", va="center",
            fontsize=17.0, fontweight="bold", color="#FFFFFF", zorder=3)
    ax.text(0.028, 0.916, subtitle, ha="left", va="center",
            fontsize=10.5, color=C_CREMA, zorder=3)
    ax.text(0.972, 0.946, slide_tag, ha="right", va="center",
            fontsize=10.5, fontweight="bold", color="#E8D8C8", zorder=3)
    return fig, ax


# =============================================================================
# SLIDE 1: WHY COFFEE MAKING & TYPES OF COFFEE BEANS
# =============================================================================
def generate_slide1():
    fig, ax = setup_canvas(
        "Why Coffee Making Matters & Types of Coffee Beans",
        "Understanding the global beverage, why processing shapes every sip, and the beans behind every cup",
        "Part 2 · Slide 1 of 3"
    )

    # --- TOP STRIP: WHY COFFEE? (3 STAT HIGHLIGHTS) ---
    why_cards = [
        ("2+ Billion Cups / Day", "World's 2nd most traded commodity\n& a rapidly growing market in India", C_TAN, C_ROAST),
        ("Bean-to-Cup Quality", "Flavor, aroma & smoothness depend on\nbean type, roasting, and grind size", C_GREEN_BG, C_GREEN),
        ("Two Major Markets", "Specialty Cafés (Ground Coffee) &\nEveryday Convenience (Instant Coffee)", C_BLUE_BG, C_BLUE),
    ]
    for i, (t, s, fc, ec) in enumerate(why_cards):
        draw_box(ax, 0.028 + i * 0.322, 0.725, 0.300, 0.130, t, s,
                 facecolor=fc, edgecolor=ec, title_color=ec, sub_color=C_ESPRESSO,
                 title_fs=12.0, sub_fs=9.0, lw=1.7, title_y=0.70, sub_y=0.30)

    # Section Heading
    ax.text(0.028, 0.678, "MAIN TYPES OF COFFEE BEANS AROUND THE WORLD",
            fontsize=11.5, fontweight="bold", color=C_ESPRESSO, ha="left", va="center")

    # --- ARABICA CARD (LEFT) ---
    draw_card(ax, 0.028, 0.120, 0.345, 0.525, facecolor=C_CARD, edgecolor=C_GREEN, lw=2.0)
    ax.add_patch(FancyBboxPatch((0.028, 0.565), 0.345, 0.080,
                                boxstyle="round,pad=0.004,rounding_size=0.015",
                                facecolor=C_GREEN, edgecolor=C_GREEN, lw=1.0, zorder=3))
    ax.text(0.200, 0.618, "1. ARABICA", ha="center", va="center", fontsize=14.0, fontweight="bold", color="#FFFFFF", zorder=4)
    ax.text(0.200, 0.584, "~60 – 70% of Global Production  ·  'The Flavor Bean'", ha="center", va="center", fontsize=8.8, color="#D8F3DC", zorder=4)

    # Bean visual inset (equal aspect)
    ax_b1 = fig.add_axes([0.145, 0.435, 0.11, 0.115])
    ax_b1.set_aspect("equal"); ax_b1.axis("off"); ax_b1.set_xlim(-1, 1); ax_b1.set_ylim(-1, 1)
    draw_bean_icon(ax_b1, 0, 0, 0.55, 0.80, -18, "#6E3F1E", C_ESPRESSO, crease="s")

    ax.text(0.200, 0.422, "Oval bean with curved 'S' crease", ha="center", va="center", fontsize=8.4, style="italic", color=C_MUTED)
    arabica_pts = (
        "•  Taste:  Smooth, sweet, fruity & aromatic\n"
        "•  Caffeine:  Lower (~1.2% — gentle kick)\n"
        "•  Growing:  High altitudes (cooler hills)\n"
        "•  Cost:  More delicate & premium priced\n"
        "•  Best For:  Specialty & Roast-and-Ground\n"
        "   coffee (Pour-over, Drip, Espresso)"
    )
    ax.text(0.050, 0.388, arabica_pts, ha="left", va="top", fontsize=9.3, color=C_ESPRESSO, linespacing=1.55)

    # --- ROBUSTA CARD (MIDDLE) ---
    draw_card(ax, 0.395, 0.120, 0.345, 0.525, facecolor=C_CARD, edgecolor=C_RUST, lw=2.0)
    ax.add_patch(FancyBboxPatch((0.395, 0.565), 0.345, 0.080,
                                boxstyle="round,pad=0.004,rounding_size=0.015",
                                facecolor=C_RUST, edgecolor=C_RUST, lw=1.0, zorder=3))
    ax.text(0.567, 0.618, "2. ROBUSTA", ha="center", va="center", fontsize=14.0, fontweight="bold", color="#FFFFFF", zorder=4)
    ax.text(0.567, 0.584, "~30 – 40% of Global Production  ·  'The Strength Bean'", ha="center", va="center", fontsize=8.8, color="#FDE2D8", zorder=4)

    ax_b2 = fig.add_axes([0.512, 0.435, 0.11, 0.115])
    ax_b2.set_aspect("equal"); ax_b2.axis("off"); ax_b2.set_xlim(-1, 1); ax_b2.set_ylim(-1, 1)
    draw_bean_icon(ax_b2, 0, 0, 0.64, 0.72, -12, "#4B2611", C_ESPRESSO, crease="straight")

    ax.text(0.567, 0.422, "Rounder bean with straight crease", ha="center", va="center", fontsize=8.4, style="italic", color=C_MUTED)
    robusta_pts = (
        "•  Taste:  Bold, earthy, strong & bitter punch\n"
        "•  Caffeine:  Nearly 2× higher (~2.2%)\n"
        "•  Growing:  Hardy; lower hills (South India)\n"
        "•  Cost:  Higher crop yield & economical\n"
        "•  Best For:  Instant Coffee powders &\n"
        "   thick-crema Espresso / Filter blends"
    )
    ax.text(0.417, 0.388, robusta_pts, ha="left", va="top", fontsize=9.3, color=C_ESPRESSO, linespacing=1.55)

    # --- LIBERICA & EXCELSA CARD (RIGHT) ---
    draw_card(ax, 0.762, 0.120, 0.210, 0.525, facecolor=C_GOLD_BG, edgecolor=C_GOLD, lw=1.8)
    ax.add_patch(FancyBboxPatch((0.762, 0.565), 0.210, 0.080,
                                boxstyle="round,pad=0.004,rounding_size=0.015",
                                facecolor=C_GOLD, edgecolor=C_GOLD, lw=1.0, zorder=3))
    ax.text(0.867, 0.618, "3. NICHE BEANS", ha="center", va="center", fontsize=12.0, fontweight="bold", color="#FFFFFF", zorder=4)
    ax.text(0.867, 0.584, "< 2% of Global Market", ha="center", va="center", fontsize=8.5, color="#FFF3CD", zorder=4)

    niche_pts = (
        "LIBERICA\n"
        "• Large, irregular teardrop\n"
        "  shaped beans\n"
        "• Smoky, woody & floral\n"
        "• Popular in SE Asia\n\n"
        "EXCELSA\n"
        "• Tart, fruity & dark notes\n"
        "• Added to blends for\n"
        "  extra depth & complexity"
    )
    ax.text(0.778, 0.525, niche_pts, ha="left", va="top", fontsize=9.0, color=C_ESPRESSO, linespacing=1.48)

    # Bottom Takeaway Ribbon
    ax.text(0.50, 0.056,
            "KEY TAKEAWAY:   Arabica delivers smooth aroma for café Ground Coffee  |  Robusta delivers bold strength & high yield for Instant Coffee",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color="#FFFFFF",
            bbox=dict(boxstyle="round,pad=0.45", facecolor=C_ESPRESSO, edgecolor=C_CREMA, lw=1.4), zorder=5)

    for ext in ["png", "svg"]:
        fig.savefig(os.path.join(OUT_DIR, f"slide1_beans_and_why.{ext}"), dpi=300, facecolor=C_BG)
    plt.close(fig)
    print("Saved slide1_beans_and_why.png & .svg")


# =============================================================================
# SLIDE 2: GENERAL COFFEE MAKING PROCEDURE (FARM CHERRY TO POWDER)
# =============================================================================
def generate_slide2():
    fig, ax = setup_canvas(
        "General Coffee Making Procedure: From Farm Cherry to Powder",
        "The 6 core stages that transform raw fruit seeds on the farm into aromatic coffee powder",
        "Part 2 · Slide 2 of 3"
    )

    # --- TOP ROW: STAGES 1, 2, 3 ---
    row1_y = 0.535
    card_w, card_h = 0.285, 0.300
    xs = [0.032, 0.357, 0.682]

    stages_r1 = [
        ("STEP 1 · HARVEST & HULLING",
         "From Red Cherry to Green Bean",
         "• Ripe coffee cherries are hand-picked\n"
         "• Outer fruit pulp is removed using:\n"
         "   - Dry (Natural) sun-drying, OR\n"
         "   - Wet (Washed) water processing\n"
         "• Leaves raw, dense Green Beans",
         "#D94F3D", "#FDECE9"),
        ("STEP 2 · CLEANING & SORTING",
         "Quality Control Before Heating",
         "• Air blowers remove light dust & husks\n"
         "• Gravity de-stoners remove tiny pebbles\n"
         "• Magnets remove stray metal bits\n"
         "• Beans are sorted by size & blended\n"
         "  (e.g., Arabica + Robusta ratios)",
         C_BLUE, C_BLUE_BG),
        ("STEP 3 · ROASTING (200–240°C)",
         "Where Coffee Gets Its Flavor!",
         "• Green beans have almost NO coffee smell\n"
         "• High heat turns beans brown, puffs\n"
         "  them up, and makes them crunchy\n"
         "• Unlocks 800+ aroma compounds\n"
         "• Light (fruity) -> Medium -> Dark (bold)",
         C_RUST, C_RUST_BG),
    ]

    for i, (hdr, sub, body, col, bg) in enumerate(stages_r1):
        draw_card(ax, xs[i], row1_y, card_w, card_h, facecolor=C_CARD, edgecolor=col, lw=1.9)
        ax.add_patch(FancyBboxPatch((xs[i], row1_y + card_h - 0.068), card_w, 0.068,
                                    boxstyle="round,pad=0.004,rounding_size=0.014",
                                    facecolor=col, edgecolor=col, lw=1.0, zorder=3))
        ax.text(xs[i] + card_w / 2, row1_y + card_h - 0.025, hdr, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color="#FFFFFF", zorder=4)
        ax.text(xs[i] + card_w / 2, row1_y + card_h - 0.052, sub, ha="center", va="center",
                fontsize=8.4, color="#FFF3EB", zorder=4)
        ax.text(xs[i] + 0.016, row1_y + card_h - 0.090, body, ha="left", va="top",
                fontsize=9.1, color=C_ESPRESSO, linespacing=1.48, zorder=4)

    # Arrows across Row 1
    draw_arrow(ax, xs[0] + card_w + 0.006, row1_y + card_h / 2, xs[1] - 0.006, row1_y + card_h / 2, color=C_ROAST, lw=3.0)
    draw_arrow(ax, xs[1] + card_w + 0.006, row1_y + card_h / 2, xs[2] - 0.006, row1_y + card_h / 2, color=C_ROAST, lw=3.0)

    # Snake connector arrow from Step 3 down to Step 4 (Row 2)
    row2_y = 0.140
    ax.plot([0.825, 0.825, 0.175, 0.175], [row1_y - 0.006, 0.488, 0.488, row2_y + card_h + 0.018],
            color=C_ROAST, lw=2.8, linestyle="-", zorder=3)
    draw_arrow(ax, 0.175, row2_y + card_h + 0.028, 0.175, row2_y + card_h + 0.005, color=C_ROAST, lw=2.8)
    ax.text(0.50, 0.498, "Roasted Beans Move Immediately to Cooling & Grinding",
            ha="center", va="center", fontsize=8.8, fontweight="bold", color=C_ROAST,
            bbox=dict(boxstyle="round,pad=0.22", facecolor=C_TAN, edgecolor=C_CREMA, lw=1.0), zorder=5)

    # --- BOTTOM ROW: STAGES 4, 5, 6 ---
    stages_r2 = [
        ("STEP 4 · RAPID COOLING",
         "Locking In Fresh Aroma",
         "• Roasted beans leave hot (~210°C)\n"
         "• Must cool quickly (< 1 minute) using\n"
         "  chilled air trays so they don't over-cook\n"
         "• Prevents burning delicate flavor oils\n"
         "• Beans rest briefly to release CO2 gas",
         C_BLUE, C_BLUE_BG),
        ("STEP 5 · GRINDING (KEY STEP!)",
         "Controlling Particle Size",
         "• Roasted beans are crushed into powder\n"
         "• Different brews need different sizes:\n"
         "   - Coarse -> French Press / Cold Brew\n"
         "   - Medium -> Filter / Pour-over\n"
         "   - Fine -> Espresso\n"
         "• Uneven grind = sour & bitter cup!",
         C_ESPRESSO, C_TAN),
        ("STEP 6 · THE FORK IN THE ROAD",
         "Two Final Coffee Products",
         "After grinding, the path splits into two:\n\n"
         "-> PATH A: GROUND COFFEE\n"
         "   Packaged directly in sealed bags!\n\n"
         "-> PATH B: INSTANT COFFEE\n"
         "   Factory brews & dries it into crystals!",
         C_GREEN, C_GREEN_BG),
    ]

    for i, (hdr, sub, body, col, bg) in enumerate(stages_r2):
        fc = C_TAN if i == 1 else (C_GREEN_BG if i == 2 else C_CARD)
        draw_card(ax, xs[i], row2_y, card_w, card_h, facecolor=fc, edgecolor=col, lw=2.2 if i >= 1 else 1.9)
        ax.add_patch(FancyBboxPatch((xs[i], row2_y + card_h - 0.068), card_w, 0.068,
                                    boxstyle="round,pad=0.004,rounding_size=0.014",
                                    facecolor=col, edgecolor=col, lw=1.0, zorder=3))
        ax.text(xs[i] + card_w / 2, row2_y + card_h - 0.025, hdr, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color="#FFFFFF", zorder=4)
        ax.text(xs[i] + card_w / 2, row2_y + card_h - 0.052, sub, ha="center", va="center",
                fontsize=8.4, color="#EFE6DD", zorder=4)
        ax.text(xs[i] + 0.016, row2_y + card_h - 0.090, body, ha="left", va="top",
                fontsize=9.1, color=C_ESPRESSO, linespacing=1.45, zorder=4)

    draw_arrow(ax, xs[0] + card_w + 0.006, row2_y + card_h / 2, xs[1] - 0.006, row2_y + card_h / 2, color=C_ROAST, lw=3.0)
    draw_arrow(ax, xs[1] + card_w + 0.006, row2_y + card_h / 2, xs[2] - 0.006, row2_y + card_h / 2, color=C_GREEN, lw=3.0)

    # Bottom Ribbon
    ax.text(0.50, 0.060,
            "INSIGHT:   Every cup of coffee — instant or café brewed — goes through Steps 1 to 5. Grinding uniformity is where great flavor is won or lost!",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color="#FFFFFF",
            bbox=dict(boxstyle="round,pad=0.45", facecolor=C_ESPRESSO, edgecolor=C_CREMA, lw=1.4), zorder=5)

    for ext in ["png", "svg"]:
        fig.savefig(os.path.join(OUT_DIR, f"slide2_general_process.{ext}"), dpi=300, facecolor=C_BG)
    plt.close(fig)
    print("Saved slide2_general_process.png & .svg")


# =============================================================================
# SLIDE 3: GROUND COFFEE VS. INSTANT COFFEE — HOW ARE THEY DIFFERENT?
# =============================================================================
def generate_slide3():
    fig, ax = setup_canvas(
        "Ground Coffee vs. Instant Coffee: How Are They Different?",
        "Same starting journey — completely different finish line, convenience, drying method, and bean choice",
        "Part 2 · Slide 3 of 3"
    )

    # --- TOP SHARED START BAR ---
    draw_box(ax, 0.14, 0.775, 0.72, 0.082,
             "SHARED STARTING JOURNEY (IDENTICAL FOR BOTH)",
             "Green Beans   ->   Cleaning & Sorting   ->   Roasting (Flavor Development)   ->   Cooling   ->   GRINDING",
             facecolor=C_TAN, edgecolor=C_ESPRESSO, title_color=C_ESPRESSO, sub_color=C_ROAST,
             title_fs=10.2, sub_fs=9.5, lw=1.8, title_y=0.70, sub_y=0.30)

    # Branching arrows down to Left (Ground) and Right (Instant)
    draw_arrow(ax, 0.36, 0.771, 0.25, 0.715, color=C_GREEN, lw=3.0)
    draw_arrow(ax, 0.64, 0.771, 0.74, 0.715, color=C_BLUE, lw=3.0)

    # --- LEFT PANEL: GROUND COFFEE (ROAST & GROUND) ---
    draw_card(ax, 0.028, 0.125, 0.450, 0.585, facecolor=C_CARD, edgecolor=C_GREEN, lw=2.2)
    ax.add_patch(FancyBboxPatch((0.028, 0.630), 0.450, 0.080,
                                boxstyle="round,pad=0.004,rounding_size=0.015",
                                facecolor=C_GREEN, edgecolor=C_GREEN, lw=1.0, zorder=3))
    ax.text(0.253, 0.682, "GROUND COFFEE (Roast & Ground)", ha="center", va="center",
            fontsize=13.0, fontweight="bold", color="#FFFFFF", zorder=4)
    ax.text(0.253, 0.648, "Stops right after grinding — You brew it yourself!", ha="center", va="center",
            fontsize=9.0, color="#D8F3DC", zorder=4)

    # Simple 2-step flow inside Ground Coffee card
    draw_box(ax, 0.052, 0.485, 0.180, 0.110, "1. Degas & Pack", "Sealed foil bags with\n1-way freshness valve",
             facecolor=C_GREEN_BG, edgecolor=C_GREEN, title_color=C_GREEN, title_fs=9.8, sub_fs=8.2)
    draw_arrow(ax, 0.236, 0.540, 0.270, 0.540, color=C_GREEN, lw=2.4)
    draw_box(ax, 0.274, 0.485, 0.180, 0.110, "2. You Brew It", "Filter / Espresso machine\n(Leaves wet grounds)",
             facecolor=C_TAN, edgecolor=C_ROAST, title_color=C_ESPRESSO, title_fs=9.8, sub_fs=8.2)

    ground_bullets = (
        "•  Typical Beans:  Mostly Arabica (or premium blends)\n"
        "•  Does It Dissolve?  NO — it is real crushed bean\n"
        "   particles; hot water passes through a filter\n"
        "•  Taste & Aroma:  Richest, freshest café flavor\n"
        "•  Preparation:  Takes 2–5 mins + brewing equipment\n"
        "•  Examples:  Blue Tokai, Filter Coffee, Café Espresso"
    )
    ax.text(0.052, 0.445, ground_bullets, ha="left", va="top", fontsize=9.3, color=C_ESPRESSO, linespacing=1.55)

    # --- RIGHT PANEL: INSTANT (SOLUBLE) COFFEE ---
    draw_card(ax, 0.502, 0.125, 0.470, 0.585, facecolor=C_CARD, edgecolor=C_BLUE, lw=2.2)
    ax.add_patch(FancyBboxPatch((0.502, 0.630), 0.470, 0.080,
                                boxstyle="round,pad=0.004,rounding_size=0.015",
                                facecolor=C_BLUE, edgecolor=C_BLUE, lw=1.0, zorder=3))
    ax.text(0.737, 0.682, "INSTANT COFFEE (Soluble Powder)", ha="center", va="center",
            fontsize=13.0, fontweight="bold", color="#FFFFFF", zorder=4)
    ax.text(0.737, 0.648, "Factory brews it first, removes the water, and jars the crystals!", ha="center", va="center",
            fontsize=9.0, color="#D6EEF8", zorder=4)

    # 3-step factory flow inside Instant Coffee card
    draw_box(ax, 0.520, 0.495, 0.130, 0.105, "1. Factory\nBrewing", "Huge hot-water\nextraction tanks",
             facecolor=C_BLUE_BG, edgecolor=C_BLUE, title_color=C_BLUE, title_fs=9.2, sub_fs=7.8)
    draw_arrow(ax, 0.653, 0.548, 0.671, 0.548, color=C_BLUE, lw=2.2)

    draw_box(ax, 0.674, 0.495, 0.130, 0.105, "2. Concentrate\nLiquor", "Evaporate water\ninto thick coffee",
             facecolor=C_BLUE_BG, edgecolor=C_BLUE, title_color=C_BLUE, title_fs=9.2, sub_fs=7.8)
    draw_arrow(ax, 0.807, 0.548, 0.825, 0.548, color=C_BLUE, lw=2.2)

    draw_box(ax, 0.828, 0.495, 0.126, 0.105, "3. Dry into\nCrystals", "Spray Drying OR\nFreeze Drying",
             facecolor=C_GOLD_BG, edgecolor=C_GOLD, title_color=C_GOLD, title_fs=9.2, sub_fs=7.8)

    # Mini side-by-side comparison: Spray Dried vs Freeze Dried
    draw_box(ax, 0.520, 0.330, 0.208, 0.135,
             "Spray-Dried Instant",
             "Sprayed into hot air tower\n• Fast & affordable\n• Fine powdery granules\n(e.g., Nescafé Classic, Bru)",
             facecolor=C_RUST_BG, edgecolor=C_RUST, title_color=C_RUST, sub_color=C_ESPRESSO,
             title_fs=9.3, sub_fs=8.0, title_y=0.82, sub_y=0.38)

    draw_box(ax, 0.746, 0.330, 0.208, 0.135,
             "Freeze-Dried Instant",
             "Frozen cold & ice removed\n• Keeps much more aroma\n• Premium gold crystals\n(e.g., Nescafé Gold, Davidoff)",
             facecolor=C_BLUE_BG, edgecolor=C_BLUE, title_color=C_BLUE, sub_color=C_ESPRESSO,
             title_fs=9.3, sub_fs=8.0, title_y=0.82, sub_y=0.38)

    instant_bullets = (
        "•  Typical Beans:  Mostly Robusta (or Arabica-Robusta blends) for strong taste\n"
        "•  Does It Dissolve?  YES — 100% soluble in hot water/milk in 5 seconds!\n"
        "•  Trade-off:  Ultra-convenient & long shelf life, slightly less fresh aroma"
    )
    ax.text(0.522, 0.295, instant_bullets, ha="left", va="top", fontsize=8.9, color=C_ESPRESSO, linespacing=1.52)

    # Bottom Bridge to BrewDz Project
    ax.text(0.50, 0.058,
            "BRIDGE TO OUR PROJECT:   Whether making café Ground Coffee or Instant Coffee, precise grinding & particle sizing is the critical step we engineer next!",
            ha="center", va="center", fontsize=9.6, fontweight="bold", color="#FFFFFF",
            bbox=dict(boxstyle="round,pad=0.45", facecolor=C_ESPRESSO, edgecolor=C_CREMA, lw=1.4), zorder=5)

    for ext in ["png", "svg"]:
        fig.savefig(os.path.join(OUT_DIR, f"slide3_ground_vs_instant.{ext}"), dpi=300, facecolor=C_BG)
    plt.close(fig)
    print("Saved slide3_ground_vs_instant.png & .svg")


if __name__ == "__main__":
    generate_slide1()
    generate_slide2()
    generate_slide3()
    print(f"All 3 clean, math-free coffee making visuals generated in: {OUT_DIR}")
