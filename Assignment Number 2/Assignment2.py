import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
import matplotlib.patches as pat
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib as mpl
import cufflinks as cf
from plotly.offline import download_plotlyjs
from plotly.offline import init_notebook_mode
from plotly.offline import plot , iplot
#cf.go_offline()
import plotly.io as pio
pio.renderers.default = 'png'

#############################################################################
def profile_line(img):
    # img[256].iplot(title='Profile Line for a single row')
    fig1 = plt.figure(figsize= (10,5), dpi=100)
    ax1 = plt.axes()
    plt.xlim(0 , 512)
    plt.ylim(0 , val_max)
    plt.xlabel("X")
    plt.ylabel("Value")
    plt.title("Profile line for 256th record")
    ax1.plot(img.iloc[256] , label = 'line 256')
    ax1.legend(loc = 1)
#############################################################################
def mean_value(img , sum):
    # img_mean = 0
    # for i in range (np.shape(img)[0]):
    #     for j in range (np.shape(img)[1]):
    #         img_mean = img_mean + img[j].loc[i]
    # return img_mean/(np.shape(img)[0]*np.shape(img)[1])
    return sum/(np.shape(img)[0]*np.shape(img)[1])
#############################################################################
def variance_value(img , img_mean) :
    img_variance = 0
    for i in range(np.shape(img)[0]) :
        for j in range(np.shape(img)[1]) :
            img_variance = img_variance + pow((img[j].loc[i] - img_mean) , 2)
    
    return img_variance / (np.shape(img)[0] * np.shape(img)[1])
#############################################################################
def histogram(img) :
    fig2 = plt.figure(figsize= (10,5), dpi=100)
    ax2 = plt.axes()
    # plt.xlim(0 , 512)
    # plt.ylim(0 , val_max)
    plt.xlabel("X")
    plt.ylabel("Value")
    plt.title("Histogram using Line")
    sns.distplot(img , rug = False , hist = False)
#############################################################################
def linear_transf(img) :
    linear_transf = pd.DataFrame(0 , index = range(np.shape(img)[0]) , columns = range(np.shape(img)[1]))
    for i in range(np.shape(img)[0]) :
        for j in range(np.shape(img)[1]) :
            linear_transf[j].iloc[i] = int(((img[j].iloc[i] - val_min) / (val_max - val_min)) * 255)
    
    fig3 = plt.figure()
    ax3 = plt.axes()
    plt.title("Linear Transformation of the Data Set")
    im = ax3.imshow(linear_transf)
    fig3.colorbar(im)
#############################################################################
# Reading the data set
ct = []
sum = 0
val_min = 0
val_max = 0
# with open('slice150.raw' , 'rb') as f :
#     while True :
#         data = f.read(2)
#         if not data :
#             break
#         val = int.from_bytes(data , byteorder='little')
#         ct.append(val)
#         # Calculating the sum to determine mean
#         sum = sum + val
#         # Calculating the minimum value in the data set without using built function
#         if val < val_min:
#             val_min = val
#         # Calculating the maximum value in the data set without using built function
#         if val > val_max:
#             val_max = val
        

# Converting the data set into an array
# img = pd.DataFrame(np.asanyarray(ct).reshape(512 , 512))

####################################################################################
# Profile Line through line 256 of the data set
# profile_line(img)
####################################################################################
# Mean Value
# img_mean = mean_value(img , sum)
# print("Mean is:",img_mean)
####################################################################################
#Variance Value
# print("Variance:", variance_value(img , img_mean))
####################################################################################
# Histogram
# histogram(img)
####################################################################################
#Linear transformation
# linear_transf(img)
####################################################################################
#
# mat = np.array([[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]])
# filter = np.array([[1,1],[1,1]])
# box = np.zeros((3,3) , dtype = 'int' )
mat = np.array([[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,7,7,7,1,1],[1,1,7,7,7,1,1],[1,1,7,7,7,1,1],[1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1]])
filter = np.array([[1,1,1],[1,1,1],[1,1,1]])
box = np.zeros((5,5),dtype = 'int')
median = np.zeros((5,5),dtype = 'int')
mean_filter = []
for i in range((np.shape(mat)[0] - np.shape(filter)[0]) + 1) :
    for j in range((np.shape(mat)[1] - np.shape(filter)[1]) + 1) :
        for a in range(np.shape(filter)[0]) :
            for b in range(np.shape(filter)[1]) :
                box[i][j] = box[i][j] + (mat[i + a][j + b] * filter[a][b])
                mean_filter.append(mat[i + a][j + b] * filter[a][b])
        # box[i][j] = int(box[i][j]/(np.shape(filter)[0]*np.shape(filter)[1]))
        box[i][j] = round(box[i][j]/(np.shape(filter)[0]*np.shape(filter)[1]))
        mean_filter.sort()
        median[i][j] = mean_filter[4]
        mean_filter = []
print("-------------------------------------")
print(box)
print("-------------------------------------")
print(median)



#plt.imshow(linear_transf , cmap = 'gray')



# print("Done")
# plt.show()




