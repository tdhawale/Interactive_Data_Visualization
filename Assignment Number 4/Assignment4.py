################################################################################################
# Author : Tejas Ravindra Dhawale
# Student Id : 6882910
################################################################################################
# References:
################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import seaborn as sns
import numpy as np
import cufflinks as cf
from plotly.offline import download_plotlyjs
# from plotly.offline import init_notebook_mode
from plotly.offline import plot , iplot
import plotly.express as px
import plotly as py
import plotly.graph_objects as go
from pandas.plotting import parallel_coordinates
#  To use plotly we need to initate it for each notebook
# init_notebook_mode(connected=True)
# sns.set()
# To use cufflinks as offline we call the below function
# cf.go_offline()
################################################################################################
# Read File
################################################################################################
# data = pd.read_csv('DataWeierstrass.csv', delimiter=";")
# print(data.tail())
# data = pd.read_csv('DataWeierstrass.csv', delimiter=";").groupby(['professor', 'lecture'], as_index = False)
data_parallel = pd.read_csv('DataWeierstrass.csv', delimiter=";")
data = pd.read_csv('DataWeierstrass.csv', delimiter=";").groupby(['professor', 'lecture'], as_index = False)
data = data.mean()
# scatter_matrix( data)
# sns.scatterplot(data)
# g = sns.PairGrid(data ,height = 3)
# g.map_diag(sns.kdeplot)
# g.map_offdiag(plt.scatter, linewidths=1, edgecolor="w", s=40)
# g.add_legend()


#text = [professor , lecture]
# Working
fig_scatter = px.scatter_matrix(data, color="professor" , symbol = 'lecture' , labels={'participants':'Participants',
                                                          'professional expertise' : ' Professional Expertise',
                                                          'motivation' : 'Motivation',
                                                          'clear presentation' : 'Presentation',
                                                          'overall impression': 'Overall Impression'} ,
                        title="Scatter matrix for Weierstrass-Price",
                        dimensions = ['participants', 'professional expertise',
                                                                         'motivation', 'clear presentation',
                                                                         'overall impression'])
fig_scatter.update_traces(diagonal_visible=False)
fig_scatter.show()
# Till here

# # print(data.head())
# parallel_coordinates(data, 'professor') #'professor','lecture',


# Working
# fig2 = px.parallel_coordinates(data_parallel  ,dimensions = ['participants',
#                                                              'professional expertise','motivation',
#                                                              'clear presentation','overall impression'])
# fig2.show()


# print(data['participants'].values)
# print(len(data['participants'].values))
# print(type(data['participants'].values))
# print(type(data['participants'].values[0]))

prof_keys = list(data['professor'])
prof_keys_unique = np.unique(prof_keys)
prof_vals_unique =  [int(x[4:]) for x in prof_keys_unique]
prof_vals =  [int(x[4:]) for x in prof_keys]

lecture_keys = list(data['lecture'])
lecture_vals =  [int(x[7:]) for x in lecture_keys]

# print(prof_keys)
# print(prof_keys_unique)
# print(prof_vals)
# print(lecture_keys)
# print(lecture_vals)

participants =  list(data['participants'].values)
professional_expertise =  list(data['professional expertise'].values)
motivation =  list(data['motivation'].values)
clear_presentation =  list(data['clear presentation'].values)
overall_impression =  list(data['overall impression'].values)

# , , tickvals = lecture_vals, ticktext = lecture_keys
fig_pocord = go.Figure(data= go.Parcoords(
        line = dict(color = prof_vals ,
                colorscale = px.colors.sequential.Plasma) ,
        dimensions = list([dict(label = 'Professor',tickvals = prof_vals_unique, ticktext = prof_keys_unique,
                                values = prof_vals),
                           dict(label = 'Lecture' , values = lecture_vals),
                           dict(label = 'Participants', values = participants),
                           dict(label = 'Professional Expertise', values = professional_expertise),
                           dict(label = 'Motivation', values = motivation),
                           dict(label = 'Clear Presentation', values = clear_presentation),
                           dict(label = 'Overall Impression', values = overall_impression)])
    )
)

fig_pocord.update_layout(
    # title={ 'text': "Parallel coordinates plot for Weierstrass-Price", 'y':0.9,  'x':0.5, 'xanchor': 'center',
    #         'yanchor': 'top'},
    title = 'Parallel coordinates plot for Weierstrass-Price',
    plot_bgcolor = 'white',
    paper_bgcolor = 'white'
)
fig_pocord.show()


#
# # Profile values
# prof_keys = list(data['professor'])
# prof_val =  [int(x[4:]) for x in prof_keys]
#
# lecture_keys = list(data['lecture'])
# lecture_vals =  [int(x[4:]) for x in lecture_keys]
#
#
#
# fig_pc = go.Figure(data=
#     go.Parcoords(
#         dimensions = list([
#             dict(range = [min(prof_val),max(prof_keys)],
#                  tickvals = prof_keys,
#                  label = 'Professor', values = prof_val),
#             dict(range = [min(lecture_vals),max(lecture_keys)],
#                  tickvals = lecture_keys,
#                  label = 'Professor', values = lecture_vals),
#         ])
#     )
# )

# fig_pc.update_layout(
#     plot_bgcolor = 'white',
#     paper_bgcolor = 'white'
# )
#
# fig_pc.show()
#
plt.show()