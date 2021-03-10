from pydantic import BaseModel
from ..db import *
from .security import get_api_key,APIKey
from datetime import datetime 
from fastapi import HTTPException,Depends
from typing import Dict,List

class ChannelData(BaseModel):
    numeric_value:float=None
    metadata:Dict=None
    time:datetime=None

def fun(
    device_id:int,
    start_time:datetime=None,end_time:datetime=None,channel:str=None,
    api_key:APIKey=Depends(get_api_key)):
    with db_session:
        device = db.Device.get(id=device_id)
        if device is None: 
            raise HTTPException(400,f"No device with id {device_id}")
        device_data = {}
        if channel is None:
            channels = [i.name for i in device.data_channels]
        else:
            channels = [channel]
        for channel in device.data_channels:
            if channel.name in channels:
                if (start_time is None) and (end_time is None):
                    channel_data = select(i for i in db.ChannelEntry if i.data_channel==channel)
                elif (start_time is not None) and (end_time is None):
                    channel_data = select(i for i in db.ChannelEntry if i.data_channel==channel and i.time>=start_time)
                elif (start_time is None) and (endtime is not None):
                    channel_data = select(i for i in db.ChannelEntry if i.data_channel==channel and i.time<=end_time)
                else:
                    channel_data = select(i for i in db.ChannelEntry if 
                        i.data_channel==channel and 
                        i.time<=end_time and
                        i.time>=start_time)
                device_data[channel.name] = [i.to_dict(only=["numeric_value","metadata","time"]) for i in channel_data]
        return device_data 
            