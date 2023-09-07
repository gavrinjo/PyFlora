
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go




def plot_config(df):
    config = {}
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['measured'], y=['moisture']))
    fig.add_trace(go.Scatter(x=df['measured'], y=['salinity']))
    # fig = px.line(df[::-1], x='measured', y=['moisture', 'salinity'], template='plotly_white', line_shape='spline')
    # fig.update_xaxes(type='category')
    # fig.update_traces(mode="markers+lines", hovertemplate=None)
    # fig.update_layout(hovermode="x unified")
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # pass

