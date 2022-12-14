config_file = 'C:\\ti\mmwave_studio_02_01_01_00\mmWaveStudio\Scripts\DataCaptureDemo_PythonPrepare.lua'


def parse_config():
    d = {}

    # Read file and update dict
    with open(config_file, 'r') as f:
        for i in range(40):
            line = f.readline()
            if not (line.startswith('-') or line.startswith('\n')):
                elems = line[:-1].split(' = ')
                param = elems[0]

                if param == 'FREQ_SLOPE':
                    d.update({elems[0]: float(elems[1].split(' -')[0])})
                elif param != 'NUM_TX' and param != 'END_CHIRP_TX':
                    d.update({elems[0]: int(elems[1].split(' -')[0])})

    # Compute remaining parameters
    d['NUM_TX'] = d['TX0_EN'] + d['TX1_EN'] + d['TX2_EN']
    d['END_CHIRP_TX'] = d['NUM_TX'] - 1

    return d


config = parse_config()

# ------------------------------
# Params from config file

TX_ANTENNAS = config['NUM_TX']
RX_ANTENNAS = config['NUM_RX']

c = 3e8  # m/s
fc = config['START_FREQ']*1e9  # chirp start frequency, Hz
Tc = config['IDLE_TIME']*1e-6  # s
Tr = config['RAMP_END_TIME']*1e-6  # s
ADC_START_TIME = config['ADC_START_TIME']*1e-6  # s
k = config['FREQ_SLOPE']*1e6/1e-6  # Hz/s
ADC_SAMPLES = config['ADC_SAMPLES']
FS = config['SAMPLE_RATE']  # ksps
RX_GAIN = config['RX_GAIN']  # dB

CHIRP_LOOPS = config['CHIRP_LOOPS']
Tframe = config['PERIODICITY']  # ms

fs = FS*1e3  # Hz
lmbda = c/fc  # wavelength, m
CHIRPS_PER_FRAME = CHIRP_LOOPS*TX_ANTENNAS

# ------------------------------
# RANGE FFT PARAMETERS CALCULATION

# Para calcular B usamos el tiempo total de sampleo
Ts = ADC_SAMPLES/fs  # sampling time, s
B = k*Ts  # bandwidth, Hz
R_BIN = c/(2*B)  # range precision, m
R_MAX = R_BIN*ADC_SAMPLES  # m
# R_MAX = c*fs/(2*k) # formula sustituyendo las expresiones anteriores
R_MAX_UNAMBIGUOUS = 0.9*R_MAX

# ------------------------------
# DOPPLER FFT PARAMETERS CALCULATION

# DOPPLER_MAX = lmbda/(4*Tc)  # m/s
