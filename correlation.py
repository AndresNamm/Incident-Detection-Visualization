import matplotlib.pyplot as plt
import pandas
import numpy
from pandas import scatter_matrix

from scipy.stats.stats import pearsonr
#filename = "/home/andres/Documents/Thesis/6september/Andres_Source/Convert Coordinates & Plot Results (Python)/resultana.csv"
#filename = "/home/andres/Documents/Thesis/6september/Andres_Source/Convert Coordinates & Plot Results (Python)/corr2.csv"
#filename = "/home/andres/Documents/Thesis/6september/Andres_Source/Convert Coordinates & Plot Results (Python)/gps_sp.csv"
#filename = "/home/andres/Documents/Thesis/6september/Andres_Source/Convert Coordinates & Plot Results (Python)/gps.csv"
#filename = "/home/andres/Documents/Thesis/6september/Andres_Source/Convert Coordinates & Plot Results (Python)/gps-cols-removed.csv"
filename = "/home/andres/Documents/Thesis/6september/Andres_Source/Convert Coordinates & Plot Results (Python)/GPS_fisker.csv"

import plotly.offline as py
import plotly.figure_factory as ff
f = open(filename)
lines = f.readlines()


font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 15}

plt.rc('font', **font)

names = lines[0].split(",")
names[-1]=names[-1].strip("\n")
print(names)
data = pandas.read_csv (filename, header=0,usecols=names)

#
#
# names = [str(i) +" "+ names[i] for i in range(len(names))]
# print(names)
# correlations = data.corr()
# print(correlations)
#
#
# # plot correlation matrix
# fig = plt.figure()
# ax = fig.add_subplot(111)
# cax = ax.matshow(correlations, vmin=-1, vmax=1)
# fig.colorbar(cax)
# ticks = numpy.arange(0,len(names),1)
# print(ticks)
# ax.set_xticks(ticks)
# ax.set_yticks(ticks)
# ax.set_yticklabels(names)
# ax.set_xticklabels([str(i) for i in range(len(names))])
# plt.show()
# plotly.offline.plot()
#plot scatter matrix
#
# pandas.plotting.scatter_matrix(data)
# plt.show()
# fig2 = ff.create_scatterplotmatrix(data)
# py.plot(fig2, filename='Basic Scatterplot Matrix')

# fisker
#data.interpolate()
data.plot(kind='box', subplots=True, layout=(int(len(names)/2),int(int(len(names))/(len(names)/2))), sharex=False, sharey=False)
plt.show()