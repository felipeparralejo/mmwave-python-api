"""

LIVE PLOTS
==========
Generate live plots.

Included functions:
    - Live Range
    - Live Range Heatmap
    - Live Azimuth-Range Heatmap

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dca1000 import DCA1000

from params import PARAMS
from fourier import rangeFFT, findPeaks
from heatmaps import generateRangeHeatmap, generateAzimuthRangeHeatmap

Y_MAX = 4e4
Y_PEAK_TH = 1e4
V_MAX = 1e4


def liveRangePreview(dca):
    '''
    Live range FFT preview for first chirp and Tx-RX pair
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

        dca._clear_buffer()
        adc_data = dca.read()
        adc_data = DCA1000.organize(
            adc_data, num_chirps=PARAMS.CHIRPS_PER_FRAME, num_rx=PARAMS.RX_ANTENNAS, num_samples=PARAMS.ADC_SAMPLES)
        adc_data = DCA1000.separate_tx(adc_data, num_tx=PARAMS.TX_ANTENNAS)
        range, bins = rangeFFT(adc_data[0, 0])

        peaks = findPeaks(range, th=Y_PEAK_TH)

        line.set_xdata(bins)
        line.set_ydata(np.abs(range))
        line.set_markevery(peaks)

        for peak in peaks:
            mag = np.abs([range[peak]])
            bin = bins[peak]
            ann = ax.annotate(f'{bin:.2f}',
                              xy=(bin, mag),
                              xytext=(bin+0.2, mag),
                              fontsize=10)
            ann_list.append(ann)

        return line

    anim = FuncAnimation(fig, animate, init_func=init,
                         interval=100)

    plt.show()


def liveRangeHeatmapPreview(dca):
    # Create fake radar input data to get range bins
    avg = np.zeros((PARAMS.CHIRP_LOOPS, PARAMS.RX_ANTENNAS*PARAMS.TX_ANTENNAS,
                   PARAMS.ADC_SAMPLES), dtype=complex)

    bins, chirps, matrix = generateRangeHeatmap(avg)

    # Figure
    fig, ax = plt.subplots()
    cax = ax.pcolormesh(bins, chirps,
                        np.abs(matrix), vmin=0, vmax=V_MAX)
    fig.colorbar(cax, ax=ax)

    ax.grid()
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Chirp #')

    def animate(i):
        dca._clear_buffer()
        adc_data = dca.read()
        adc_data = DCA1000.organize(
            adc_data, num_chirps=PARAMS.CHIRPS_PER_FRAME, num_rx=PARAMS.RX_ANTENNAS, num_samples=PARAMS.ADC_SAMPLES)
        adc_data = DCA1000.separate_tx(adc_data, num_tx=PARAMS.TX_ANTENNAS)
        _, _, matrix = generateRangeHeatmap(adc_data)

        cax.set_array(np.abs(matrix))

    anim = FuncAnimation(fig, animate, interval=100)

    plt.show()


def liveAzimuthRangePreview(dca):
    # Create fake radar input data to get range and azimuth bins
    avg = np.zeros((PARAMS.CHIRP_LOOPS, PARAMS.RX_ANTENNAS*PARAMS.TX_ANTENNAS,
                   PARAMS.ADC_SAMPLES), dtype=complex)

    range_bins, azimuth_bins, matrix = generateAzimuthRangeHeatmap(avg)

    # Figure
    fig, ax = plt.subplots()
    cax = ax.pcolormesh(range_bins, azimuth_bins,
                        np.abs(matrix), vmin=0, vmax=V_MAX)
    fig.colorbar(cax, ax=ax)

    ax.grid()
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Azimuth (°)')

    def animate(i):
        dca._clear_buffer()
        adc_data = dca.read()
        adc_data = DCA1000.organize(
            adc_data, num_chirps=PARAMS.CHIRPS_PER_FRAME, num_rx=PARAMS.RX_ANTENNAS, num_samples=PARAMS.ADC_SAMPLES)
        adc_data = DCA1000.separate_tx(adc_data, num_tx=PARAMS.TX_ANTENNAS)
        _, _, matrix = generateAzimuthRangeHeatmap(adc_data)

        cax.set_array(np.abs(matrix))

    anim = FuncAnimation(fig, animate, interval=100)

    plt.show()
