import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Carregar os dados processados
data_file = './data/processed_weather_data.csv'
df = pd.read_csv(data_file)

#Criar subplots com dados meteorológicos
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
        x=df['name'], 
        y=df['main.temp'], 
        name="Temperatura (°C)", 
        marker_color='royalblue', 
        text=df['main.temp'], 
        textposition='outside'
    ), 
    row=1, col=1
)

#Umidade
fig.add_trace(
    go.Scatter(
        x=df['name'], 
        y=df['main.humidity'], 
        mode="lines+markers", 
        name="Umidade (%)"
    ), 
    row=1, col=2
)

#Velocidade do Vento
fig.add_trace(
    go.Bar(
        x=df['name'], 
        y=df['wind.speed'], 
        name="Velocidade do Vento (m/s)", 
        marker_color='orange'
    ), 
    row=2, col=1
)

#Pressão Atmosférica
fig.add_trace(
    go.Scatter(
        x=df['name'], 
        y=df['main.pressure'], 
        mode="lines", 
        name="Pressão (hPa)"
    ), 
    row=2, col=2
)

#Ajustar layout
fig.update_layout(
    title="Clima Atual em Ribeirão Preto",
    title_font_size=24,
    showlegend=True,
    font=dict(size=16), 
    xaxis_title_font_size=18,
    yaxis_title_font_size=18,
    plot_bgcolor='rgb(230, 230, 250)',  #cor de fundo
    paper_bgcolor='white'
)

#Exibir o dashboard no navegador
fig.show()
