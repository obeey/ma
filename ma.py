import os, sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
from numpy import loadtxt
import time
from functools import reduce
#import tushare as ts

#jhjt = ts.get_hist_data('000732', start='2016-01-04')

readFile = open('h:/Analysis/Data/SZ#000732.txt')
lines = readFile.readlines()
lines = lines[:-1]
readFile.close()

#lineLen = (len(lines)*2)//3
lineLen = len(lines) //10
lines = lines[-lineLen:]
date,op,hi,lo,cl,vol,tv = np.loadtxt(lines, unpack=True,
                                                #delimiter=' ',
                                                converters={0:mdates.bytespdate2num('%Y/%m/%d')},
                                                skiprows = 2)
def runningMean(x, N):
    y = np.zeros((len(x),))
    for ctr in range(len(x)-N+1):
         y[ctr+N-1] = np.sum(x[ctr:(ctr+N)])
    return y/N

def maSlope(x):
    y = np.zeros((len(x),))
    for p in range(1,len(x)):
        if 0 == x[p-1]:
            y[p] = 0
        else:
            y[p] = (x[p] - x[p-1])/x[p-1]

    return y*10000

def bsPointGet(x):
    buy = False

    transication = []
    oDate = []
    oOp = []
    oStyle = []
    if 5 > len(x):
        return

    for p in range(4, len(x)):
        if False == buy and x[p]>x[p-1] and x[p-1] < x[p-2] and x[p-2] < x[p-3]:
            #print('B: ' , lines[p]) #, date[p] , op[p], cl[p], lo[p], hi[p])
            #transication.append(['B', date[p], op[p]], 'gs')
            oDate.append(date[p])
            oOp.append(op[p])
            oStyle.append('r^')
            buy = True
            continue

        if x[p-1] > 0 and x[p-1] > x[p] and True == buy:
            #print('S: '  , lines[p]) #, date[p] , op[p], cl[p], lo[p], hi[p])
            #transication.append(['S', date[p], op[p]], 'b^')
            oDate.append(date[p])
            oOp.append(op[p])
            oStyle.append('rs')
            buy = False

    return oDate,oOp,oStyle

def bsOutput():
    ma5 = runningMean(cl, 5)
    slope = maSlope(ma5)
    return bsPointGet(slope)

def graphRawFX():
    ma5 = runningMean(cl, 5)
#    ma5 = runningMean(jhjt['close'], 5)
    slope = maSlope(ma5)

    fig=plt.figure(figsize=(70,10))
    ax1 = plt.subplot2grid((40,40), (0,0), rowspan=40, colspan=40)
    ax2 = ax1.twinx()
    ax1.plot(date, cl, 'o')
    ax1.plot(date, ma5, 'k')
    trDate,trOp,trStyle = bsPointGet(slope)
    for p in range(len(trDate)):
        ax1.plot(trDate[p], trOp[p], trStyle[p])

    zeroLine = np.zeros(len(date))
    ax2.plot(date, zeroLine, linewidth=2.0, color='y')
    ax2.plot(date, slope, 'k', color='g')
    ax2.plot(date, slope, 'o', color='g')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.grid(True)
    for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    fig.tight_layout()
    plt.show()



if __name__ == '__main__':
    #bsOutput()
    graphRawFX()
