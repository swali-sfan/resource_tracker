from dash import Dash , html , dcc , Output , Input , State , no_update
import dash_bootstrap_components as dbc
from ui.resource_tracker_ui import resource_layout , register_callbacks
from ui.login_ui import login_layout
from flask_login import current_user , logout_user , login_user
from auth import login_manager , User
import json
import os

app = Dash(
    __name__ ,
    external_stylesheets=[dbc.themes.BOOTSTRAP] , 
    suppress_callback_exceptions= True
)
users = json.loads(os.environ["USERS"])
server = app.server
server.secret_key = "your-secret-key"

login_manager.init_app(server)
login_manager.login_view = "/"

@server.route("/health")
def health():
    return "OK", 200

app.layout = html.Div(
       [
           dcc.Location(
               id="url",
               refresh=False
           ),
           html.Div(
               id="page-content"
           )
       ]
)

@app.callback(
        Output("page-content" , "children"),
        Input("url" , "pathname")
)
def resourceTracker(pathname):
    if pathname == "/tracker":
        if not current_user.is_authenticated:
            return dcc.Location(
                href="/",
                id = "redirect_to_login",
                refresh= True
            )
        return resource_layout
    return login_layout

@app.callback(
        Output("url" , "pathname"),
        Output ("login-message" , "children") , 
        Input("submit_button" , "n_clicks"),
        State("username" , "value"),
        State("password" , "value"),
        prevent_initial_call = True
)
def login(n_clicks , username , password):
    if not username or not password:
        return ("/" , "Please provide username and password")

    if username in users and users[username]== password:
        user = User(username)
        login_user(user)
        return ("/tracker" , "")

    return (no_update , "invalid username or password")

register_callbacks(app)

if __name__ =='__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8050)),
        debug=False
    )

