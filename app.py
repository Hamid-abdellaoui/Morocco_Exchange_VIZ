################################ imporing libraries ################################
from re import X
import dash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash_bootstrap_components._components.Navbar import Navbar
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import load_figure_template
import math


################################ importing Data ################################
################################################################################

Export_total = pd.read_csv("Data/Export_total.csv")
annual = pd.read_csv("Data/Annual_processed.csv", sep=",")
export_map=pd.read_csv('Data/for_map0.csv',sep=',')
import_map=pd.read_csv('Data/for_map1.csv',sep=',')


############################ Extracting Data ################################
############################################################################


            ##### les données de 5em graph #####
pays_exports=annual[(annual['Libellé du flux']=="Exportations FAB") | (annual['Libellé du flux']=="Importations CAF")]
annualdf=pays_exports.set_index(['Libellé du pays','Libellé du flux'])
annualdf=annualdf.transpose().set_index(pd.date_range(start='2010-01-01', periods=11, freq='Y'))
annualdf=annualdf.unstack()
annualdf=annualdf.to_frame()[:]
annualdf=annualdf.reset_index()


 
          ##### for KpiS and others ##### 
total_import =annual[(annual["Libellé du flux"] == "Importations CAF")].groupby(["Libellé du flux"]).sum().sort_values("Valeur DHS 2020", ascending=False)
total_export =annual[(annual["Libellé du flux"] == "Exportations FAB")].groupby(["Libellé du flux"]).sum().sort_values("Valeur DHS 2020", ascending=False)

pays_export =annual[(annual["Libellé du flux"] == "Exportations FAB")].groupby(["Libellé du pays"]).sum().sort_values("Valeur DHS 2020", ascending=False)
pays_import =annual[(annual["Libellé du flux"] == "Importations CAF")].groupby(["Libellé du pays"]).sum().sort_values("Valeur DHS 2020", ascending=False)

pays_export0 = pays_export.transpose()
pays_export0["date"] = pd.date_range(start="2010-01-01", periods=11, freq="Y")



            #### for Pie charts #######

continent_import =Export_total[(Export_total["Libellé du flux"] == "Importations CAF")].groupby(["Continent"]).mean().sort_values("Total dh", ascending=False)
continent_export =Export_total[(Export_total["Libellé du flux"] == "Exportations FAB")].groupby(["Continent"]).mean().sort_values("Total dh", ascending=False)
utilisation_import =Export_total[(Export_total["Libellé du flux"] == "Importations CAF")].groupby(["Libellé du groupement d'utilisation"]).mean().sort_values("Total dh", ascending=False)
utilisation_export =Export_total[(Export_total["Libellé du flux"] == "Exportations FAB")].groupby(["Libellé du groupement d'utilisation"]).mean().sort_values("Total dh", ascending=False)



            ##### for bar chart #######
            
section_export =Export_total[(Export_total["Libellé du flux"] == "Importations CAF")].groupby(["Libellé de la section CTCI"]).mean().sort_values("Total dh", ascending=False)
section_import =Export_total[(Export_total["Libellé du flux"] == "Exportations FAB")].groupby(["Libellé de la section CTCI"]).mean().sort_values("Total dh", ascending=False)
sections=df = pd.DataFrame()
sections['total imports']=section_import['Total dh']
sections['total exports']=section_export['Total dh']


################################ a function to deal with large numbers in the KPIs ################################
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

########## some variables for KPIs
max_p_i = millify(pays_import["Valeur DHS 2020"][0])
max_p_i_i = pays_import.index[0]

max_p_e = millify(pays_export["Valeur DHS 2020"][0])
max_p_e_i = pays_export.index[0]

max_t_i = millify(total_import["Valeur DHS 2020"][0])
max_t_i_i = total_import.index[0]

max_t_e = millify(total_export["Valeur DHS 2020"][0])
max_t_e_i = total_export.index[0]



################################ Loading the theme and creating my personnalised palette ################################
load_figure_template(["QUARTZ"])
my_palette=["#29d4f7","#FF5677","#40f190","#B958A5","#f7c76f","cadetblue", "saddlebrown", "darkslateblue"]



############# initialisation de l'app  dash #########

app = dash.Dash(
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
        "https://bootswatch.com/_vendor/bootstrap/dist/js/bootstrap.bundle.min.js",
        "https://bootswatch.com/_vendor/bootstrap/dist/js/bootstrap.bundle.min.js",
    ],
    # these meta_tags ensure content is scaled correctly on different devices
    # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

######### the functions used to draw the graphs #####
    
def drawFig():
    labels = continent_import.index
    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=continent_import['Total dh'], name="Partition des importations par utilisation"),
              1, 1)
    fig.add_trace(go.Pie(labels=labels, values=continent_export['Total dh'], name="Partition des exportations par utilisation"),
              1, 2)
    fig.update_traces(hole=.5, hoverinfo="label+percent+name")
    fig.update_layout(
    annotations=[dict(text='Import', x=0.20, y=0.5, font_size=14, showarrow=False),
                 dict(text='Export', x=0.80, y=0.5, font_size=14, showarrow=False)])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(138, 138, 138, 0)",
            "paper_bgcolor": "rgba(138, 138, 138, 0)",
        },
        font=dict(family="Lato, monospace", size=12, color="#fff"),
        xaxis =  {'showgrid': False},
        yaxis = {'showgrid': True}
    )
    fig.update_layout(legend_font_size=9)
    fig.update_layout(legend_itemsizing='trace')
    fig.update_layout(legend_uirevision=X)
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return html.Div(
        [
            html.Div(
                [
                     html.Div("Partition des importations par continents(moyen des 3 derniers années)"),
                     html.Br(),
                    dcc.Graph(
                        id="example-graph",
                        figure=fig,
                        responsive=True,
                        style={"width": "auto", "height": "270px"},
                    ),
                ],
                style={"textAlign": "center"},
                className="mycard",
            )
        ]
    )

def drawMap():
    
    return html.Div(
        [
            html.Div(
                [
            dbc.Tabs([
                dbc.Tab(label="Exportations", tab_id="tab-1",tabClassName="flex-grow-1 text-center",active_label_style={'background-color':'rgb(196, 125, 230)','color':'rgb(42, 42, 53)'},tab_style={'margin':'0px'} , label_style={'background-color':'#e9e9e92a','color':'rgb(42, 42, 53)'}),
                dbc.Tab(label="Importations", tab_id="tab-2",tabClassName="flex-grow-1 text-center",active_label_style={'background-color':'rgb(196, 125, 230)','color':'rgb(42, 42, 53)'},tab_style={'margin':'0px'} , label_style={'background-color':'#e9e9e92a','color':'rgb(42, 42, 53)'}),
                ],
            id="tabs",
            active_tab="tab-1",style={'padding':'0px 40px',}
        ),
        html.Div(id="content"),
                    
                ],
                style={"textAlign": "center"},
                className="mycard",
            )
        ]
    )

def drawFigure3():
    fig = px.pie(utilisation_import,
    values='Total dh',
    names=utilisation_import.index,
        color_discrete_sequence=my_palette,
    )
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        },
        font=dict(family="Lato, monospace", size=12, color="#fff"),
    )
    
    fig.update_layout(legend_font_size=9)
    fig.update_layout(legend_itemsizing='trace')
    fig.update_layout(legend_uirevision=X)
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return html.Div(
        [
            html.Div(
                [
                     html.Div("Partition des importations par utilisation(moyen des 3 derniers années)"),
                    dcc.Graph(
                        id="3-graph",
                        figure=fig,
                        responsive=True,
                        style={"width": "auto", "height": "270px"},
                    ),
                ],
                style={"textAlign": "center"},
                className="mycard",
            )
        ]
    )

def drawFigure4():
    fig = px.pie(utilisation_export,
    values='Total dh',
    names=utilisation_export.index,
        color_discrete_sequence=my_palette,
    )
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        },
        font=dict(family="Lato, monospace", size=12, color="#fff"),
    )
    
    fig.update_layout(legend_font_size=9)
    fig.update_layout(legend_itemsizing='trace')
    fig.update_layout(legend_uirevision=X)
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return html.Div(
        [
            html.Div(
                [
                     html.Div("Partition des exportations par utilisation(moyen des 3 derniers années)"),
                    dcc.Graph(
                        id="4-graph",
                        figure=fig,
                        responsive=True,
                        style={"width": "auto", "height": "270px"},
                    ),
                ],
                style={"textAlign": "center"},
                className="mycard",
            )
        ]
    )

def drawSections(col):
    fig = px.bar(
        sections.sort_values(by=col, ascending=False),
        x=sections.index,
        y=col,
        orientation='v',
        color_discrete_sequence=my_palette,
    )
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(138, 138, 138, 0)",
            "paper_bgcolor": "rgba(138, 138, 138, 0)",
        },
        font=dict(family="Lato, monospace", size=12, color="#fff"),
        xaxis =  {                                     
                                    'showgrid': False
                                         },
                                yaxis = {                              
                                   'showgrid': True
                                        }
    )
    fig.update_layout(
        margin=dict(b=0))
    fig.update_traces(textfont_size=8, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})
    fig.update_layout(xaxis={'visible': False, 'showticklabels': False})
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Partitions des "+col[6:]+"  par section"),
                    dcc.Graph(
                        id="example-graph",
                        figure=fig,
                        responsive=True,
                        style={"width": "auto", "height": "270px"},
                    ),
                ],
                style={"textAlign": "center"},
                className="mycard",
            )
        ]
    )

def myf(Title,theid):
    return html.Div(
        [
            html.Div(
                [
                    dbc.Row([
                        dbc.Col(dcc.Dropdown(
                                    id="ticker",
                                    options=[
                                        {"label": x, "value": x}
                                        for x in pays_export0.columns[0:]
                                    ] , style=
                                    { 'width': '165px',
                                      'color': '#212121',
                                      'background-color': '#83838350',
                                      'align':'center',
                                      'font-size':'13px'
                                    } ,
                                    value=pays_export0.columns[0],
                                    clearable=True,searchable=False,
                                ),md=6,sm=6,lg=6,xl=6),
                        dbc.Col(html.Div(Title),md=6,sm=6,lg=6,xl=6)
                        ]),

                    dcc.Graph(
                        id=theid,
                        responsive=True,
                        style={"width": "auto", "height": "270px"},
                    ),
                ],
                style={"textAlign": "center"},
                className="mycard",
            )
        ]
    )


######## function to return the KPIs cards ######
 
def kpi1():
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Plus grand importateur ", className="title"),
                    html.Hr(),
                    html.B(
                    max_p_i + " Dh"),
                    html.Br(),
                    max_p_i_i,
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
                    html.Div("Plus grand exportateur ", className="title"),
                    html.Hr(),
                    html.B(max_p_e + " Dh"),
                    html.Br(),
                    max_p_e_i,
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
                    html.Div("Total exportations 2020", className="title"),
                    html.Hr(),
                    html.B(max_t_e + " Dh"),
                    html.Br(),
                    max_t_e_i,
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
                    html.Div("Total importations 2020", className="title"),
                    html.Hr(),
                    html.B(max_t_i + " Dh"),
                    html.Br(),
                    max_t_i_i,
                ],
                style={"textAlign": "center"},
                className="KPI",
            )
        ]
    )


########## The header of sidebare ##########
sidebar_header = dbc.Row(
    [
        dbc.Col(
            html.H6("OEM", className="display-6 "),
            align="start",
            xs=8,
            md=8,
            lg=8,
            xl=8,
            xxl=8,
            sm=8,
        ),
        dbc.Col(" ", xs=2, md=2, lg=2, xl=2, xxl=2, sm=2),
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
            align="end",
            xs=2,
            md=2,
            lg=2,
            xl=2,
            xxl=2,
            sm=2,
        ),
    ]
)
 
########### the sidebar #############
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
                    dbc.NavLink("Data prep", href="/page-1", active="exact"),
                    dbc.NavLink("About", href="/page-2", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)
 
######### items to define the theme and change it #####
content = html.Div(id="page-content")
blank = html.Div(id="blank_output")

############ the home page (dashboard) ###########
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
                                [
                                    dbc.Switch(
                                        value=True,
                                        id="theme",
                                        className="ms-4 switcher_icon",
                                    ),
                                ]
                            ),
                            html.Span(className="fa fa-moon mt-1"),
                        ],
                        className="justify-content-center switcher",
                    ),
                    xs=4,
                    sm=4,
                    md=4,
                    lg=4,
                    xl=4,
                ),
            ]
        ),
        html.Br(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Row(
                            dbc.Col(html.B("Quelques metrics de 2020")),
                            style={"textAlign": "center"},
                            className="titre",
                        ),
                        dbc.Col(
                            [kpi1()],
                            xs=6,
                            sm=6,
                            md=6,
                            lg=3,
                            xl=2,
                        ),
                        dbc.Col(
                            [kpi2()],
                            xs=6,
                            sm=6,
                            md=6,
                            lg=3,
                            xl=2,
                        ),
                        dbc.Col(
                            [kpi3()],
                            xs=6,
                            sm=6,
                            md=6,
                            lg=3,
                            xl=2,
                        ),
                        dbc.Col(
                            [kpi4()],
                            xs=6,
                            sm=6,
                            md=6,
                            lg=3,
                            xl=2,
                        ),
                    ],
                    id="",
                    style={"textAlign": "center"},
                    align="center",
                    className="justify-content-between",
                ),
                html.Hr(),
                dbc.Row(
                    [
                        
                        
                        dbc.Col([drawFig()], xs=12, sm=12, md=6, lg=6, xl=6),
                        dbc.Col([myf('Les échanges entre 2010 et 2020 ',"time-series-chart")
                            ],xs=12,sm=12,md=12,lg=6,xl=6,),
                        dbc.Col([drawFigure3()], xs=12, sm=12, md=6, lg=6, xl=6),
                        dbc.Col([drawFigure4()], xs=12, sm=12, md=6, lg=6, xl=6),
                        dbc.Col([drawMap()], xs=12, sm=12, md=12, lg=12, xl=12),
                        dbc.Col([drawSections("total exports")], xs=12, sm=12, md=12, lg=6, xl=6),
                        dbc.Col([drawSections("total imports")], xs=12, sm=12, md=12, lg=6, xl=6),
                    ],
                    id="",
                    style={"textAlign": "center"},
                    align="center",
                    className="justify-content-center",
                ),
            ],
            style={"textAlign": "center"},
            className="justify-content-center bCard",
        ),
    ],
)






########################################################################################
#################################### callbacks #########################################


############  assigning content to pages depending on a url ############ 
app.layout = html.Div([dcc.Location(id="url"), sidebar, blank, content])


############  swwitching between themes ############ 
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

############  render page according to path ############ 
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(row)
    elif pathname == "/page-1":
        return html.Div(
            [
                html.Div(
                    [
                        html.H2("HEY THERE !", style={"textAlign": "center"}),
                        html.Hr(),
                        html.H6(
                            "Cette dashbord traite les échanges d'importation et exportation entre le maroc et les autres pays",
                        ),
                        html.Div(
                            "les données utilisées dans cette app sont passé d'abord par des étapes de traitement , exploration... ",
                        ),
                        html.P("le notebook suivant montre ces étapes :"),
                        html.Iframe(
                            src="assets/Data_prep.html", width="100%", height="560px"
                        ),
                    ],
                    className="mycard",
                )
            ]
        )
    elif pathname == "/page-2":
        return html.Div(
            [
                html.Br(),
                html.Br(),
                html.Div(
                    [
                        html.Br(),
                        html.Br(),
                        html.H4("Aout this App", style={"textAlign": "center"}),
                        html.Hr(),
                        html.Div(
                            "Les données utilisées sont extraites du site officiel de l'office des changes marocain"
                        ),
                        html.A(
                            "lien vers le websit officiel de l'office",
                            href="https://www.oc.gov.ma/",
                            className="link",
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.A(
                            html.Span(
                                className="fab fa-linkedin fa-2x",
                            ),
                            href="https://www.linkedin.com/in/hamid-abdellaoui/",
                        ),
                        html.A(
                            html.Span(
                                className="fab fa-github-square fa-2x ms-2",
                            ),
                            href="https://github.com/Hamid-abdellaoui",
                        ),
                        html.A(
                            html.Span(
                                className="fa fa-envelope-square fa-2x ms-2",
                            ),
                            href="mailto:hamidabdellaoui55@gmail.com",
                        ),
                    ],
                    className="mycard",
                ),
            ],
        )
    # If the user tries to reach a different page, return a 404 message
    else:
        return dbc.Row(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

############  sidebar toggletr ############ 
@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""

############  navbar toggletr ############ 
@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

############  emprtations/exportations by country line chart ############ 
@app.callback(Output("time-series-chart", "figure"), [Input("ticker", "value")])
def display_time_series(ticker):
    fig = px.line(annualdf[(annualdf['Libellé du pays']==ticker)], x='level_2', y=0, color='Libellé du flux',
    labels={
                     "level_2": "Date",
                     "0": "valeur en DH"
                 },color_discrete_sequence= my_palette,
                 )
    fig.update_layout(
        {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
        },
        font=dict(family="Lato, monospace", size=12, color="#fff"),
        xaxis =  {                                     
                                    'showgrid': False
                                         },
                                yaxis = {                              
                                   'showgrid': True
                                        }
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(9, 145, 199, 0.932)', gridcolor='rgba(240, 240, 240, 0.233)  ')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(9, 145, 199, 0.932)', gridcolor='rgba(240, 240, 240, 0.233)  ')
    return fig

############  the map graph (Choropleth) ############ 
@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        fig = go.Figure(data=go.Choropleth(
        locations = export_map['alpha-3'],
        z = export_map['Valeur moyen des exportations sur 10ans'],
        text = export_map['Libellé du pays'],
        colorscale = ['#99004d', '#ff3287', '#fc76c4', '#ca89bd'],
        #colorscale='Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='white',
        marker_line_width=1,
        colorbar_tickprefix = 'dh ',
        colorbar_title = 'Exports en Dh',))
        fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'),
        annotations = [dict(
            x=0.5,
            y=0,
            xref='paper',
            yref='paper',
            text='Moyenne annuel entre 2010 et 2020',
            showarrow = False)
            ]
            )
        fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(224, 223, 223, 0.137)")
        fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
        fig.update_layout(hovermode='closest',)
        fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },
            font=dict(family="Lato, monospace", size=12, color="#fff"),
        )
        fig.update_coloraxes(colorbar_exponentformat="power")
        return dcc.Graph(
                        figure=fig,
                        responsive=True,
                        style={"width": "auto", "height": "420px"},
                    ),
    elif at == "tab-2":
        fig = go.Figure(data=go.Choropleth(
        locations = import_map['alpha-3'],
        z = import_map['Valeur moyen des importations sur 10ans'],
        text = import_map['Libellé du pays'],
        colorscale = ['#99004d', '#ff3287', '#fc76c4', '#ca89bd'],
        #colorscale='Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='white',
        marker_line_width=1,
        colorbar_tickprefix = 'dh ',
        colorbar_title = 'Imports en Dh',))
        fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'),
        annotations = [dict(
            x=0.5,
            y=0,
            xref='paper',
            yref='paper',
            text='Moyenne annuel entre 2010 et 2020',
            showarrow = False)
            ]
            )
        fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(224, 223, 223, 0.137)")
        fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))
        fig.update_layout(hovermode='closest',)
        fig.update_layout(
            {
                "plot_bgcolor": "rgba(0, 0, 0, 0)",
                "paper_bgcolor": "rgba(0, 0, 0, 0)",
            },
            font=dict(family="Lato, monospace", size=12, color="#fff"),
        )
        fig.update_coloraxes(colorbar_exponentformat="power")
        return dcc.Graph(
                        figure=fig,
                        responsive=True,
                        style={"width": "auto", "height": "420px"},
                    ),
    
    
############ starting the server ########
if __name__ == "__main__":
    app.run_server(
        #port=8080,
        #debug=False,
        #host="0.0.0.0",
    )
