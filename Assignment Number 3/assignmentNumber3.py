import numpy as np
import matplotlib.pyplot as plt
import csv

def ReadData(filename):
    arrayn = list(csv.reader(open(filename, "r"), delimiter=","))
    arrayn = np.array(arrayn, dtype=np.float32)
    arrayn = np.flip(arrayn , axis = 0)
    return arrayn

band1 =ReadData("i170b1h0_t0.txt")
band2 =ReadData("i170b2h0_t0.txt")
band3 =ReadData("i170b3h0_t0.txt")
band4 =ReadData("i170b4h0_t0.txt")

min_val = band2.min()
max_val = band2.max()
mean_val = band2.mean()
var_val = band2.var()
print("Min", min_val)
print("Max", max_val)
print("Mean", mean_val)
print("Var", var_val)

# Histogram
index = np.argmax(np.max(band2, axis = 1))
fig_profile = plt.figure()
plt.plot(band2[index], label = 'Line number {}'.format(index+1))
plt.xlabel("X")
plt.ylabel("Values")
plt.title("Profile line for the maximum value")
fig_profile.savefig("Rescaled")

# Resaling
rescale = np.zeros((500,500),dtype = 'int')
for i in range(band2.shape[0]):
    for j in range(band2.shape[1]):
        rescale[i][j] = round(((band2[i][j] - min_val) / (max_val - min_val)) * 255)


fig_rescale = plt.figure()
plt.imshow(rescale , cmap = 'gray')
plt.xlabel("X")
plt.ylabel("Y")
plt.title ("Rescaled")
fig_rescale.savefig("Rescaled")

# Histogram equalised for band1
arr1 , indices = np.unique(band1 , return_inverse = True)
arr2 = np.zeros(len(arr1))
for i in indices :
	if arr1[i] in arr1 :
		arr2[i] += 1

arr3 = np.zeros(len(arr1))
cumulative = np.zeros(len(arr1))
final = np.zeros(len(arr1))
sum_val = 0
for i , v in enumerate(arr2) :
	if arr2[i] > 0 :
		arr3[i] = v / (500 * 500)
	else :
		arr3[i] = 0
	
	sum_val += arr3[i]
	cumulative[i] = sum_val
	final[i] = cumulative[i] * 255
	
	cdf255_all = final[indices]
	band1_final = np.ndarray.reshape(cdf255_all , (500 , 500))

fig_band1 = plt.figure()
plt.imshow(band1_final , cmap = 'gray')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Band1")
fig_band1.savefig("Histogram_Equalised Band_1")
plt.colorbar()

# Histogram equalised for band1
arr1 , indices = np.unique(band2 , return_inverse = True)
arr2 = np.zeros(len(arr1))
for i in indices :
	if arr1[i] in arr1 :
		arr2[i] += 1

arr3 = np.zeros(len(arr1))
cumulative = np.zeros(len(arr1))
final = np.zeros(len(arr1))
sum_val = 0
for i , v in enumerate(arr2) :
	if arr2[i] > 0 :
		arr3[i] = v / (500 * 500)
	else :
		arr3[i] = 0
	
	sum_val += arr3[i]
	cumulative[i] = sum_val
	final[i] = cumulative[i] * 255
	
	cdf255_all = final[indices]
	band2_final = np.ndarray.reshape(cdf255_all , (500 , 500))

fig_band2 = plt.figure()
plt.imshow(band2_final , cmap = 'gray')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Band2")
plt.colorbar()
fig_band2.savefig("Histogram_Equalised_Band_2")

# Histogram equalised for band1
arr1 , indices = np.unique(band3 , return_inverse = True)
arr2 = np.zeros(len(arr1))
for i in indices :
	if arr1[i] in arr1 :
		arr2[i] += 1

arr3 = np.zeros(len(arr1))
cumulative = np.zeros(len(arr1))
final = np.zeros(len(arr1))
sum_val = 0
for i , v in enumerate(arr2) :
	if arr2[i] > 0 :
		arr3[i] = v / (500 * 500)
	else :
		arr3[i] = 0
	
	sum_val += arr3[i]
	cumulative[i] = sum_val
	final[i] = cumulative[i] * 255
	
	cdf255_all = final[indices]
	band3_final = np.ndarray.reshape(cdf255_all , (500 , 500))

fig_band3 = plt.figure()
plt.imshow(band3_final , cmap = 'gray')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Band3")
plt.colorbar()
fig_band3.savefig("Histogram_Equalised_Band_3")

# Histogram equalised for band1
arr1 , indices = np.unique(band4 , return_inverse = True)
arr2 = np.zeros(len(arr1))
for i in indices :
	if arr1[i] in arr1 :
		arr2[i] += 1

arr3 = np.zeros(len(arr1))
cumulative = np.zeros(len(arr1))
final = np.zeros(len(arr1))
sum_val = 0
for i , v in enumerate(arr2) :
	if arr2[i] > 0 :
		arr3[i] = v / (500 * 500)
	else :
		arr3[i] = 0
	
	sum_val += arr3[i]
	cumulative[i] = sum_val
	final[i] = cumulative[i] * 255
	
	cdf255_all = final[indices]
	band4_final = np.ndarray.reshape(cdf255_all , (500 , 500))

fig_band4 = plt.figure()
plt.imshow(band4_final , cmap = 'gray')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Band4")
plt.colorbar()
fig_band4.savefig("Histogram_Equalised_Band_4")

# Combined Band
Merged = np.zeros((500,500,3), dtype = 'int')
for i in range(500):
    for j in range(500):
        red =  int(round(band4_final[i][j]))
        green =  int(round(band3_final[i][j]))
        blue =  int(round(band1_final[i][j]))
        color_list = [red, green, blue]
        Merged[i][j] = color_list

fig_merged = plt.figure()
plt.imshow(Merged)
plt.xlabel("X")
plt.ylabel("Y")
plt.title ("Merged")
plt.colorbar()
fig_merged.savefig("Merged")
plt.show()