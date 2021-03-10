import dash
import dash_bootstrap_components as dbc
import dash_auth
import os

app = dash.Dash(__name__, requests_pathname_prefix="/dash/",external_stylesheets=[dbc.themes.LUX])

username = os.environ.get("ADMIN_USERNAME","admin")
password = os.environ.get("ADMIN_PASSWORD")
if password is None:
    raise Exception("You must set a password using the ADMIN_PASSWORD environment variable")
user_pass = {username:password}
auth = dash_auth.BasicAuth(
    app,
    user_pass
)
