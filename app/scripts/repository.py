
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# from ipychart import Chart
from random import randint
from app.models import Gauge, Pot
from app import db


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


def get_columns(pot):
        columns = []
        for column in db.inspect(pot).attrs:
            if column.key.endswith("status"):
                columns.append(column.key)
        return columns

def get_norm_data(query):

    min_array = [getattr(x, 'min_value') for x in query]
    min_median = np.median(min_array)

    max_array = [getattr(x, 'max_value') for x in query]
    max_median = np.median(max_array)

    avg_value = np.ceil(np.median([min_median, max_median]))

    off_value = np.ceil(avg_value * 0.1)

    return min(min_array), max(max_array), avg_value, off_value

def get_mapped_data(array: tuple):

    pass

def sensor_data_generator():
    query = Gauge.query
    columns = get_columns(Pot.query.get(1))
    columns.remove('temperature_status')
    for column in columns:
        filter_by = query.filter_by(name=column[:column.find('_')]).all()
        ds = get_norm_data(filter_by) # dataset
        print(ds)
        sensor = simulate(ds[2], ds[0], ds[1], ds[3])
        print(sensor)
        print('-'*10)


def simulate(value, min_value, max_value, offset):
    """Randomize and return multi sensor data set

    Returns:
        tuple: Resturns tuple of sensor data in particular order (ph, salinity, moisture)
    """
    # if value is None:
    #     return (value, min_value, max_value)

    # else:
    if value <= min_value:
        mi = min_value
    else:
        mi = value - offset

    if value >= max_value:
        mx = max_value
    else:
        mx = value + offset

    return randint(mi, mx)
