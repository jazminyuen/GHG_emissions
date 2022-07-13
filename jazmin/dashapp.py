# import dependencies
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy import text
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# connect to database and query data
db_string = 'postgresql://ghg_emissions:Password00@ghgemissions.cg3dqiowwhnr.us-west-1.rds.amazonaws.com:5432/ghg_data'
engine = create_engine(db_string)

# query for sector emissions bar chart
query = text('SELECT * FROM sector_emissions')
sector_df = pd.read_sql(query,engine)
sector_df = sector_df.rename(columns={"_2011":"2011","_2012":"2012","_2013":"2013","_2014":"2014","_2015":"2015","_2016":"2016","_2017":"2017","_2018":"2018","_2019":"2019","_2020":"2020","sector":"Sector"})

# query for total emissions summary line chart
query_summary = text('SELECT * FROM summary')
summary_df = pd.read_sql(query_summary, engine)

# query for total emissions by year bar chart
query = text('SELECT * FROM direct_emissions')
df = pd.read_sql(query,engine)
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

# create the datasets for total emissions by year bar chart
data = {'2011':total_2011, '2012':total_2012, '2013':total_2013, '2014':total_2014,'2015':total_2015,'2016':total_2016,'2017':total_2017,'2018':total_2018,'2019':total_2019, '2020':total_2020,  }
years = list(data.keys())
emissions = list(data.values())
table = {'Year':years, 'emissions':emissions}
emissions_df = pd.DataFrame(table)

# figure - total emissions by year bar chart
fig1 = px.bar(emissions_df, x='Year', y='emissions', title="Total Direct Emissions by Year", labels={"emissions":"Emissions"}, color="emissions", color_continuous_scale='ylorrd')
fig1.update_traces( marker_line_width=3.0, opacity=0.8)

# create the datasets for ml figure
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

# figure - total emissions by sector by class scatter plot
mlfig = px.scatter(data_frame=direct_emitters_total, x="total_emissions", y="industry_type_sector", color="class",
           size="total_emissions", color_discrete_sequence=["gold", "darkorange", "red"],
                           labels={
                     "total_emissions": "Total Emissions (metric tons CO2 equivalent)",
                     "industry_type_sector": "Industry Type (Sector)"
                 },
                title="Direct Emitters Classification Model", size_max=35, opacity=0.7)

# figure - total emissions by sector by class 3D scatter plot
fig3d = px.scatter_3d(direct_emitters_total, x="total_emissions", y="industry_type_sector", z="class", color="class", title="Direct Emitters Classification Model 3D",
           color_discrete_sequence=["yellow", "orange", "red"],
           labels={
                     "total_emissions": "Total Emissions (metric tons CO2 equivalent)",
                     "industry_type_sector": "Industry Type (Sector)"},
                      width=800)
fig3d.update_layout(legend=dict(x=0,y=1))


# app design

# the style arguments for the sidebar
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#608B74'
}

SIDE_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#FFFFFF'
}

# the style arguments for the main content page
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'margin-top': '2%',
    'margin-bottom': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#608B74'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#608B74'
}




# sidebar layout
sidebar = html.Div(
    [
        html.H3('About the Data', style=SIDE_TEXT_STYLE),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.P(id = 'bar_text_1', children = ['The U.S. Environmental Protection Agency’s Greenhouse Gas Reporting Program (GHGRP) requires the reporting of facilities from 2011-2020 that are considered direct, large-emitting sources of greenhouse gases, or those emitting 25,000 metric tons or more of carbon dioxide equivalent per year. The program estimates that this covers 85 to 90 percent of total U.S. greenhouse gas emissions from more than 8,000 facilities.'],  style=CARD_TEXT_STYLE)
                    ]
                )
            ]
        )
    ],
    style=SIDEBAR_STYLE,
)

# first row layout
content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['Greenhouse gases trap heat in our atmosphere'], className='card-title',
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
                        html.H4(id='card_title_3', children=['In 2020, U.S. Carbon Dioxide emissions totaled 5,222 million metric tons of CO2e'],className='card-title', style=CARD_TEXT_STYLE),
                        html.P(['CO2 emissions have decreased by 10.3 percent from 2019 to 2020'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
            dcc.Graph(figure = fig1), md=6
        ),

])

# second row layout
content_second_row = dbc.Row(
    [
        dbc.Col(
            
            dcc.Graph(figure=fig3d), md=6,
            
        ),
        dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_2', children=['The largest sources of emissions are from Transportation, Industry, and Electricity'],className='card-title', style=CARD_TEXT_STYLE),
                        html.P(['Almost all of the increase of greenhouse gases in the atmosphere over the last 150 years is due to human activity'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=6
    ),
    ])

# third row layout
content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(figure = mlfig), md=12,
        ),
    ]
)

# fourth row layout
content_fourth_row = dbc.Row(
     [
        dbc.Col(
        html.Div([
        html.H4(),
        dcc.Graph(id="emissionsgraph"),
        dcc.Checklist(id="checklist", options=["mean","median","sum"])
])
        )
    ]
)

# fifth row layout
content_fifth_row = dbc.Row(
     [
        dbc.Col(
        html.Div([
        html.H4(),
        dcc.Graph(id="sectorgraph"),
        dcc.Dropdown(id="dropdown2", options=['Power Plants', 'Waste', 'Other', 'Petroleum and Natural Gas Systems',
        'Minerals', 'Chemicals', 'Metals', 'Pulp and Paper', 'Other,Waste','Pulp and Paper,Waste',
        'Natural Gas and Natural Gas Liquids Suppliers,Petroleum and Natural Gas Systems',
        'Petroleum Product Suppliers,Refineries'])
])
        )
    ]
)

# content holds set layout and style variables
content = html.Div(
    [
        html.H1('Greenhouse Gas Emissions Dashboard', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        content_third_row,
        content_second_row,
        content_fourth_row,
        content_fifth_row
    ],
    style=CONTENT_STYLE
)

# initialize app with set layouts
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])


# create callback to update total emissions summary line chart
@app.callback(
    Output("emissionsgraph", "figure"), 
    Input("checklist", "value"))
def update_summary_chart(value):
    df = summary_df
    year = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019','2020'] 
    fig = px.line(df, x=year, y=value, markers=True, color_discrete_sequence=["gold", "darkorange", "red"], labels=dict(value="Total Emissions (metric tons CO2 equivalent)", x="Year", variable="Metric"), title="Total Emissions Summary")
    fig.update_traces( marker_line_width=3.0, opacity=0.8)
    return fig

# create callback to update sector emissions bar chart
@app.callback(
    Output("sectorgraph", "figure"), 
    Input("dropdown2", "value"))
def update_sector_chart(sector):
    df = sector_df.loc[sector_df["Sector"]==sector]
    df.drop(["Sector"], axis=1, inplace=True)
    sum = df.sum(axis=0).tolist()
    year = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
       '2020'] 
    fig = px.bar(x=year,y=sum, color= sum, color_continuous_scale='ylorrd', title=f'Emissions by Sector: {sector}',labels={'y':'Total Emissions (metric tons CO2 equivalent)', 'x':'Year'})
    fig.update_traces(marker_line_width=2.5, opacity=0.8)
    return fig


# run app
if __name__ == '__main__':
    app.run_server(port='8085')