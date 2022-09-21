import requests
import pandas as pd
import numpy as np
import datetime as dt

def get_table(table_name):
    # Pedimos json a API
    url = 'https://api.estadisticasbcra.com/' + table_name
    headers = {
        'Accept' : 'aplication/json',
        'Authorization' : 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTEwMDc3NjEsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJmY28uY2VydmFudGVzcmR6QGdtYWlsLmNvbSJ9.NhjESd0FNSiuvG5h3B0bIqz8SoskFTbeRmyZwNeCUzUE60o3HrXIfxk2rvUsBdtFGuaOUR0wq9vPoep5N2loXw'
        }
    response = requests.get(url, headers = headers)

    # Convertimos json a DataFrame
    table =  pd.DataFrame(response.json())
    table.rename(columns= {'d': 'date', 'v': 'value'}, inplace= True)   # Cambiamos nombres de columnas   
    if table_name == 'milestone':
        table.rename(columns= {'t': 'type_event'}, inplace= True) #Milestone tiene el parámetro 't'
    
    # La comlumna 'date' la convertimos a formato date de pandas
    table['date'] = pd.to_datetime(table['date'])
    return table

def get_simple_table(table_name):
        # Pedimos json a API
    url = 'https://api.estadisticasbcra.com/' + table_name
    headers = {
        'Accept' : 'aplication/json',
        'Authorization' : 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTEwMDc3NjEsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJmY28uY2VydmFudGVzcmR6QGdtYWlsLmNvbSJ9.NhjESd0FNSiuvG5h3B0bIqz8SoskFTbeRmyZwNeCUzUE60o3HrXIfxk2rvUsBdtFGuaOUR0wq9vPoep5N2loXw'
        }
    response = requests.get(url, headers = headers)

    # Convertimos json a DataFrame
    return pd.DataFrame(response.json())

def fill_missing_values(dataframe, columns):
    '''Esta función toma un DataFrame como argumento, para rellenar valores faltantes en las columnas especificadas.

       Para rellenar los valores faltantes, esta función verifica el anterior y el siguiente valor no faltante y 
       utiliza esta información para calcular el o los valores faltantes permitiendo así generar un comportamiento
       lineal entre los dos valores no faltantes.'''
    dataframe = dataframe.copy()
    for col in columns:
        faltantes = dataframe[dataframe[col].isna()]
        max_index = len(dataframe)-1
        min_index = 0
        for index in faltantes.index:
            index_after = index
            while index_after in faltantes.index:
                if index_after == max_index:
                    index_after = None
                    break
                index_after += 1
            index_before = index
            while index_before in faltantes.index:
                if index_before == min_index:
                    index_before = None
                    break
                index_before -= 1
            if index_before:
                value_before = dataframe.loc[index_before][col]
            else:
                value_before = None
            if index_after:
                value_after = dataframe.loc[index_after][col]
            else:
                value_before = None
            if not value_before:
                actual_value = value_after
            elif not value_after:
                actual_value = value_before
            else:
                actual_value = value_before + (value_after-value_before)/(index_after-index_before)*(index-index_before)
            dataframe.loc[index,col] = actual_value
    return dataframe

def add_variation(table, colums):
    table = table.copy()
    for col in colums:
        volatilidad = np.array([])
        for index in table.index:
            if index == 0:
                volatilidad = np.append(volatilidad, 0)
                continue
            vol = (table.loc[index, col]/table.loc[index-1, col]-1) * 100
            volatilidad = np.append(volatilidad, vol)
        table[col + '_var'] = volatilidad
    return table

def date_to_x(date, date_0):
    date = dt.datetime.toordinal(date)
    x_i =  date - dt.datetime.toordinal(date_0)
    if x_i < 0:
        return np.nan
    return x_i**2

def x_to_date(x, date_0):
    x = int(x**0.5)
    date = x + dt.datetime.toordinal(date_0)
    return dt.datetime.fromordinal(date)
