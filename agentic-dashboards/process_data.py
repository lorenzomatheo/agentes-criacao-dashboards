import pandas as pd

# Carregar o arquivo de dados brutos gerado pelo main.py
raw_data_file = './data/weather_data.csv'
processed_data_file = './data/processed_weather_data.csv'

# Verificar se o arquivo de dados brutos existe
try:
    df = pd.read_csv(raw_data_file)

    # Limpeza e transformação dos dados
    df['main.temp'] = pd.to_numeric(df['main.temp'], errors='coerce')  # Converter temperatura
    df['main.humidity'] = pd.to_numeric(df['main.humidity'], errors='coerce')  # Umidade
    df['wind.speed'] = pd.to_numeric(df['wind.speed'], errors='coerce')  # Velocidade do vento
    df['main.pressure'] = pd.to_numeric(df['main.pressure'], errors='coerce')  # Pressão

    # Salvar o arquivo processado
    df.to_csv(processed_data_file, index=False)
    print(f'Dados processados e salvos em {processed_data_file}')

except FileNotFoundError:
    print(f'Arquivo {raw_data_file} não encontrado. Execute o script main.py primeiro.')
