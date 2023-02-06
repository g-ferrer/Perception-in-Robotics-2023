#!/usr/bin/python

"""
Sudhanva Sreesha
ssreesha@umich.edu
20-Mar-2018

Task 4 (25 pts)
"""

from argparse import ArgumentParser

import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main():
    parser = ArgumentParser('EECS 568: PS1 - Task 4 Data Generation')
    parser.add_argument('output_data_filename',
                        type=str,
                        default='./ps1/data_task4.npy',
                        help='The file which to which the data for Task #4 will be written.')
    args = parser.parse_args()

    # Time interval between two consecutive samples.
    dt = 0.1
    # Number of points to use while approximating the spline for data generation.
    M = 10
    # Time series in the interval [0, 100 + dt) with dt increments.
    t = np.arange(0, 100 + dt, dt)
    # Number of points in the data sequence.
    N = t.size
    # Sigma of action noise.
    R_action = 10
    # Sigma of measurement noise.
    Q = 5
    # Initial state: only used for saving to data file.
    x_0 = 0  # Initial state mean.
    P_0 = 0  # Initial state covariance.

    # Data to approximate a spline for data generation.
    x = 10. * np.arange(M + 1)
    y = 10. * np.random.uniform(size=(M + 1, )) + 65
    # Add a stopping condition at the start and end of the loop.
    y[0] = 0
    y[-1] = 0
    f = interp1d(x, y, kind='cubic')
    # The real velocity data points.
    x_real = f(t)

    # Generate noisy control actions.
    u = np.diff(x_real) / dt + np.sqrt(R_action) * np.random.standard_normal(size=(N - 1, ))
    # Generate noisy observation data.
    z = x_real[1:] + np.sqrt(Q) * np.random.standard_normal(size=(N - 1, ))

    # Plot velocity data.
    plt.figure(0)
    plt.plot(t[1:], z, 'g')
    plt.plot(t, x_real, 'r')
    plt.plot(x, y, 'bo')
    plt.title('Ground Truth Generation')
    plt.legend(['Noisy Observations', 'Ground Truth', 'Spline Points'])
    plt.xlabel('Time')
    plt.ylabel('Velocity')
    plt.draw()

    # Plot controls data.
    plt.figure(1)
    plt.plot(t[1:], u)
    plt.title('Control Actions')
    plt.xlabel('Time')
    plt.ylabel('Acceleration')
    plt.draw()

    plt.show()

    with open(args.output_data_filename, 'wb') as output_data_file:
        np.savez(output_data_file,
                 t=t,
                 dt=dt,
                 N=N,
                 M=R_action,
                 Q=Q,
                 u=u,
                 z=z,
                 x_real=x_real,
                 x_0=x_0,
                 P_0=P_0)


if __name__ == '__main__':
    main()
