import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig = plt.figure()
ax = fig.add_subplot(111)
ax.text(5, 6, "Inputs", fontsize=15, verticalalignment="center")
ax.text(21, 6, "Outputs", fontsize=15, verticalalignment="center")
ax.text(
    17,
    1,
    "Good enough?",
    fontsize=15,
    verticalalignment="center",
    horizontalalignment="center",
)
ax.text(
    26 ,
    1,
    "Yes! Done.",
    fontsize=15,
    verticalalignment="center",
    horizontalalignment="center",
)
ax.text(
    5,
    1,
    "No! Try again!",
    fontsize=15,
    verticalalignment="center",
    horizontalalignment="center",
)
ax.text(
    15,
    6,
    "Black Box",
    color="white",
    fontsize=15,
    verticalalignment="center",
    horizontalalignment="center",
    bbox={"facecolor": "Black", "alpha": 1.0, "pad": 10},
)
style = "Simple,tail_width=0.5,head_width=4,head_length=8"
kw = dict(arrowstyle=style, color="k")
a1 = patches.FancyArrowPatch((9, 6), (11, 6), **kw)
a2 = patches.FancyArrowPatch((18, 6), (21, 6), **kw)
a3 = patches.FancyArrowPatch((22, 5.5), (20, 1.5), **kw)
a4 = patches.FancyArrowPatch((12, 1), (10, 1), **kw)
a5 = patches.FancyArrowPatch((5, 1.5), (7, 5.5), **kw)


for a in [a1, a2, a3, a4, a5]:
    ax.add_patch(a)

ax.axis([0, 30, 0, 7])
ax.axis("off")
plt.savefig("black_box.png")
