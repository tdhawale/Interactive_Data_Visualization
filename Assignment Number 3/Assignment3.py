################################################################################################
# Author : Tejas Ravindra Dhawale
# Student Id : 6882910
################################################################################################
# References:
################################################################################################
import numpy as np
import matplotlib.pyplot as plt
import math as m
from collections import OrderedDict
################################################################################################
# Read File
################################################################################################
def readfile(filename , cal) :
    # cal specifies whether to calculate min max mean variance and histogram
    data = []
    i = 0
    sum = 0
    hist = {}
    orion = np.zeros((size , size) , dtype = np.float64)
    with open(filename , 'r') as f :
        fdata = f.read()
    
    fdata = fdata.replace('"' , "").split("\n")
    
    # So now we have entire file data in fdata. Now we split the file data at \n
    # fdata contains 500 rows with each row as a string consisting of 500 values
    for i in range(len(fdata) - 1) :
        data = fdata[i].split(",")
        for j in range(len(data)) :
            orion[i][j] = float(data[j])
            
            # To calculate the mean without using library
            sum = sum + orion[i][j]
            if orion[i][j] in hist.keys() :
                hist[orion[i][j]] += 1
            else :
                hist[orion[i][j]] = 1
    orion = np.flip(orion , axis = 0)  # Vertically  flip
    if cal == True :
        return orion.reshape(((size * size) ,))  , orion.min() , orion.max() , hist , sum
    else :
        return orion.reshape(((size * size) ,)) , hist

################################################################################################
# Calculate Mean
################################################################################################
def mean_value(size , sum):
    return sum/(size*size)


################################################################################################
# Calculate Variance
################################################################################################
def variance_value(band , mean) :
    band_variance = 0
    for i in range(band.shape[0]) :
              band_variance = band_variance + pow((band[i] - mean) , 2)
    return band_variance / (size * size)


################################################################################################
# Profile Line
################################################################################################
def profile_line(band):
    # Profile line through line which contains the maximum value
    band = band.reshape(500,500)
    # Getting the index of the row which has the maximum value
    pl = np.argmax(np.max(band, axis=1))
    fig1 = plt.figure(figsize= (10,5), dpi=100)
    ax1 = plt.axes()
    plt.xlabel("X")
    plt.ylabel("Values")
    plt.title("Profile line for maximum value of the data set ")
    ax1.plot(band[pl] , label = 'Record {}'.format(pl))
    ax1.legend(loc = 1)
    fig1.savefig('Profile_Line.png' , bbox_inches = "tight" , dpi = 150)

################################################################################################
# Histogram
################################################################################################
def histogram_line(hist) :
    fig2 = plt.figure(figsize= (10,5), dpi=100)
    ax2 = plt.axes()
    plt.xlabel("Value")
    plt.ylabel("Count")
    plt.title("Histogram as a line graph")
    # Sorting the dictionary based on the Key values to represent the histogram as line plot(clear view)
    hist = OrderedDict(sorted(hist.items()))
    # keys = np.array(np.fromiter(hist.keys() , dtype = float))
    keys = np.array(np.fromiter(hist.keys() , dtype = int))
    # vals = np.array(np.fromiter(hist.values() , dtype = float))
    vals = np.array(np.fromiter(hist.values() , dtype = int))
    plt.plot(keys , vals)
    fig2.savefig('Histogram.png' , bbox_inches = "tight" , dpi = 150)


################################################################################################
# Rescale between 0 to 255 using non linear transformation
################################################################################################
def nonlinear_trans(band, min , max):
    import matplotlib.patches as mpatches
    
    log_min = m.log(min) if min > 0 else 0
    log_max = m.log(max) if max > 0 else 0
    # 1D nonlinear array for storing non-linear data
    # nonlinear_transf = np.zeros((len(band),))
    nonlinear_transf = []
    
    for i in range(len(band)):
        if band[i] > 0:
            log = m.log(band[i])
            if log > 0 :
                # nonlinear_transf[i] = (log - log_min) / (log_max - log_min) * 255
                val = (log - log_min) / (log_max - log_min) * 255
                nonlinear_transf.append(val)
                

    # Reshaping data to 500x500
    nonlinear_transf = np.asarray(nonlinear_transf).reshape(500 , 500)
    # nonlinear_transf = nonlinear_transf.reshape((500,500))
    fig4 = plt.figure( )
    ax4 = plt.axes()
    plt.title("Rescaled Image")
    im4 = ax4.imshow(nonlinear_transf , cmap = 'gray' , label = ["Max" , "Min"])
    ax4.set_aspect('equal')
    # ax4.legend((nonlinear_transf.min(),nonlinear_transf.max()),("Min","Max"))
    # cb4 = fig4.colorbar( mappable = im4 , orientation = 'vertical' , label = 'Intensity', ticks =
    # [nonlinear_transf.min(),nonlinear_transf.max()])
    # cb4.ax.set_yticklabels(['Low','High'])
    # bbox_to_anchor = (1 , -0.05) ncol=2,
    max_patch = mpatches.Patch(color = 'white' , label = 'Maximum Value {}'.format(nonlinear_transf.max()))
    min_patch = mpatches.Patch(color = 'black' , label = 'Min Value {}'.format(nonlinear_transf.min()))
    plt.legend(handles = [max_patch, min_patch], bbox_to_anchor=(0.92, -0.05) , fancybox=True, shadow=True,
               facecolor="gray", fontsize='small',  ncol=2)
    fig4.savefig('Rescaled.png' , bbox_inches = "tight" , dpi = 150)


################################################################################################
# Histogram Equalization
################################################################################################
def hist_equalisation(band , hist , name):
    # band_dimensions = [500, 500]
    hist = OrderedDict(sorted(hist.items()))
    # r = np.fromiter(hist.keys() , dtype = float)
    r = list(np.fromiter(hist.keys() , dtype = float))
    # p = np.fromiter(hist.values() , dtype = float)
    p = list(np.fromiter(hist.values() , dtype = float))
    # pr = [val/(band_dimensions[0] * band_dimensions[1]) for val in p ]
    pr = [val / (size * size) for val in p]
    # Calculating cdf
    sum = 0
    cdf = []
    cdf255 = []
    for val in pr:
        sum = sum + val
        cdf.append(sum)
        cdf255.append(sum*255)
    # Calculating s = cdf*(L-1) here l is 500*500 = 250000
    # cdf255 = np.asarray([val*255 for val in cdf])
    # HistogramEqualied = np.zeros(((band_dimensions[0]*band_dimensions[0]),)
    # for i in range(band_dimensions[0]) :
    #     for j in range(band_dimensions[1]) :
    #         # Finding the index of element in r
    #         ItemIndex = np.where( r == band[i][j])
    #         # Finding the equalized value in cdf255
    #         HistogramEqualied[i][j] = cdf255[ItemIndex]
    # HistogramEqualised = np.zeros(((500*500),))
    HistogramEqualised = np.zeros(((500*500),), dtype = 'int')
    # HistogramEqualised = np.zeros((500,500),dtype = 'int')
    for i in range(len(band)):
        # Find the index of element in r
        ItemIndex = r.index(band[i])
        # ItemIndex = np.where( r == band[i])
        HistogramEqualised[i] = round(cdf255[ItemIndex])

    HistogramEqualised = HistogramEqualised.reshape(500,500)
    fig5 = plt.figure()
    ax5 = plt.axes()
    plt.title("Histogram Equalised "+name)
    im5 = ax5.imshow(HistogramEqualised , cmap = 'gray')
    # plt.gca().invert_yaxis()
    # x = [10 , 150 , 290 , 430]
    # y = [60 , 180 , 300 , 380 , 420]
    # xlabels = ['5h45m' , '5h30m' , '5h15m' , '5h00m']
    # ylabels = ['-15:00' , '-12:00' , '-9:00' ,'-6:00']
    # ylabels_minor = ['5h45m']
    # ax5.set_xticks([10 , 150 , 290 , 430])
    # ax5.set_yticks([60 , 180 , 300 , 420 ])
    # ax5.set_yticks([380], minor = True)
    # ax5.set_xticklabels(xlabels)
    # ax5.set_yticklabels(ylabels)
    # ax5.set_yticklabels(ylabels_minor , minor = True)
    plt.grid()
    ax5.set_aspect('equal')
    cb5 = fig5.colorbar(mappable = im5 , orientation = 'vertical' , label = 'Intensity' , ticks =
    [HistogramEqualised.min() , HistogramEqualised.max()])
    cb5.ax.set_yticklabels(['Low' , 'High'])
    fig5.savefig('Histogram {}.png'.format(name) , bbox_inches = "tight" , dpi = 150)
    return HistogramEqualised


################################################################################################
# Combine Histogram for color image
################################################################################################
def hist_combine(band_r , band_g , band_b):
    # combine_data = np.zeros((500,500,3), dtype = 'int')
    # for i in range(500):
    #     for j in range(500):
    #         red = int(round(band_r[i][j]))
    #         green = int(round(band_g[i][j]))
    #         blue = int(round(band_b[i][j]))
    #         color = [red,green,blue]
    #         combine_data[i][j] = color
    
    band_r = band_r.reshape(500*500,)
    band_g = band_g.reshape(500*500,)
    band_b = band_b.reshape(500*500,)
    combine_data = np.zeros((500*500,3), dtype = 'int')
    for i in range(500*500):
        red = int(round(band_r[i]))
        green = int(round(band_g[i]))
        blue = int(round(band_b[i]))
        color = [red, green,blue]
        combine_data[i] = color
    combine_data = combine_data.reshape((500,500,3))
    
    fig6 = plt.figure()
    ax6 = plt.axes()
    plt.title("Combined band")
    im6 = ax6.imshow(combine_data)
    ax6.set_aspect('equal')
    cb6 = fig6.colorbar(mappable = im6 , orientation = 'vertical' , label = 'Intensity' , ticks =
    [combine_data.min() , combine_data.max()])
    cb6.ax.set_yticklabels(['Low' , 'High'])
    fig6.savefig('Combined.png' , bbox_inches = "tight" , dpi = 150)
    print("combined")
    print(combine_data[2 :4 , 2 :4])
################################################################################################
size = 500
# Reading the data set
band1, hist1  = readfile('i170b1h0_t0.txt' , False )
band2 , min2 , max2 , hist2 , sum = readfile('i170b2h0_t0.txt', True)
band3 , hist3 = readfile('i170b3h0_t0.txt', False)
band4 , hist4 = readfile('i170b4h0_t0.txt', False)

################################################################################################
# Mean , Max , Min , Variance Value
print("The min value in band 2 is: ", band2.min())
print("The max value in band 2 is: ", band2.max())
mean = mean_value(size,sum)
print("The mean value in band 2 is: ", mean)
print("The variance value in band 2 is: ", variance_value(band2, mean))
################################################################################################
# Profile Line
profile_line(band2)
# Histogram
histogram_line(hist2)
# Linear Transformation
nonlinear_trans(band2 , band2.min(), band2.max())
# Histogram Equaliation
equalised_band1 = hist_equalisation(band1 , hist1 , 'Band 1')
equalised_band2 = hist_equalisation(band2 , hist2, 'Band 2')
equalised_band3 = hist_equalisation(band3 , hist3, 'Band 3')
equalised_band4 = hist_equalisation(band4 , hist4, 'Band 4')
hist_combine(equalised_band4 , equalised_band3 , equalised_band1)

print("band1")
equalised_band1 = np.asarray(equalised_band1.reshape(500,500))
equalised_band2 = np.asarray(equalised_band2.reshape(500,500))
equalised_band3 = np.asarray(equalised_band3.reshape(500,500))
equalised_band4 = np.asarray(equalised_band4.reshape(500,500))
print(equalised_band1[2:4 , 2:4])
print("band2")
print(equalised_band2[2:4 , 2:4])
print("band3")
print(equalised_band3[2:4 , 2:4])
print("band4")
print(equalised_band4[2:4 , 2:4])

plt.show()










































# import pandas as pd
# # arr = np.array(['a5','a4','a3','a2','a1','b5','b4','b3','b2','b1','c5','c4','c3','c2','c1']).reshape(3,5)
# # # arr = np.array([1,2,3,4,5])
# # arr_reversed = np.flip(arr , 1)
# # print(arr)
# # print(arr_reversed.reshape(3,5))
# import re
