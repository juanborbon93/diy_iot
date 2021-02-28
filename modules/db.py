import os
from datetime import datetime
from pony.orm import *


db = Database()


class Device(db.Entity):
    id = PrimaryKey(int, auto=True)
    data_channels = Set('DataChannel')
    name = Required(str)


class ChannelEntry(db.Entity):
    id = PrimaryKey(int, auto=True)
    time = Required(datetime)
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
    id = PrimaryKey(str, auto=True)
    data_channels = Set(DataChannel)
    metadata_config = Optional(Json)



db.bind(provider='postgres', dsn=os.environ['DATABASE_URL'])
db.generate_mapping(create_tables=True)