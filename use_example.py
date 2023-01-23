"""

READ SAVED DATA AND PROCESS
===========================

Read saved .dat file and perform signal processing.

Usage:
   1. Read saved file and set_playback_mode in PARAMS using read config
   2. Create RadarData object with params
   3. Fill RadarData raw_data with raw frame
   4. Access RadarData's separated_data and separated_vx_data properties
   5. Adjust data to your needings and continue processing

"""

import pickle
import numpy as np
import heatmaps
# from animated_plots import animateFFTRange, animateRangeHeatmap, animateDopplerRangeHeatmap, animateAzimuthRangeHeatmap
from fourier import rangeFFT, angleFFT
from params import PARAMS
from raw_signal import RadarData, plot_signal
import matplotlib.pyplot as plt

# Load data from file
data = pickle.load(open('data\openradar_12-01-23_SCRQO.dat', 'rb'))
# Configure playback mode
config = data['config']
PARAMS.set_playback_mode(config)
# Read main parameters
rdata = RadarData(device='IWR6843ISK-ODS',
                  tx=PARAMS.TX_ANTENNAS,
                  rx=PARAMS.RX_ANTENNAS,
                  loops=PARAMS.CHIRP_LOOPS,
                  samples=PARAMS.ADC_SAMPLES)

# Get data frame
frames = data['data']
# Choose frame
adc_data = frames[5]
# Set RadarData raw_data
rdata.raw_data = adc_data
# Access data separated by Rx and Tx antennas
v_array = rdata.separated_vx_data
# 1D RANGE FFT and radar cube
[RC, rFFT, rBins] = rangeFFT(v_array[1,:,:],rdata.device)
# The range profile can be extracted from this as
plt.plot(rBins[8:],np.mean(abs(rFFT),axis=0)[8:])
plt.show()
# 2D AZIMUTH & ELEVATION FFTs
[aFFT, eFFT, aBins, eBins] = angleFFT(RC)
heatmaps.plotAzimuthRangeHeatmap(rBins[:60],aBins[2:],aFFT[2:,:60])

# TODO Cartesian HEATMAP
# heatmaps.plotXYheatmap(rBins,aBins,aFFT)

heatmaps.plotElevationRangeHeatmap(rBins,eBins,eFFT)


