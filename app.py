# importing libraries

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import requests
import sqlalchemy
import plotly.express as px
import plotly.graph_objects as go

# reading the dataset 

engine = sqlalchemy.create_engine("postgres://wctkjwkwhxdjwt:1dfdd5d327207ab6016a843ca30138a6b6da831769cabee2becc138242e6d1a4@ec2-54-90-68-208.compute-1.amazonaws.com:5432/dfoo06e5oo512s")

caso_full = pd.read_sql_query('select * from caso_full', con=engine)
tabela = pd.read_sql_query('select * from tabela', con=engine)

# creating charts

tabelaMostra = go.Figure(data=[go.Table(header=dict(values=list(tabela.columns)), 
                                        cells=dict(values=[tabela.Data, 
                                                           tabela.Casos, 
                                                           tabela.Mortes]))])

mediaCasosDia = go.Figure()

mediaCasosDia.add_trace(
    go.Scatter(
        x=caso_full["date"],
        y=caso_full["mediaMovelCasos"],
        name="Média Móvel"))

mediaCasosDia.add_trace(
    go.Bar(
        x=caso_full["date"],
        y=caso_full["new_confirmed"],
        name="Casos no dia"))

mediaMortesDia = go.Figure()

mediaMortesDia.add_trace(
    go.Scatter(
        x=caso_full["date"],
        y=caso_full["mediaMovelMortes"],
        name="Média Móvel"))

mediaMortesDia.add_trace(
    go.Bar(
        x=caso_full["date"],
        y=caso_full["new_deaths"],
        name="Mortes no dia"))

# creating dash app

app = dash.Dash(__name__)
server = app.server
app.title = 'Covid-19 Ribeirão Preto'

app.layout = html.Div([
    html.Div('Atualizações sobre a pandemia de Covid-19 em Ribeirão Preto', 
              style={'textAlign':'center'}),
    html.Div([html.A(href='mailto:jornalistagustavoribeiro@gmail.com', 
                    children="jornalistagustavoribeiro@gmail.com")],
              style={'textAlign':'center'}),
    html.Div([html.A(href='https://github.com/jornalistagustavoribeiro/PainelCovid19RibeiraoPreto', 
                    children="Github")],
              style={'textAlign':'center'}), 
    html.Div([dcc.Graph(id="casos", figure=mediaCasosDia)]), 
    html.Div([dcc.Graph(id="mortes", figure=mediaMortesDia)]),
    html.Div([dcc.Graph(id='ultimas', figure=tabelaMostra)])
])

if __name__ == '__main__':
    app.run_server()

