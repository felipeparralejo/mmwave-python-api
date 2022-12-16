"""

READ SAVED DATA AND PROCESS
===========================

Read saved .dat file and perform signal processing.

Right after reading file, it is compulsory to set playblack mode in
PARAMS to use radar configuration from the saved data.

"""

from params import PARAMS
import pickle
import heatmaps
from fourier import plotFFTrange
from dca1000 import DCA1000

data = pickle.load(open('data\openradar_14-12-22_MOAA5.dat', 'rb'))

frames = data['data']
config = data['config']

PARAMS.set_playback_mode(config)

adc_data = frames[0]
adc_data = DCA1000.organize(
    adc_data, num_chirps=PARAMS.CHIRPS_PER_FRAME, num_rx=PARAMS.RX_ANTENNAS, num_samples=PARAMS.ADC_SAMPLES)
adc_data = DCA1000.separate_tx(adc_data, num_tx=PARAMS.TX_ANTENNAS)

# plotFFTrange(adc_data[0, 0])
# matrix = heatmaps.plotRangeHeatmap(adc_data)
# matrix = heatmaps.plotDopplerRangeHeatmap(adc_data)
matrix = heatmaps.plotAzimuthRangeHeatmap(adc_data)
