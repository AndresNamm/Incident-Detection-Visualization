import numpy as np
s = np.random.poisson(100, 100000)
k = np.random.poisson(40,10000)
t = np.concatenate((s, k), axis=0)
import matplotlib.pyplot as plt
count , bins, ignored = plt.hist(t ,14, normed=False)


plt.show()
