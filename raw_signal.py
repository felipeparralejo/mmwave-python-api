"""

RAW SIGNAL UTILITIES
====================

Included functions:
    - Plot raw signal

"""

import matplotlib.pyplot as plt
import numpy as np

from dca1000 import DCA1000


class RadarData:
    """Class that holds radar data for a device and performs the necessary transformations
        such as TX-RX antenna separation or phase inversion.
        Currently, supported devices are:
            - IWR1843 (no phase inversion)
            - IWR6843ISK-ODS (phase inversion on RX2 and RX3)

        Attributes
        ----------
        device : str
            radar model identifier
        tx : int
            number of TX antennas used in the data emission process
        rx : int
            number of RX antennas used in the data capturing process
        loops : int
            number of chirp loops per frame
        samples : int
            number of ADC samples

        Properties
        ----------
        raw_data : Numpy Array
            Byte I-Q data captured with DCA1000 library of shape (tx*rx*loops*samples*2,)
        separated_vx_data : Numpy array
            Radar data separated by VX antennas of shape (loops, num_vx, samples)
        separated_data : Numpy array
            Radar data separated by RX and TX antenna pairs of shape (tx, rx, loops, samples)

        Usage
        ------
        Instantiate a RadarData object with its attributes and set raw_data property, then
        access vx_data and radar_data calculated properties, and methods and proceed with
        calculations.

        Methods
        -------
        printDataConfig():
            Prints data parameters.
        """

    def __init__(self, device, tx, rx, loops, samples):
        self.device = device
        self.tx = tx
        self.rx = rx
        self.loops = loops
        self.samples = samples

        self.printDataConfig()

    @property
    def raw_data(self):
        """Byte I-Q data captured with DCA1000 library of shape (tx*rx*loops*samples*2,)"""
        return self._raw_data

    @raw_data.setter
    def raw_data(self, value):
        self._raw_data = value

    @property
    def _organized_data(self):
        """INTERNAL USE ONLY.
        Radar data separated by RX antennas of shape (tx*loops, rx, samples) and phase
        inverted if needed"""
        data = DCA1000.organize(
            self.raw_data, num_chirps=self.loops*self.tx, num_rx=self.rx, num_samples=self.samples)

        if (self.device == 'IWR6843ISK-ODS'):
            data[:, 1, :] *= -1
            data[:, 2, :] *= -1

        return data

    @property
    def separated_vx_data(self):
        """Radar data separated by VX antennas of shape (loops, num_vx, samples)"""
        return DCA1000.separate_tx(self._organized_data, num_tx=self.tx)

    @property
    def separated_data(self):
        """Radar data separated by RX and TX antenna pairs of shape (tx, rx, loops, samples)"""
        data = np.zeros(shape=(self.tx, self.rx, self.loops,
                        self.samples), dtype=complex)

        tx_list = [self._organized_data[i::self.tx, ...]
                   for i in range(self.tx)]

        for antx in range(self.tx):
            for anrx in range(self.rx):
                data[antx, anrx, :, :] = tx_list[antx][:, anrx, :]

        return data

    def printDataConfig(self):
        print("Device", self.device)
        print("TX Antennas", self.tx)
        print("RX Antennas", self.rx)
        print("Number of loops", self.loops)
        print("ADC Samples", self.samples)


def plot_signal(signal):
    fig, axv = plt.subplots()

    sI = np.real(signal)
    sQ = np.imag(signal)

    axv.plot(sI, "b-")
    axv.plot(sQ, "r-")
    axv.grid()
    axv.legend(["real", "imag"])
    axv.set_xlabel("sample index")
    axv.set_ylabel("raw ADC output")

    plt.show()
