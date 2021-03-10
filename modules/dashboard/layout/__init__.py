from .device_feeds import show_device_feeds
from .devices import device_dropdown
from .login import show_login
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from .callbacks import register_callbacks
from .add_device import add_device_ui
def show():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Jumbotron(
                            dbc.Container(
                                [
                                    html.H1("IOT Dashboard", className="display-3")
                                ],
                                fluid=True,
                            ),
                            style={"padding":"1rem","margin-bottom":"0"}
                        ),
                        dcc.Tabs(
                            [
                                dcc.Tab(
                                    label="Device Feeds",
                                    children = [
                                        device_dropdown(),
                                        html.Div(id="device-feeds"),
                                        dcc.Interval(id="device-refresh-interval",interval=5000)
                                    ]
                                ),
                                dcc.Tab(
                                    label="Admin Tools",
                                    children=[
                                        add_device_ui
                                    ]
                                )
                            ]
                        )
                    ],
                    width=10
                ),
                justify="center"
            )
        ],
        fluid=True)
