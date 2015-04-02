import numpy as np
import math
import cmath
import matplotlib.pyplot as plt

# builds the matrix needed to solve the TDSE
def buildMatrix(numX, numT, V, deltaX, deltaT):
	array = np.zeros((numX,numT), dtype=complex)
	matrix = np.matrix(array)
	matrix[0,0] = 1
	matrix[-1,-1] = 1

	for n in range(1,numT-1):
		for i in range(numX):
			if i==n:
				matrix[n,i] = V[i] - 2/deltaX**2 - 1j/deltaT
			elif abs(i-n) == 1:
				matrix[n,i] = 1/deltaX**2

	return matrix

# solves for psi using the finite difference algorithm
def finiteDifference(numX, numT, deltaX, deltaT, matrix, psi_init):
	psi = np.zeros((numX,numT), dtype=complex)
	psi[:,0] = psi_init

	# boundary conditions
	psi[0,:] = 0
	psi[-1,:] = 0

	return psi

# constructs the initial wave function
def wavePacket(x):
	return math.exp(-(x)**2) + 0J

# run parameters
a=0
b=1
ti=0
tf=1
deltaX=.1
deltaT=.1

# matrix dimensions
numX = int((b-a)/deltaX)
numT = int((tf-ti)/deltaT)

# initialize the wavefunction
psi_init = np.arange(a,b,deltaX)

for i in range(numX):
	psi_init[i] = psi_init[i] + 0J

psi_init2 = map(wavePacket,psi_init)


# normalize the wavefunction
normfactor = 0;
for i in range(numX):
	normfactor+=abs(psi_init[i])**2

psi_init[:] /= normfactor

# set the potential
V = np.zeros(numX)

# build the matrix
mat = buildMatrix(numX,numT,V,deltaX,deltaT)
print mat

# solve for psi
psi = finiteDifference(numX, numT, mat, deltaX, deltaT, psi_init)
print psi


