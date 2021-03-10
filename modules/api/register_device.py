from pydantic import BaseModel
from ..db import *
from .security import get_api_key,APIKey
from fastapi import HTTPException,Depends
from typing import List
from ..channel_types import channel_type_dict

class ChannelConfig(BaseModel):
    name:str
    data_type:str
class DeviceConfig(BaseModel):
    name:str
    channels:List[ChannelConfig]

@db_session
def fun(body:DeviceConfig,api_key:APIKey=Depends(get_api_key)):
    Error = None
    existing_device = db.Device.get(name=body.name)
    if existing_device:
        raise HTTPException(status_code=400,detail=f"Device {body.name} already exists")
    new_device = db.Device(name=body.name)
    for channel_config in body.channels:
        if channel_config.data_type in channel_type_dict:
            new_channel = db.Channel(
                name = channel_config.name,
                device = new_device,
                data_type = channel_config.data_type)
        else: 
            error = f"Invalid data_type for {channel_config.name} channel"
    if error is None:
        db.commit()
    else:
        raise HTTPException(status_code=400,detail=error)
