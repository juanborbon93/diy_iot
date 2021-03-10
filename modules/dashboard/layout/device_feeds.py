import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from ...db import db,select,db_session

@db_session
def show_device_feeds(device_name):
    output = None
    device = db.Device.get(name=device_name)
    if device is not None:
        channels = device.data_channels
        channel_names = [c.name for c in channels]
        fig = make_subplots(len(channels),1,subplot_titles=channel_names)
        for j,channel in enumerate(channels):
            channel_entries = select((i.time,i.numeric_value) for i in db.ChannelEntry if i.data_channel == channel)
            data_points = [i[1] for i in channel_entries]
            data_times = [i[0] for i in channel_entries]
            fig.add_trace(go.Scatter(x=data_times,y=data_points),j+1,1)
        fig.update_xaxes(matches="x")
        fig.update_layout(height=100+200*len(channels),showlegend=False)
        children = [
            html.H4(device.name),
            dcc.Graph(figure=fig)
        ]
        output = html.Div(children)
    return output
        
