import pandas as pd
import numpy as np
import re
import plotly as py
import matplotlib.pyplot as plt
import pandas.plotting as pp
import seaborn as sns
import plotly.express as px


data = pd.read_csv('DataWeierstrass.csv',sep=';',encoding='utf8')
data_scatter = data.groupby(['professor', 'lecture']).mean()
data['prof'] = pd.to_numeric(data['professor'].str.split("f", n = 1, expand = True) [1])
data['lec'] = pd.to_numeric(data['lecture'].str.split("lecture", n = 1, expand = True) [1])
data = data.groupby(['professor', 'lecture']).mean()


#Method 1
'''Task a: Visualize given data with a scatterplot matrix.'''
pp.scatter_matrix(data_scatter,
                  diagonal = 'kde',alpha = 0.2, marker = 'o')
plt.show()


# Task 2
fig = px.parallel_coordinates(data,
                              color="overall impression",
                              dimensions = ['prof', 'lec', 'participants', 'professional expertise','motivation','clear presentation','overall impression' ],
                              labels={"prof": "professor", "lec": "lecture", "participants": "participants","professional expertise": "professional expertise", "motivation": "motivation","clear presentation":"clear presentation","overall impression":"overall impression"},
                             color_continuous_midpoint=2)
fig.show()
plt.show()

