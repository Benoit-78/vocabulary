import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "static/welcome.css"]
)


# Welcome layout
welcome_layout = html.Div(
    [
        html.H1("Welcome to Vocabulary"),
        dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    dbc.Button("Get started", href="/get_started", color="primary"),
                    style={"border": "none"}
                ),
                dbc.ListGroupItem(
                    dbc.Button("Interrooo !!!", href="/interro_settings", color="primary"),
                    style={"border": "none"}
                ),
                dbc.ListGroupItem(
                    dbc.Button("Vocabulary", href="/database", color="primary"),
                    style={"border": "none"}
                ),
                dbc.ListGroupItem(
                    dbc.Button("Dashboard", href="/dashboard", color="primary"),
                    style={"border": "none"}
                ),
                dbc.ListGroupItem(
                    dbc.Button("Settings", href="/settings", color="primary"),
                    style={"border": "none"}
                ),
            ],
            className="link-list",
            flush=True,
        ),
    ],
)



interro_settings_layout = html.Div(
    [
        html.H1("Choose your preferences"),
        # Test type
        dbc.Row([
            dbc.Col([
                dbc.Label("Test type:"),
            ],
            width=3)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id="test-type",
                    options=[
                        {"label": "Version", "value": "Version"},
                        {"label": "Theme", "value": "Theme"}
                    ],
                    value="Version",
                    clearable=False,
                    style={"width": "200px"}
                )
            ],
            width=9),
        ]),
        # Number of words
        dbc.Row([
            dbc.Col([
                dbc.Label("Words asked:"),
            ],
            width=3)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id="num-words",
                    options=[
                        {"label": "100", "value": 100},
                        {"label": "50", "value": 50},
                        {"label": "20", "value": 20},
                        {"label": "10", "value": 10}
                    ],
                    value=100,
                    clearable=False,
                    style={"width": "200px"}
                )
            ],
            width=9),
        ]),
        # Number of rattraps
        dbc.Row([
            dbc.Col([
                dbc.Label("Catch-up tests:"),
            ],
            width=3)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id="num-rattraps",
                    options=[
                        {"label": "2", "value": 2},
                        {"label": "1", "value": 1},
                        {"label": "0", "value": 0},
                        {"label": "Until the end", "value": -1}
                    ],
                    value=2,
                    clearable=False,
                    style={"width": "200px"}
                )
            ],
            width=9),
        ]),
        html.Br(),
        # Start button
        dbc.Button(
            "Start Test",
            id="start-test-button",
            color="primary",
            href="/interro"
        ),
    ]
)


# Page layout for asking user information
interro_layout = html.Div(
    [
        html.H1("Hi! We'd like to know more about you."),
        html.Div(id="preferences-output"),
        dcc.Input(
            id="name",
            type="text",
            placeholder="Name",
            required=True
        ),
        dcc.Input(
            id="age",
            type="number",
            placeholder="Age",
            required=True
        ),
        html.Br(),
        dbc.Button(
            "Submit",
            id="submit-button",
            color="primary"
        ),
    ]
)


# dcc.Location: to handle the page URL
# main-container: div
# class name: for styling
app.layout = dbc.Container(
    dcc.Location(id="url"),
    id="main-container",
    className="p-5"
)


# Callback to switch between pages
@app.callback(
    Output("main-container", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    pages_dict = {
        "/": welcome_layout,
        "/interro_settings": interro_settings_layout,
        "/interro": interro_layout
    }
    page = pages_dict[pathname]
    return page


# Callback to show selected preferences
@app.callback(
    Output("preferences-output", "children"),
    Input("test-type", "value"),
    Input("num-words", "value"),
    Input("num-rattraps", "value")
)
def show_preferences(test_type, num_words, num_rattraps):
    message = ', '.join([
        f"Selected Preferences: Test Type - {test_type}",
        f"Number of Words - {num_words}",
        f"Number of Catch-ups - {num_rattraps}"
    ])
    return message


if __name__ == "__main__":
    app.run_server(debug=True)
