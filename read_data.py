import params
import pickle
import numpy as np
import heatmaps
from fourier import plotFFTrange
from mmwave.dataloader import DCA1000
from mmwave.dsp import separate_tx

frames = pickle.load(
    open('data\openradar_10_frames_14-12-22_13h04m04s.dat', 'rb'))

adc_data = frames[0]
adc_data = DCA1000.organize(
    adc_data, num_chirps=params.CHIRPS_PER_FRAME, num_rx=params.RX_ANTENNAS, num_samples=params.ADC_SAMPLES)
adc_data = separate_tx(adc_data, num_tx=params.TX_ANTENNAS)

plotFFTrange(adc_data[0, 0])
# matrix = heatmaps.plotRangeHeatmap(adc_data)
# matrix = heatmaps.plotDopplerRangeHeatmap(adc_data[:, 0, :])
# matrix = heatmaps.plotAzimuthRangeHeatmap(adc_data[0, :, :])
