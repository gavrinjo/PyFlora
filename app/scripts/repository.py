
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# from ipychart import Chart
from random import randint
from datetime import datetime
from app.models import Gauge, Pot, SensorMeasurements
from app.repo import Weather
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


class SensorSim():

    def __init__(self, pot, last_measurement) -> None:
        self.pot = pot
        self.last_measurement = last_measurement
        self.columns = self.get_columns(self.pot)

    
    def get_columns(self, pot: object) -> list:
            columns = []
            for column in db.inspect(pot).attrs:
                if column.key.endswith("status"):
                    columns.append(column.key)
            return columns

    def get_ref_values(self, query: object) -> tuple:
        min_array = [getattr(x, 'min_value') for x in query] # array of minimum values column
        min_median = np.median(min_array) # median value of minimum values array, used as minimum value
        max_array = [getattr(x, 'max_value') for x in query] # array of maximum values column
        max_median = np.median(max_array) # median value of maximum values array, used as maximum value
        std_value = np.ceil(np.median([min_median, max_median])) # median value over minimum and maximum values, used as standard value
        off_value = np.ceil(std_value * 0.1) # 10% of median value over minimum and maximum values, used as offset value
        # ref_values = {
        #     'min_val': min(min_array),
        #     'max_val': max(max_array),
        #     'std_val': std_value,
        #     'off_val': off_value
        # }
        return min(min_array), max(max_array), std_value, off_value


    def get_random_value(self, value: int, min_value: int, max_value: int, offset: int) -> int:

        if value <= min_value:
            mi = min_value
        else:
            mi = value - offset

        if value >= max_value:
            mx = max_value
        else:
            mx = value + offset

        return randint(mi, mx)
    

    def generate(self) -> object:
        new_measurement = SensorMeasurements()

        # columns = self.get_columns(self.pot.id)
        
        for column in self.columns:
            column = column[:column.find('_')]
            query = Gauge.query.filter_by(name=column).all()
            if getattr(self.pot, column + '_status'):
                if column != 'temperature':
                    ds = self.get_ref_values(query) # dataset
                    if self.last_measurement is None:
                        sensor = self.get_random_value(ds[2], ds[0], ds[1], ds[3])
                    else:
                        sensor = self.get_random_value(getattr(self.last_measurement, column), ds[0], ds[1], ds[3])
                else:
                    sensor = round(float(Weather('Zagreb').temperature['value']))
            else:
                sensor = None
            setattr(new_measurement, column, sensor)
        
        new_measurement.measured = datetime.utcnow()
        new_measurement.pot = self.pot

        return new_measurement


