import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

#############################################################################
def profile_line(img):
    img[256].iplot(title='Profile Line for a single row')
#############################################################################
def mean_value(img):
    img_mean = 0
    for i in range (np.shape(img)[0]):
        for j in range (np.shape(img)[1]):
            img_mean = img_mean + img[j].loc[i]
    return img_mean/(np.shape(img)[0]*np.shape(img)[1])
#############################################################################
def variance_value(img , img_mean) :
    img_variance = 0
    for i in range(np.shape(img)[0]) :
        for j in range(np.shape(img)[1]) :
            img_variance = img_variance + pow((img[j].loc[i] - img_mean) , 2)
    
    return img_variance / (np.shape(img)[0] * np.shape(img)[1])
#############################################################################
def linear_transf(img) :
    linear_transf = pd.DataFrame(0 , index = range(np.shape(img)[0]) , columns = range(np.shape(img)[1]))
    min_data = img.min().min()
    max_data = img.max().max()
    for i in range(np.shape(img)[0]) :
        for j in range(np.shape(img)[1]) :
            linear_transf[j].iloc[i] = int(((img[j].iloc[i] - min_data) / (max_data - min_data)) * 255)
    
    return linear_transf
#############################################################################






ct = []
with open('slice150.raw' , 'rb') as f :
    while True :
        data = f.read(2)
        if not data :
            break
        # img = np.append(img,data)
        ct.append(int.from_bytes(data , byteorder='little'))

# Converting the data set into an array
img = pd.DataFrame(np.asanyarray(ct).reshape(512 , 512))

linear_transf = linear_transf(img)
print(linear_transf.head())





plt.imshow(linear_transf)




plt.show()




