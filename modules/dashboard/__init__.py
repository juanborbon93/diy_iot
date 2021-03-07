from .app import app
from .layout import show,register_callbacks
from dash.dependencies import Input, Output

app.layout = show
register_callbacks(app)