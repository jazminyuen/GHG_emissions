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
app.layout = html.Div([
    html.H4('Emissions by Top Sectors'),
    dcc.Graph(id="graph"),
    dcc.Dropdown(id="dropdown", options=['Power Plants', 'Waste', 'Other', 'Petroleum and Natural Gas Systems',
       'Minerals', 'Chemicals', 'Metals', 'Pulp and Paper', 'Other,Waste','Pulp and Paper,Waste',
       'Natural Gas and Natural Gas Liquids Suppliers,Petroleum and Natural Gas Systems',
       'Petroleum Product Suppliers,Refineries']),
])

# Connect to database
db_string = 'postgresql://ghg_emissions:Password00@ghgemissions.cg3dqiowwhnr.us-west-1.rds.amazonaws.com:5432/ghg_data'
engine = create_engine(db_string)
query = text('SELECT * FROM direct_emissions')
df = pd.read_sql(query,engine)
# Create emissions df
em_df = pd.DataFrame(df[["total_emissions_2011",
                                "total_emissions_2012",
                                "total_emissions_2013",
                                "total_emissions_2014",
                                "total_emissions_2015",
                                "total_emissions_2016",
                                "total_emissions_2017",
                                "total_emissions_2018",
                                "total_emissions_2019",
                                "total_emissions_2020",
                                "industry_type_sector"]])
# Rename columns
em_df = em_df.rename(columns={"total_emissions_2011":"2011",
                                "total_emissions_2012":"2012",
                                "total_emissions_2013":"2013",
                                "total_emissions_2014":"2014",
                                "total_emissions_2015":"2015",
                                "total_emissions_2016":"2016",
                                "total_emissions_2017":"2017",
                                "total_emissions_2018":"2018",
                                "total_emissions_2019":"2019",
                                "total_emissions_2020":"2020",
                                 "industry_type_sector":"Sector"})



# Create callback
@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
def update_line_chart(sector):
    df = em_df.loc[em_df["Sector"]==sector]
    df.drop(["Sector"], axis=1, inplace=True)
    sum = df.sum(axis=0).tolist()
    year = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
       '2020'] 
    #mask = df.year.isin(year)
    fig = px.bar(x=year,y=sum,title=f'Emissions by Sector: {sector}',labels={'y':'Emissions', 'x':'Year'})
    return fig


app.run_server(debug=True)