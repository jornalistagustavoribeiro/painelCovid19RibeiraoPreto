# importing libraries

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# reading the dataset with the specified header by brasil.io

url = "https://brasil.io/api/dataset/covid19/caso_full/data/?city=Ribeir%C3%A3o+Preto&format=json"
headers = {"User-Agent": "python-urllib"}
r = requests.get(url, headers=headers)

# get only the column "results" from the json into a dataframe

caso_full = pd.DataFrame(r.json()["results"])

# cleaning dataframe and renaming the columns

caso_full = caso_full.drop(
    ['city', 'city_ibge_code', 
     'epidemiological_week', 
     'estimated_population_2019', 
     'is_last', 'is_repeated', 
     'last_available_confirmed_per_100k_inhabitants', 
     'last_available_date', 
     'last_available_death_rate', 
     'order_for_place', 
     'place_type', 
     'state'], axis=1)

# creating table

tabela = caso_full.drop(['new_confirmed', 'new_deaths'], axis=1)
tabela = tabela.rename(columns={'date':'Data', 
                                'last_available_confirmed':'Casos', 
                                'last_available_deaths':'Mortes'})
tabelaMostra = go.Figure(data=[go.Table(header=dict(values=list(tabela.columns)), 
                                        cells=dict(values=[tabela.Data, 
                                                           tabela.Casos, 
                                                           tabela.Mortes]))])

# creating charts

casosDia = px.bar(caso_full, x="date", y="new_confirmed", 
                  labels={"date":"Dia", "new_confirmed":"Total"}, 
                  title="Casos por dia")

mortesDia = px.bar(caso_full, x="date", y="new_deaths", 
                   labels={"date":"Dia", "new_deaths":"Total"}, 
                   title="Mortes por dia")

# creating dash app

app = dash.Dash(__name__)
app.title = 'Covid-19 Ribeirão Preto'

app.layout = html.Div([
    html.Div('Atualizações sobre a pandemia de Covid-19 em Ribeirão Preto', 
              style={'textAlign':'center'}),
    html.Div([dcc.Graph(id='Últimas atualizações', figure=tabelaMostra)]), 
    html.Div([dcc.Graph(id="Casos por dia", figure=casosDia)]), 
    html.Div([dcc.Graph(id="Mortes por dia", figure=mortesDia)]),
    html.Div('Desenvolvido por Gustavo Ribeiro; https://github.com/jornalistagustavoribeiro/PainelCovid19RibeiraoPreto', 
              style={'textAlign':'center'})
])

if __name__ == '__main__':
    app.run_server(debug=True)

