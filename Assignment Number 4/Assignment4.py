################################################################################################
# Author : Tejas Ravindra Dhawale
# Student Id : 6882910
################################################################################################
# References: https://plotly.com/python/splom/
# https://plotly.com/python/parallel-coordinates-plot/
################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
################################################################################################
# Read File
################################################################################################
# Read file and group by based on professor and lecture (since there are multiple values for same professor- lecture
#                                                         combination)
data = pd.read_csv('DataWeierstrass.csv', delimiter=";").groupby(['professor', 'lecture'], as_index = False)
data = data.mean()

# Interactive Scatter Plot (screen size may distort the labels, make sure the resolution is correct)
fig_scatter = px.scatter_matrix(data, color="professor" ,symbol="professor", labels={'participants':'Participants',
                                                          'professional expertise' : ' Professional Expertise',
                                                          'motivation' : 'Motivation',
                                                          'clear presentation' : 'Presentation',
                                                          'overall impression': 'Overall Impression'} ,
                        title="Scatter matrix for Weierstrass-Price",
                        dimensions = ['participants', 'professional expertise',
                                                                         'motivation', 'clear presentation',
                                                                         'overall impression'])
# fig_scatter.update_traces(diagonal_visible=False)
fig_scatter.show()


# Since you cannot plot nominal data in parallel coordinates, converting the nominal data (professor and lecture)
# into quantitative value which will be plotted
prof_keys = list(data['professor'])
prof_keys_unique = np.unique(prof_keys)                    # for ticks on the plot need unique values
prof_vals_unique =  [int(x[4:]) for x in prof_keys_unique] # quantitative value for unique ticks
prof_vals =  [int(x[4:]) for x in prof_keys]

# quantitative value for lecture
lecture_keys = list(data['lecture'])
lecture_vals =  [int(x[7:]) for x in lecture_keys]


participants =  list(data['participants'].values)
professional_expertise =  list(data['professional expertise'].values)
motivation =  list(data['motivation'].values)
clear_presentation =  list(data['clear presentation'].values)
overall_impression =  list(data['overall impression'].values)

# Interactive Parallel Coordinates
fig_pocord = go.Figure(data= go.Parcoords(
        line = dict(color = overall_impression , showscale = True,
                    cmax = 6, cmin = 1,
                colorscale = px.colors.diverging.RdYlGn,) ,
        dimensions = list([dict(label = 'Professor',tickvals = prof_vals_unique, ticktext = prof_keys_unique,
                                values = prof_vals),
                           dict(label = 'Lecture' , values = lecture_vals),
                           dict(label = 'Participants', values = participants),
                           dict(label = 'Professional Expertise', values = professional_expertise),
                           dict(label = 'Motivation', values = motivation),
                           dict(label = 'Clear Presentation', values = clear_presentation),
                           dict(label = 'Overall Impression', values = overall_impression, range = [1,6])])
    )
)

fig_pocord.update_layout(
    title = 'Parallel coordinates plot for Weierstrass-Price',
    plot_bgcolor = '#E5E5E5' ,
    paper_bgcolor = '#E5E5E5'
)
fig_pocord.show()
plt.show()