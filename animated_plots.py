"""

ANIMATED PLOTS
==============
Generate animated plots through multiple frames of radar data.

Included functions:
    - Range FFT 
    - Range Profile GIF
    - Azimuth-Range Heatmap GIF
    - Elevation-Range Heatmap GIF
    - Doppler-Range Heatmap GIF

"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import os
import imageio

from dca1000 import DCA1000
from fourier import rangeFFT, dopplerFFT, angleFFT
# from heatmaps import generateRangeHeatmap, generateDopplerRangeHeatmap, generateAzimuthRangeHeatmap
from params import PARAMS

Y_MAX = 1e5
V_MAX = 100


def animateFFTRange(frames, rdata):
    '''
    Range FFT preview for multiple frames
    '''
    # Figure
    fig = plt.figure()
    ax = plt.axes(xlim=(0.5, PARAMS.R_MAX//2), ylim=(0, Y_MAX))
    line = ax.plot([], [], 'b-')[0]

    ax.grid()
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Signal Strength')

    def init():
        line.set_xdata(np.arange(PARAMS.ADC_SAMPLES))
        return line

    def animate(i):
        adc_data = frames[i]
        # Set RadarData raw_data
        rdata.raw_data = adc_data
        # Access data separated by Rx and Tx antennas
        v_array = rdata.separated_vx_data

        # 1D RANGE FFT and radar cube
        [RC, rFFT, rBins] = rangeFFT(v_array[1, :, :], rdata.device)

        line.set_xdata(rBins[8:])
        line.set_ydata(np.mean(abs(rFFT), axis=0)[8:])

        return line

    anim = FuncAnimation(fig, animate, np.arange(len(frames)), init_func=init,
                         interval=100, repeat=False)

    plt.show()


def createRangeProfileGIF(frames, rdata):
    filenames = []
    i = 0

    # create folder to store files
    if 'tmp_imgs' not in os.listdir('.'):
        os.mkdir('tmp_imgs')

    print('Creating plots...')
    for adc_data in frames:
        # Set RadarData raw_data
        rdata.raw_data = adc_data
        # Access data separated by Rx and Tx antennas
        v_array = rdata.separated_vx_data

        [RC, rFFT, rBins] = rangeFFT(v_array[1, :, :], rdata.device)

        fig, ax = plt.subplots()

        ax.plot(rBins[8:80], np.mean(abs(rFFT), axis=0)[8:80])
        ax.set_title('Range Profile')
        ax.set_xlabel('Range (m)')
        ax.set_ylabel('Signal Strength')
        ax.set_ylim(ymin=0, ymax=2e5)

        # create file name and append it to a list
        i += 1
        filename = f'tmp_imgs/{i}.png'
        filenames.append(filename)

        # save frame
        plt.savefig(filename, dpi=200)
        plt.close()

    # build gif
    print('Building GIF...')
    with imageio.get_writer('range_profile.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            writer.append_data(image)

    # Remove files
    print('Removing files...')
    for filename in filenames:
        os.remove(filename)

    # Remove dir
    os.rmdir('tmp_imgs')

    print('Done!')


def createAzimuthRangeHeatmapGIF(frames, rdata):
    filenames = []
    i = 0

    # create folder to store files
    if 'tmp_imgs' not in os.listdir('.'):
        os.mkdir('tmp_imgs')

    print('Creating plots...')
    for adc_data in frames:
        # Set RadarData raw_data
        rdata.raw_data = adc_data
        # Access data separated by Rx and Tx antennas
        v_array = rdata.separated_vx_data

        [RC, rFFT, rBins] = rangeFFT(v_array[1, :, :], rdata.device)
        [aFFT, _, aBins, _] = angleFFT(RC)

        range_bins = rBins[:60]
        azimuth_bins = aBins[1:]
        matrix = aFFT[1:, :60]

        fig, ax = plt.subplots()

        c = ax.pcolormesh(range_bins, azimuth_bins, matrix, vmax=7e5)
        fig.colorbar(c, ax=ax)
        ax.set_title('Azimuth-Range Heatmap')
        ax.set_xlabel('Range (m)')
        ax.set_ylabel('Azimuth (°)')

        # create file name and append it to a list
        i += 1
        filename = f'tmp_imgs/{i}.png'
        filenames.append(filename)

        # save frame
        plt.savefig(filename, dpi=200)
        plt.close()

    # build gif
    print('Building GIF...')
    with imageio.get_writer('azimuth_range_heatmap.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            writer.append_data(image)

    # Remove files
    print('Removing files...')
    for filename in filenames:
        os.remove(filename)

    # Remove dir
    os.rmdir('tmp_imgs')

    print('Done!')


def createElevationRangeHeatmapGIF(frames, rdata):
    filenames = []
    i = 0

    # create folder to store files
    if 'tmp_imgs' not in os.listdir('.'):
        os.mkdir('tmp_imgs')

    print('Creating plots...')
    for adc_data in frames:
        # Set RadarData raw_data
        rdata.raw_data = adc_data
        # Access data separated by Rx and Tx antennas
        v_array = rdata.separated_vx_data

        [RC, rFFT, rBins] = rangeFFT(v_array[1, :, :], rdata.device)
        [_, eFFT, _, eBins] = angleFFT(RC)

        range_bins = rBins[:60]
        elevation_bins = eBins[1:]
        matrix = eFFT[1:, :60]

        fig, ax = plt.subplots()

        c = ax.pcolormesh(range_bins, elevation_bins, matrix, vmax=7e5)
        fig.colorbar(c, ax=ax)
        ax.set_title('Elevation-Range Heatmap')
        ax.set_xlabel('Range (m)')
        ax.set_ylabel('Elevation (°)')

        # create file name and append it to a list
        i += 1
        filename = f'tmp_imgs/{i}.png'
        filenames.append(filename)

        # save frame
        plt.savefig(filename, dpi=200)
        plt.close()

    # build gif
    print('Building GIF...')
    with imageio.get_writer('elevation_range_heatmap.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            writer.append_data(image)

    # Remove files
    print('Removing files...')
    for filename in filenames:
        os.remove(filename)

    # Remove dir
    os.rmdir('tmp_imgs')

    print('Done!')


def createDopplerRangeHeatmapGIF(frames, rdata):
    filenames = []
    i = 0

    # create folder to store files
    if 'tmp_imgs' not in os.listdir('.'):
        os.mkdir('tmp_imgs')

    print('Creating plots...')
    for adc_data in frames:
        # Set RadarData raw_data
        rdata.raw_data = adc_data
        # Access data separated by Rx and Tx antennas
        v_array = rdata.separated_vx_data

        [dFFT, dBins, rBins] = dopplerFFT(v_array)

        range_bins = rBins[:60]
        doppler_bins = dBins
        matrix = abs(dFFT[:, :60])

        fig, ax = plt.subplots()

        c = ax.pcolormesh(range_bins, doppler_bins, matrix, vmax=1e7)
        fig.colorbar(c, ax=ax)
        ax.set_title('Doppler-Range Heatmap')
        ax.set_xlabel('Range (m)')
        ax.set_ylabel('Doppler (m/s)')

        # create file name and append it to a list
        i += 1
        filename = f'tmp_imgs/{i}.png'
        filenames.append(filename)

        # save frame
        plt.savefig(filename, dpi=200)
        plt.close()

    # build gif
    print('Building GIF...')
    with imageio.get_writer('doppler_range_heatmap.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            writer.append_data(image)

    # Remove files
    print('Removing files...')
    for filename in filenames:
        os.remove(filename)

    # Remove dir
    os.rmdir('tmp_imgs')

    print('Done!')


# def animateRangeHeatmap(frames):
#     # Create fake radar input data to get range bins
#     avg = np.zeros((PARAMS.CHIRP_LOOPS, PARAMS.RX_ANTENNAS*PARAMS.TX_ANTENNAS,
#                    PARAMS.ADC_SAMPLES), dtype=complex)

#     bins, chirps, matrix = generateRangeHeatmap(avg)

#     # Figure
#     fig, ax = plt.subplots()
#     cax = ax.pcolormesh(bins, chirps,
#                         np.abs(matrix), vmin=0, vmax=V_MAX)
#     fig.colorbar(cax, ax=ax)

#     ax.grid()
#     ax.set_xlabel('Range (m)')
#     ax.set_ylabel('Chirp #')

#     def animate(i):
#         adc_data = frames[i]
#         adc_data = DCA1000.organize(
#             adc_data, num_chirps=PARAMS.CHIRPS_PER_FRAME, num_rx=PARAMS.RX_ANTENNAS, num_samples=PARAMS.ADC_SAMPLES)
#         adc_data = DCA1000.separate_tx(adc_data, num_tx=PARAMS.TX_ANTENNAS)
#         _, _, matrix = generateRangeHeatmap(adc_data)

#         cax.set_array(np.abs(matrix))

#     anim = FuncAnimation(fig, animate, np.arange(len(frames)),
#                          interval=100, repeat=False)

#     plt.show()


# def animateDopplerRangeHeatmap(frames):
#     # Create fake radar input data to get range bins
#     avg = np.zeros((PARAMS.CHIRP_LOOPS, PARAMS.RX_ANTENNAS*PARAMS.TX_ANTENNAS,
#                    PARAMS.ADC_SAMPLES), dtype=complex)

#     range_bins, doppler_bins, matrix = generateDopplerRangeHeatmap(avg)

#     # Figure
#     fig, ax = plt.subplots()
#     cax = ax.pcolormesh(range_bins, doppler_bins,
#                         np.abs(matrix), vmin=0, vmax=V_MAX)
#     fig.colorbar(cax, ax=ax)

#     ax.grid()
#     ax.set_xlabel('Range (m)')
#     ax.set_ylabel('Doppler (m/s)')

#     def animate(i):
#         adc_data = frames[i]
#         adc_data = DCA1000.organize(
#             adc_data, num_chirps=PARAMS.CHIRPS_PER_FRAME, num_rx=PARAMS.RX_ANTENNAS, num_samples=PARAMS.ADC_SAMPLES)
#         adc_data = DCA1000.separate_tx(adc_data, num_tx=PARAMS.TX_ANTENNAS)
#         _, _, matrix = generateDopplerRangeHeatmap(adc_data)

#         cax.set_array(np.abs(matrix))

#     anim = FuncAnimation(fig, animate, np.arange(len(frames)),
#                          interval=100, repeat=False)

#     plt.show()


# def animateAzimuthRangeHeatmap(frames):
#     # Create fake radar input data to get range bins
#     avg = np.zeros((PARAMS.CHIRP_LOOPS, PARAMS.RX_ANTENNAS*PARAMS.TX_ANTENNAS,
#                    PARAMS.ADC_SAMPLES), dtype=complex)

#     range_bins, azimuth_bins, matrix = generateAzimuthRangeHeatmap(avg)

#     # Figure
#     fig, ax = plt.subplots()
#     cax = ax.pcolormesh(range_bins, azimuth_bins,
#                         np.abs(matrix), vmin=0, vmax=V_MAX)
#     fig.colorbar(cax, ax=ax)

#     ax.grid()
#     ax.set_xlabel('Range (m)')
#     ax.set_ylabel('Azimuth (°)')

#     def animate(i):
#         adc_data = frames[i]
#         adc_data = DCA1000.organize(
#             adc_data, num_chirps=PARAMS.CHIRPS_PER_FRAME, num_rx=PARAMS.RX_ANTENNAS, num_samples=PARAMS.ADC_SAMPLES)
#         adc_data = DCA1000.separate_tx(adc_data, num_tx=PARAMS.TX_ANTENNAS)
#         _, _, matrix = generateAzimuthRangeHeatmap(adc_data)

#         cax.set_array(np.abs(matrix))

#     anim = FuncAnimation(fig, animate, np.arange(len(frames)),
#                          interval=100, repeat=False)

#     plt.show()
