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
    html.H4('Average emissions by year'),
    dcc.Graph(id="graph"),
    dcc.Dropdown(id="dropdown", options=["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]),
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
                                "total_emissions_2020"]])
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
                                "total_emissions_2020":"2020"})
# Create summary df
summary = em_df.describe()
summary_df = pd.DataFrame(summary)
summary_df = summary_df.transpose()
summary_df["sum"] = em_df.sum().to_list()


# Create callback
@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
def update_line_chart(continents):
    df = summary_df # replace with your own data source
    #mask = df.continent.isin(continents)
    fig = px.line(df,y="mean")
    return fig


app.run_server(debug=True)