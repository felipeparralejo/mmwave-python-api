import params
import numpy as np
import matplotlib.pyplot as plt


def plotRangeHeatmap(signal):
    '''
    Plot range-doppler heatmap of one TX-RX pair
    '''

    # Average antennas
    # avg = np.mean(signal, axis=1)
    avg = signal[:, 0, :]

    matrix = np.zeros_like(avg, dtype=complex)

    # Do FFT along each chirp's samples (range)
    # Shift zero freq.
    for i in range(avg.shape[0]):
        matrix[i, :] = np.fft.fftshift(np.fft.fft(avg[i]))

    # Find vertical and horizontal bins
    chirps = np.arange(avg.shape[0])
    bins = np.fft.fftfreq(avg.shape[1])

    # Shift bins
    bins = np.fft.fftshift(bins)

    # Rearrange data
    # n = bins.size//2
    # beg = bins[:n]
    # end = bins[n:]
    # bins = np.concatenate([end, beg])*params.R_MAX

    # mbeg = matrix[:, :n]
    # mend = matrix[:, n:]
    # matrix = np.concatenate([mend, mbeg], axis=1)

    fig, ax = plt.subplots()

    c = ax.pcolormesh(bins, chirps, np.log2(np.abs(matrix)))
    fig.colorbar(c, ax=ax)
    ax.set_title('Range Heatmap')
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Chirp #')

    plt.show()

    return matrix


def plotDopplerRangeHeatmap(raw_data):
    '''
    Plot range-doppler heatmap of one TX-RX pair
    '''
    matrix = np.zeros_like(raw_data, dtype=complex)

    # Do FFT along each chirp's samples (range)
    for i in range(raw_data.shape[0]):
        matrix[i, :] = np.fft.fft(raw_data[i])

    # Do FFT along chirps (doppler)
    for i in range(raw_data.shape[1]):
        matrix[:, i] = np.fft.fft(matrix[:, i])

    fig, ax = plt.subplots()
    im = ax.imshow(np.log2(np.abs(matrix)))
    cbar = ax.figure.colorbar(im,
                              ax=ax,
                              shrink=0.5)
    ax.set_frame_on(False)  # remove all spines
    ax.set_title('Doppler-Range Heatmap')
    ax.set_xlabel('Range bins')
    ax.set_ylabel('Doppler bins')

    plt.show()

    return matrix


def plotAzimuthRangeHeatmap(raw_data):
    '''
    Plot azimuth-doppler heatmap of one chirp
    TODO: find which antennas are for azimuth and elevation
          using all for now...
    '''

    # Another way to plot heatmaps
    # rangegrid = np.arange(raw_data.shape[1])
    # azimuthgrid = np.arange(raw_data.shape[0])
    # ax.pcolormesh(rangegrid, azimuthgrid, np.log2(np.abs(matrix)))

    matrix = np.zeros_like(raw_data, dtype=complex)

    # Do FFT along each chirp's samples (range)
    for i in range(raw_data.shape[0]):
        matrix[i, :] = np.fft.fft(raw_data[i])

    # Do FFT along antennas (azimuth)
    for i in range(raw_data.shape[1]):
        matrix[:, i] = np.fft.fft(matrix[:, i])

    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.imshow(np.log2(np.abs(matrix)),
                   aspect='auto')  # , interpolation='none')
    cbar = ax.figure.colorbar(im,
                              ax=ax,
                              shrink=0.5)
    ax.set_frame_on(False)  # remove all spines
    ax.set_title('Azimuth-Range Heatmap')
    ax.set_xlabel('Range bins')
    ax.set_ylabel('Azimuth bins')

    plt.show()

    return matrix
