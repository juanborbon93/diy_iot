# import json
# from pydantic import BaseModel
# from typing import List
# from datetime import datetime
# import pandas as pd
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# class ChannelSamples(BaseModel):
#     time:datetime
#     data:float
# class DeviceChannel(BaseModel):
#     name:str
#     data:List[ChannelSamples]
# class Device(BaseModel):
#     name:str
#     channels:List[DeviceChannel]
#     @property 
#     def dataframe(self):
#         df = None
#         for channel in self.channels:
#             channel_data = [{"time":a.time,"data":a.data,"channel":channel.name} for a in channel.data]
#             channel_df = pd.DataFrame(channel_data)
#             if df is not None:
#                 df = df.append(channel_df,ignore_index=True)
#             else:
#                 df = channel_df
#         return df
#     @property
#     def channel_plot(self):
#         channel_names = [c.name for c in self.channels]
#         fig = make_subplots(len(self.channels),1,subplot_titles=channel_names)
#         for i,channel in enumerate(self.channels):
#             data_points = [datapoint.data for datapoint in channel.data]
#             date_times = [datapoint.time for datapoint in channel.data]
#             fig.add_trace(go.Scatter(x=date_times,y=data_points),i+1,1)
#         fig.update_xaxes(matches="x")
#         # fig.update_layout(title_text=self.name)
#         return fig

# with open("modules/dashboard/layout/device_data.json") as json_file:
#     data = json.load(json_file)
# devices = [Device.parse_obj(i) for i in data]