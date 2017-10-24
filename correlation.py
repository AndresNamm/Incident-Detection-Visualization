import matplotlib.pyplot as plt
import pandas
import numpy
from pandas import scatter_matrix

from scipy.stats.stats import pearsonr
#filename = "/home/andres/Documents/Thesis/6september/Andres_Source/Convert Coordinates & Plot Results (Python)/resultana.csv"
filename = "/home/andres/Documents/Thesis/6september/Andres_Source/Convert Coordinates & Plot Results (Python)/corr.csv"
f = open(filename)
lines = f.readlines()

names = lines[0].split(",")
names[-1]=names[-1].strip("\n")
print(names)

data = pandas.read_csv (filename, header=0)
correlations = data.corr()
print(correlations)
# plot correlation matrix
# fig = plt.figure()
# ax = fig.add_subplot(111)
# cax = ax.matshow(correlations, vmin=-1, vmax=1)
# fig.colorbar(cax)
# ticks = numpy.arange(0,9,1)
# print(ticks)
# ax.set_xticks(ticks)
# ax.set_yticks(ticks)
# ax.set_xticklabels(names)
# ax.set_yticklabels(names)
# plt.show()
#
# scatter_matrix(data)
# plt.show()

data.plot(kind='box', subplots=True, layout=(2,4), sharex=False, sharey=False)
plt.show()