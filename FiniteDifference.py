import numpy as np
import WaveFunction

def solve(xs, ts, potential, psi_init):
    matrix = build_matrix(xs, ts, potential)
    return finite_difference(xs, ts, psi_init, matrix)

def build_matrix(xs, ts, potential):
    num_x = xs.get_num_divisions()
    delta_x = xs.get_delta()
    delta_t = ts.get_delta()
    matrix = np.zeros((num_x, num_x), dtype=complex)
    matrix[0,0] = 1.0
    matrix[-1,-1] = 1.0
    for n in xrange(1,num_x-1):
        for i in xrange(num_x):
            if i==n:
                matrix[n,i] = potential[i] + 2/delta_x**2 - 1j/delta_t
            elif abs(i-n) == 1:
                matrix[n,i] = -1/delta_x**2
    return matrix

def finite_difference(xs, ts, psi_init, matrix):
    num_x = xs.get_num_divisions()
    num_t = ts.get_num_divisions()
    delta_t = ts.get_delta()
    psi = np.zeros((num_t,num_x), dtype=complex)
    psi[0,:] = psi_init
    # boundary conditions
    psi[:,0] = 0
    psi[:,-1] = 0
    for n in xrange(num_t-1):
        psi[n+1,:] = np.linalg.solve(matrix, -1j*psi[n,:]/delta_t)
        psi[n+1,0] = 0
        psi[n+1,-1] = 0
        psi[n+1,:] = WaveFunction.normalize(psi[n+1,:])
    return psi