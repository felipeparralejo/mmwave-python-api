"""

HEATMAPS GENERATION
===================

Included functions:
    - Range Heatmap
    - Doppler-Range Heatmap
    - Azimuth-Range Heatmap
    - Elevation-Range Heatmap

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dca1000 import DCA1000
from fourier import matlabMultip

from params import PARAMS


def plotRangeHeatmap(signal):
    '''
    Plot range heatmap
    '''

    # bins, chirps, matrix = generateRangeHeatmap(signal)

    fig, ax = plt.subplots()

    c = ax.pcolormesh(bins, chirps, matrix)
    fig.colorbar(c, ax=ax)
    ax.set_title('Range Heatmap')
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Chirp #')

    plt.show()

    # return matrix


def plotDopplerRangeHeatmap(range_bins, doppler_bins, matrix):
    '''
    Plot Doppler-Range heatmap
    '''
    # range_bins, doppler_bins, matrix = generateDopplerRangeHeatmap(raw_data)

    fig, ax = plt.subplots()

    c = ax.pcolormesh(range_bins, doppler_bins, matrix)
    fig.colorbar(c, ax=ax)
    ax.set_title('Doppler-Range Heatmap')
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Doppler (m/s)')

    plt.show()

    # return matrix


def plotAzimuthRangeHeatmap(range_bins, azimuth_bins, matrix):
    '''
    Plot Azimuth-Range heatmap
    '''

    fig, ax = plt.subplots()

    c = ax.pcolormesh(range_bins, azimuth_bins, matrix)
    fig.colorbar(c, ax=ax)
    ax.set_title('Azimuth-Range Heatmap')
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Azimuth (°)')

    plt.show()

    # return matrix


def plotElevationRangeHeatmap(range_bins, elevation_bins, matrix):
    '''
    Plot Elevation-Range heatmap
    '''

    fig, ax = plt.subplots()

    c = ax.pcolormesh(range_bins, elevation_bins, matrix)
    fig.colorbar(c, ax=ax)
    ax.set_title('Elevation-Range Heatmap')
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Elevation (°)')

    plt.show()

    # return matrix


def plotXYheatmap(range_bins, azimuth_bins, matrix):

    fig = plt.figure()
    ax = plt.axes()

    X = matlabMultip(range_bins.T, np.sin(azimuth_bins*np.pi/180))
    Y = matlabMultip(range_bins.T, np.cos(azimuth_bins*np.pi/180))

    # ax = fig.add_subplot(1, 1, 1)
    # plt.tight_layout()
    ax.pcolormesh(X, Y, matrix.T, cmap=plt.cm.jet)
    ax.set_title('XY Heatmap')
    # ax.view_init(90, 90)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')

    plt.show()
