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
    hist = {}       # Dictionary to store the values and count for histogram
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
            # Creating dictionary element for histogram without using library
            if orion[i][j] in hist.keys() :
                hist[orion[i][j]] += 1
            else :
                hist[orion[i][j]] = 1
    orion = np.flip(orion , axis = 0)  # Vertically flip according to data characteristics
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
    band = band.reshape(size,size)
    # Getting the index of the row which has the maximum value
    pl = np.argmax(np.max(band, axis=1))
    fig1 = plt.figure(figsize= (10,6), dpi=100)
    ax1 = plt.axes()
    ax1.margins(x=0)
    plt.xlabel("X")
    plt.ylabel("Values \n (Measured in log scale)")
    plt.title("Profile line for maximum value of the data set ")
    ax1.plot(band[pl] , label = 'Record {}'.format(pl+1))
    ax1.legend(loc = 1)
    plt.yscale('log')
    fig1.savefig('Profile_Line.png' , bbox_inches = "tight" , dpi = 150)

################################################################################################
# Histogram
################################################################################################
def histogram_line(hist) :
    # Zoom in the output to observe the difference
    fig2 = plt.figure(figsize= (10,7), dpi=100)
    ax2 = plt.axes()
    plt.xlabel("Value \n (Measured in log scale)")
    plt.ylabel("Count \n (Measured in log scale)")
    plt.title("Histogram as a line graph")
    # Sorting the dictionary based on the Key values to represent the histogram as line plot(clear view)
    hist = OrderedDict(sorted(hist.items()))
    keys = np.array(np.fromiter(hist.keys() , dtype = float))
    vals = np.array(np.fromiter(hist.values() , dtype = float))
    plt.plot(keys , vals)
    plt.xscale('log')
    plt.yscale('log')
    fig2.savefig('Histogram.png' , bbox_inches = "tight" , dpi = 150)

################################################################################################
# Rescale between 0 to 255
################################################################################################
def rescale(band, log_min , log_max):
    import matplotlib.patches as mpatches
    rescaled = []
    
    for i in range(len(band)):
        if band[i] > 0:
            log = m.log(band[i])
            if log > 0 :
                val = (log - log_min) / (log_max - log_min) * 255
                rescaled.append(val)
    #0.92, -0.05
    # Reshaping data to 500x500
    rescaled = np.asarray(rescaled).reshape(size , size)
    fig4 = plt.figure(figsize= (8,7) )
    ax4 = plt.axes()
    plt.title("Rescaled Image")
    im4 = ax4.imshow(rescaled , cmap = 'gray' , label = ["Max" , "Min"])
    ax4.set_aspect('equal')
    max_patch = mpatches.Patch(color = 'white' , label = 'Maximum Value {}'.format(rescaled.max()))
    min_patch = mpatches.Patch(color = 'black' , label = 'Min Value {}'.format(rescaled.min()))
    plt.legend(handles = [max_patch, min_patch], bbox_to_anchor=(0.82, -0.08) , fancybox=True, shadow=True,
               facecolor="gray", fontsize='small',  ncol=2)
    plt.xlabel("X Values")
    plt.ylabel("Y Values")
    fig4.savefig('Rescaled.png' , bbox_inches = "tight" , dpi = 150)

################################################################################################
# Histogram Equalization
################################################################################################
def hist_equalisation(band , hist , name):
    hist = OrderedDict(sorted(hist.items()))
    # Calculating data values
    r = list(np.fromiter(hist.keys() , dtype = float))
    # Calculating absolute occurance
    p = list(np.fromiter(hist.values() , dtype = float))
    # Calculating relative occurrence
    pr = [val / (size * size) for val in p]
    # Calculating Cumulative Density Function and final output cdf*255
    sum = 0
    cdf = []
    cdf255 = []
    for val in pr:
        sum = sum + val
        cdf.append(sum)
        cdf255.append(sum*255)
    
    HistogramEqualised = []
    for i in range(len(band)):
        # Find the index of element in r
        ItemIndex = r.index(band[i])
        HistogramEqualised.append(int(round(cdf255[ItemIndex])))

    HistogramEqualised = np.asarray(HistogramEqualised)
    HistogramEqualised = HistogramEqualised.reshape(500,500)
    fig5 = plt.figure()
    ax5 = plt.axes()
    plt.title("Histogram Equalised "+name)
    plt.xlabel("X Values")
    plt.ylabel("Y Values")
    im5 = ax5.imshow(HistogramEqualised , cmap = 'gray')
    plt.grid()
    ax5.set_aspect('equal')
    cb5 = fig5.colorbar(mappable = im5 , orientation = 'vertical' , label = 'Emission Measurements' , ticks =
    [HistogramEqualised.min() , HistogramEqualised.max()])
    cb5.ax.set_yticklabels(['Low({})'.format(HistogramEqualised.min()) , 'High({})'.format(HistogramEqualised.max())])
    fig5.savefig('Histogram {}.png'.format(name) , bbox_inches = "tight" , dpi = 150)
    return HistogramEqualised

################################################################################################
# Combine Histogram for color image
################################################################################################
def hist_combine(band_r , band_g , band_b):
    # Reshaping the bands for faster computations
    band_r = band_r.reshape(size*size,)
    band_g = band_g.reshape(size*size,)
    band_b = band_b.reshape(size*size,)
    combine_data = np.zeros((size*size,3), dtype = 'int')
    for i in range(size*size):
        red = int(round(band_r[i]))
        green = int(round(band_g[i]))
        blue = int(round(band_b[i]))
        color = [red, green,blue]
        combine_data[i] = color
    combine_data = combine_data.reshape((size,size,3))
    
    fig6 = plt.figure()
    ax6 = plt.axes()
    plt.title("Combined band")
    im6 = ax6.imshow(combine_data)
    ax6.set_aspect('equal')
    plt.xlabel("X Values")
    plt.ylabel("Y Values")
    fig6.savefig('Combined.png' , bbox_inches = "tight" , dpi = 150)
    
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
rescale(band2 , m.log(band2.min()) if band2.min() > 0 else 0, m.log(band2.max()) if band2.max() > 0 else 0 )
# Histogram Equalization
equalised_band1 = hist_equalisation(band1 , hist1, 'Band 1 (Wavelength 12 µm)')
equalised_band2 = hist_equalisation(band2 , hist2, 'Band 2 (Wavelength 25 µm)')
equalised_band3 = hist_equalisation(band3 , hist3, 'Band 3 (Wavelength 60 µm)')
equalised_band4 = hist_equalisation(band4 , hist4, 'Band 4 (Wavelength 100 µm)')
hist_combine(equalised_band4 , equalised_band3 , equalised_band1)

plt.show()
