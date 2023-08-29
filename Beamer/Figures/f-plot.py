#!/usr/bin/env python3
# taritz: python3 %

import matplotlib.pyplot as plt
import numpy as np
import config
from scipy.special import erf

config.source_matplotlib_options()

def f(di, dx, t):
    return ( (1.0 / (2.0 * t**2.0))
           * ( np.exp(-dx**2.0 * (di - 1.0)**2.0 * t**2.0)
             - 2.0 * np.exp(-dx**2.0 * di**2.0 * t**2.0)
             + np.exp(-dx**2.0 * (di + 1.0)**2.0 * t**2.0)
             + dx * np.sqrt(np.pi) * t * ( -2.0 * di * erf(dx * di * t)
                                         + (di + 1.0) * erf(dx * (di + 1.0) * t)
                                         - (di -1.0) * erf(dx * (-di + 1.0) * t)
                                         )
             )
           )


T = np.linspace(0.001, 10, 200)
print(T)
print(f(0.0, 1.0, 1.0))

plt.plot(T, [f(1.0, 1.0, t)**2 for t in T],
        label="$F(1,t)^2$",
        linestyle="solid")
plt.plot(T, [f(0.0, 1.0, t) * f(1.0, 1.0, t) for t in T],
        label="$F(0, t)F(1,t)$",
        linestyle="dashed")
plt.plot(T, [f(0.0, 1.0, t)**2 for t in T],
        label="$F(0,t)^2$",
        linestyle="dashdot")
plt.xlabel("$t$ (arb. unit.)")
plt.xlim(0, 10)
plt.ylim(0, 1)
plt.legend()
#plt.show()
plt.savefig(__file__.replace("py", "pdf"))
