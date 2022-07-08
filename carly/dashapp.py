from itertools import dropwhile
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import plotly.graph_objects as go
import json
import plotly.express as px



from sqlalchemy import text
#connect to database
db_string = 'postgresql://ghg_emissions:Password00@ghgemissions.cg3dqiowwhnr.us-west-1.rds.amazonaws.com:5432/ghg_data'
engine = create_engine(db_string)

query = text('SELECT * FROM direct_emissions')

df = pd.read_sql(query,engine)
print(df)



total_2011 = df["total_emissions_2011"].sum()
total_2012 = df["total_emissions_2012"].sum()
total_2013 = df["total_emissions_2013"].sum()
total_2014 = df["total_emissions_2014"].sum()
total_2015 = df["total_emissions_2015"].sum()
total_2016 = df["total_emissions_2016"].sum()
total_2017 = df["total_emissions_2017"].sum()
total_2018 = df["total_emissions_2018"].sum()
total_2019 = df["total_emissions_2019"].sum()
total_2020 = df["total_emissions_2020"].sum()


# creating the dataset
data = {'2011':total_2011, '2012':total_2012, '2013':total_2013, '2014':total_2014,'2015':total_2015,'2016':total_2016,'2017':total_2017,'2018':total_2018,'2019':total_2019, '2020':total_2020,  }
years = list(data.keys())
emissions = list(data.values())
table = {'Year':years, 'emissions':emissions}
emissions_df = pd.DataFrame(table)


#json
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/jazminyuen/GHG_emissions/vanessa/basins_map/static/basins.json') as response:
    basins = json.load(response)


# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

controls = dbc.FormGroup(
    [
        html.P('Select Year', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown',
            options=[{
                'label': '2011',
                'value': 'total_emissions_2011'
            }, {
                'label': '2012',
                'value': 'total_emissions_2011'
            },
                {
                    'label': '2013',
                    'value': 'total_emissions_2013'
                }
            ],
            value=['value1'],  # default value
            multi=True
        ),
        # html.Br(),
        # html.P('Range Slider', style={
        #     'textAlign': 'center'
        # }),
        # dcc.RangeSlider(
        #     id='range_slider',
        #     min=0,
        #     max=20,
        #     step=0.5,
        #     value=[5, 15]
        # ),
        html.P('Select Sectors', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.Checklist(
            id='check_list',
            options=[{
                'label': 'Power Plants',
                'value': 'df.loc[df[industry_type_sector] == Power Plants]'
            },
                {
                    'label': 'Waste',
                    'value': 'df.loc[df[industry_type_sector] == Power Plants]'
                },
                {
                    'label': 'Petroleum and Natural Gas Systems',
                    'value': 'df.loc[df[industry_type_sector] == Power Plants]'
                }
            ],
            value=['value1', 'value2'],
            inline=True
        )]),
        # html.Br(),
        # html.P('Radio Items', style={
        #     'textAlign': 'center'
        # }),
        # dbc.Card([dbc.RadioItems(
        #     id='radio_items',
        #     options=[{
        #         'label': 'Value One',
        #         'value': 'value1'
        #     },
        #         {
        #             'label': 'Value Two',
        #             'value': 'value2'
        #         },
        #         {
        #             'label': 'Value Three',
        #             'value': 'value3'
        #         }
        #     ],
        #     value='value1',
        #     style={
        #         'margin': 'auto'
        #     }
        # )]),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        ),
    ]
)

sidebar = html.Div(
    [
        html.H2('Select Data to Display', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['greenhouse gases trap heat in our atmosphere'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=['The most abundant greenhouse gases are Carbon Dioxide, Methane, Nitrous Oxide, and Fluorinated Gases'], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_2', children=['In 2020, U.S. CO2 emissions totaled 5,222 million metric tons of carbon dioxide equivalents'],className='card-title', style=CARD_TEXT_STYLE),
                        html.P(['CO2 emissions have decreased by 10.3 percent from 2019 to 2020'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_3', children=['Almost all of the increase of greenhouse gases in the atmosphere over the last 150 years is due to human activity'], className='card-title', style=CARD_TEXT_STYLE),
                        html.P(['The largest sources of emissions are from Transportation, Industry, and Electricity'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_4', children=['Global average temperatures have increased by about 1.8 degrees F'],className='card-title', style=CARD_TEXT_STYLE),
                        html.P('Even a small increase in average temperature has climate change impacts and cause extreme weather events. Floods, droughts, and severe head waves all are more likely to occur with climate change', style=CARD_TEXT_STYLE),
                    ]
                ),
            ]
        ),
        md=3
    )
])
fig1 = px.bar(emissions_df, x='Year', y='emissions')
content_second_row = dbc.Row(
    [
        dbc.Col(
            
            dcc.Graph(figure=fig1), md=6,
            
        ),
        dbc.Col(
            dcc.Graph(id='graph_2'), md=6
        ),
        # dbc.Col(
        #     dcc.Graph(id='graph_3'), md=4
        # )
    ]
)

mapfig = px.scatter_geo(basins, locations="type")

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(figure = mapfig), md=12,
        )
    ]
)

# content_fourth_row = dbc.Row(
#     [
#         dbc.Col(
#             dcc.Graph(id='graph_5'), md=6
#         ),
#         dbc.Col(
#             dcc.Graph(id='graph_6'), md=6
#         )
#     ]
# )

content = html.Div(
    [
        html.H2('Greenhouse Gas Emissions Dashboard', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        content_second_row,
        content_third_row,
        # content_fourth_row
    ],
    style=CONTENT_STYLE
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])



# @app.callback(
#     Output("graph", "figure"), 
#     Input("dropdown", "value"))
# def update_bar_chart(day):
#     df = df # replace with your own data source
#     fig = px.bar(df, x="industry_type_sector", y="total_emissions_2020", 
#                  color='rgb(158,202,225)', barmode="group")
#     return fig




@app.callback(
    Output('graph_1', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('check_list', 'value'),
     ])
def update_graph_1(n_clicks, dropdown_value, check_list_value):
    print(n_clicks)
    print(dropdown_value)
    print(check_list_value)
    fig = px.bar(df, x=check_list_value, y=dropdown_value)
    return fig


# @app.callback(
#     Output('graph_2', 'figure')
#     [Input('submit_button', 'n_clicks')]
#     # [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#     #  State('radio_items', 'value')
#      )
# def update_graph_2(n_clicks, check_list_value):
#     print(n_clicks)
#     # print(dropdown_value)
#     # print(range_slider_value)
#     # print(check_list_value)
#     # print(radio_items_value)
#     fig = px.bar(emissions_df, x='Year', y='emissions')
#     return fig


# @app.callback(
#     Output('graph_3', 'figure'),
#     [Input('submit_button', 'n_clicks')],
#     [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#      State('radio_items', 'value')
#      ])
# def update_graph_3(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#     print(n_clicks)
#     print(dropdown_value)
#     print(range_slider_value)
#     print(check_list_value)
#     print(radio_items_value)
#     df = px.data.iris()
#     fig = px.density_contour(df, x='sepal_width', y='sepal_length')
#     return fig


# @app.callback(
#     Output('graph_4', 'figure'),
#     [Input('submit_button', 'n_clicks')],
#     [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#      State('radio_items', 'value')
#      ])
# def update_graph_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#     print(n_clicks)
#     print(dropdown_value)
#     print(range_slider_value)
#     print(check_list_value)
#     print(radio_items_value)  # Sample data and figure
#     df = px.data.gapminder().query('year==2007')
#     fig = px.scatter_geo(df, locations='iso_alpha', color='continent',
#                          hover_name='country', size='pop', projection='natural earth')
#     fig.update_layout({
#         'height': 600
#     })
#     return fig


# @app.callback(
#     Output('graph_5', 'figure'),
#     [Input('submit_button', 'n_clicks')],
#     [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#      State('radio_items', 'value')
#      ])
# def update_graph_5(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#     print(n_clicks)
#     print(dropdown_value)
#     print(range_slider_value)
#     print(check_list_value)
#     print(radio_items_value)  # Sample data and figure
#     df = px.data.iris()
#     fig = px.scatter(df, x='sepal_width', y='sepal_length')
#     return fig


# @app.callback(
#     Output('graph_6', 'figure'),
#     [Input('submit_button', 'n_clicks')],
#     [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#      State('radio_items', 'value')
#      ])
# def update_graph_6(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#     print(n_clicks)
#     print(dropdown_value)
#     print(range_slider_value)
#     print(check_list_value)
#     print(radio_items_value)  # Sample data and figure
#     df = px.data.tips()
#     fig = px.bar(df, x='total_bill', y='day', orientation='h')
#     return fig


# @app.callback(
#     Output('card_title_1', 'children'),
#     [Input('submit_button', 'n_clicks')],
#     [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#      State('radio_items', 'value')
#      ])
# def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#     print(n_clicks)
#     print(dropdown_value)
#     print(range_slider_value)
#     print(check_list_value)
#     print(radio_items_value)  # Sample data and figure
#     return 'Card Tile 1 change by call back'


# @app.callback(
#     Output('card_text_1', 'children'),
#     [Input('submit_button', 'n_clicks')],
#     [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#      State('radio_items', 'value')
#      ])
# def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#     print(n_clicks)
#     print(dropdown_value)
#     print(range_slider_value)
#     print(check_list_value)
#     print(radio_items_value)  # Sample data and figure
#     return 'Card text change by call back'


if __name__ == '__main__':
    app.run_server(port='8085')