"""

FOURIER OPERATIONS
==================

Included functions:
    - Range FFT
    - Doppler FFT
    - Azimuth FFT
    - Plot Range FFT
    - Fink peaks in range signal

"""

import numpy as np
import matplotlib.pyplot as plt

from params import PARAMS


def rangeFFT(signal):
    # Los primeros 5-8 frames ponerlos a 0, o quitar el DC que es la componente de freq=0 (media de valores de amplitud)
    range = np.fft.fft(signal)
    range = np.fft.fftshift(range)[signal.size//2:]

    # Remove first bin
    range[0] = 0

    bins = np.fft.fftfreq(signal.size)*PARAMS.R_MAX
    bins = np.fft.fftshift(bins)[signal.size//2:]

    return range, bins


def dopplerFFT(signal):
    doppler = np.fft.fft(signal)
    doppler = np.fft.fftshift(doppler)

    bins = np.fft.fftfreq(signal.size)*PARAMS.DOPPLER_MAX
    bins = np.fft.fftshift(bins)

    return doppler, bins


def azimuthFFT(signal):
    azimuth = np.fft.fft(signal)
    azimuth = np.fft.fftshift(azimuth)

    bins = np.fft.fftfreq(signal.size)*PARAMS.AZIM_MAX
    bins = np.fft.fftshift(bins)

    return azimuth, bins


def plotFFTrange(signal):
    range, bins = rangeFFT(signal)
    peaks = findPeaks(range, th=2.0e6)

    # Plot the magnitudes of the range bins
    fig, ax = plt.subplots()

    for peak in peaks:
        mag = np.abs([range[peak]])
        bin = bins[peak]
        ax.annotate(f'{bin:.2f}',
                    xy=(bin, mag),
                    xytext=(bin+0.2, mag),
                    fontsize=10)

    ax.plot(bins, np.abs(range), '-8', markevery=peaks)
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Reflected Power')
    ax.set_title('Interpreting a Single Chirp')
    plt.show()


def findPeaks(rang, th):
    # Find peaks bigger than th
    peaks = []

    for i in range(len(rang)):
        mag = np.abs(rang[i])
        if mag > th:
            peaks.append(i)

    return peaks
