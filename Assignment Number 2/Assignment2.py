#############################################################################
# Author : Tejas Ravindra Dhawale
# Student Id : 6882910
#############################################################################
# References:
# https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
# https://people.revoledu.com/kardi/tutorial/Regression/nonlinear/NonLinearTransformation.htm
# https://theailearner.com/tag/log-transformation/
# https://www.youtube.com/watch?v=qSTv_m-KFk0&list=PLZbbT5o_s2xq7LwI2y8_QtvuXZedL6tQU&index=21
# https://medium.com/@george.seif94/a-tour-of-the-top-5-sorting-algorithms-with-python-code-43ea9aa02889
#############################################################################
# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import math as m
from collections import OrderedDict
#############################################################################
# Sorting algorithm for Median filter (# Reference for sorting)
# Implementing Merge sort
def sorting(median_list):

    if len(median_list) <= 1 :
        return median_list
    mid = len(median_list) // 2
    # Perform merge_sort recursively on both halves
    left , right = sorting(median_list[:mid]) , sorting(median_list[mid :])
    # Merge each side together
    return merge(left , right , median_list.copy())


def merge(l , r , merged) :
    lc , rc = 0 , 0
    while lc < len(l) and rc < len(r) :
        # Sort each one and place into the result
        if l[lc] <= r[rc] :
            merged[lc + rc] = l[lc]
            lc += 1
        else :
            merged[lc + rc] = r[rc]
            rc += 1
    for lc in range(lc , len(l)) :
        merged[lc + rc] = l[lc]
    for rc in range(rc , len(r)) :
        merged[lc + rc] = r[rc]
    
    return merged
#############################################################################
def profile_line(img):
    # Profile line through line 256 of the 2D data set
    fig1 = plt.figure(figsize= (10,5), dpi=100)
    ax1 = plt.axes()
    plt.xlim(0 , 512)
    plt.ylim(0 , val_max)
    plt.xlabel("X")
    plt.ylabel("Value")
    plt.title("Profile line for 256th record")
    ax1.plot(img[256] , label = 'line 256')
    ax1.legend(loc = 1)
    # ax1.set_aspect('equal')
    fig1.savefig('Profile_Line.png' , bbox_inches = "tight" , dpi = 150)
#############################################################################
def mean_value(img , sum):
    return sum/(np.shape(img)[0]*np.shape(img)[1])
#############################################################################
def variance_value(img , img_mean) :
    img_variance = 0
    for i in range(np.shape(img)[0]) :
        for j in range(np.shape(img)[1]) :
            img_variance = img_variance + pow((img[i][j] - img_mean) , 2)
    
    return img_variance / (np.shape(img)[0] * np.shape(img)[1])
#############################################################################
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
#############################################################################
# Both linear and nonlinear transformations could have been combined into a single
# function but to make it modular and reusable separating the functions
def linear_transf(img , img_dimensions) :
    # Implementing linear function
    linear_transf = np.zeros((img_dimensions[0] , img_dimensions[1]), dtype = 'int')
    for i in range(img_dimensions[0]) :
        for j in range(img_dimensions[1]) :
            # S = T(R) = ((R - Rmin)/(Rmax - Rmin))* Smax
            linear_transf[i][j] = round(((img[i][j] - val_min) / (val_max - val_min)) * 255)
    fig3 = plt.figure( )
    ax3 = plt.axes()
    plt.title("Linear Transformation")
    im3 = ax3.imshow(linear_transf)
    # ax3.tick_params(labelbottom=True, labeltop=True, labelleft=True, labelright=True,
    #                  bottom=True, top=True, left=True, right=True)
    ax3.set_aspect('equal')
    fig3.savefig('Linear_Transformation.png' , bbox_inches = "tight" , dpi = 150)
    return linear_transf

#############################################################################
def nonlinear_trans(img , img_dimensions):
    # Implementing non-linear function sigmoid
    nonlinear_transf = np.zeros((img_dimensions[0] , img_dimensions[1]),dtype = 'int')
    for i in range(img_dimensions[0]) :
        for j in range(img_dimensions[1]) :
            nonlinear_transf[i][j] = round(m.sqrt(img[i][j]+1))
    fig4 = plt.figure( )
    ax4 = plt.axes()
    plt.title("Non Linear Transformation")
    im4 = ax4.imshow(nonlinear_transf)
    ax4.set_aspect('equal')
    fig4.savefig('Nonlinear_Transformation.png' , bbox_inches = "tight" , dpi = 150)
#############################################################################
# Smoothing filter
def smoothing(img , img_dimensions ):
    # Reference - Deeplizard link
    # If the image is of size N x N , and the filter is of size F x F
    # then the resulting image after convolution will be (N-F+1) x (N-F+1)
    filter = np.ones((11,11), dtype = 'int')
    filter_dimensions = [np.shape(filter)[0] , np.shape(filter)[1]]
    boxcar = np.zeros(((img_dimensions[0] - filter_dimensions[0] + 1),
                       (img_dimensions[1] - filter_dimensions[1] + 1)),dtype = 'int')
    median = np.zeros(((img_dimensions[0] - filter_dimensions[0] + 1),
                       (img_dimensions[1] - filter_dimensions[1] + 1)),dtype = 'int')
    median_list = []
    # i and j are for the dimensions of the image
    for i in range((img_dimensions[0] - filter_dimensions[0]) + 1) :
        for j in range((img_dimensions[1] - filter_dimensions[1]) + 1) :
            # a and b are for the dimensions of the filter
            for a in range(filter_dimensions[0]) :
                for b in range(filter_dimensions[1]) :
                    # sum all the values of element wise multiplication between image and filter
                    boxcar[i][j] = boxcar[i][j] + (img[i + a][j + b] * filter[a][b])
                    # Appending the values to median list
                    median_list.append(img[i + a][j + b] * filter[a][b])
            # Final convolved result for one filter x image element wise multiplication(divide by filter dimension)
            boxcar[i][j] = round(boxcar[i][j] / (filter_dimensions[0] * filter_dimensions[1]))
            # Sort the median list to determine the median value
            median_list = sorting(median_list)
            # Median value(middle of the list)
            median[i][j] = median_list[int(len(median_list) / 2)]
            # clear median list . median_list.clear()
            median_list = []
  
    fig5 = plt.figure()
    ax5 = plt.axes()
    plt.title("Boxcar Filter")
    im5 = ax5.imshow(boxcar)
    ax5.set_aspect('equal')
    fig5.savefig('Boxcar_Filter.png' , bbox_inches = "tight" , dpi = 150)
    
    fig6 = plt.figure()
    ax6 = plt.axes()
    plt.title("Median Filter")
    im6 = ax6.imshow(median)
    ax6.set_aspect('equal')
    fig6.savefig('Median_Filter.png' , bbox_inches = "tight" , dpi = 150)
#############################################################################
def histogram_bar(hist) :
    # Plotting histogram as a bar graph plot
    fig7 = plt.figure()
    ax7 = plt.axes()
    plt.xlabel("Value")
    plt.ylabel("Count")
    plt.title("Histogram as a bar plot")
    plt.bar(list(hist.keys()),list(hist.values()))
    fig7.savefig('Histogram_Bar.png' , bbox_inches = "tight" , dpi = 150)
#############################################################################
# Reading the data set
ct = []
sum = 0
val_min = 0
val_max = 0
hist = {}
with open('slice150.raw' , 'rb') as f :
    while True :
        data = f.read(2)
        if not data :
            break
        val = int.from_bytes(data , byteorder='little')
        ct.append(val)
        # Calculating the sum to determine mean
        sum = sum + val
        # Calculating the minimum value in the data set without using built function
        if val < val_min:
            val_min = val
        # Calculating the maximum value in the data set without using built function
        if val > val_max:
            val_max = val
        # Determining Histogram without using built in function
        # Saving the values in dictionary as key value pairs
        if val in hist.keys():
            hist[val] += 1
        else :
            hist[val] = 1

# Converting the data set into an array
img = np.asanyarray(ct).reshape(512 , 512)
img_dimensions = [np.shape(img)[0], np.shape(img)[1]]
###################################################################################
#Profile Line through line 256 of the data set
profile_line(img)
###################################################################################
#Mean Value
img_mean = mean_value(img , sum)
print("Mean is:",img_mean)
###################################################################################
#Variance Value
print("Variance:", variance_value(img , img_mean))
###################################################################################
# Histogram as a bar plot
histogram_bar(hist)
###################################################################################
# Histogram as a line graph
histogram_line(hist)
###################################################################################
#Linear transformation
img_rescaled = linear_transf(img , img_dimensions)
###################################################################################
# Non linear Transformation
nonlinear_trans(img_rescaled, img_dimensions)
###################################################################################
# Smoothing filter
smoothing(img_rescaled , img_dimensions )
###################################################################################
# Show figure
plt.show()


