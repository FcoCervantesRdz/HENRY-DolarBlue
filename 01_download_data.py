import pandas as pd
from my_functions import get_simple_table

# Importamos en DataFrame las tablas necesarias
usd_b = get_simple_table('usd') # Valor del dolar blue en soles
usd_o = get_simple_table('usd_of') # Valor del dolar oficial en soles
events = get_simple_table('milestones') # eventos importantes

# Exportamos en csv
usd_b.to_csv('API_tables/usd_b.csv', index = False)
usd_o.to_csv('API_tables/usd_o.csv', index = False)
events.to_csv('API_tables/events.csv', index = False)

print('Tablas importadas con éxito')
input() # Pausa para ver el mensaje