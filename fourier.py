"""

FOURIER OPERATIONS
==================

Included functions:
    - Range FFT
    - Doppler FFT
    - Angle FFT

"""

import numpy as np
from params import PARAMS


def rangeFFT(signal, device):
    '''
    Signal must come in the way "rdata.separated_data"
    Device is the radar name

    '''

    # 1D-range FFT
    rFFT = np.fft.fft(signal, axis=1)
    # Removing near-field effect
    rFFT[:, 0:8] = 0
    # rFFT = 10*np.log10(rFFT)
    # Range bins
    nBins = np.size(signal, 1)

    # Radar Cube for different devices
    if device == 'IWR6843ISK-ODS':
        radarCube = np.zeros((4, 4, nBins), dtype=complex)
        for n in range(nBins):
            radarCube[:, :, n] = [[rFFT[0, n], rFFT[3, n], rFFT[4, n], rFFT[7, n]],
                                  [rFFT[1, n], rFFT[2, n], rFFT[5, n], rFFT[6, n]],
                                  [0.+0.j,         0.+0.j,
                                      rFFT[8, n], rFFT[11, n]],
                                  [0.+0.j,         0.+0.j,         rFFT[9, n], rFFT[10, n]]]
    elif device == 'IWR1843':
        radarCube = np.zeros((2, 8, nBins), dtype=complex)
        for n in range(nBins):
            radarCube[:, :, n] = [[0,         0,         rFFT[4, n], rFFT[5, n], rFFT[6, n], rFFT[7, n], 0,         0],
                                  [rFFT[0, n], rFFT[1, n], rFFT[2, n], rFFT[3, n], rFFT[8, n], rFFT[9, n], rFFT[10, n], rFFT[11, n]]]

    rBins = np.linspace(0, PARAMS.R_MAX, PARAMS.NUM_RANGE_BINS)

    return radarCube, rFFT, rBins


def angleFFT(signal):
    '''
    Signal is "rFFT" coming from "rangeFFT"

    '''
    # Azimuth and elevation bins
    azBins = PARAMS.NUM_AZIM_BINS
    elBins = PARAMS.NUM_ELEV_BINS

    # Angle FFTs
    angFFT = np.fft.fft2(signal, (elBins, azBins), axes=(0, 1))
    angFFT = np.fft.fftshift(angFFT, axes=0)
    angFFT = np.fft.fftshift(angFFT, axes=1)
    # For azimuth and elevation, the average is taken. It can also be replaced
    # with "max" or any other convenient function
    aFFT = np.mean(abs(angFFT), axis=0)
    eFFT = np.mean(abs(angFFT), axis=1)

    # Finally, the bins are extracted from the configuration
    # Azimuth bins
    aBins = np.linspace(-azBins/2, azBins/2-1, azBins) * 2/azBins
    aBins = np.arcsin(aBins)*180/np.pi
    # Elevation bins
    eBins = np.linspace(-elBins/2, elBins/2-1, elBins) * 2/elBins
    eBins = np.arcsin(eBins)*180/np.pi

    return aFFT, eFFT, aBins, eBins


def dopplerFFT(signal):

    # Virtual antenna to do the calculations:
    # 2D-range/Doppler FFT
    vB = np.shape(signal)[0]*4
    rB = np.shape(signal)[2]*4
    nAnt = np.shape(signal)[1]
    dFFT = np.zeros(
        (vB, nAnt, rB), dtype=complex)
    for n in range(np.shape(dFFT)[1]):
        dFFT[:, n, :] = np.fft.fft2(signal[:, n, :], (vB, rB), axes=(0, 1))

    dFFT = np.mean(abs(dFFT), axis=1)

    dFFT = np.fft.fftshift(dFFT, axes=0)
    # Removing near-field effect
    dFFT[:, 0:8*4] = 0
    # dFFT = 10*np.log10(dFFT)

    # Bins for range and velocity
    rBins = np.linspace(0, PARAMS.R_MAX, num=np.shape(dFFT)[1])
    dBins = np.linspace(-PARAMS.DOPPLER_MAX,
                        PARAMS.DOPPLER_MAX, num=np.shape(dFFT)[0])

    return dFFT, dBins, rBins


def matlabMultip(f, t):
    """
    create an n x m array from 2 vectors of size n and m.
    Resulting rows are the multiplication of each element of the first vector for 
    all the elements of the second vector
    f=np.array([2,4])
    t=np.array([1,2,3,4,5])
    [[ 2  4  6  8 10]
     [ 4  8 12 16 20]]

    """
    if t.size == t.shape[0]:
        k = f[0]*t
        for i in f[1:]:
            j = i*t
            k = np.vstack((k, j))
    else:
        raise Exception('arrays should 1D arrays')

    return k


# def plotFFTrange(signal, PEAK_TH=None):

#     rProf, rbins = rangeProfile(signal)

#     # Plot the magnitudes of the range bins
#     fig, ax = plt.subplots()

#     if PEAK_TH is not None:
#         peaks = findPeaks(rProf, th=PEAK_TH)

#         for peak in peaks:
#             mag = np.abs([rProf[peak]])
#             bin = rbins[peak]
#             ax.annotate(f'{bin:.2f}',
#                         xy=(bin, mag),
#                         xytext=(bin+0.2, mag),
#                         fontsize=10)
#     else:
#         peaks = []

#     ax.plot(rbins, np.abs(rProf), '-8', markevery=peaks)
#     ax.set_xlabel('Range (m)')
#     ax.set_ylabel('Reflected Power')
#     ax.set_title('Interpreting a Single Chirp')
#     plt.show()


# def plotFFTdoppler(signal):
#     doppler, bins = dopplerFFT(signal)

#     fig, ax = plt.subplots()

#     ax.plot(bins, np.abs(doppler))
#     ax.set_xlabel('Doppler (m/s)')
#     ax.set_ylabel('Reflected Power')
#     ax.set_title('Interpreting a Single Sample')
#     plt.show()


# def plotFFTazimuth(signal):
#     azimuth, bins = azimuthFFT(signal)

#     fig, ax = plt.subplots()

#     ax.plot(bins, np.abs(azimuth))
#     ax.set_xlabel('Azimuth (°)')
#     ax.set_ylabel('Reflected Power')
#     ax.set_title('Interpreting a Chirps Avg.')
#     plt.show()


# def plotFFTelevation(signal):
#     elevation, bins = elevationFFT(signal)

#     fig, ax = plt.subplots()

#     ax.plot(bins, np.abs(elevation))
#     ax.set_xlabel('Elevation (°)')
#     ax.set_ylabel('Reflected Power')
#     ax.set_title('Interpreting a Chirps Avg.')
#     plt.show()


# def findPeaks(rang, th):
#     # Find peaks bigger than th
#     peaks = []

#     for i in range(len(rang)):
#         mag = rang[i]
#         if mag > th:
#             peaks.append(i)

#     return peaks
