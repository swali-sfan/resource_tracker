from dash import Dash , html , dash_table , Output , Input , dcc
import dash_bootstrap_components as dbc
# from import_script import getResourceSheet
import pandas as pd
from database import getResourceDf


resource_df = getResourceDf()
resource_layout = dbc.Container(
    [
    dcc.Interval(
        id="refresh_interval" , 
        interval= 5*60*1000,
        n_intervals=0
    ),
    dcc.Store(
        id= "resource_data"
    ),
    html.Div(
    [
        # Right-side company name + logout
        html.Div(
            [
                html.Div(
                    "XAD Technologies",
                    style={
                        "color": "#ffffff",
                        "fontSize": "14px",
                        "fontWeight": "600",
                        "padding": "8px 16px",
                        "border": "1px solid #495057",
                        "borderRadius": "6px",
                        "marginBottom": "8px"
                    }
                ),

                html.Button(
                    "Logout",
                    id="logout-button",
                    style={
                        "backgroundColor": "#94121f",
                        "color": "#ffffff",
                        "fontSize": "14px",
                        "fontWeight": "600",
                        "padding": "8px 16px",
                        "border": "1px solid #495057",
                        "borderRadius": "6px",
                        "marginBottom": "8px"
                    }
                )
            ],
            style={
                "position": "absolute",
                "right": "30px",
                "top": "20px",
                "width": "150px"
            }
        ),

        # Center content
        html.Div(
            [
                html.H1(
                    "Resource Tracker",
                    className="mb-1",
                    style={
                        "color": "#ffffff",
                        "fontSize": "42px",
                        "fontWeight": "800",
                        "letterSpacing": "0.5px"
                    }
                )
            ],
            style={
                "textAlign": "center"
            }
        )
    ],
    style={
        "position": "relative",
        "backgroundColor": "#212529",
        "padding": "35px 20px 32px 20px",
        "borderBottom": "4px solid #0d6efd",
        "boxShadow": "0 2px 6px rgba(0, 0, 0, 0.15)"
    }
),
    # search bar
    html.Div(
    [
        html.Div(
            [
                html.Div(
                    "Search Resources",
                    style={
                        "fontSize": "15px",
                        "fontWeight": "600",
                        "color": "#343a40",
                        "marginBottom": "8px"
                    }
                ),

                dbc.InputGroup(
                    [
                        dbc.Input(
                            id="resource_search",
                            placeholder="Search by employee name or XAD ID...",
                            type="text",
                            style={
                                "width": "100%",
                                "height": "45px",
                                "fontSize": "15px",
                                "border": "1px solid #ced4da",
                                "boxShadow": "none"
                            }
                        )
                    ],
                    style={
                        "width": "100%",
                        "maxWidth": "650px",
                        "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.08)",
                        "borderRadius": "7px",
                        "overflow": "hidden"
                    }
                )
            ],
            style={
                "width": "100%",
                "maxWidth": "650px"
            }
        )
    ],
    style={
        "display": "flex",
        "justifyContent": "center",
        "padding": "25px 20px 20px 20px",
        "backgroundColor": "#f8f9fa"
    }
),
    # resource table 
    html.Div(
    dash_table.DataTable(
        id="resource_table",

        data=resource_df.to_dict("records"),

        columns=[
            {
                "name": col,
                "id": col
            }
            for col in resource_df.columns
        ],

        # -----------------------------
        # Table container
        # -----------------------------
        style_table={
            "overflowX": "auto",
            "border": "1px solid #dee2e6",
            "borderRadius": "6px",
        },

        # -----------------------------
        # Header
        # -----------------------------
        style_header={
            "backgroundColor": "#f1f3f5",
            "color": "#212529",
            "fontWeight": "600",
            "fontSize": "14px",
            "textAlign": "left",
            "border": "1px solid #dee2e6",
            "padding": "12px",
        },

        # -----------------------------
        # Cells
        # -----------------------------
        style_cell={
            "fontFamily": "Arial, sans-serif",
            "fontSize": "13px",
            "color": "#343a40",
            "textAlign": "left",
            "padding": "10px",
            "border": "1px solid #e9ecef",
            "whiteSpace": "normal",
            "height": "auto",
            "minWidth": "120px",
        },

        # -----------------------------
        # Data rows
        # -----------------------------
        style_data={
            "backgroundColor": "white",
            "border": "1px solid #e9ecef",
        },

        # -----------------------------
        # Alternating rows
        # -----------------------------
        style_data_conditional=[
            {
                "if": {
                    "row_index": "odd"
                },
                "backgroundColor": "#f8f9fa",
            },

            # Hover effect
            {
                "if": {
                    "state": "active"
                },
                "backgroundColor": "#e7f1ff",
                "border": "1px solid #b6d4fe",
            },
        ],

        # -----------------------------
        # Pagination
        # -----------------------------
        page_size=15,

        # -----------------------------
        # Sorting / filtering
        # -----------------------------
        sort_action="native",
        filter_action="native",

        # -----------------------------
        # Selection
        # -----------------------------
        row_selectable="single",
        selected_rows=[],
    ),

    style={
        "width": "100%",
        "marginTop": "10px",
    }
)
    
    ]
)


def register_callbacks(app):
    @app.callback(
            Output("resource_data" , "data"),
            Input("refresh_interval" , "n_intervals")
    )
    def refresh_database(n_intervals):
        resource_data = resource_df
        resource_data = resource_data.to_dict("records")
        print(len(resource_data))
        return resource_data.to_dict("records")

    @app.callback(Output("resource_table" , "data") , 
                  Input("resource_search" , "value") , 
                  Input("resource_data" , "data"))
    def search_value(value , data):
        if not data:
            return []
        if value:
            value = value.strip().lower()
            resource_df = pd.DataFrame(data)
            mask = (
                resource_df["Staff Name"].astype(str).str.lower().str.contains(value , na=False)
                |
                resource_df["File No"].astype(str).str.lower().str.contains(value , na=False)
            )

            filtered_df = resource_df[mask]
            return filtered_df.to_dict("records")
        return pd.DataFrame(data).to_dict("records")
