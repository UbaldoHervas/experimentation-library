"""Reproduce the README banner and sample-size figure."""
from pathlib import Path
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from matplotlib.ticker import FuncFormatter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experimentpy import sample_size_proportions

OUT = ROOT / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)
NAVY, BLUE, TEAL, MUTED, PALE = "#172b58", "#3159bd", "#078d90", "#66758d", "#f3f6fc"


def rounded(ax, xy, width, height, color, radius=20):
    ax.add_patch(FancyBboxPatch(xy, width, height,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=color, edgecolor="none"))


def banner():
    fig, ax = plt.subplots(figsize=(18, 6.5), dpi=100)
    fig.patch.set_facecolor(PALE)
    ax.set_xlim(0, 1800)
    ax.set_ylim(650, 0)
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    ax.text(95, 88, "STATISTICAL EXPERIMENTATION", color=MUTED,
            fontsize=13, fontweight="semibold", va="center")
    ax.text(86, 215, "ExperimentPy", color=NAVY,
            fontsize=68, fontweight="bold", va="center")
    ax.text(95, 320, "Design experiments.\nValidate allocation.",
            color=NAVY, fontsize=28, linespacing=1.4, va="center")
    for x, w, label, color in [(95, 208, "Sample size", BLUE),
        (320, 208, "SRM checks", TEAL), (545, 188, "Open source", MUTED)]:
        rounded(ax, (x, 443), w, 54, "white", radius=15)
        ax.text(x+w/2, 470, label, ha="center", va="center", color=color,
                fontsize=15, fontweight="semibold")
    ax.text(95, 579, "Python 3.10+  /  MIT License", color=MUTED, fontsize=14)
    rounded(ax, (913, 73), 790, 485, "#e6ebf7", radius=32)
    rounded(ax, (905, 65), 790, 485, "white", radius=32)
    ax.text(955, 114, "RANDOM ASSIGNMENT", color=MUTED,
            fontsize=12, fontweight="semibold")
    ax.add_patch(Circle((1040, 305), 45, facecolor=NAVY, edgecolor="none"))
    ax.text(1040, 305, "A/B", ha="center", va="center", color="white",
            fontsize=20, fontweight="bold")
    for y, color, label in [(190, BLUE, "CONTROL"), (390, TEAL, "VARIANT")]:
        ax.add_patch(FancyArrowPatch((1091, 305), (1235, y+10),
            arrowstyle="-|>", mutation_scale=18, color="#a5b3ce", linewidth=2.5))
        rounded(ax, (1240, y-60), 393, 138, "#f7f9fd", radius=20)
        ax.text(1270, y-22, label, color=color, fontsize=12,
                fontweight="bold", va="center")
        ax.text(1598, y-22, "50%", color=NAVY, fontsize=17,
                ha="right", va="center", fontweight="bold")
        for row in range(3):
            for col in range(8):
                ax.add_patch(Circle((1278+col*42, y+7+row*21), 5.5,
                    facecolor=color, edgecolor="none", alpha=0.85))
    ax.text(1300, 512, "Illustrative 50/50 split", color=MUTED,
            fontsize=11, ha="center")
    fig.savefig(OUT / "experimentpy-banner.png", facecolor=PALE, dpi=100)
    fig.savefig(OUT / "experimentpy-banner.svg", facecolor=PALE)
    plt.close(fig)


def sample_size_curve():
    mde_pp = np.linspace(0.2, 1.0, 100)
    counts = [sample_size_proportions(0.05, float(mde)/100).n_control
              for mde in mde_pp]
    selected = sample_size_proportions(0.05, 0.005)
    fig, ax = plt.subplots(figsize=(11, 5.4), dpi=160)
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(left=0.11, right=0.96, top=0.76, bottom=0.23)
    fig.text(0.11, 0.92, "Smaller effects need larger experiments",
             fontsize=20, color=NAVY, fontweight="bold")
    fig.text(0.11, 0.85, "5% baseline  |  80% power  |  5% alpha  |  Equal allocation",
             fontsize=11, color=MUTED)
    ax.plot(mde_pp, counts, color=BLUE, linewidth=3)
    ax.fill_between(mde_pp, counts, color=BLUE, alpha=0.045)
    ax.scatter([0.5], [selected.n_control], color=TEAL, s=75, zorder=5)
    ax.axvline(0.5, color=TEAL, linestyle=(0, (3, 4)), linewidth=1, alpha=0.5)
    ax.annotate(f"{selected.n_control:,} per arm\n5% → 5.5% conversion",
        xy=(0.5, selected.n_control), xytext=(0.60, 92000),
        fontsize=12, color=NAVY, linespacing=1.5,
        bbox=dict(boxstyle="round,pad=0.8", facecolor=PALE, edgecolor="none"),
        arrowprops=dict(arrowstyle="-", color=TEAL, linewidth=1.5))
    ax.set_xlim(0.2, 1.0)
    ax.set_ylim(0, max(counts)*1.07)
    ax.set_xlabel("Minimum detectable effect (percentage points)",
                  fontsize=11, labelpad=13, color=NAVY)
    ax.set_ylabel("Experimental units per arm", fontsize=11,
                  labelpad=12, color=NAVY)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
    ax.grid(axis="y", color="#e6ebf4", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis="both", labelsize=10, colors=MUTED, length=0, pad=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.text(0.11, 0.055,
        "Calculated with ExperimentPy. Two-sided fixed-horizon normal approximation; independent binary outcomes.",
        fontsize=8.5, color=MUTED)
    fig.savefig(OUT / "sample-size-curve.png", facecolor="white", dpi=160)
    fig.savefig(OUT / "sample-size-curve.svg", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    banner()
    sample_size_curve()
    print(OUT)
