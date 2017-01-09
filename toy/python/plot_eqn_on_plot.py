#! /usr/bin/python
import pylab as pl
import numpy as np

x = np.random.randn(100)
y = 1 + 2 * x + 3 * x * x + np.random.randn(100) * 2

poly = pl.polyfit(x, y, 2)
print poly

def poly2latex(poly, variable="x", width=2):
    t = ["{0:0.{width}f}"]
    t.append(t[-1] + " {variable}")
    t.append(t[-1] + "^{1}")

    def f():
        for i, v in enumerate(reversed(poly)):
            idx = i if i < 2 else 2
            yield t[idx].format(v, i, variable=variable, width=width)

    return "${}$".format("+".join(f()))

print poly2latex(poly)
pl.plot(x, y, "o", alpha=0.4)
x2 = np.linspace(-2, 2, 100)
y2 = np.polyval(poly, x2)
pl.plot(x2, y2, lw=2, color="r")
pl.text(x2[5], y2[5], poly2latex(poly), fontsize=16)
pl.show()
