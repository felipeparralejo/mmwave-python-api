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
from animated_plots import animateFFTRange, animateRangeHeatmap, animateDopplerRangeHeatmap, animateAzimuthRangeHeatmap
from fourier import plotFFTazimuth, plotFFTelevation, plotFFTrange
from params import PARAMS
from raw_signal import RadarData, plot_signal

data = pickle.load(open('data\openradar_11-01-23_PWCWPFDVFC.dat', 'rb'))

config = data['config']

PARAMS.set_playback_mode(config)

rdata = RadarData(device='IWR1843',
                  tx=PARAMS.TX_ANTENNAS,
                  rx=PARAMS.RX_ANTENNAS,
                  loops=PARAMS.CHIRP_LOOPS,
                  samples=PARAMS.ADC_SAMPLES)

# Get raw data frame
frames = data['data']
adc_data = frames[50]
# Set RadarData raw_data
rdata.raw_data = adc_data
# Access data separated by Rx and Tx antennas
separated = rdata.separated_data
# Alternatively, access data separated by Vx antennas
separated_vx = rdata.separated_vx_data

plot_signal(separated_vx[0, 0])
# The following lines produce the same result
# plotFFTrange(separated_vx[0, 0], PEAK_TH=90)
# plotFFTrange(separated[0, 0, 0], PEAK_TH=90)
# matrix = heatmaps.plotRangeHeatmap(separated_vx)
# matrix = heatmaps.plotDopplerRangeHeatmap(separated_vx)
# matrix = heatmaps.plotAzimuthRangeHeatmap(separated_vx)
# matrix = heatmaps.plotElevationRangeHeatmap(separated_vx)
# animateFFTRange(frames, PEAK_TH=95)
# animateRangeHeatmap(frames)
# animateDopplerRangeHeatmap(frames)
# animateAzimuthRangeHeatmap(frames)
