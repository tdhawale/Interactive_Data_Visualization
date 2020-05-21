#############################################################################
# Author : Tejas Ravindra Dhawale
# Student Id : 6882910
#############################################################################
# References:
#############################################################################
import numpy as np
import matplotlib.pyplot as plt
import math as m
from collections import OrderedDict
import pandas as pd
# arr = np.array(['a5','a4','a3','a2','a1','b5','b4','b3','b2','b1','c5','c4','c3','c2','c1']).reshape(3,5)
# # arr = np.array([1,2,3,4,5])
# arr_reversed = np.flip(arr , 1)
# print(arr)
# print(arr_reversed.reshape(3,5))
import re
def profile_line(band):
    # Profile line through line 256 of the 2D data set
    pl = np.argmax(np.max(band, axis=1))
    fig1 = plt.figure(figsize= (10,5), dpi=100)
    ax1 = plt.axes()
    # plt.xlim(0 , 500)
    # plt.ylim(0 , band.max())
    plt.xlabel("X")
    plt.ylabel("Values")
    plt.title("Profile line for maximum valueof the data set ")
    ax1.plot(band[pl] , label = 'Line 256')
    ax1.legend(loc = 1)
    fig1.savefig('Profile_Line.png' , bbox_inches = "tight" , dpi = 150)
    
def histogram_line(hist) :
    fig2 = plt.figure(figsize= (10,5), dpi=100)
    ax2 = plt.axes()
    plt.xlabel("Value")
    plt.ylabel("Count")
    plt.title("Histogram as a line graph")
    # Sorting the dictionary based on the Key values to represent the histogram as line plot(clear view)
    hist = OrderedDict(sorted(hist.items()))
    keys = np.array(np.fromiter(hist.keys() , dtype = float))
    vals = np.array(np.fromiter(hist.values() , dtype = float))
    plt.plot(keys , vals)
    fig2.savefig('Histogram_LineGraph.png' , bbox_inches = "tight" , dpi = 150)
    
def nonlinear_trans(band):
    band_dimensions = [np.shape(band)[0], np.shape(band)[1]]
    # Implementing non-linear function sigmoid
    nonlinear_transf = np.zeros((band_dimensions[0] , band_dimensions[1]),dtype = 'int')
    for i in range(band_dimensions[0]) :
        for j in range(band_dimensions[1]) :
            nonlinear_transf[i][j] = round(m.sqrt(band[i][j]+1))
    fig4 = plt.figure( )
    ax4 = plt.axes()
    plt.title("Non Linear Transformation")
    im4 = ax4.imshow(nonlinear_transf , cmap = 'gray')
    ax4.set_aspect('equal')
    fig4.savefig('Nonlinear_Transformation.png' , bbox_inches = "tight" , dpi = 150)
    cb4 = fig4.colorbar( mappable = im4 , orientation = 'vertical' , label = 'Density of Tissue', ticks =
    [nonlinear_transf.min(),nonlinear_transf.max()])
    # cb4.ax.set_yticklabels(['{}{}{}'.format('Low(', nl_min,')'),'{}{}{}'.format('High(', nl_max,')')])
    cb4.ax.set_yticklabels(['Low','High'])
    cb4.set_label('Density of Tissue')
    # return linear_transf
    
def hist_equalisation(band , hist , name):
    band_dimensions = [np.shape(band)[0] , np.shape(band)[1]]
    hist = OrderedDict(sorted(hist.items()))
    r = np.fromiter(hist.keys() , dtype = float)
    p = np.fromiter(hist.values() , dtype = float)
    pr = [val/(band_dimensions[0] * band_dimensions[1]) for val in p ]
    # Calculating cdf
    sum = 0
    cdf = []
    for val in pr:
        sum = sum + val
        cdf.append(sum)
    # Calculating s = cdf*(L-1) here l is 500*500 = 250000
    cdf255 = np.asarray([val*255 for val in cdf])
    HistogramEqualied = np.zeros((band_dimensions[0],band_dimensions[0]))
    for i in range(band_dimensions[0]) :
        for j in range(band_dimensions[1]) :
            # Finding the index of element in r
            ItemIndex = np.where( r == band[i][j])
            # Finding the equalized value in cdf255
            HistogramEqualied[i][j] = cdf255[ItemIndex]
    fig5 = plt.figure()
    ax5 = plt.axes()
    plt.title("Histogram Equalised"+name)
    plt.imshow(HistogramEqualied , cmap = 'gray')
    plt.gca().invert_yaxis()
    x = [10 , 150 , 290 , 430]
    y = [60 , 180 , 300 , 380 , 420]
    xlabels = ['5h45m' , '5h30m' , '5h15m' , '5h00m']
    ylabels = ['-15:00' , '-12:00' , '-9:00' ,'-6:00']
    ylabels_minor = ['5h45m']
    # plt.xticks(x , xlabels)
    # plt.yticks(y , ylabels1)
    # plt.yticks(y , ylabels2)
    ax5.set_xticks([10 , 150 , 290 , 430])
    ax5.set_yticks([60 , 180 , 300 , 420 ])
    ax5.set_yticks([380], minor = True)
    ax5.set_xticklabels(xlabels)
    ax5.set_yticklabels(ylabels)
    ax5.set_yticklabels(ylabels_minor , minor = True)
    plt.grid()
    ax5.set_aspect('equal')
    
    
    
def hist_combine(band_r , band_g , band_b):
    combine_data = np.zeros((500,500,3), dtype = 'int')
    for i in range(500):
        for j in range(500):
            red = int(round(band_r[i][j]))
            green = int(round(band_g[i][j]))
            blue = int(round(band_b[i][j]))
            color = [red,green,blue]
            combine_data[i][j] = color
            
def readfile(filename , cal):
    # cal specifies whether to calculate min max mean variance and histogram
    data = []
    i = 0
    hist = {}
    orion = np.zeros((500 ,500) , dtype = np.float64)
    with open(filename , 'r') as f:
        fdata = f.read()
        
    fdata = fdata.replace('"' , "").split("\n")

    # So now we have entire file data in fdata. Now we split the file data at \n
    # fdata contains 500 rows with each row as a string consisting of 500 values
    for i in range(len(fdata)-1):
        data = fdata[i].split(",")
        for j in range(len(data)):
            orion[i][j] = float(data[j])
            if orion[i][j] in hist.keys() :
                hist[orion[i][j]] += 1
            else :
                hist[orion[i][j]] = 1
    
    # orion = np.flip(orion , axis = 1)  # horizontal flip
    # orion = np.flip(orion , axis = 0)  # Vertically  flip
    if cal == True :
        return orion , orion.mean() , orion.var() , orion.min(), orion.max() , hist
    else:
        return orion , hist

band1, hist1  = readfile('i170b1h0_t0.txt' , False )
band2 , mean2 , var2 , min2 , max2 , hist2 = readfile('i170b2h0_t0.txt', True)
band3 , hist3 = readfile('i170b3h0_t0.txt', False)
band4 , hist4 = readfile('i170b4h0_t0.txt', False)

#######################################################################################
# Profile Line
profile_line(band2)
# Histogram
# histogram_line(hist2)
# Linear Transformation
# nonlinear_trans(band2)
# Histogram Equaliation
hist_equalisation(band1 , hist1 , 'Band 1')
# hist_equalisation(band2 , hist2, 'Band 2')
# hist_equalisation(band3 , hist3, 'Band 3')
# hist_equalisation(band4 , hist4, 'Band 4')

plt.show()


