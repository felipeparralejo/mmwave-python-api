"""

CAPON BEAMFORMING
==================


"""

import warnings
import numpy as np
from numpy import linalg as LA


def aoa_capon(x, steering_vector, magnitude=False):
    """Perform AOA estimation using Capon (MVDR) Beamforming on a rx by chirp slice
    Calculate the aoa spectrum via capon beamforming method using one full frame as input.
    This should be performed for each range bin to achieve AOA estimation for a full frame
    This function will calculate both the angle spectrum and corresponding Capon weights using
    the equations prescribed below.
    .. math::
        P_{ca} (\\theta) = \\frac{1}{a^{H}(\\theta) R_{xx}^{-1} a(\\theta)}

        w_{ca} (\\theta) = \\frac{R_{xx}^{-1} a(\\theta)}{a^{H}(\\theta) R_{xx}^{-1} a(\\theta)}
    Args:
        x (ndarray): Output of the 1d range fft with shape (num_ant, numChirps)
        steering_vector (ndarray): A 2D-array of size (numTheta, num_ant) generated from gen_steering_vec
        magnitude (bool): Azimuth theta bins should return complex data (False) or magnitude data (True). Default=False
    Raises:
        ValueError: steering_vector and or x are not the correct shape
    Returns:
        A list containing numVec and steeringVectors
        den (ndarray: A 1D-Array of size (numTheta) containing azimuth angle estimations for the given range
        weights (ndarray): A 1D-Array of size (num_ant) containing the Capon weights for the given input data

    Example:
        >>> # In this example, dataIn is the input data organized as numFrames by RDC
        >>> Frame = 0
        >>> dataIn = np.random.rand((num_frames, num_chirps, num_vrx, num_adc_samples))
        >>> for i in range(256):
        >>>     scan_aoa_capon[i,:], _ = dss.aoa_capon(dataIn[Frame,:,:,i].T, steering_vector, magnitude=True)
    """

    if steering_vector.shape[1] != x.shape[0]:
        raise ValueError("'steering_vector' with shape (%d,%d) cannot matrix multiply 'input_data' with shape (%d,%d)"
                         % (steering_vector.shape[0], steering_vector.shape[1], x.shape[0], x.shape[1]))

    Rxx = cov_matrix(x)
    Rxx = forward_backward_avg(Rxx)
    Rxx_inv = np.linalg.inv(Rxx)
    # Calculate Covariance Matrix Rxx
    first = Rxx_inv @ steering_vector.T
    den = np.reciprocal(np.einsum('ij,ij->i', steering_vector.conj(), first.T))
    weights = np.matmul(first, den)

    if magnitude:
        return np.abs(den), weights
    else:
        return den, weights


def musicPS(rFFT, A):

    HM = np.zeros((np.shape(rFFT)[1], np.shape(A)[1]), dtype=complex)

    for ii in range(np.shape(rFFT)[1]):
        R = 1/np.shape(A)[0] * np.conjugate(np.matmul(np.transpose(rFFT[:,
                                                                        ii][np.newaxis]), rFFT[:, ii][np.newaxis]))
        _, Qn = LA.eig(R)
        Qn = np.delete(Qn, -1, 1)

        Qn = np.matmul(Qn, np.transpose(Qn))

        HM[ii, :] = 1/np.diag(np.array(np.transpose(A) @ np.transpose(Qn) @ A))

    return HM

# ------------------------------- HELPER FUNCTIONS -------------------------------

# def steervec(antLay, lam, theta):
#     """"
#     Returns the steering vector with an antenna layout given by 'antLay' and the angles given
#     by 'theta'.

#     """
#     A = np.zeros((np.shape(antLay)[0], np.shape(theta)[0]), dtype=complex)
#     for n in range(np.shape(antLay)[0]):
#         for m in range(np.shape(theta)[0]):
#             A[n, m] = np.exp(-1j * 2*np.pi/lam * antLay[n] *
#                              np.sin(np.deg2rad(theta[m])))
#     return A
#  [1,  e^ [j * pi * ( sin(azimuth) * cos(elevation) + sin(elevation) ) ]

# import capon


def steervec(antLay, lam, theta, phi=0):
    """"
    Returns the steering vector with an antenna layout given by 'antLay' and the angles given
    by 'theta'.

    """
    numAnt = np.shape(antLay)[1]
    numTheta = np.shape(theta)[0]

    if (np.size(phi) == 0):
        A = np.zeros((numAnt, numTheta), dtype=complex)
        for n in range(numAnt):
            for m in range(numTheta):
                A[n, m] = np.exp(-1j * 2*np.pi/lam * antLay[n] *
                                 np.sin(np.deg2rad(theta[m])))

    else:
        numPhi = np.shape(phi)[0]
        A = np.zeros((numAnt, numTheta*numPhi), dtype=complex)
        for n in range(numAnt):
            for m in range(numTheta):
                for p in range(numPhi):
                    A[n, numPhi*m+p] = np.exp(-1j * 2*np.pi/lam * np.sqrt(pow(antLay[1, n], 2)+pow(antLay[2, n], 2)) *
                                              (np.sin(np.deg2rad(theta[m])) * np.cos(np.deg2rad(phi[p])) + np.sin(np.deg2rad(phi[p]))))

    return A


def cov_matrix(x):
    """ Calculates the spatial covariance matrix (Rxx) for a given set of input data (x=inputData). 
        Assumes rows denote Vrx axis.
    Args:
        x (ndarray): A 2D-Array with shape (rx, adc_samples) slice of the output of the 1D range fft
    Returns:
        Rxx (ndarray): A 2D-Array with shape (rx, rx)
    """

    if x.ndim > 2:
        raise ValueError("x has more than 2 dimensions.")

    if x.shape[0] > x.shape[1]:
        warnings.warn(
            "cov_matrix input should have Vrx as rows. Needs to be transposed", RuntimeWarning)
        x = x.T

    _, num_adc_samples = x.shape
    Rxx = x @ np.conjugate(x.T)
    Rxx = np.divide(Rxx, num_adc_samples)

    return Rxx


def forward_backward_avg(Rxx):
    """ Performs forward backward averaging on the given input square matrix
    Args:
        Rxx (ndarray): A 2D-Array square matrix containing the covariance matrix for the given input data
    Returns:
        R_fb (ndarray): The 2D-Array square matrix containing the forward backward averaged covariance matrix
    """
    assert np.size(Rxx, 0) == np.size(Rxx, 1)

    # --> Calculation
    M = np.size(Rxx, 0)  # Find number of antenna elements
    Rxx = np.matrix(Rxx)  # Cast np.ndarray as a np.matrix

    # Create exchange matrix
    J = np.eye(M)  # Generates an identity matrix with row/col size M
    J = np.fliplr(J)  # Flips the identity matrix left right
    J = np.matrix(J)  # Cast np.ndarray as a np.matrix

    R_fb = 0.5 * (Rxx + J * np.conjugate(Rxx) * J)

    return np.array(R_fb)
