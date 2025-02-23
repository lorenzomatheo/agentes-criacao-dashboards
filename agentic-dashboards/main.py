import requests
import pandas as pd

# Configuração da API
API_KEY = '6d733a370c11db7fb913903173f0f8c4'  #chave da OpenWeather
CITIES = ['Ribeirão Preto', 'São Paulo', 'Campinas', 'Santos'] 

#armazenar os dados
weather_data = []

#Coleta de dados da API para cada cidade
for city in CITIES:
    URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=pt_br&appid={API_KEY}'
    try:
        response = requests.get(URL)
        response.raise_for_status()  #Lança erro se a requisição falhar
        data = response.json()

        #Salvar os dados coletados
        weather_info = {
            'name': city,
            'main.temp': data['main']['temp'],
            'main.humidity': data['main']['humidity'],
            'wind.speed': data['wind']['speed'],
            'main.pressure': data['main']['pressure']
        }
        weather_data.append(weather_info)
        print(f'Dados coletados com sucesso para {city}')

    except requests.exceptions.RequestException as e:
        print(f'Erro ao buscar dados para {city}: {e}')

#Transformar os dados em um DataFrame
df = pd.DataFrame(weather_data)

#Salvar os dados no diretório 'data'
output_file = 'data/processed_weather_data.csv'
df.to_csv(output_file, index=False)
print(f'Dados salvos com sucesso em {output_file}')
