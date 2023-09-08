
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# from ipychart import Chart

from app.models import Gauge


def plot_config(fig: go.Figure, df: pd.DataFrame):



    columns = list(set(df.columns.tolist()) - set(['id', 'pot_id', 'measured']))
    data = []
    for column in columns:
        if column == 'temperature':
            yy = df[column]
        else:
            yy = mapper(df[column], column)['mapped_value']
        data.append(go.Scatter(x=df['measured'], y=yy, name=column, line_shape='spline')) # np.interp(df[column], [0,100], [1,10])
    fig.add_traces(data)
    fig.update_xaxes(type='category', showticklabels=False)
    # fig.update_yaxes(
    #     ticktext=[1,2,3,4,5,6,7,8,9,56],
    #     tickvals=np.interp(df[column], [0,100], [1,10]),
    #     tick0=0, dtick=1)
    fig.update_traces(mode="lines+markers", hovertemplate=None)
    fig.update_layout(
        hovermode="x unified",
        template='plotly_white',
        legend=dict(
            orientation="h",
            # entrywidth=70,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        width=900
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)




# dataset = {
#   'labels': ['Data 1', 'Data 2', 'Data 3', 'Data 4', 
#              'Data 5', 'Data 6', 'Data 7', 'Data 8'],
#   'datasets': [{'data': [14, 22, 36, 48, 60, 90, 28, 12]}]
# }
# options= {
#         'scales': {
#             'y': {
#                 'ticks': {
#                     # Include a dollar sign in the ticks
#                     'callback': '''function(value, index, values) {
#                         return '$' + value;
#                     }'''
#                 }
#             }
#         },
#     }

# mychart = Chart(data=dataset, kind='line', options=options)
# print(mychart.get_html_template())


def mapper(value, column: str):
    miv = Gauge.query.filter_by(name=column).order_by(Gauge.min_value).first()
    mav = Gauge.query.filter_by(name=column).order_by(Gauge.max_value.desc()).first()
    av = Gauge.query.filter_by(name=column, eiv=5).first()
    if column not in ['sunlight', 'temperature']:
        mapped_value = np.interp(value, [miv.min_value, mav.max_value], [1, 10])
    elif column == 'sunlight':
        mapped_value = np.interp(np.log10(value)*20, [np.log10(miv.min_value)*20, np.log10(mav.max_value)*20], [1, 10])

    
    return {
        'mapped_value': mapped_value,
        'value': value,
        'min_value': miv.min_value,
        'max_value': mav.max_value,
        'avg_value': (av.min_value + av.max_value) / 2
    }
