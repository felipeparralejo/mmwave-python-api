
# %%
# IMPORTS and DEFINITIONS

import pickle
import numpy as np
from fourier import rangeFFT, angleFFT, dopplerFFT
from raw_signal import RadarData
from params import PARAMS
import PyQt6
import datetime
import matplotlib.pyplot as plt
from IPython.display import display, clear_output

# Butterworth filter definition
from scipy.signal import butter, lfilter
from scipy.signal import freqz


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


# %%
# Load Data

data = pickle.load(open('data/openradar_23-03-23_UDE-IHRABST4PA.dat', 'rb'))
# Load config parameters
config = data['config']
PARAMS.set_playback_mode(config)
# Read main parameters
rdata = RadarData(device='IWR1843',
                  tx=PARAMS.TX_ANTENNAS,
                  rx=PARAMS.RX_ANTENNAS,
                  loops=PARAMS.CHIRP_LOOPS,
                  samples=PARAMS.ADC_SAMPLES)

# Get data frame
frames = data['data']


# %%
# PHASE CALCULATION

fini = 1
ffin = 451

P_slow = np.zeros(((ffin-fini), 12))
P_fast = np.zeros(((ffin-fini)*255, 12))

for fr in range(fini, ffin):
    # for n in range(0):
    adc_data = frames[fr]
    # Set RadarData raw_data
    rdata.raw_data = adc_data
    # Access data separated by Rx and Tx antennas
    v_array = rdata.separated_vx_data
    for chirp in range(np.size(v_array, 0)):
        # 1D RANGE FFT
        [_, rFFT, _] = rangeFFT(v_array[chirp, :, :], rdata.device)
        # Bin for max in range
        # One of the antennas must be taken (arbitrarily 2 for now)
        binMax = np.argmax(abs(rFFT[:, :40]), axis=1)[2]
        # Accumulative phase in fast time
        P_fast[255*(fr-fini)+chirp, :] = np.angle(rFFT[:,
                                                       int(binMax)], deg=True)

    # Median in low time
    P_slow[fr-fini, :] = np.median(P_fast[255 *
                                   (fr-fini):255*(fr-fini+1)-1, :], axis=0)


# Time Calculation
t = [datetime.timedelta(0)]
for n in range(fini, ffin-1):
    t.append(t[n-fini] + data["timestamps"][n]-data["timestamps"][n-1])
# Slow time
t_slow = []
for n in range(len(t)):
    t_slow.append(t[n].total_seconds())

t_fast = []
for n in range(np.size(t_slow)):
    t_fast.append(np.linspace(t_slow[n], t_slow[n]+40e-3, 255))
t_fast = np.concatenate(t_fast)

# %%
# PHASE DIFFERENCE CALCULATION

P_diff = np.zeros((np.size(P_slow, 0)-1, 12))
for ant in range(12):
    for n in range(np.size(P_slow[:, ant])-1):
        P_diff[n, ant] = (P_slow[n+1, ant] - P_slow[n, ant])
    # P_diff[:,ant] = np.unwrap(P_diff[:,ant],axis=0)

# %%
# FOURIER ANALYSIS

# Figure definition
fig, ax = plt.subplots()
ax.set_xlabel('Frequency (Hz)')
ax.grid(visible=True)

# Parameters
T = []
for pp in range(len(t)-1):
    T.append(t_slow[pp+1]-t_slow[pp])
T = np.mean(T)

Fs = 1/T
L = 1000  # Zero-padded FFT
freq = np.fft.fftshift(np.fft.fftfreq(L, T))
freq = freq[int(L/2):]

for i in range(ffin-50):
    PD = np.unwrap(P_diff[i:i+50, 3], period=360)
    # Heart rate signal 0.8-2.0 Hz
    y2 = butter_bandpass_filter(PD, 0.8, 2.0, Fs, order=20)
    # Breathing signal 0.1-0.6 Hz (0.4 in the following function for a proper filter performance)
    y1 = butter_bandpass_filter(PD, 0.1, 0.4, Fs, order=7)

    FT1 = np.fft.fftshift(abs(np.fft.fft(y1, L, axis=0))/L)
    FT1 = FT1[int(L/2):]
    FT2 = np.fft.fftshift(abs(np.fft.fft(y2, L, axis=0))/L)
    FT2 = FT2[int(L/2):]

    ax.cla()
    ax.set_xlabel('Frequency (Hz)')
    ax.grid(visible=True)
    ax.plot(freq, abs(FT1),
            '.-', c="C0", label="Breathing rate")
    ax.plot(freq, abs(FT2),
            '.-', c="C1", label="Heart rate")
    ax.set_ylim(0, 2.5)
    ax.legend()
    ax.text(0, 1.80, "BR: " +
            str(round(freq[np.argmax(FT1)]*60, 2)) + " breaths/minute")
    ax.text(0, 1.60, "HR: " +
            str(round(freq[np.argmax(FT2)]*60, 2)) + " beats/minute")
    display(fig)
    clear_output(wait=True)
    # fig.savefig('images/rProf'+str(n+1),dpi=600)
    plt.pause(T)

# %%
