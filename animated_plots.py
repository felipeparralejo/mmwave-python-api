"""

ANIMATED PLOTS
==============
Generate animated plots through multiple frames of radar data.

Included functions:
    - Range FFT 
    - Range Heatmap
    - Doppler-Range Heatmap
    - Azimuth-Range Heatmap

"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from dca1000 import DCA1000
from fourier import findPeaks, rangeFFT
from heatmaps import generateRangeHeatmap, generateDopplerRangeHeatmap, generateAzimuthRangeHeatmap
from params import PARAMS

Y_MAX = 120
V_MAX = 100


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
    ax.set_ylabel('Relative Power (dB)')

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
        range, bins = rangeFFT(adc_data[0, 0], remove_beg=False)

        if PEAK_TH is not None:
            peaks = findPeaks(range, th=PEAK_TH)

            for peak in peaks:
                mag = range[peak]
                bin = bins[peak]
                ann = ax.annotate(f'{bin:.2f}',
                                  xy=(bin, mag),
                                  xytext=(bin+0.2, mag),
                                  fontsize=10)
                ann_list.append(ann)
        else:
            peaks = []

        line.set_xdata(bins)
        line.set_ydata(range)
        line.set_markevery(peaks)

        return line

    anim = FuncAnimation(fig, animate, np.arange(len(frames)), init_func=init,
                         interval=100, repeat=False)

    plt.show()


def animateRangeHeatmap(frames):
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
        adc_data = frames[i]
        adc_data = DCA1000.organize(
            adc_data, num_chirps=PARAMS.CHIRPS_PER_FRAME, num_rx=PARAMS.RX_ANTENNAS, num_samples=PARAMS.ADC_SAMPLES)
        adc_data = DCA1000.separate_tx(adc_data, num_tx=PARAMS.TX_ANTENNAS)
        _, _, matrix = generateRangeHeatmap(adc_data)

        cax.set_array(np.abs(matrix))

    anim = FuncAnimation(fig, animate, np.arange(len(frames)),
                         interval=100, repeat=False)

    plt.show()


def animateDopplerRangeHeatmap(frames):
    # Create fake radar input data to get range bins
    avg = np.zeros((PARAMS.CHIRP_LOOPS, PARAMS.RX_ANTENNAS*PARAMS.TX_ANTENNAS,
                   PARAMS.ADC_SAMPLES), dtype=complex)

    range_bins, doppler_bins, matrix = generateDopplerRangeHeatmap(avg)

    # Figure
    fig, ax = plt.subplots()
    cax = ax.pcolormesh(range_bins, doppler_bins,
                        np.abs(matrix), vmin=0, vmax=V_MAX)
    fig.colorbar(cax, ax=ax)

    ax.grid()
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Doppler (m/s)')

    def animate(i):
        adc_data = frames[i]
        adc_data = DCA1000.organize(
            adc_data, num_chirps=PARAMS.CHIRPS_PER_FRAME, num_rx=PARAMS.RX_ANTENNAS, num_samples=PARAMS.ADC_SAMPLES)
        adc_data = DCA1000.separate_tx(adc_data, num_tx=PARAMS.TX_ANTENNAS)
        _, _, matrix = generateDopplerRangeHeatmap(adc_data)

        cax.set_array(np.abs(matrix))

    anim = FuncAnimation(fig, animate, np.arange(len(frames)),
                         interval=100, repeat=False)

    plt.show()


def animateAzimuthRangeHeatmap(frames):
    # Create fake radar input data to get range bins
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
        adc_data = frames[i]
        adc_data = DCA1000.organize(
            adc_data, num_chirps=PARAMS.CHIRPS_PER_FRAME, num_rx=PARAMS.RX_ANTENNAS, num_samples=PARAMS.ADC_SAMPLES)
        adc_data = DCA1000.separate_tx(adc_data, num_tx=PARAMS.TX_ANTENNAS)
        _, _, matrix = generateAzimuthRangeHeatmap(adc_data)

        cax.set_array(np.abs(matrix))

    anim = FuncAnimation(fig, animate, np.arange(len(frames)),
                         interval=100, repeat=False)

    plt.show()
