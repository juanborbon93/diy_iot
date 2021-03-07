import os
from datetime import datetime
from pony.orm import *


db = Database()


class Device(db.Entity):
    name = PrimaryKey(str)
    data_channels = Set('DataChannel')


class ChannelEntry(db.Entity):
    id = PrimaryKey(int, auto=True)
    time = Required(datetime,default=lambda:datetime.utcnow())
    numeric_value = Optional(float)
    metadata = Optional(Json)
    data_channel = Required('DataChannel')


class DataChannel(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    device = Required(Device)
    device_time_entrys = Set(ChannelEntry)
    data_type = Required('DataType')


class DataType(db.Entity):
    id = PrimaryKey(str)
    data_channels = Set(DataChannel)
    metadata_config = Optional(Json)


database_url = os.environ.get('DATABASE_URL')
if database_url:
    db.bind(provider='postgres', dsn=database_url)
else: 
    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)