from dash.dependencies import Input, Output
from .device_feeds import show_device_feeds

def register_callbacks(app):

    @app.callback(
        Output("device-feeds","children"),
        Input("device-selection-dropdown","value")
    )
    def fun(devices):
        if devices:
            return [show_device_feeds(name) for name in devices]