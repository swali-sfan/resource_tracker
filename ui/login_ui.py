import dash_bootstrap_components as dbc
from dash import Dash, html, dcc



login_layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            # Title
                            html.H2(
                                "Du SFAN Resource Database",
                                className="text-center fw-bold mb-2"
                            ),

                            # Subtitle
                            html.P(
                                "Sign in to access dashboard",
                                className="text-center text-muted mb-4"
                            ),

                            # Username
                            dbc.Label(
                                "Username",
                                html_for="username",
                                className="fw-semibold"
                            ),

                            dbc.Input(
                                id="username",
                                type="text",
                                placeholder="Enter your username",
                                className="mb-3"
                            ),

                            # Password
                            dbc.Label(
                                "Password",
                                html_for="password",
                                className="fw-semibold"
                            ),

                            dbc.Input(
                                id="password",
                                type="password",
                                placeholder="Enter your password",
                                className="mb-4"
                            ),

                            # Login Button
                            dbc.Button(
                                "Login",
                                id="submit_button",
                                color="dark",
                                className="w-100 fw-semibold",
                                size="lg"
                            ),

                            # Login message
                            html.Div(
                                id="login-message",
                                className="text-danger text-center mt-3"
                            )
                        ]
                    ),
                    className="shadow-lg border-0 rounded-4"
                ),
                width=12,
                sm=10,
                md=7,
                lg=5,
                xl=4
            ),
            justify="center",
            align="center",
            className="vh-100"
        )
    ],
    fluid=True,
    className="bg-light"
)
