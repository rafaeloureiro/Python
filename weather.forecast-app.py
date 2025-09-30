import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Lista de cidades brasileiras com coordenadas
CIDADES = {
    "Santos/SP": (-23.9608, -46.3334),
    "São Paulo/SP": (-23.5505, -46.6333),
    "Rio de Janeiro/RJ": (-22.9068, -43.1729),
    "Belo Horizonte/MG": (-19.9167, -43.9345),
    "Brasília/DF": (-15.7939, -47.8828),
    "Salvador/BA": (-12.9714, -38.5014),
    "Fortaleza/CE": (-3.7172, -38.5433),
    "Curitiba/PR": (-25.4284, -49.2733),
    "Porto Alegre/RS": (-30.0346, -51.2177),
    "Recife/PE": (-8.0476, -34.8770),
    "Florianópolis/SC": (-27.5954, -48.5480),
    "Manaus/AM": (-3.1190, -60.0217),
    "Belém/PA": (-1.4558, -48.5039),
    "Goiânia/GO": (-16.6869, -49.2648),
    "Campinas/SP": (-22.9099, -47.0626)
}

st.set_page_config(
    page_title="Previsão do Tempo Brasil",
    page_icon="⛅",
    layout="centered"
)

st.title("⛅ Previsão do Tempo - 7 dias")
st.write("Escolha uma cidade para ver a previsão do tempo dos próximos 7 dias.")

cidade = st.selectbox("Selecione a cidade", list(CIDADES.keys()))

if st.button("Ver previsão"):
    lat, lon = CIDADES[cidade]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
        "timezone": "America/Sao_Paulo",
        "forecast_days": 7
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        dados = response.json()["daily"]
        df = pd.DataFrame(dados)
        df["time"] = pd.to_datetime(df["time"])
        df = df.rename(columns={
            "time": "Data",
            "temperature_2m_min": "Temp. Mín (°C)",
            "temperature_2m_max": "Temp. Máx (°C)",
            "precipitation_sum": "Precipitação (mm)",
            "precipitation_probability_max": "Prob. de Chuva (%)"
        })
        df = df[["Data", "Temp. Mín (°C)", "Temp. Máx (°C)", "Precipitação (mm)", "Prob. de Chuva (%)"]]
        df["Data"] = df["Data"].dt.strftime("%d/%m/%Y")
        st.subheader(f"Previsão de 7 dias para {cidade}")
        st.dataframe(df, use_container_width=True)
        st.line_chart(df.set_index("Data")[["Temp. Máx (°C)", "Temp. Mín (°C)"]])
    else:
        st.error("Erro ao obter a previsão do tempo. Tente novamente mais tarde.")
