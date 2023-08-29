#!/usr/bin/env python3
# taritz: python3 %

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import config

config.source_matplotlib_options()

cols = dict(omega=0, nelec=1, nv=2, eom=3, fh=4, mp2=5, ccsd=6)

data = np.loadtxt("../data/AllDATA", skiprows=1)
def data_per_omega_n(omega, n):
    return np.array([d for d in data
                        if d[cols["omega"]] == omega and d[cols["nelec"]] == n])

reg_points = 2
omegas = np.sort(np.unique(data[:, cols["omega"]]))
nelecs = np.sort(np.unique(data[:, cols["nelec"]]))
n_rows = len(omegas)
n_cols = n_rows
print("omegas = ", omegas, "nelecs = ", nelecs)
colors = ["blue", "green"]

legend_where = 7
plot_ylabel = 4
plot_xlabel = 8

f, axes = plt.subplots(n_rows, n_cols, sharex=True)
f.subplots_adjust(hspace=0.08)
f.subplots_adjust(wspace=0.25)

yticks_translation = {
    # (omega, N)
    (1.0, 2): dict(points=[-0.130, -0.150],),
    (1.0, 6): dict(points=[-0.35, -0.5],),
    (1.0, 12): dict(points=[-0.65, -1.05],),
    ####
    (0.5, 2): dict(points=[-0.115, -0.135], decimals=3),
    (0.5, 6): dict(points=[-0.32, -0.45],),
    (0.5, 12): dict(points=[-0.6, -0.9],),
    ####
    (0.28, 2): dict(points=[-0.105, -0.12],),
    (0.28, 6): dict(points=[-0.3, -0.4],),
    (0.28, 12): dict(points=[-0.50, -0.8],),
}

text_position_translation = {
    # (omega, N)
    (1.0, 2): (0.55, 0.15),
    (1.0, 6): (0.55, 0.15),
    (1.0, 12): (0.55, 0.15),
    ####
    (0.5, 2): (0.55, 0.15),
    (0.5, 6): (0.55, 0.15),
    (0.5, 12): (0.55, 0.15),
    ####
    (0.28, 2): (0.55, 0.15),
    (0.28, 6): (0.55, 0.15),
    (0.28, 12): (0.55, 0.15),
}


for inelec, nelec in enumerate(nelecs):
    for iomega, omega in enumerate(reversed(omegas)):
        plot_index = inelec + n_rows * iomega + 1
        ax = plt.subplot(n_rows, n_cols, plot_index)
        _data = data_per_omega_n(omega, nelec)
        nv_rec = 1/_data[:, cols["nv"]]
        nv_rec_with_zero = np.array([0] + list(nv_rec))

        mp2 = _data[:, cols["mp2"]]
        slope, intersection, _, _, _ \
            = stats.linregress(nv_rec[-(reg_points+1):-1],
                               mp2[-(reg_points+1):-1])
        min_yrange = intersection
        print(nv_rec[-(reg_points+1):-1], mp2[-(reg_points+1):-1])
        plt.plot(nv_rec, mp2, "o",
                color=colors[0],
                label="MP2")
        plt.plot(nv_rec_with_zero, intersection + slope * nv_rec_with_zero,
                linestyle="dotted",
                color=colors[0])

        ccsd =  _data[:, cols["ccsd"]]
        slope, intersection, _, _, _ \
            = stats.linregress(nv_rec[-(reg_points+1):-1],
                               ccsd[-(reg_points+1):-1])
        min_yrange = min(intersection, min_yrange)
        plt.plot(nv_rec, ccsd, "^",
                color=colors[1],
                label="CCSD")
        plt.plot(nv_rec_with_zero, intersection + slope * nv_rec_with_zero,
                linestyle="dotted",
                color=colors[1])


        max_yrange = max(max(ccsd), max(mp2))
        ypadding = lambda p: (max_yrange - min_yrange) * p

        translation_key = (omega, nelec)
        if translation_key in yticks_translation:
            yticks = yticks_translation[translation_key]["points"]
            yticks_decimals = yticks_translation[translation_key].get("decimals", 2)
            plt.ylim(min_yrange, max_yrange + ypadding(0.05))
        else:
            yticks_decimals = 2
            yticks = [min_yrange + ypadding(0.2), max_yrange - ypadding(0.2)]
            plt.ylim(min_yrange, max_yrange + ypadding(0.05))

        ax.set_yticks(yticks)
        ax.set_yticklabels(
                [("{:." + str(yticks_decimals) + "f}").format(f) for f in yticks],
                verticalalignment="center",
                rotation=90)

        if iomega == n_rows - 1:
            xticks = [1/40, 0.05, 0.1]
            ax.set_xticks([0] + xticks)
            ax.set_xticklabels(
                [r"$0$"] +
                [r"${:d}^{{-1}}$".format(int(1/i)) for i in xticks],
                rotation=30)
        else:
            ax.set_xticks([])

        text_position = text_position_translation[translation_key]
        ax.text(x=text_position[0], y=text_position[1],
                s=("$N = {:.0f}$"
                   "\n"
                   "$\omega = {}$"
                  ).format(nelec, omega),
                fontsize=12,
                verticalalignment="center",
                #bbox=dict(facecolor="white", alpha=0.5),
                transform=ax.transAxes)

        if plot_index == legend_where:
            plt.legend(#loc="lower right",
                       loc=(-0.0,-0.65),
                       ncol=2,
                       labelspacing=0.1,
                       borderpad=0.2,
                       #handlelength=0.8,
                       handletextpad=0.2,
                       fontsize="small",
                       columnspacing=0.01)
        if plot_index == plot_xlabel:
            plt.xlabel(r"$N_\mathrm{v}^{-1}$")
        if plot_index == plot_ylabel:
            plt.ylabel(r"Energy (a.u.)")

plt.savefig(__file__.replace("py", "pdf"))
