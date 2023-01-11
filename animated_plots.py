"""

ANIMATED PLOTS
==============
Generate animated plots.

Included functions:
    - Range FFT plot through multiple frames

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dca1000 import DCA1000

from params import PARAMS
from fourier import rangeFFT, findPeaks

Y_MAX = 4e4


def animateFFTRange(frames, PEAK_TH=None):
    '''
    Range FFT preview for multiple frames
    '''
    # Figure
    fig = plt.figure()
    ax = plt.axes(xlim=(0, PARAMS.R_MAX/2), ylim=(0, Y_MAX))
    line = ax.plot([], [], 'b-8')[0]

    ax.grid()
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Reflected Power')

    ann_list = []

    def init():
        line.set_xdata(np.arange(PARAMS.ADC_SAMPLES))
        return line

    def animate(i):
        # Clear previous frame annotations
        for a in ann_list:
            a.remove()
        ann_list[:] = []

        adc_data = frames[i]
        adc_data = DCA1000.organize(
            adc_data, num_chirps=PARAMS.CHIRPS_PER_FRAME, num_rx=PARAMS.RX_ANTENNAS, num_samples=PARAMS.ADC_SAMPLES)
        adc_data = DCA1000.separate_tx(adc_data, num_tx=PARAMS.TX_ANTENNAS)
        range, bins = rangeFFT(adc_data[0, 0])

        if PEAK_TH is not None:
            peaks = findPeaks(range, th=PEAK_TH)

            for peak in peaks:
                mag = np.abs([range[peak]])
                bin = bins[peak]
                ann = ax.annotate(f'{bin:.2f}',
                                  xy=(bin, mag),
                                  xytext=(bin+0.2, mag),
                                  fontsize=10)
                ann_list.append(ann)
        else:
            peaks = []

        line.set_xdata(bins)
        line.set_ydata(np.abs(range))
        line.set_markevery(peaks)

        return line

    anim = FuncAnimation(fig, animate, np.arange(len(frames)), init_func=init,
                         interval=100, repeat=False)

    plt.show()
