from pydantic import BaseModel
from ..db import *
from .security import get_api_key,APIKey
from typing import Union,Dict,List
from datetime import datetime
from fastapi import HTTPException,Depends

class ChannelData(BaseModel):
    channel:str
    numeric_value:float=None
    metadata:Dict=None
    time:datetime=None
class Model(BaseModel):
    device_name:str
    data:List[ChannelData]
    
def fun(body:Model,api_key:APIKey=Depends(get_api_key)):
    with db_session:
        device = db.Device.get(name=body.device_name)
        if device is None:
            raise HTTPException(400,f"No device in database with id of {body.device_id}")
        for channel_entry in body.data:
            channel = db.DataChannel.get(device=device,name=channel_entry.channel)
            if channel is None:
                raise HTTPException(400,f"No channel {channel_entry.name} for device {device.id}")
            if channel_entry.time is None:
                channel_entry.time = datetime.utcnow()
            new_entry = db.ChannelEntry(
                time=channel_entry.time,
                numeric_value=channel_entry.numeric_value,
                data_channel=channel
            )
            if channel_entry.metadata:
                new_entry.metadata = channel_entry.metadata
        db.commit()