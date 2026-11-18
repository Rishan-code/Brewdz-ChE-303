"""
BrewDz Particle Engineering Pvt. Ltd. — ChE 303 Competitor Study Slide Generator
Generates a crisp, executive 16:9 (300 DPI) Competitor Comparison Table slide (PNG + SVG)
featuring 5 direct coffee competitors across Indore (MP) and Pan-India.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "slide_visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# BrewDz Brand Palette
C_BG       = "#FAF6F0"
C_CARD     = "#FFFFFF"
C_ROW_ALT  = "#FBF8F3"
C_ESPRESSO = "#2C1810"
C_CREMA    = "#D4A373"
C_ROAST    = "#8A5A2B"
C_TAN      = "#F3E8DC"
C_GREEN    = "#1B6B3A"
C_GREEN_BG = "#E8F5EE"
C_RUST     = "#B84A1A"
C_RUST_BG  = "#FCECE6"
C_BLUE     = "#1D5B79"
C_BLUE_BG  = "#E6F2F8"
C_GOLD     = "#9A6B16"
C_GOLD_BG  = "#FDF6E3"
C_MUTED    = "#6B5B53"
C_BORDER   = "#DDD0C0"

plt.rcParams["font.family"] = "DejaVu Sans"


def generate_competitor_slide():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # --- TOP HEADER BANNER ---
    ax.add_patch(Rectangle((0, 0.892), 1, 0.108, facecolor=C_ESPRESSO, edgecolor="none", zorder=1))
    ax.add_patch(Rectangle((0, 0.884), 1, 0.008, facecolor=C_CREMA, edgecolor="none", zorder=2))

    ax.text(0.025, 0.956, "Competitor Study & BrewDz Market Differentiation",
            ha="left", va="center", fontsize=17.0, fontweight="bold", color="#FFFFFF", zorder=3)
    ax.text(0.025, 0.916, "Benchmarking 5 Direct Coffee Competitors Across Indore (MP) and Pan-India",
            ha="left", va="center", fontsize=10.5, color=C_CREMA, zorder=3)
    ax.text(0.975, 0.946, "BrewDz Particle Engineering · ChE 303",
            ha="right", va="center", fontsize=10.2, fontweight="bold", color="#E8D8C8", zorder=3)

    # --- TABLE GEOMETRY ---
    x0 = 0.022
    col_ws = [0.195, 0.125, 0.195, 0.218, 0.223]  # sums to 0.956
    col_xs = [x0]
    for w in col_ws[:-1]:
        col_xs.append(col_xs[-1] + w)
    table_w = sum(col_ws)

    table_top = 0.858
    table_bot = 0.156
    ax.add_patch(FancyBboxPatch((x0, table_bot), table_w, table_top - table_bot,
                                boxstyle="round,pad=0.002,rounding_size=0.012",
                                facecolor=C_CARD, edgecolor=C_BORDER, lw=1.6, zorder=1))

    # --- TABLE HEADER ROW ---
    hdr_h = 0.062
    hdr_y = table_top - hdr_h
    headers = [
        "Competitor & Location",
        "Market Focus",
        "Current Offering / Tech",
        "Key Limitation / Gap",
        "How BrewDz Differentiates"
    ]
    for i, (cx, cw, label) in enumerate(zip(col_xs, col_ws, headers)):
        fc = C_GREEN if i == 4 else C_ESPRESSO
        ax.add_patch(Rectangle((cx, hdr_y), cw, hdr_h, facecolor=fc, edgecolor="#4A3226", lw=0.7, zorder=3))
        ax.text(cx + cw / 2, hdr_y + hdr_h / 2, label, ha="center", va="center",
                fontsize=9.8, fontweight="bold", color="#FFFFFF", zorder=4)

    # --- 5 DIRECT COFFEE COMPETITORS ---
    rows = [
        {
            "name": "Kaapi Machines India",
            "loc": "Bengaluru · Pan-India",
            "url": "kaapimachines.com",
            "cat": "Commercial\nGrinders",
            "cat_fg": C_RUST, "cat_bg": C_RUST_BG,
            "offer": "Imported Mahlkönig & Ditting\ncommercial flat-burr coffee\ngrinders (single-pass batch)",
            "gap": "• Open-loop (no recycle loop)\n• High import cost (₹3L–₹15L)\n• Low continuous throughput",
            "diff": "Indigenous closed-loop roller\nmill + screen at ~40% lower\nCapEx (50–500 kg/h continuous)"
        },
        {
            "name": "Siolim Specialty Coffee",
            "loc": "Indore, Madhya Pradesh",
            "url": "siolim.coffee",
            "cat": "Local Indore\nRoastery",
            "cat_fg": C_GOLD, "cat_bg": C_GOLD_BG,
            "offer": "Indore specialty roastery &\npre-ground coffee pouches\n(standalone retail burrs)",
            "gap": "• 14–18% fines clog cold brew\n• Manual hand-sifting wastes\n  15–20% of pricey coffee",
            "diff": "Certified narrow-span grounds\nvia B2B toll-grinding or compact\nunit with zero sifting waste"
        },
        {
            "name": "Blue Tokai Roasters",
            "loc": "Gurugram · Pan-India",
            "url": "bluetokaicoffee.com",
            "cat": "National R&G\nCoffee Brand",
            "cat_fg": C_RUST, "cat_bg": C_RUST_BG,
            "offer": "India's largest specialty brand\nselling custom-ground retail\npouches (burr mill banks)",
            "gap": "• Open-loop grinding only\n• No inline classification; both\n  boulders & fines reach cups",
            "diff": "Automated multi-deck screen +\noversize recycle removes 100%\nboulders for uniform extraction"
        },
        {
            "name": "Subko Specialty Coffee",
            "loc": "Mumbai · Pan-India",
            "url": "subko.coffee",
            "cat": "Craft / Micro-Lot\nR&G Coffee",
            "cat_fg": C_GOLD, "cat_bg": C_GOLD_BG,
            "offer": "Premium Indian micro-lot &\nartisanal roast-and-ground\nspecialty coffee packs",
            "gap": "• Small-batch burr grinding\n• Frictional heat (40–50°C)\n  & batch-to-batch grind drift",
            "diff": "Chilled double-roll crushing\n(<28°C) locks in delicate aroma\nwith repeatable narrow PSD"
        },
        {
            "name": "Tata Coffee Limited",
            "loc": "Bengaluru · Pan-India",
            "url": "tatacoffee.com",
            "cat": "Industrial R&G\n& Instant",
            "cat_fg": C_BLUE, "cat_bg": C_BLUE_BG,
            "offer": "Large-scale roast & ground\nplus spray-dried & freeze-dried\ninstant coffee manufacturing",
            "gap": "• Built for massive ton-scale\n  commodity runs, not custom\n  narrow-span specialty batches",
            "diff": "Modular SME-scale circuit that\nco-produces calibrated Ground\n(PROD) & Instant feed (FINE)"
        },
    ]

    row_area = hdr_y - table_bot
    row_h = row_area / len(rows)

    for idx, r in enumerate(rows):
        ry = hdr_y - (idx + 1) * row_h
        base_fc = C_CARD if idx % 2 == 0 else C_ROW_ALT

        for c_i, (cx, cw) in enumerate(zip(col_xs, col_ws)):
            fc = "#F1FAF4" if c_i == 4 else base_fc
            ax.add_patch(Rectangle((cx, ry), cw, row_h, facecolor=fc, edgecolor=C_BORDER, lw=0.8, zorder=2))

        # Col 0: Company, Location, URL
        ax.text(col_xs[0] + 0.012, ry + row_h * 0.72, r["name"],
                ha="left", va="center", fontsize=9.6, fontweight="bold", color=C_ESPRESSO, zorder=3)
        ax.text(col_xs[0] + 0.012, ry + row_h * 0.45, r["loc"],
                ha="left", va="center", fontsize=8.3, color=C_MUTED, zorder=3)
        ax.text(col_xs[0] + 0.012, ry + row_h * 0.21, r["url"],
                ha="left", va="center", fontsize=7.8, color=C_BLUE, style="italic", zorder=3)

        # Col 1: Market Focus Badge
        bx = col_xs[1] + col_ws[1] / 2
        by = ry + row_h / 2
        ax.text(bx, by, r["cat"], ha="center", va="center",
                fontsize=8.3, fontweight="bold", color=r["cat_fg"], linespacing=1.25,
                bbox=dict(boxstyle="round,pad=0.35", facecolor=r["cat_bg"], edgecolor=r["cat_fg"], lw=1.0),
                zorder=3)

        # Col 2: Offering
        ax.text(col_xs[2] + 0.011, ry + row_h / 2, r["offer"],
                ha="left", va="center", fontsize=8.4, color=C_ESPRESSO, linespacing=1.35, zorder=3)

        # Col 3: Key Gap
        ax.text(col_xs[3] + 0.011, ry + row_h / 2, r["gap"],
                ha="left", va="center", fontsize=8.3, color="#5C2B1A", linespacing=1.35, zorder=3)

        # Col 4: BrewDz Differentiation
        ax.text(col_xs[4] + 0.011, ry + row_h / 2, r["diff"],
                ha="left", va="center", fontsize=8.4, fontweight="bold", color=C_GREEN, linespacing=1.35, zorder=3)

    # --- BOTTOM BREWDZ PROFITABILITY ADVANTAGE STRIP (4 PROFIT DRIVERS) ---
    ax.text(x0, 0.132, "WHY BREWDZ IS MORE PROFITABLE THAN COMPETITORS:",
            ha="left", va="center", fontsize=8.6, fontweight="bold", color=C_ESPRESSO, zorder=4)

    pillars = [
        ("+23.8% Revenue / Batch", "Recycle recovers +8 kg/h extra\nsalable coffee at zero bean cost", C_GREEN_BG, C_GREEN),
        ("100% Bean Monetization", "Zero waste: sell PROD (Ground)\n+ sell FINE (Instant feedstock)", C_GOLD_BG, C_GOLD),
        ("~40% Lower CapEx & Fast ROI", "₹5–7L local skid vs ₹10–15L\nimported · <3 month payback", C_TAN, C_ROAST),
        ("Ultra-Low OpEx & B2B Scale", "~1.1 kW power (<₹10/hr) · No\ncostly retail café rent overhead", C_BLUE_BG, C_BLUE),
    ]
    pw = 0.228
    gap = (table_w - 4 * pw) / 3
    for i, (pt, ps, pfc, pec) in enumerate(pillars):
        px = x0 + i * (pw + gap)
        ax.add_patch(FancyBboxPatch((px, 0.018), pw, 0.098,
                                    boxstyle="round,pad=0.003,rounding_size=0.010",
                                    facecolor=pfc, edgecolor=pec, lw=1.5, zorder=3))
        ax.text(px + pw / 2, 0.092, pt, ha="center", va="center",
                fontsize=9.1, fontweight="bold", color=pec, zorder=4)
        ax.text(px + pw / 2, 0.048, ps, ha="center", va="center",
                fontsize=7.8, color=C_ESPRESSO, linespacing=1.28, zorder=4)

    for ext in ["png", "svg"]:
        out_path = os.path.join(OUT_DIR, f"slide_competitor_study.{ext}")
        fig.savefig(out_path, dpi=300, facecolor=C_BG)
    plt.close(fig)
    print("Saved updated slide_competitor_study.png & .svg")


if __name__ == "__main__":
    generate_competitor_slide()
