import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mmwave.dataloader import DCA1000
from mmwave.dsp import separate_tx

import params


def doRangeFFT(signal):
    range = np.fft.fft(signal, axis=-1)
    range = np.fft.fftshift(range)

    bins = np.fft.fftfreq(signal.size)*params.R_MAX
    bins = np.fft.fftshift(bins)

    return range, bins


def liveRangePreview(dca):
    # Figure
    fig = plt.figure()
    ax = plt.axes(xlim=(0, params.R_MAX), ylim=(0, 1e7))
    line = ax.plot([], [], 'b-')[0]

    ax.grid()
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Reflected Power')

    def init():
        line.set_xdata(np.arange(params.ADC_SAMPLES))
        return line

    def animate(i):
        dca._clear_buffer()
        adc_data = dca.read()
        adc_data = DCA1000.organize(
            adc_data, num_chirps=params.CHIRPS_PER_FRAME, num_rx=params.RX_ANTENNAS, num_samples=params.ADC_SAMPLES)
        adc_data = separate_tx(adc_data, num_tx=params.TX_ANTENNAS)
        range, bins = doRangeFFT(adc_data[0, 0])
        line.set_xdata(bins)
        line.set_ydata(np.abs(range))

        return line

    anim = FuncAnimation(fig, animate, init_func=init,
                         interval=100)

    plt.show()


def plotFFTrange(signal):
    range, bins = doRangeFFT(signal)

    # Plot the magnitudes of the range bins
    plt.plot(bins, np.abs(range))
    plt.xlabel('Range (m)')
    plt.ylabel('Reflected Power')
    plt.title('Interpreting a Single Chirp')
    plt.show()
