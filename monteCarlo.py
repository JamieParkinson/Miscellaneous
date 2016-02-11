import numpy as np

# Wrapper funcs
genHeight = lambda prev: np.abs(np.random.normal(prev, 0.5)) # keep the new height "near" the previous
uniform = lambda : np.random.rand()
energyChange = lambda h, p: h - p
gibbs = lambda DE: np.exp(-DE)

N_MC_STEPS = 1000000

height = 2*uniform()
avg = 0.0
ACCEPT = False
for i in range(N_MC_STEPS):
	# Online averaging
	avg += (height - avg)/(i+1)

	# Generate new config
	newHeight = genHeight(height)
	DE = energyChange(newHeight, height)

	ACCEPT = DE < 0.0 or uniform() < gibbs(DE)

	height = newHeight if ACCEPT else height

print("<x'> = " + str(avg))

