import dash
from dash.html.Col import Col
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash_bootstrap_components._components.Navbar import Navbar
import plotly.express as px
import pandas as pd
from plotly import graph_objs
from dash_bootstrap_templates import load_figure_template

import math

millnames = ["", " Mille", " Million", " Milliard", "000 milliards"]


def millify(n):
    n = float(n)
    millidx = max(
        0,
        min(
            len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))
        ),
    )

    return "{:.0f}{}".format(n / 10 ** (3 * millidx), millnames[millidx])


load_figure_template(["CYBORG", "QUARTZ"])


### importing Data and extracting
Export_total = pd.read_csv("Data/Export_total.csv")
new_df = pd.read_csv("Data/new_df.csv")
annual=pd.read_csv('Data/Annual.csv',sep=';',decimal=',')

total_import= annual[(annual["Libellé du flux"]=="Importations CAF")].groupby(["Libellé du flux"]).sum().sort_values("Valeur DHS 2020", ascending=False)
total_export= annual[(annual["Libellé du flux"]=="Exportations FAB")].groupby(["Libellé du flux"]).sum().sort_values("Valeur DHS 2020", ascending=False)

utilisation_import = (
    Export_total[(Export_total["Libellé du flux"] == "Importations CAF")]
    .groupby(["Libellé du groupement d'utilisation"])
    .sum()
    .sort_values("Total dh", ascending=False)
)
utilisation_export = (
    Export_total[(Export_total["Libellé du flux"] == "Exportations FAB")]
    .groupby(["Libellé du groupement d'utilisation"])
    .sum()
    .sort_values("Total dh", ascending=False)
)
pays_export = (
    annual[(annual["Libellé du flux"] == "Exportations FAB")]
    .groupby(["Libellé du pays"])
    .sum()
    .sort_values("Valeur DHS 2020", ascending=False)
)
pays_import = (
    annual[(annual["Libellé du flux"] == "Importations CAF")]
    .groupby(["Libellé du pays"])
    .sum()
    .sort_values("Valeur DHS 2020", ascending=False)
)
continent_import = (
    Export_total[(Export_total["Libellé du flux"] == "Importations CAF")]
    .groupby(["Continent"])
    .sum()
    .sort_values("Total dh", ascending=False)
)
continent_export = (
    Export_total[(Export_total["Libellé du flux"] == "Exportations FAB")]
    .groupby(["Continent"])
    .sum()
    .sort_values("Total dh", ascending=False)
)


# some variables
max_p_i = millify(pays_import['Valeur DHS 2020'][0])
max_p_i_i = pays_import.index[0]

max_p_e = millify(pays_export['Valeur DHS 2020'][0])
max_p_e_i = pays_export.index[0]

max_t_i= millify(total_import['Valeur DHS 2020'][0])
max_t_i_i = total_import.index[0]

max_t_e= millify(total_export['Valeur DHS 2020'][0])
max_t_e_i = total_export.index[0]

app = dash.Dash(
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.CYBORG,
        dbc.icons.FONT_AWESOME,
        "https://bootswatch.com/_vendor/bootstrap/dist/js/bootstrap.bundle.min.js",
        "https://bootswatch.com/_vendor/bootstrap/dist/js/bootstrap.bundle.min.js",
    ],
    # these meta_tags ensure content is scaled correctly on different devices
    # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)


sidebar_header = dbc.Row(
    [
        dbc.Col(html.H6("OEM", className="display-6 "),align="start",xs=8, md=8, lg=8, xl=8, xxl=8, sm=8),
        dbc.Col(" ",xs=2, md=2, lg=2, xl=2, xxl=2, sm=2),
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
            className="mb-3",
            # vertically align the toggle in the center
            align="end",xs=2, md=2, lg=2, xl=2, xxl=2, sm=2
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
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
    df = pd.DataFrame(
        {
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
        }
    )
    fig = px.bar(
        df,
        x="Fruit",
        y="Amount",
        color="City",
        color_continuous_scale=px.colors.sequential.Viridis,
    )
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(138, 138, 138, 0)",
            "paper_bgcolor": "rgba(138, 138, 138, 0)",
        },
        font=dict(family="Lato, monospace", size=9, color="#fff"),
    )
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Title"),
                    dcc.Graph(
                        id="example-graph",
                        figure=fig,
                        responsive=True,
                        style={"width": "auto", "height": "200px"},
                    ),
                ],
                style={"textAlign": "center"},
                className="mycard",
            )
        ]
    )


def kpi1():
    return html.Div(
        [
            html.Div(
                [
                    html.Div('Plus grand importateur',className='title'),
                    html.Hr(),
                    max_p_i + " Dh",
                    html.Br(),
                    max_p_i_i
                    ],
                style={"textAlign": "center"},
                className="KPI",
                )
                ]
    )


def kpi2():
    return html.Div(
        [
            html.Div(
                [
                    html.Div('Plus grand exportateur',className='title'),
                    html.Hr(),
                    max_p_e + " Dh",
                    html.Br(),
                    max_p_e_i
                    ],
                style={"textAlign": "center"},
                className="KPI",
                )
                ]
    )


def kpi3():
    return html.Div(
        [
            html.Div(
                [
                    html.Div('Total exportations 2020',className='title'),
                    html.Hr(),
                    max_t_e + " Dh",
                    html.Br(),
                    max_t_e_i
                    ],
                style={"textAlign": "center"},
                className="KPI",
                )
                ]
    )


def kpi4():
    return html.Div(
        [
            html.Div(
                [
                    html.Div('Total importations 2020',className='title'),
                    html.Hr(),
                    max_t_i + " Dh",
                    html.Br(),
                    max_t_i_i
                    ],
                style={"textAlign": "center"},
                className="KPI",
                )
                ]
    )


content = html.Div(id="page-content")
blank = html.Div(id="blank_output")

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col("", xs=2, sm=2, md=2, lg=2, xl=2),
                dbc.Col(html.H6(""), xs=2, sm=2, md=2, lg=2, xl=2),
                dbc.Col("", xs=2, sm=2, md=2, lg=2, xl=2),
                dbc.Col("", xs=2, sm=2, md=2, lg=2, xl=2),
                dbc.Col(
                    html.Div(
                        [
                            html.Span(
                                className="fa fa-sun mt-1",
                            ),
                            html.Span(
                                [dbc.Switch(
                                value=True,
                                id="theme",
                                className="ms-4 switcher_icon",),]
                            ),
                            
                            html.Span(className="fa fa-moon mt-1"),
                        ],
                        className="justify-content-center switcher",
                    ), xs=4, sm=4, md=4, lg=4, xl=4
                ),
            ]
        ),
        html.Br(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Row(dbc.Col('Quelques metrics de 2020'),style={"textAlign": "center"},className="titre"),
                        dbc.Col([kpi1()],xs=6, sm=6, md=6, lg=3, xl=2,
                        ),
                        dbc.Col([kpi2()],xs=6, sm=6, md=6, lg=3, xl=2,
                        ),
                        dbc.Col([kpi3()],xs=6, sm=6, md=6, lg=3, xl=2,
                        ),
                        dbc.Col([kpi4()],xs=6, sm=6, md=6, lg=3, xl=2,
                        ),
                    ],
                    id="",style={"textAlign": "center"},
                    align="center",
                    className='justify-content-center'
                ),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col([drawFigure()], xs=12, sm=6, md=6, lg=6, xl=3),
                        dbc.Col([drawFigure()], xs=12, sm=6, md=6, lg=6, xl=3),
                        dbc.Col([drawFigure()], xs=12, sm=6, md=6, lg=6, xl=3),
                        dbc.Col([drawFigure()], xs=12, sm=6, md=6, lg=6, xl=3),
                        dbc.Col([drawFigure()], xs=12, sm=12, md=12, lg=6, xl=6),
                        dbc.Col([drawFigure()], xs=12, sm=4, md=4, lg=3, xl=3),
                        dbc.Col([drawFigure()], xs=12, sm=4, md=4, lg=3, xl=3),
                        dbc.Col([drawFigure()], xs=12, sm=4, md=4, lg=3, xl=3),
                    ],
                    id="",style={"textAlign": "center"},
                    align="center",
                    className='justify-content-center'
                ),
            ],
            style={"textAlign": "center"},
                    className='justify-content-center bCard'
        ),
    ]
)


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
        return [
            html.H2("HEY THERE !", style={"textAlign": "center"}),
            html.Hr(),
            html.Div(
                "cette dashbord traite les échanges d'importation et exportation entre le maroc et les autres pays",
                style={"textAlign": "center"},
            ),
            html.Iframe(srcDoc='assets\Data_prep.html')
        ]
    elif pathname == "/page-2":
        return html.H2("What are u looking for?!", style={"textAlign": "center"})
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
    return is_open


if __name__ == "__main__":
    app.run_server(
        port=8080,
        debug=True,
        # host="0.0.0.0",
    )
