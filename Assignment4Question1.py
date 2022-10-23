# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 12:08:13 2022

@author: JAV9028
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import json
import colorlover as cl
import plotly.offline as py
import plotly.graph_objs as go
from plotly import tools
import dash
import dash_core_components as dcc
import dash_html_components as html

url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)

#Question2
    
    
trees_q2 = trees[['spc_common','status','boroname']]
trees_q2['spc_common'].fillna('Unknown',inplace = True)

#create columns that specify tree status
for statusq2 in set(trees_q2['status']):
    trees_q2[statusq2] = np.where(trees_q2['status']==statusq2,1,0)
    
trees_q2 = pd.DataFrame(trees_q2.groupby(['boroname','spc_common']).sum())
trees_q2.head()

#find out boroughs
boroughsq2 = list(set(trees['boroname']))

trace_list_q2 =[]

#create plot titles
borough_listq2 = list(map(lambda x: str(x), boroughsq2))

trees_q2 = trees[['spc_common','health','boroname','steward']]

trees_q2['spc_common'].fillna('Unknown',inplace = True)
trees_q2.dropna(inplace = True)
trees_q2[['steward','health']] = trees_q2[['steward','health']].apply(lambda x : pd.factorize(x)[0])
trees_q2_cor = pd.DataFrame(trees_q2.groupby(['boroname','spc_common']).corr())
fig_q2 = tools.make_subplots(rows=1, cols=len(boroughsq2), subplot_titles=tuple(borough_listq2))



boroughsq2 = list(set(trees_q2['boroname']))
plantsq2 = list(set(trees_q2['spc_common']))

for boroughq2 in boroughsq2:
    traceq2 = go.Bar(
            x = list(trees_q2.loc[boroughq2].index),
            y = list(trees_q2_cor.loc[boroughq2]['steward'][::2])
            )
    trace_list_q2 += [traceq2]

for i in range(len(boroughsq2)):
    fig_q2.append_trace(trace_list_q2[i], 1, i+1) 


        
fig_q2['layout'].update(showlegend=False,height=500, width=1400, title='Proportion of Trees in Good, Fair and Poor Conditions')




app = dash.Dash()

colors = {
    'background': '#ffffff',
    'text': '#111111'
}



app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Question #2',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Correlation between stewardsand health of trees', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    
    html.Div([
        dcc.Graph(figure=fig_q2, id='my-figure')
])
    ])


if __name__ == '__main__':
   app.run_server(debug=True) 