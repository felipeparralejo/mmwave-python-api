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
from mpl_toolkits import mplot3d
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


def plotDopplerRangeHeatmap(raw_data):
    '''
    Plot Doppler-Range heatmap
    '''
    # range_bins, doppler_bins, matrix = generateDopplerRangeHeatmap(raw_data)

    fig, ax = plt.subplots()

    c = ax.pcolormesh(range_bins, doppler_bins, np.abs(matrix))
    fig.colorbar(c, ax=ax)
    ax.set_title('Doppler-Range Heatmap')
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Doppler (m/s)')

    plt.show()

    # return matrix


def plotAzimuthRangeHeatmap(range_bins,azimuth_bins,matrix):
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

    fig = plt.figure(figsize = (12,10))
    ax = plt.axes(projection='3d')

    X = matlabMultip(range_bins,np.sin(azimuth_bins*np.pi/180))
    Y = matlabMultip(range_bins,np.cos(azimuth_bins*np.pi/180))

    # ax = fig.add_subplot(1, 1, 1, projection='3d')
    plt.tight_layout()
    ax.plot_surface(X,Y,matrix.T,cmap = plt.cm.cividis)
    ax.set_title('Surface Heatmap')

    plt.show()
    