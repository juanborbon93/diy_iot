import dash_html_components as html
import dash_core_components as dcc
from ...db import db,select,db_session

@db_session
def device_dropdown():
    device_names = select(i.name for i in db.Device)[:]
    children =  [
        html.H3("Select Devices"),
        dcc.Dropdown(
            id='device-selection-dropdown',
            options=[ {"label":i,"value":i} for i in device_names],
            multi=True
        )
    ]
    return html.Div(children)
    