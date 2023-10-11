
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from flask import current_app
from app.models import Pot, Sensor, Reading
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
    
    def config(self):
        df = self.data_frame(self.pot)
        fig = px.line(df, x='measured', y='value', custom_data=['unit'], color='indicator', facet_row='indicator')
        fig.update_xaxes(
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
            ),
            xaxis_range=[datetime.utcnow() - timedelta(days=1), datetime.utcnow()]
        )
        fig.for_each_trace(lambda t: t.update(hovertemplate='%{y}%{customdata[0]}'))
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        return fig


class PlotlyHisto():

    def __init__(self, pot: object) -> None:
        self.pot = pot
    
    def pot_df(self, pot):
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
    
    def config(self):
        df = self.pot_df(self.pot)
        fig = px.histogram(df, x="indicator", color="indicator", nbins=8)
        fig.update_xaxes(
            showline=True,
            linewidth=1,
            linecolor='lightgrey',
            mirror=True
        )
        fig.update_yaxes(
            showline=True,
            linewidth=1,
            linecolor='lightgrey',
            mirror=True
        )
        fig.update_layout(
                autosize= True,
                template='plotly_white',
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    xanchor="center",
                    y=1.2,
                    x=0.5
                )
            )
        return fig
    
class PlotlyPie():
    def __init__(self, pot: object) -> None:
        self.pot = pot
    
    def pot_df(self, pot):
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
    
    def config(self):
        df = self.pot_df(self.pot)
        fig = px.pie(df, values='value', names='indicator')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_xaxes(
            showline=True,
            linewidth=1,
            linecolor='lightgrey',
            mirror=True
        )
        fig.update_yaxes(
            showline=True,
            linewidth=1,
            linecolor='lightgrey',
            mirror=True
        )
        fig.update_layout(
            height=600,
            autosize= True,
            template='plotly_white',
            legend=dict(
                orientation="h",
                yanchor="top",
                xanchor="center",
                y=1.2,
                x=0.5
            )
        )
        return fig
    