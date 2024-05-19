import requests
from datetime import datetime, timedelta

def get_dolar_data():
    yesterday = datetime.now() - timedelta(days=2)
    day = yesterday.day
    month = yesterday.month
    year = yesterday.year
    url = f"https://api.cmfchile.cl/api-sbifv3/recursos_api/dolar/{year}/{month}/dias/{day}?apikey=cff8592ff8e2a57cf5441f179e68077246b81141&formato=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

data = get_dolar_data()
if data is not None:
    dolar_value = data['Dolares'][0]['Valor']
    print(dolar_value)
else:
    print("Error al obtener los datos")

