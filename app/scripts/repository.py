
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from ipychart import Chart



def plot_config(fig: go.Figure, df: pd.DataFrame):



    columns = list(set(df.columns.tolist()) - set(['id', 'pot_id', 'measured']))
    data = []
    for column in columns:
        data.append(go.Scatter(x=df['measured'], y=df[column], name=column, line_shape='spline'))
    fig.add_traces(data)
    fig.update_xaxes(type='category', showticklabels=False)
    fig.update_traces(mode="lines", hovertemplate=None)
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
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)




dataset = {
  'labels': ['Data 1', 'Data 2', 'Data 3', 'Data 4', 
             'Data 5', 'Data 6', 'Data 7', 'Data 8'],
  'datasets': [{'data': [14, 22, 36, 48, 60, 90, 28, 12]}]
}
options= {
        'scales': {
            'y': {
                'ticks': {
                    # Include a dollar sign in the ticks
                    'callback': '''function(value, index, values) {
                        return '$' + value;
                    }'''
                }
            }
        },
    }

mychart = Chart(data=dataset, kind='line', options=options)
print(mychart.get_html_template())