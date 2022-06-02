import plotly.express as px
from dash import Dash, dcc, html,  Input, Output
import plotly.graph_objects as go

app = Dash(__name__)

app.layout = html.Div([
 html.H4('Interactive color selection with simple Dash example'),
    html.P("Select color:"),
    dcc.Dropdown(
        id="dropdown",
        options=['Gold', 'MediumTurquoise', 'LightGreen'],
        value='Gold',
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output('graph', 'figure'),
    Input('dropdown', 'value'))
def display_value(value):
    df = px.data.iris()
    fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species', size='sepal_length')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)