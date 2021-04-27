import dash
import dash_auth
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

auth_enable = False
# Data Exploration with pandas
# ---------------------------------------
PATH_TASKS = "resources/ovTasks_TestsPlanned.xlsx"
PATH_PUNCH = "resources/ovPunchlist.xlsx"
df_task = pd.read_excel(PATH_TASKS)
df_punch = pd.read_excel(PATH_PUNCH)
#print(df_punch[:5])
#print((df_punch['Workflow - Status'].nunique()))
#print((df_punch['Workflow - Status'].unique()))
#print(sorted(df_punch['Workflow - Status'].unique()))
#
# Data Visulsation with Plotly
# ---------------------------------------
#fig_pie = px.histogram(data_frame=df_punch,x="Year",y="North American Sales")
# fig_pie.show()


# Dash Start up
# ---------------------------------------
#app = dash.Dash(__name__)

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.LITERA])
# https://bootswatch.com/ for more options



# Basic Authentication
# ---------------------------------------
if auth_enable:
    auth = dash_auth.BasicAuth(app,
                               {'Cadia': 'Moly',
                                'Admin': "Admin"})
# Preconditioining of data
#----------------------------------------

# Simplify punch status to "Open" or "Closed"
df_punch.loc[df_punch['Workflow - Status'] == 'Originated', 'Workflow - Status'] = "Open"
df_punch.loc[df_punch['Workflow - Status'] == 'Submitted', 'Workflow - Status'] = "Open"
df_punch.loc[df_punch['Workflow - Status'] == 'Accepted', 'Workflow - Status'] = "Closed"
df_punch.loc[df_punch['Workflow - Status'] == 'Closed', 'Workflow - Status'] = "Closed"
df_punch.loc[df_punch['Workflow - Status'] == 'Rejected', 'Workflow - Status'] = "Closed"
#todo filter out blank items that could cause issues



# Page Layout
# ---------------------------------------
app.layout = html.Div([
    html.H1("Graph Anaylsis with some random Data"),
    dbc.Button("Success",color="success",className="mr-1"),
    dcc.Dropdown(id='Status-choice',
                 options=[{'label':x, 'value':x}
                          for x in sorted(df_punch['Punchlist Category (Name)'].unique())],
                 value="A"
                 ),
    dcc.Graph(id='my-graph', figure={})

])
# Page Interaction
# ---------------------------------------
@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id="Status-choice", component_property="value")
)
def interactive_graphing(value_status):
    dff_punch = (df_punch[df_punch['Punchlist Category (Name)'] == value_status])

    fig = px.bar(data_frame=dff_punch,
                 x = 'Discipline (Name)',
                 color= 'Workflow - Status',
                 title='This is the title',
                 barmode='group',
                 hover_data=['Punchlist ID', 'Systemization - Subsystem (Summary)', 'Asset (Summary)'])
    return fig


if __name__ =="__main__":
    app.run_server(debug=True)

