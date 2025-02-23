import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import os

#Inicializar o aplicativo Dash
app = dash.Dash(__name__)

    #Função para carregar dados
def carregar_dados(cidade='Ribeirão Preto'):
    data_file = './data/processed_weather_data.csv'
    df = pd.read_csv(data_file)
    dados_cidade = df[df['name'] == cidade]
    
    #Verificação de DataFrame vazio
    if dados_cidade.empty:
        print(f"⚠️ Dados não encontrados para {cidade}.")
        return pd.DataFrame({
            'name': [cidade],
            'main.temp': [0],
            'main.humidity': [0],
            'wind.speed': [0],
            'main.pressure': [0]
        })
    return dados_cidade

def integrar_api_externa(cidade):
    API_KEY = '6d733a370c11db7fb913903173f0f8c4'
    URL = f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&units=metric&lang=pt_br&appid={API_KEY}'
    
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        df = pd.json_normalize(data)
        df.to_csv('./data/processed_weather_data.csv', mode='a', header=False, index=False)
        print(f'Dados atualizados para {cidade}')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao acessar API externa: {e}')

#Criar o dashboard visualizado
def criar_dashboard(df):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Temperatura (°C)",
            "Umidade (%)",
            "Velocidade do Vento (m/s)",
            "Pressão Atmosférica (hPa)"
        )
    )
    #Temperatura
    fig.add_trace(
        go.Bar(
            x=df['name'], y=df['main.temp'],
            name="Temperatura (°C)", marker_color='#1f77b4',
            text=df['main.temp'], textposition='outside'
        ), row=1, col=1
    )
    #Umidade
    fig.add_trace(
        go.Scatter(
            x=df['name'], y=df['main.humidity'],
            mode="lines+markers", name="Umidade (%)",
            marker=dict(color='#17becf')
        ), row=1, col=2
    )
    #Velocidade do Vento
    fig.add_trace(
        go.Bar(
            x=df['name'], y=df['wind.speed'],
            name="Velocidade do Vento (m/s)", marker_color='#ff7f0e'
        ), row=2, col=1
    )
    #Pressão Atmosférica
    fig.add_trace(
        go.Scatter(
            x=df['name'], y=df['main.pressure'],
            mode="lines", name="Pressão (hPa)",
            marker=dict(color='#9467bd')
        ), row=2, col=2
    )
    #Layout customizado
    fig.update_layout(
        title="Clima Atual na Cidade Selecionada",
        title_font_size=24,
        showlegend=True,
        font=dict(size=14, family="Arial"),
        plot_bgcolor='#f5f5f5',
        paper_bgcolor='#ffffff',
        margin=dict(l=50, r=50, t=80, b=50)
    )
    return fig

#filtros interativos
app.layout = html.Div(style={'backgroundColor': '#f5f5f5', 'padding': '20px'}, children=[
    html.H1("Dashboard Interativo de Clima", style={'textAlign': 'center', 'color': '#333'}),

    html.Label("Selecione a cidade:", style={'fontSize': 18}),
    dcc.Dropdown(
        id='cidade-dropdown',
        options=[
            {'label': 'Ribeirão Preto', 'value': 'Ribeirão Preto'},
            {'label': 'São Paulo', 'value': 'São Paulo'},
            {'label': 'Campinas', 'value': 'Campinas'},
            {'label': 'Santos', 'value': 'Santos'}
        ],
        value='Ribeirão Preto',
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.Graph(id='dashboard-clima'),
    dcc.Interval(id='intervalo-atualizacao', interval=60000, n_intervals=0)
])

#Callback para atualizar o gráfico
@app.callback(
    Output('dashboard-clima', 'figure'),
    Input('cidade-dropdown', 'value'),
    Input('intervalo-atualizacao', 'n_intervals')
)
def atualizar_dashboard(cidade, n):
    print(f"🔄 Atualizando dados para: {cidade}")
    df = carregar_dados(cidade)
    print(df.head())  #Exibe os dados carregados no terminal
    return criar_dashboard(df)

#Rodar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
