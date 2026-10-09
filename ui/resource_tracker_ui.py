from dash import Dash , html , dash_table , Output , Input , State , dcc , ctx , no_update
import dash_bootstrap_components as dbc
# from import_script import getResourceSheet
import pandas as pd
from database import getResourceDf
resource_df = getResourceDf()
resource_layout = dbc.Container(
    [
    dcc.Interval(
        id="refresh_interval" , 
        interval= 5*30*1000,
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
    # copy selected data button
    html.Div(
        [
            html.Button(
                "Copy Selected Data",
                id="copy_button",
                n_clicks=0,
                style={
                    "backgroundColor": "#0d6efd",
                    "color": "#ffffff",
                    "fontSize": "14px",
                    "fontWeight": "600",
                    "padding": "8px 16px",
                    "border": "1px solid #0b5ed7",
                    "borderRadius": "6px",
                    "cursor": "pointer"
                }
            ),
            html.Span(
                id="copy_status",
                style={
                    "marginLeft": "12px",
                    "fontSize": "14px",
                    "color": "#198754",
                    "fontWeight": "600"
                }
            )
        ],
        style={
            "display": "flex",
            "alignItems": "center",
            "marginTop": "10px"
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
        # Selection  ("multi" renders checkboxes instead of radio buttons)
        # -----------------------------
        row_selectable="multi",
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
        resource_data = getResourceDf()
        print(f"REFRESH CALLBACK FIRED: {n_intervals}", flush=True)
        resource_data = resource_data.to_dict("records")
        print(f"length of resource_data {len(resource_data)}")
        return resource_data

    @app.callback(Output("resource_table" , "data") , 
                  Output("resource_table" , "selected_rows") ,
                  Output("resource_table" , "page_current") ,
                  Input("resource_search" , "value") , 
                  Input("resource_data" , "data"))
    def search_value(value , data):
        # always clear the old selection (on search change AND on the periodic data refresh)
        selected_rows = []
        # go back to page 1 only when the user changes the search text
        if ctx.triggered_id == "resource_search":
            page_current = 0
        else:
            page_current = no_update

        if not data:
            return [] , selected_rows , page_current
        if value:
            value = value.strip().lower()
            resource_df = pd.DataFrame(data)
            mask = (
                resource_df["Staff Name"].astype(str).str.lower().str.contains(value , na=False)
                |
                resource_df["File No"].astype(str).str.lower().str.contains(value , na=False)
            )

            filtered_df = resource_df[mask]
            return filtered_df.to_dict("records") , selected_rows , page_current
        return pd.DataFrame(data).to_dict("records") , selected_rows , page_current

    # ------------------------------------------------------------------
    # Copy selected row(s) to the clipboard when the button is clicked
    # (runs in the browser). Pastes into Excel as one cell per column,
    # and into Word as a table.
    # ------------------------------------------------------------------
    app.clientside_callback(
        """
        function(n_clicks, selected_rows, virtual_data, columns) {
            if (!n_clicks) {
                return window.dash_clientside.no_update;
            }

            if (!selected_rows || selected_rows.length === 0 || !virtual_data) {
                return "Please select at least one row first.";
            }

            // keep only rows that still exist (after search / filter / sort)
            const rows = selected_rows
                .map(i => virtual_data[i])
                .filter(r => r !== undefined && r !== null);

            if (rows.length === 0) {
                return "Please select at least one row first.";
            }

            const clean = v => (v === null || v === undefined)
                ? ""
                : String(v).replace(/[\\t\\r\\n]+/g, " ").trim();

            const esc = s => s
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;");

            // column headers (in the same order as the table) + the cell values in that same order
            const headers = columns.map(c => clean(c.name));
            const body = rows.map(r => columns.map(c => clean(r[c.id])));

            // plain text: tab between cells, newline between rows (Excel friendly)
            const text = [headers].concat(body)
                .map(cells => cells.join("\\t"))
                .join("\\n");

            // html table (Word / Excel / Outlook friendly)
            const html = "<table border='1'>"
                + "<tr>" + headers.map(h => "<th>" + esc(h) + "</th>").join("") + "</tr>"
                + body.map(cells => "<tr>" + cells
                    .map(v => "<td>" + esc(v) + "</td>").join("") + "</tr>").join("")
                + "</table>";

            const fallbackCopy = () => {
                const ta = document.createElement("textarea");
                ta.value = text;
                ta.style.position = "fixed";
                ta.style.opacity = "0";
                document.body.appendChild(ta);
                ta.focus();
                ta.select();
                try { document.execCommand("copy"); } catch (e) { console.error(e); }
                document.body.removeChild(ta);
            };

            if (navigator.clipboard && window.ClipboardItem) {
                const item = new ClipboardItem({
                    "text/plain": new Blob([text], {type: "text/plain"}),
                    "text/html": new Blob([html], {type: "text/html"})
                });
                navigator.clipboard.write([item]).catch(fallbackCopy);
            } else if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).catch(fallbackCopy);
            } else {
                fallbackCopy();
            }

            return "Copied " + rows.length + " row(s) to clipboard";
        }
        """,
        Output("copy_status" , "children"),
        Input("copy_button" , "n_clicks"),
        State("resource_table" , "derived_virtual_selected_rows"),
        State("resource_table" , "derived_virtual_data"),
        State("resource_table" , "columns"),
        prevent_initial_call=True,
    )