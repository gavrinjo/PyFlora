
import json
import pandas as pd
import numpy as np
import xmltodict

from requests import get
from contextlib import closing
from random import randint
from datetime import datetime
from plotly.subplots import make_subplots

from flask import current_app
from app.models import Gauge, Plant
from app import db

"""
class ZaPlotlyLine():

    COLORS = {
        'sunlight': 'orange',
        'temperature': 'orangered',
        'moisture': 'lightblue',
        'reaction': 'darkorange',
        'nutrient': 'forestgreen',
        'salinity': 'sienna'
    }

    def __init__(self, pypot) -> None:
        self.pypot = pypot
        self.columns = self.get_columns(self.pypot)

    
    def get_columns(self, pot: object) -> list:
        columns = []
        for column in db.inspect(pot).attrs:
            if column.key.endswith("status") and getattr(pot, column.key):
                columns.append(column.key)
        return columns

    def get_measured_data(self, pot: object, N=10):
        df = pd.read_sql_query(db.select(SensorMeasurements), current_app.config['SQLALCHEMY_DATABASE_URI']) 
        df = df.sort_values(by=['measured'], ascending=False)[:N]
        df = df[df['pot_id']==pot.id]
        return df

    def configure(self):
        df = self.get_measured_data(self.pypot, N=20)
        fig = make_subplots(rows=6, cols=1, shared_xaxes=True, vertical_spacing=0.02) # , shared_yaxes='all')
        plant = Plant.query.get(self.pypot.plant_id)
        for i, column in enumerate(self.columns):
            column = column[:column.find('_')]
            min_value, max_value = getattr(plant, column).split(';')
            text = [f'{column.capitalize()} : {val}' for val in df[column]]
            fig.add_scatter(
                x=df['measured'],
                y=df[column],
                line_shape='linear',
                line_color=self.COLORS[column],
                mode='lines',#+markers',
                name=column.capitalize(),
                hovertext=text,
                hoverinfo='x + text',
                row=i+1, col=1
            )
            fig.add_hrect(
                y0=min_value,
                y1=max_value,
                annotation_text=f'Optimal {column} range : {min_value}-{max_value}',
                annotation_position='top left',
                fillcolor=self.COLORS[column],
                opacity=.25,
                line_width=0,
                row=i+1,
                col=1
            )
            fig.update_xaxes(
                # type='category',
                type='date',
                ticksuffix = "  ",
                showline=True,
                linewidth=1,
                linecolor='lightgrey',
                mirror=True
            )
            fig.update_yaxes(
                ticksuffix = "  ",
                showline=True,
                linewidth=1,
                linecolor='lightgrey',
                mirror=True,
                fixedrange=True
            )
            fig.update_layout(
                height=1600,
                autosize= True,
                # hovermode="x unified",
                hoverlabel=dict(
                    font_size=12,
                    bgcolor='rgba(255,255,255,0.2)'
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
        return fig

"""