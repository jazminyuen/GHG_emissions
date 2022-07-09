# Import dependencies
from dash import Dash, dcc, html, Input, Output
import numpy as np
import pandas as pd
import plotly.express as px
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy import text

# Name app
app = Dash(__name__)

# Setup layout
# app.layout = html.Div([
#     html.H4('Emissions by Top Sectors'),
#     dcc.Graph(id="graph"),
#     dcc.Dropdown(id="dropdown", options=['Power Plants', 'Waste', 'Other', 'Petroleum and Natural Gas Systems',
#        'Minerals', 'Chemicals', 'Metals', 'Pulp and Paper', 'Other,Waste','Pulp and Paper,Waste',
#        'Natural Gas and Natural Gas Liquids Suppliers,Petroleum and Natural Gas Systems',
#        'Petroleum Product Suppliers,Refineries'])
# ])



# Connect to database
db_string = 'postgresql://ghg_emissions:Password00@ghgemissions.cg3dqiowwhnr.us-west-1.rds.amazonaws.com:5432/ghg_data'
engine = create_engine(db_string)
query = text('SELECT * FROM sector_emissions')
df = pd.read_sql(query,engine)
# Rename columns
em_df = df.rename(columns={"_2011":"2011","_2012":"2012","_2013":"2013","_2014":"2014","_2015":"2015","_2016":"2016","_2017":"2017","_2018":"2018","_2019":"2019","_2020":"2020","sector":"Sector"})
# Get summary table
query_summary = text('SELECT * FROM summary')
summary_df = pd.read_sql(query_summary, engine)

# Layout
app.layout = html.Div([
    html.H4('Total Emissions Stats'),
    dcc.Graph(id="graph"),
    dcc.Checklist(id="checklist", options=["mean","median","sum"])
])

# Create callback for emissions by sector
# @app.callback(
#     Output("graph", "figure"), 
#     Input("dropdown", "value"))
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

# Create callback for summary charts, average/median/sum overall for each year
@app.callback(
    Output("graph", "figure"), 
    Input("checklist", "value"))
def update_summary_chart(value):
    df = summary_df
    fig = px.line(df, x="year", y=value, labels={"year":"Year", "value":f"{value}"})
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
    return fig
    

app.run_server(debug=True)
