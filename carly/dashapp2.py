
#import dependencies

from itertools import dropwhile
from tkinter.tix import CheckList
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
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sqlalchemy import text
from dash import Dash, dcc, html, Input, Output




#connect to database
db_string = 'postgresql://ghg_emissions:Password00@ghgemissions.cg3dqiowwhnr.us-west-1.rds.amazonaws.com:5432/ghg_data'
engine = create_engine(db_string)

query = text('SELECT * FROM direct_emissions')

df = pd.read_sql(query,engine)


# creating the datasets
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

data = {'2011':total_2011, '2012':total_2012, '2013':total_2013, '2014':total_2014,'2015':total_2015,'2016':total_2016,'2017':total_2017,'2018':total_2018,'2019':total_2019, '2020':total_2020,  }
years = list(data.keys())
emissions = list(data.values())
table = {'Year':years, 'emissions':emissions}
emissions_df = pd.DataFrame(table)


#jazmin summary data

query2 = text('SELECT * FROM sector_emissions')
df1 = pd.read_sql(query2,engine)
# Rename columns
em_df = df1.rename(columns={"_2011":"2011","_2012":"2012","_2013":"2013","_2014":"2014","_2015":"2015","_2016":"2016","_2017":"2017","_2018":"2018","_2019":"2019","_2020":"2020","sector":"Sector"})
# Get summary table
query_summary = text('SELECT * FROM summary')
summary_df = pd.read_sql(query_summary, engine)
print(summary_df)




#vanessa ml figure

direct_emitters_df = df[['industry_type_sector', 'total_emissions_2020', 'total_emissions_2019', 'total_emissions_2018',
       'total_emissions_2017', 'total_emissions_2016', 'total_emissions_2015',
       'total_emissions_2014', 'total_emissions_2013', 'total_emissions_2012',
       'total_emissions_2011']]

direct_emitters_df['total_emissions'] = direct_emitters_df.sum(axis=1, numeric_only=True)
direct_emitters_total = direct_emitters_df[['industry_type_sector', 'total_emissions']]
industry_counts = direct_emitters_total.industry_type_sector.value_counts()
replace_industry = list(industry_counts[industry_counts < 100].index)

for industry in replace_industry:
    direct_emitters_total.industry_type_sector = direct_emitters_total.industry_type_sector.replace(industry,"Other")

industry_num = {
   "Other": 1,
   "Power Plants": 2,
   "Waste": 3,
   "Petroleum and Natural Gas Systems": 4,
   "Minerals": 5,
   "Chemicals": 6,
   "Metals": 7,
   "Pulp and Paper": 8,
}
direct_emitters_total["industry_type_sector"] = direct_emitters_total["industry_type_sector"].apply(lambda x: industry_num[x])
scaler = StandardScaler()
scaler.fit(direct_emitters_total)
scaled_data = scaler.transform(direct_emitters_total)
transformed_scaled_data = pd.DataFrame(scaled_data, columns=direct_emitters_total.columns)

# Find the best value for K
inertia = []
k = list(range(1, 11))

# Calculate the inertia for the range of K values
for i in k:
    km = KMeans(n_clusters=i, random_state=0)
    km.fit(direct_emitters_total)
    inertia.append(km.inertia_)

model = KMeans(n_clusters=3, random_state=5)
model.fit(direct_emitters_total)

direct_emitters_total["class"] = model.labels_
industry_name = {
   "1": "Other",
   "2": "Power Plants",
   "3": "Waste",
   "4": "Petroleum and Natural Gas Systems",
   "5":"Minerals",
   "6": "Chemicals",
   "7": "Metals",
   "8": "Pulp and Paper",
}

direct_emitters_total["industry_type_sector"] = direct_emitters_total["industry_type_sector"].astype(str)
direct_emitters_total["industry_type_sector"] = direct_emitters_total["industry_type_sector"].apply(lambda x: industry_name[x])
direct_emitters_total['class'] = direct_emitters_total['class'].replace(['0','1','2'],['Low','Mid','High'])
direct_emitters_total["class"] = direct_emitters_total["class"].astype(str)






#json
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/jazminyuen/GHG_emissions/vanessa/basins_map/static/basins.json') as response:
    basins = json.load(response)







# app design

# # the style arguments for the sidebar.
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
        html.P('Dropdown', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown',
            options=['Power Plants', 'Waste', 'Other', 'Petroleum and Natural Gas Systems',
       'Minerals', 'Chemicals', 'Metals', 'Pulp and Paper', 'Other,Waste','Pulp and Paper,Waste',
       'Natural Gas and Natural Gas Liquids Suppliers,Petroleum and Natural Gas Systems',
       'Petroleum Product Suppliers,Refineries'],
            value=['Power Plants'],  # default value
            multi=True
        ),

        html.P('Check list', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.Checklist(
            id='check_list',
                        options=[{
                'label': 'mean',
                'value': summary_df['mean']
            },
                {
                    'label': 'median',
                    'value': summary_df['median']
                },
                {
                    'label': 'sum',
                    'value': summary_df['median']
                }
            ],
            value=[summary_df['mean']],
            inline=True
        )]),
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





defig = px.bar(emissions_df, x='Year', y='emissions', title="Total Direct Emissions by Year", color='emissions')
mlfig = px.scatter(data_frame=direct_emitters_total, x="total_emissions", y="industry_type_sector", color="class",
           size="total_emissions", color_discrete_sequence=["gold", "darkorange", "red"],
                           labels={
                     "total_emissions": "Total Emissions (metric tons CO2 equivalent)",
                     "industry_type_sector": "Industry Type (Sector)",
                 },
                title="Direct Emitters Classification Model", size_max=35, opacity=0.7)
fig3d = px.scatter_3d(direct_emitters_total, x="total_emissions", y="industry_type_sector", z="class", color="class",
           color_discrete_sequence=["yellow", "orange", "red"], width=800)
fig3d.update_layout(legend=dict(x=0,y=1))


content_second_row = dbc.Row(
    [
        dbc.Col(
            
            dcc.Graph(figure=defig), md=6,
            
        ),
        dbc.Col(
            dcc.Graph(figure = fig3d), md=6
        ),
    ])

  

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(figure = mlfig), md=12,
        ),
    ]
)
app = Dash(__name__)

sector = ['Power Plants', 'Waste', 'Other', 'Petroleum and Natural Gas Systems',
       'Minerals', 'Chemicals', 'Metals', 'Pulp and Paper', 'Other,Waste','Pulp and Paper,Waste',
       'Natural Gas and Natural Gas Liquids Suppliers', 'Petroleum and Natural Gas Systems',
       'Petroleum Product Suppliers, Refineries']
secdf = em_df #.loc[em_df["Sector"]== sector]
secdf.drop(["Sector"], axis=1, inplace=True)
sum = secdf.sum(axis=0).tolist()
year = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019','2020'] 
mean = df.mean(axis=0).tolist()
sectorfig = px.bar(x=year,y=sum,title=f'Emissions by Sector: {sector}',labels={'y':'Emissions', 'x':'Year'})
sectorfig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)





# content_fourth_row = dbc.Row(
#     [
#         dbc.Col(
#             html.H4('Emissions by Top Sectors'),
#             dcc.Graph(figure = sectorfig, id="sectorgraph"), md=12,
#         ),
#     ]
# )
emissionsfig = px.line(summary_df, x="year", y='mean', labels={"year":"Year", "value":'mean'})
emissionsfig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

content_fifth_row = dbc.Row(
    [
        dbc.Col(
            html.H4('Emissions by Top Sectors'),
            dcc.Graph(figure = emissionsfig, id="emissionsgraph"), md=12,
        ),
    ]
)    


# content_fourth_row = dbc.Row(
#     [
#         dbc.Col(html.H4('Total Emissions Stats')),
#         dbc.Col(html.H4(dcc.Checklist(["mean","median","sum"]))),
#         dbc.Col(html.H4(dcc.Graph(update_summary_chart('value'))))
        
#         ["mean"])
#     ]
# )
# content_fourth_row = dbc.Row(
#     dbc.Col(html.Div(
#             [
#             html.H4('Total Emissions Stats'),
#             dcc.Graph(id="graph6"),
#             dcc.Checklist(id="checklist6", options=["mean","median","sum"])
#              ]
#                         ),
                    
#                 )
#                 md=12
#             )


# @app.callback(
#     Output("graph6", "figure"), 
#     Input("checklist6", "value"))
# def update_summary_chart(value):
#     df6 = summary_df
#     fig6 = px.line(df6, x="year", y=value, labels={"year":"Year", "value":f"{value}"})
#     fig6.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
#                   marker_line_width=1.5, opacity=0.6)
#     return fig6

content = html.Div(
    [
        html.H2('Greenhouse Gas Emissions Dashboard', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        content_second_row,
        content_third_row,
        content_fifth_row,

    ],
    style=CONTENT_STYLE
)



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([content])


app.layout = html.Div([sidebar, content])




# @app.callback(
#     Output("chart", "figure"), 
#     Input("dropdown2", "value"))
# def update_line_chart(continents):
#     df = summary_df 
#     #mask = df.continent.isin(continents)
#     fig = px.line(df,y="mean")
#     return fig


# @app.callback(
#     Output("chart", "figure"), 
#     Input("dropdown2", "value"))
# def update_sector_chart(sector):
#     df = em_df.loc[em_df["Sector"]==sector]
#     df.drop(["Sector"], axis=1, inplace=True)
#     sum = df.sum(axis=0).tolist()
#     year = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
#        '2020'] 
#     # mean = df.mean(axis=0).tolist()
#     fig = px.bar(x=year,y=sum,title=f'Emissions by Sector: {sector}',labels={'y':'Emissions', 'x':'Year'})
#     fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
#                   marker_line_width=1.5, opacity=0.6)
#     return fig

# @app.callback(
#     Output("emissionsgraph", "figure"), 
#     Input("checklist1", "value"))
# def update_summary_chart(value):
#     df = summary_df
#     fig = px.line(df, x="year", y=value, labels={"year":"Year", "value":f"{value}"})
#     fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
#                   marker_line_width=1.5, opacity=0.6)
#     return fig
    




# @app.callback(
#     Output('graph_1', 'figure'),
#     [Input('submit_button', 'n_clicks')],
#     [State('dropdown', 'value'), State('check_list', 'value')
#      ])
# def update_graph_1(n_clicks, dropdown_value, check_list_value):
#     print(n_clicks)
#     print(dropdown_value)
#     print(check_list_value)
#     fig = px.bar(df, x=check_list_value, y=dropdown_value)
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


if __name__ == '__main__':
    app.run_server(port='8085')