####################################################################################################
# Author : Tejas Ravindra Dhawale
# Student Id : 6882910
####################################################################################################
# References used :
#https://stackoverflow.com/questions/25505674/python-matplotlib-add-colorbar
#https://stackoverflow.com/questions/8931268/using-colormaps-to-set-color-of-line-in-matplotlib
#https://pythonforundergradengineers.com/quiver-plot-with-matplotlib-and-jupyter-notebooks.html
#https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.15-Quiver-and-Stream-Plots/
#https://mplcursors.readthedocs.io/en/stable/examples/nondraggable.html
####################################################################################################

# Importing necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib as mpl
import mplcursors


# Reading the data set
data = pd.read_csv('field2.irreg.txt', sep=" " , header=None , skiprows= 6)
# Adding labels to column to display value when hovering over it
data.columns = ["x","y","z","dx","dy","dz"]


# Normalize and set color
cmap = plt.cm.coolwarm
cNorm  = colors.Normalize(vmin=0, vmax=1)
scalarMap = cmx.ScalarMappable(norm=cNorm,cmap=cmap)


# Calculating length of the arrow to determine the color values
data["length"] = np.hypot(data["dx"] , data["dy"])


# Plot Figure
fig = plt.figure()
ax  = fig.add_axes([0.1, 0.1, 0.7, 0.85])
ax.quiver(data["x"],data["y"],data["dx"],data["dy"],color = scalarMap.to_rgba(data["length"]) ,pivot='mid' , scale = 8  )
ax.set_title('Vector Field Visualization')
ax.set_aspect('equal')
ax.set_xlabel('X Equivalent of Vectors')
ax.set_ylabel('Y Equivalent of Vectors')
ax.use_sticky_edges = False


# Setting the Color Bar and it labels
cax = fig.add_axes([0.80, 0.10, 0.02, 0.85])
cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=cNorm , ticks=[0, 0.5, 1])
cax.set_yticklabels(['Low', 'Medium','High'])
cb.set_label('Flow Velocity')


# Interactive Plotting
# Displaying values on Hovering. You can check values of the tip of the arrow
mplcursors.cursor( hover=True ).connect(
    "add" ,lambda sel : sel.annotation.set_text("x = {:.2f}, y = {:.2f} , dx = {:.2f} , dy = {:.2f} , length = {:.2f}"
																		   .format(
                                                                           data["x"][sel.target.index],
                                                                           data["y"][sel.target.index],
                                                                           data["dx"][sel.target.index],
                                                                           data["dy"][sel.target.index],
                                                                           data["length"][sel.target.index]))
    )


# Save Figure
fig.savefig('Assignment1.png' , bbox_inches="tight" , dpi=150)
plt.show()
