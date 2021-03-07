from ...db import db,db_session,select
import dash_ace
from pydantic import BaseModel,validator
from typing import List
from ..app import app
from dash.dependencies import Input, Output,State
import dash_html_components as html
import dash_bootstrap_components as dbc
import json

class ChannelModel(BaseModel):
    name:str
    data_type:str
    @validator('data_type')
    @db_session
    def validate_data_type(cls,v):
        data_type_match = db.DataType.get(id=v)
        if data_type_match is None:
            raise ValueError(f"{v} is not a supported datatype")
        return v

class DeviceConfig(BaseModel):
    name:str
    channels:List[ChannelModel]

    @validator('name')
    @db_session
    def validate_name(cls,v):
        existing_device = db.Device.get(name=v)
        if existing_device is not None:
            raise ValueError(f"Device with name {v} already in database")
        return v
    @validator('channels')
    def validate_channels(cls,v):
        if len(v)==0:
            raise ValueError("Device must have at least one channel definition")
    @db_session
    def register_device(self):
        new_device = db.Device(name=self.name)
        db.commit()
        for channel in self.channels:
            new_channel = db.DataChannel(name=channel.name,device=new_device,data_type=db.DataType[channel.data_type])
            db.commit()
        


    


default_config = '''{
    "name":"device_name",
    "channels":[
        {
            "name":"channel_0",
            "data_type":"numeric"
        },
        {
            "name":"channel_1",
            "data_type":"image"
        }
    ]
}
'''
add_device_ui = html.Div(
    [
        html.H3("Add New Device",style={"margin-top":"1rem"}),
        html.P("Enter device config below:"),
        dash_ace.DashAceEditor(
            id='new-device-config',
            value=default_config,
            theme='github',
            mode='json',
            tabSize=2,
            enableBasicAutocompletion=True,
            maxLines=20,
            style={'width':"100%"}
        ),
        dbc.Button("Add Device",block=True,id='new-device-button'),
        html.Div(id='new-device-message')
    ]
)

@app.callback(
    Output('new-device-message','children'),
    Input('new-device-button','n_clicks'),
    State('new-device-config','value')
)
def make_new_device(n_clicks,config_str):
    message = None
    if n_clicks:
        try:
            device_config = DeviceConfig.parse_raw(config_str)
            device_config.register_device()
            message = f"Device {device_config.name} has been registered"
        except Exception as e:
            message = f"Invalid config: {e}"
    return message
        