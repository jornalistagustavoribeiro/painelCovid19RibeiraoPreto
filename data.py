# importing libraries

import pandas as pd
import requests
import sqlalchemy
import psycopg2

# reading the dataset with the specified header by brasil.io

url = "https://brasil.io/api/dataset/covid19/caso_full/data/?city=Ribeir%C3%A3o+Preto&format=json"
headers = {"User-Agent": "python-urllib"}
r = requests.get(url, headers=headers)

# get only the column "results" from the json into a dataframe

caso_full = pd.DataFrame(r.json()["results"])

# cleaning dataframe

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

# adding moving average

caso_full['mediaMovelCasos'] = caso_full.rolling(window=7)['new_confirmed'].mean()
caso_full['mediaMovelMortes'] = caso_full.rolling(window=7)['new_deaths'].mean()

# creating the table dataframe

tabela = caso_full.drop(
    ['new_confirmed',
     'new_deaths',
     'mediaMovelCasos',
     'mediaMovelMortes'], axis=1)

tabela = tabela.rename(columns=
                       {'date':'Data', 
                        'last_available_confirmed':'Casos', 
                        'last_available_deaths':'Mortes'})

# saving to database

engine = sqlalchemy.create_engine("postgres://wctkjwkwhxdjwt:1dfdd5d327207ab6016a843ca30138a6b6da831769cabee2becc138242e6d1a4@ec2-54-90-68-208.compute-1.amazonaws.com:5432/dfoo06e5oo512s")
conexao = engine.connect()
caso_full.to_sql('caso_full', conexao, index=False, if_exists='append')
tabela.to_sql('tabela', conexao, index=False, if_exists='append')
conexao.close()
