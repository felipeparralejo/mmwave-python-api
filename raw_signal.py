"""

RAW SIGNAL UTILITIES
====================

Included functions:
    - Plot raw signal

"""

import matplotlib.pyplot as plt
import numpy as np


def plot_signal(signal):
    fig, axv = plt.subplots()

    sI = np.real(signal)
    sQ = np.imag(signal)

    axv.plot(sI, "b-")
    axv.plot(sQ, "r-")
    axv.grid()
    axv.legend(["real", "imag"])
    axv.set_xlabel("sample index")
    axv.set_ylabel("raw ADC output")

    plt.show()
