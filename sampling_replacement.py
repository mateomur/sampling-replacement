import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager

np.random.seed(42)

BLUE          = "#2a78d6"
GREEN         = "#1baf7a"
BG            = "#ffffff"
LIGHT         = "#f5f5f3"
DARK_TEXT     = "#0b0b0b"
MUTED         = "#898781"
COLOR_REMOVED = "#d3d1c7"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "text.color": DARK_TEXT,
})

names = ["Amir", "Brian", "Claire", "Damian"]

def draw_pool(ax, available, picked=None, prob=None):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_facecolor(BG)

    box = mpatches.FancyBboxPatch((0.3, 0.6), 9.4, 2.8,
                                   boxstyle="round,pad=0.2",
                                   linewidth=1, edgecolor="#d3d1c7",
                                   facecolor=LIGHT)
    ax.add_patch(box)

    xs = np.linspace(1.3, 8.7, len(names))

    for i, name in enumerate(names):
        if name in available:
            fc, tc, alpha = BLUE, "white", 1.0
        else:
            fc, tc, alpha = COLOR_REMOVED, MUTED, 0.4

        rect = mpatches.FancyBboxPatch((xs[i]-0.95, 1.1), 1.9, 1.2,
                                        boxstyle="round,pad=0.12",
                                        linewidth=0,
                                        facecolor=fc, alpha=alpha)
        ax.add_patch(rect)
        ax.text(xs[i], 1.72, name, ha="center", va="center",
                fontsize=12, fontweight="bold", color=tc)

    if picked:
        px = xs[names.index(picked)]
        rect2 = mpatches.FancyBboxPatch((px-0.95, 3.55), 1.9, 1.1,
                                         boxstyle="round,pad=0.12",
                                         linewidth=2.5,
                                         edgecolor=GREEN, facecolor=BG)
        ax.add_patch(rect2)
        ax.text(px, 4.1, picked, ha="center", va="center",
                fontsize=12, fontweight="bold", color=GREEN)
        ax.annotate("", xy=(px, 3.52), xytext=(px, 2.33),
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))

    if prob:
        ax.text(5.0, 0.22, prob, ha="center", va="center",
                fontsize=10, color=MUTED, style="italic")


def make_image(configs, pick_labels, header_title, header_sub, code_label, footer_text, filename):
    n = len(configs)
    # extra top space for header
    fig = plt.figure(figsize=(9, 4.5 * n + 2.2))
    fig.patch.set_facecolor(BG)

    # header block
    fig.text(0.06, 0.985, code_label,
             fontsize=16, fontweight="bold", color=DARK_TEXT,
             va="top", fontfamily="monospace")
    fig.text(0.06, 0.955, header_sub,
             fontsize=11, color=MUTED, va="top")

    # divider line
    fig.add_artist(plt.Line2D([0.06, 0.94], [0.935, 0.935],
                               transform=fig.transFigure,
                               color="#d3d1c7", linewidth=1))

    # axes below the header
    top_start = 0.90
    panel_h = (top_start - 0.04) / n

    for i, (cfg, label) in enumerate(zip(configs, pick_labels)):
        top = top_start - i * panel_h
        bottom = top - panel_h + 0.03
        ax = fig.add_axes([0.06, bottom, 0.90, panel_h - 0.04])
        draw_pool(ax, **cfg)

        # pick label as text above each panel, clean and separated
        fig.text(0.06, top - 0.005, label,
                 fontsize=12, fontweight="bold", color=DARK_TEXT,
                 va="top")

    fig.text(0.5, 0.008, footer_text,
             ha="center", fontsize=9, color=MUTED)

    fig.savefig(f"/mnt/user-data/outputs/{filename}",
                dpi=180, bbox_inches="tight", facecolor=BG)
    print(f"Saved {filename}")
    plt.close(fig)


# ── IMAGE 1: WITHOUT replacement ─────────────────────────────────────────────
make_image(
    configs=[
        dict(available=["Amir","Brian","Claire","Damian"],
             picked="Brian",
             prob="P(Brian) = 1/4 = 25%"),
        dict(available=["Amir","Claire","Damian"],
             picked="Claire",
             prob="P(Claire | Brian gone) = 1/3 = 33%"),
        dict(available=["Amir","Damian"],
             picked="Amir",
             prob="P(Amir | Brian & Claire gone) = 1/2 = 50%"),
    ],
    pick_labels=["Pick 1 — full pool",
                 "Pick 2 — Brian removed from pool",
                 "Pick 3 — pool keeps shrinking"],
    header_title="Without replacement",
    header_sub="Each pick removes the item  →  probabilities change  →  dependent events",
    code_label="replace=False",
    footer_text="df.sample(n, replace=False)  |  simulation by @mateomur",
    filename="sampling_without_replacement.png"
)

# ── IMAGE 2: WITH replacement ─────────────────────────────────────────────────
make_image(
    configs=[
        dict(available=["Amir","Brian","Claire","Damian"],
             picked="Brian",
             prob="P(Brian) = 1/4 = 25%"),
        dict(available=["Amir","Brian","Claire","Damian"],
             picked="Brian",
             prob="P(Brian) = 1/4 = 25%  ← same!"),
        dict(available=["Amir","Brian","Claire","Damian"],
             picked="Claire",
             prob="P(Claire) = 1/4 = 25%  ← always the same"),
    ],
    pick_labels=["Pick 1 — full pool",
                 "Pick 2 — pool resets, Brian is back",
                 "Pick 3 — pool always full"],
    header_title="With replacement",
    header_sub="Pool resets after every pick  →  probabilities stay the same  →  independent events",
    code_label="replace=True",
    footer_text="df.sample(n, replace=True)  |  simulation by @mateomur",
    filename="sampling_with_replacement.png"
)
