"""

MMWAVE DCA1000 PARAMETERS
=========================

Import PARAMS object to get access to all variables.
Call PARAMS.set_playback_mode(config) to use custom config dictionary (when reading saved data).

"""


class __PARAMS_CLASS():
    '''
    Parameter parsing class.
    This class should not be used.
    Import PARAMS object instead.
    '''

    RECORD_MODE = 1
    PLAYBACK_MODE = 2
    CONFIG_FILE = '/Users/air-josete/Documents/GitHub/mmwaveFelipe/mmWave Studio Scripts/DataCaptureDemo_PythonPrepare.lua'

    c = 299792458  # m/s

    def __init__(self):
        # Setting record mode by default
        self.set_record_mode()
        self.printSummary()

    def parse_config(self):
        # ------------------------------
        # Params from config file

        self.TX_ANTENNAS = int(self.CONFIG['NUM_TX'])
        self.RX_ANTENNAS = int(self.CONFIG['NUM_RX'])

        self.fc = self.CONFIG['START_FREQ']*1e9  # chirp start frequency, Hz
        self.Tc = self.CONFIG['IDLE_TIME']*1e-6  # s
        self.Tr = self.CONFIG['RAMP_END_TIME']*1e-6  # s
        self.ADC_START_TIME = self.CONFIG['ADC_START_TIME']*1e-6  # s
        self.k = self.CONFIG['FREQ_SLOPE']*1e6/1e-6  # Hz/s
        self.ADC_SAMPLES = int(self.CONFIG['ADC_SAMPLES'])
        self.FS = self.CONFIG['SAMPLE_RATE']  # ksps
        self.RX_GAIN = self.CONFIG['RX_GAIN']  # dB

        self.CHIRP_LOOPS = int(self.CONFIG['CHIRP_LOOPS'])
        self.Tperiodicity = self.CONFIG['PERIODICITY']  # ms

        self.fs = self.FS*1e3  # Hz
        self.lmbda = self.c/self.fc  # wavelength, m
        self.Tchirp = self.Tc + self.Tr  # total chirp duration, s
        self.Tsep_chirp = self.Tchirp*self.TX_ANTENNAS  # time between same chirp, s
        self.MIN_PERIODICITY = self.Tchirp*self.CHIRP_LOOPS*self.TX_ANTENNAS*1000  # ms
        self.CHIRPS_PER_FRAME = self.CHIRP_LOOPS*self.TX_ANTENNAS

        # ------------------------------
        # RANGE FFT PARAMETERS CALCULATION

        self.NUM_RANGE_BINS = self.ADC_SAMPLES

        # Para calcular B usamos el tiempo total de sampleo
        self.k_temp = 48*self.k * 2**26 * 1e3/((3.6*1e9)*900)
        self.Ts = self.ADC_SAMPLES/self.fs  # sampling time, s
        self.B1 = self.k_temp*self.Ts  # bandwidth, Hz
        self.B2 = self.k*self.Tr
        self.R_BIN = self.c/(2*self.B2)  # range precision, m
        self.R_MAX = self.R_BIN*self.NUM_RANGE_BINS  # m
        self.R_MAX_UNAMBIGUOUS = 0.9*self.R_MAX

        # ------------------------------
        # DOPPLER FFT PARAMETERS CALCULATION

        self.NUM_DOPPLER_BINS = self.CHIRP_LOOPS

        self.DOPPLER_BIN = self.lmbda / \
            (2*self.CHIRP_LOOPS*self.Tsep_chirp)  # m/s
        self.DOPPLER_MAX = self.lmbda/(4*self.Tsep_chirp)  # m/s

        # ------------------------------
        # AZIMUTH FFT PARAMETERS CALCULATION

        self.NUM_AZIM_BINS = 64

        # ------------------------------
        # ELEVATION FFT PARAMETERS CALCULATION

        self.NUM_ELEV_BINS = 32

    def set_record_mode(self):
        self.MODE = self.RECORD_MODE
        self.CONFIG = self.parse_config_file()
        self.parse_config()

    def set_playback_mode(self, playback_config):
        self.MODE = self.PLAYBACK_MODE
        self.CONFIG = playback_config
        self.parse_config()

    def parse_config_file(self):
        d = {}
        # Read file and update dict
        with open(self.CONFIG_FILE, 'r') as f:
            for _ in range(39):
                line = f.readline()
                if not (line.startswith('-') or line.startswith('\n')):
                    elems = line[:-1].split(' = ')
                    param = elems[0]

                    if param != 'NUM_TX' and param != 'END_CHIRP_TX':
                        d.update({elems[0]: float(elems[1].split(' -')[0])})

        # Compute remaining parameters
        d['NUM_TX'] = d['TX0_EN'] + d['TX1_EN'] + d['TX2_EN']
        d['END_CHIRP_TX'] = d['NUM_TX'] - 1

        return d

    def printSummary(self):

        print("Slope", self.k)
        # print("Slope 2", self.k_temp)
        # print("Bandwith 1",self.B1/1e6, "GHz")
        print("Bandwith", self.B2/1e6, "GHz")

        print("Minimum Frame Periodicity:", self.MIN_PERIODICITY, "ms")
        print("Chirps Per Frame:", self.CHIRPS_PER_FRAME)

        print("Num Range Bins:", self.NUM_RANGE_BINS)
        print("Range Resolution:", self.R_BIN, "m")
        print("Max Unambiguous Range:", self.R_MAX_UNAMBIGUOUS, "m")

        print("Num Doppler Bins:", self.NUM_DOPPLER_BINS)
        print("Doppler Resolution:", self.DOPPLER_BIN, "m/s")
        print("Max Doppler:", self.DOPPLER_MAX, "m/s")

        print("Num Azimuth Bins:", self.NUM_AZIM_BINS)

        print("Num Elevation Bins:", self.NUM_ELEV_BINS)


PARAMS = __PARAMS_CLASS()


"""
Params from openradar examples for the same config
>> > print("Minimum Frame Periodicity:", MIN_PERIODICITY)
Minimum Frame Periodicity: 63.744
>> > print("Chirps Per Frame:", CHIRPS_PER_FRAME)
Chirps Per Frame: 384
>> > print("Num Doppler Bins:", NUM_DOPPLER_BINS)
Num Doppler Bins: 128.0
>> > print("Num Range Bins:", NUM_RANGE_BINS)
Num Range Bins: 128
>> > print("Range Resolution:", RANGE_RESOLUTION)
Range Resolution: 0.19542975785471284
>> > print("Max Unambiguous Range:", MAX_RANGE)
Max Unambiguous Range: 22.513508104862918
>> > print("Doppler Resolution:", DOPPLER_RESOLUTION)
Doppler Resolution: 0.03170657467532467
>> > print("Max Doppler:", MAX_DOPPLER)
Max Doppler: 2.029220779220779
"""
