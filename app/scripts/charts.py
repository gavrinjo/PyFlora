
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from flask import current_app
from app.models import Pot, Sensor, Reading
from app import db

class PLine():

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
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df[df['indicator']=='moisture']['measured'],
                y=df[df['indicator']=='moisture']['value'],
                name='Moisture'
                # yaxis='y1'
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df[df['indicator']=='nutrient']['measured'],
                y=df[df['indicator']=='nutrient']['value'],
                name='Nutrient'
                # yaxis='y1'
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df[df['indicator']=='salinity']['measured'],
                y=df[df['indicator']=='salinity']['value'],
                name='Salinity'
                # yaxis='y1'
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df[df['indicator']=='sunlight']['measured'],
                y=df[df['indicator']=='sunlight']['value'],
                name='Sunlight',
                yaxis='y2')
        )
        fig.add_trace(
            go.Scatter(
                x=df[df['indicator']=='temperature']['measured'],
                y=df[df['indicator']=='temperature']['value'],
                name='Temperature',
                yaxis='y3')
        )
        fig.add_trace(
            go.Scatter(
                x=df[df['indicator']=='reaction']['measured'],
                y=df[df['indicator']=='reaction']['value'],
                name='Reaction',
                yaxis='y4')
        )

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
            xaxis=dict(
                domain=[0.1, 0.9]
            ),
            yaxis=dict(
                title="%",
                titlefont=dict(color="#1f77b4"),
                tickfont=dict(color="#1f77b4")
            ),
            yaxis2=dict(
                title="Lux",
                titlefont=dict(color="#ff7f0e"),
                tickfont=dict(color="#ff7f0e"),

                anchor="free",
                overlaying="y",
                side="left",
                position=0
            ),
            yaxis3=dict(
                title="°C",
                titlefont=dict(color="#d62728"),
                tickfont=dict(color="#d62728"),

                anchor="x",
                overlaying="y",
                side="right"
            ),
            yaxis4=dict(
                title="pH",
                titlefont=dict(color="#9467bd"),
                tickfont=dict(color="#9467bd"),

                anchor="free",
                overlaying="y",
                side="right",
                position=1
            )
        )

        fig.update_layout(
            height=600,
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
                y=1.09,
                x=0.5
            ),
            xaxis_range=[datetime.utcnow() - timedelta(hours=1), datetime.utcnow()]
        )
        return fig


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
            xaxis_range=[datetime.utcnow() - timedelta(hours=1), datetime.utcnow()]
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
    