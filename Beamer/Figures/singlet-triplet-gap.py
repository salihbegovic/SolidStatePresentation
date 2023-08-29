#!/usr/bin/env python3
# taritz: python3 %

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import config

config.source_matplotlib_options()

cols = dict(omega=0, uhf=1, ump2=2, eom=3)
data = np.loadtxt("../data/singlet_triplet_gap", skiprows=1)

Ω = data[:, cols["omega"]]

plt.plot(Ω, data[:, cols["uhf"]], label="UHF")
plt.plot(Ω, data[:, cols["ump2"]], linestyle="dashdot", label="UMP2")
plt.plot(Ω, data[:, cols["eom"]], linestyle="dashed", label="EOM-CCSD")
#plt.grid([0])
plt.xlabel("$\omega$ ($E_h/\hbar$)")
plt.ylabel("Singlet-triplet Gap (a.u.)")
plt.legend()
#plt.show()
plt.xlim(0, 1)
plt.hlines(0, min(Ω)-2, max(Ω)+2, linestyle="dotted", color="grey")
plt.savefig(__file__.replace("py", "pdf"))
