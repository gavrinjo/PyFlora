
import json
import pandas as pd
import numpy as np
import xmltodict
import plotly.express as px

from requests import get
from contextlib import closing
from random import randint
from datetime import datetime
from plotly.subplots import make_subplots

from flask import current_app
from app.models import Gauge, Plant, Value, Pot, Sensor, Reading
from app import db


class PlotlyLine():
    def __init__(self, pot) -> None:
        self.pot = pot
    
    def data_frame(self, pot: object):
        obj = (
            db.select(Pot.name, Sensor.indicator, Reading.value, Reading.unit, Reading.measured)
            .select_from(Pot)
            .join(Sensor)
            .join(Reading)
            .filter(Pot.id == pot.id)
            .order_by(Reading.measured.desc())
        )
        df = pd.read_sql_query(obj, current_app.config['SQLALCHEMY_DATABASE_URI'])
        return df
    
    def plant_df(self, pot: object):
        obj = (
            db.select(Plant.name, Value.indicator, Value.min_value, Value.max_value, Value.unit)
            .select_from(Plant)
            .join(Value)
            .filter(Plant.id==pot.plant_id)
        )
        df = pd.read_sql_query(obj, current_app.config['SQLALCHEMY_DATABASE_URI']) 
        return df[::-1]
    
    def config(self):
        df = self.data_frame(self.pot)
        fig = px.line(df, x='measured', y='value', custom_data=['unit'], color='indicator', facet_row='indicator')
        fig.update_xaxes(
            type='category',
            showticklabels=False,
            title='',
            showline=True,
            linewidth=1,
            linecolor='lightgrey',
            mirror=True
        )
        fig.update_yaxes(
            matches=None,
            title='',
            ticksuffix = "  ",
            fixedrange=True,
            showline=True,
            linewidth=1,
            linecolor='lightgrey',
            mirror=True
        )
        for i, (indicator, min_val, max_val) in enumerate(zip(self.plant_df(self.pot).indicator, self.plant_df(self.pot).min_value, self.plant_df(self.pot).max_value)):
            fig.add_hrect(
                y0=min_val,
                y1=max_val,
                annotation_text=f'Optimal {indicator} range : {min_val}-{max_val}',
                annotation_position='top left',
                fillcolor='green',
                opacity=.25,
                line_width=0,
                row=i+1,
                col=1
            )
        fig.update_layout(
            height=1600,
            autosize= True,
            hovermode="x unified",
            hoverlabel=dict(
                font_size=12,
                bgcolor='rgba(255,255,255)'
            ),
            template='plotly_white',
            legend=dict(
                orientation="h",
                yanchor="top",
                xanchor="center",
                y=1.05,
                x=0.5
            )
        )
        fig.for_each_trace(lambda t: t.update(hovertemplate='%{y}%{customdata[0]}'))
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        return fig




# class PlotlyLine():

#     def __init__(self, pot: object) -> None:
#         self.pot = pot

#     def pot_df(self, q_object):
#         obj = (
#             db.select(Pot.name, Sensor.indicator, Reading.value, Reading.unit, Reading.measured)
#             .select_from(Pot)
#             .join(Sensor)
#             .join(Reading)
#             .filter(Pot.id == self.pot.id)
#             .order_by(Reading.measured.desc())
#         )
#         df = pd.read_sql_query(obj, current_app.config['SQLALCHEMY_DATABASE_URI'])
#         # df['measured'] = df['measured'].dt.strftime("%d.%m.%Y. %H:%M:%S.%f")
#         return df
    
#     def plant_df(self, q_object):
#         obj = (
#             db.select(Plant.name, Value.indicator, Value.min_value, Value.max_value, Value.unit)
#             .select_from(Plant)
#             .join(Value)
#             .filter(Plant.id==self.pot.plant_id)
#         )
#         df = pd.read_sql_query(obj, current_app.config['SQLALCHEMY_DATABASE_URI']) 
#         return df

#     # def get_measured_data(self, pot: object, N=10):
#     #     df = pd.read_sql_query(db.select(SensorMeasurements), current_app.config['SQLALCHEMY_DATABASE_URI']) 
#     #     df = df.sort_values(by=['measured'], ascending=False)[:N]
#     #     df = df[df['pot_id']==pot.id]
#     #     return df

#     def config(self):
#         # df = self.data_frame(self.query_obj)
#         pot_df = self.pot_df(self.pot)
#         plant_df = self.plant_df(self.pot)
#         sensors = pot_df.indicator.unique()
#         # df = self.get_measured_data(self.pypot, N=20)
#         fig = make_subplots(rows=6, cols=1, shared_xaxes=True, vertical_spacing=0.02) # , shared_yaxes='all')
#         # plant = Plant.query.get(self.pypot.plant_id)

#         for i, sensor in enumerate(sensors):
#             plant_min_val = plant_df.loc[plant_df['indicator']== sensor.capitalize()]['min_value'].values[0]
#             plant_max_val = plant_df.loc[plant_df['indicator']== sensor.capitalize()]['max_value'].values[0]
#             # min_value, max_value = plant_df.getattr(plant, column).split(';')
#             text = [f'{sensor.capitalize()} : {val}' for val in pot_df.loc[pot_df['indicator']== sensor]['value']]
#             fig.add_scatter(
#                 x=pot_df['measured'],
#                 y=pot_df.loc[pot_df['indicator']== sensor]['value'],
#                 line_shape='linear',
#                 # line_color=sensors,
#                 mode='lines',#+markers',
#                 name=sensor.capitalize(),
#                 hovertext=text,
#                 hoverinfo='x + text',
#                 row=i+1, col=1
#             )
#             fig.add_hrect(
#                 y0=plant_min_val,
#                 y1=plant_max_val,
#                 annotation_text=f'Optimal {sensor} range : {plant_min_val}-{plant_max_val}',
#                 annotation_position='top left',
#                 # fillcolor=sensors,
#                 opacity=.25,
#                 line_width=0,
#                 row=i+1,
#                 col=1
#             )
#             fig.update_xaxes(
#                 type='category',
#                 # type='date',
#                 ticksuffix = "  ",
#                 showline=True,
#                 linewidth=1,
#                 linecolor='lightgrey',
#                 mirror=True
#             )
#             fig.update_yaxes(
#                 ticksuffix = "  ",
#                 showline=True,
#                 linewidth=1,
#                 linecolor='lightgrey',
#                 mirror=True,
#                 fixedrange=True
#             )
#             fig.update_layout(
#                 height=1600,
#                 autosize= True,
#                 # hovermode="x unified",
#                 hoverlabel=dict(
#                     font_size=12,
#                     bgcolor='rgba(255,255,255,0.2)'
#                 ),
#                 template='plotly_white',
#                 legend=dict(
#                     orientation="h",
#                     yanchor="top",
#                     xanchor="center",
#                     y=1.05,
#                     x=0.5
#                 )
#             )
#         return fig

