import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash_bootstrap_components._components.Navbar import Navbar
import plotly.express as px
import pandas as pd
from plotly import graph_objs
from dash_bootstrap_templates import load_figure_template



load_figure_template(["CYBORG", "QUARTZ"])


app = dash.Dash(suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.CYBORG, dbc.icons.FONT_AWESOME, "https://bootswatch.com/_vendor/bootstrap/dist/js/bootstrap.bundle.min.js",
                                      "https://bootswatch.com/_vendor/bootstrap/dist/js/bootstrap.bundle.min.js"],
                # these meta_tags ensure content is scaled correctly on different devices
                # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ],
                )

# we use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
sidebar_header = dbc.Row(
    [
        dbc.Col(html.H6("OCM", className="display-4")),
        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="fa fa-bars"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(255, 255, 255, 0.9)",
                        "border": "none",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="fa fa-bars"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(255, 255, 255, 0.9)",
                        "border": "none",
                    },
                    id="sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(),
                html.P(
                    "Ce tableau de bord s'inscrit dans le cadre d'un projet académique de data visualisation",
                    className="lead",
                ),
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Page 1", href="/page-1", active="exact"),
                    dbc.NavLink("Page 2", href="/page-2", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)


def drawFigure():
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]})
    fig = px.bar(df, x="Fruit", y="Amount", color="City", color_continuous_scale=px.colors.sequential.Viridis)
    fig.update_layout({'plot_bgcolor': 'rgba(138, 138, 138, 0)',
                      'paper_bgcolor': 'rgba(138, 138, 138, 0)', },
    font=dict(
        family="Lato, monospace",
        size=9,
        color="#fff"
    ))
    return html.Div([
            
                html.Div([ html.Div("Title"),
                    dcc.Graph(
                        id='example-graph',
                        figure=fig, responsive=True,
                        style={'width': '35vh', 'height': '35vh'},
                    ),
                ], style={'textAlign': 'center'}, className="mycard")
           
        
    ])


def drawText():
    return dbc.Row([
        dbc.Row([
            dbc.Col(dbc.Nav([html.H2("Text")], pills=True),
                    className="KPI", xs=12, sm=4, md=4, lg=4, xl=2),
            dbc.Col(dbc.Nav([html.H2("Text")], pills=True),
                    className="KPI", xs=12, sm=4, md=4, lg=4, xl=2),
            dbc.Col(dbc.Nav([html.H2("Text")], pills=True),
                    className="KPI", xs=12, sm=4, md=4, lg=4, xl=2),
            dbc.Col(dbc.Nav([html.H2("Text")], pills=True),
                    className="KPI", xs=12, sm=4, md=4, lg=4, xl=2),
        ], className="justify-content-center", style={'textAlign': 'center'})
    ], className="justify-content-end", id="mycollapse")


content = html.Div(id="page-content")
blank = html.Div(id="blank_output")

row = html.Div([
    dbc.Row(
        [
            dbc.Col("", xs=2, sm=2, md=2, lg=2, xl=2),
            dbc.Col(html.H3("Bonjour"), xs=2, sm=2, md=2, lg=2, xl=2),
            dbc.Col("", xs=2, sm=2, md=2, lg=2, xl=2),
            dbc.Col("", xs=2, sm=2, md=2, lg=2, xl=2),
            dbc.Col(html.Div(
                    [
                        html.Span(className="fa fa-sun",),
                        dbc.Switch(value=True, id="theme", className="",),
                        html.Span(className="fa fa-moon"),
                    ],
                    className="d-flex p-2 justify-content-between",
                    ), xs=2, sm=2, md=2, lg=2, xl=2),
            dbc.Col("", xs=2, sm=2, md=2, lg=2, xl=2),
        ]),


    html.Br(),
        html.Div([
            dbc.Row([
                drawText()
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawFigure()
                ],  xs=12, sm=6, md=6, lg=3, xl=3),
                dbc.Col([
                    drawFigure()
                ], xs=12, sm=6, md=6, lg=3, xl=3),
                dbc.Col([
                    drawFigure()
                ], xs=12, sm=6, md=6, lg=3, xl=3),
                dbc.Col([
                    drawFigure()
                ], xs=12, sm=6, md=6, lg=3, xl=3),
            ], align='center'),
            dbc.Row([
                dbc.Col([
                    drawFigure()
                ],  xs=12, sm=12, md=12, lg=6, xl=6),
                dbc.Col([
                    drawFigure()
                ], xs=12, sm=4, md=4, lg=3, xl=3),
                dbc.Col([
                    drawFigure()
                ], xs=12, sm=4, md=4, lg=3, xl=3),
                dbc.Col([
                    drawFigure()
                ], xs=12, sm=4, md=4, lg=3, xl=3),
            ], align='center'),

        ],className="bCard")
    
])


app.layout = html.Div([dcc.Location(id="url"), sidebar, blank, content])

app.clientside_callback(
    """
    function(themeToggle) {
        //  To use different themes,  change these links:
        const theme1 = "https://bootswatch.com/5/CYBORG/bootstrap.min.css"
        const theme2 = "https://bootswatch.com/5/quartz/bootstrap.min.css"
        const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://bootswatch"]')        
        var themeLink = themeToggle ? theme1 : theme2;
        stylesheet.href = themeLink
    }
    """,
    Output("blank_output", "children"),
    Input("theme", "value"),
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(row)
    elif pathname == "/page-1":
        return [html.H2("HEY THERE !", style={'textAlign': 'center'}),
                html.Hr(),
                html.Div("cette dashbord traite les échanges d'importation et exportation entre le maroc et les autres pays", style={'textAlign': 'center'})]
    elif pathname == "/page-2":
        return html.H2("What are u looking for?!", style={'textAlign': 'center'})
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("mycollapse", "is_open"),
    [Input("KPI-toggle", "n_clicks")],
    [State("mycollapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return  is_open


if __name__ == "__main__":
    app.run_server(port=8888, debug=True,
                   #host="0.0.0.0",
                   )
