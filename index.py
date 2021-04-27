import dash
import dash_auth
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

auth_enable = False
# Data Exploration with pandas
# ---------------------------------------
PATH = "resources/vgsales.csv"
df = pd.read_csv(PATH)
# # print(df[:5])
# print((df.Genre.nunique()))
# print((df.Genre.unique()))
# print(sorted(df.Year.unique()))
#
# Data Visulsation with Plotly
# ---------------------------------------

fig_pie = px.histogram(data_frame=df,x="Year",y="North American Sales")
# fig_pie.show()


# Dash Start up
# ---------------------------------------
app = dash.Dash(__name__)

# app = dash.Dash(__name__,
#                 external_stylesheets=[dbc.themes.LITERA])
# https://bootswatch.com/ for more options

# Basic Authentication
# ---------------------------------------
if auth_enable:
    auth = dash_auth.BasicAuth(app,
                               {'Cadia': 'Moly',
                                'Admin': "Admin"})

app.layout = html.Div([
    html.H1("Graph Anaylsis with some random Data"),
    dbc.Button("Success",color="success",className="mr-1"),
    dcc.Dropdown(id='genre-choice',
                 options=[{'label':x, 'value':x}
                          for x in sorted(df.Genre.unique())],
                 value="Sports"
                 ),
    dcc.Graph(id='my-graph', figure={})

])
#test

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id="genre-choice", component_property="value")
)
def interactive_graphing(value_genre):
    dff = df[df.Genre == value_genre]
    fig = px.bar(data_frame=dff, x = 'Year', y = "World Sales")
    return fig


if __name__ =="__main__":
    app.run_server()