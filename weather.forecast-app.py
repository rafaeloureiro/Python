import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import sqlite3
import hashlib

# Page configuration
st.set_page_config(
    page_title="Automatic weather forecast",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database Initialization 
def init_db():
    conn = sqlite3.connect('weather_alerts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE,
                  password TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS alerts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  city_name TEXT,
                  latitude REAL,
                  longitude REAL,
                  email_dest TEXT,
                  frequency TEXT,
                  time TEXT,
                  active BOOLEAN,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    conn.commit()
    conn.close()

init_db()

# Popular cities in brazil
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

# Funções auxiliares??????????
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# weather forecast api consume
def obter_previsao_tempo(lat, lon):
    """Get weather forecast"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,precipitation_probability,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
        "timezone": "America/Sao_Paulo",
        "forecast_days": 7
    }
    response = requests.get(url, params=params)
    return response.json()

def formatar_resumo_html(dados, cidade):
    """Formata resumo HTML"""
    daily = dados['daily']
    hourly = dados['hourly']
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; margin-top: 0; }}
            h2 {{ color: #34495e; margin-top: 25px; font-size: 1.3em; }}
            .dia {{ background: #f8f9fa; padding: 20px; margin: 15px 0; border-left: 4px solid #3498db; border-radius: 5px; }}
            .alerta-chuva {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .horario-chuva {{ margin: 8px 0; padding: 8px 12px; background: white; border-radius: 3px; }}
            .temp {{ color: #e74c3c; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📅 Weather forecast - {city}</h1>
            <p>Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
    """
    
    weekdays = ['monday', 'tuesday', 'wednesday', 'thurday', 'friday', 'saturday', 'sunday']
    
    for i in range(7):
        data = datetime.fromisoformat(daily['time'][i])
        dia_nome = weekdays[data.weekday()]
        
        html += f"""
        <div class="dia">
            <h2>{dia_nome}, {data.strftime('%d/%m/%Y')}</h2>
            <p>🌡️ Temperature: <span class="temp">{daily['temperature_2m_min'][i]:.1f}°C - {daily['temperature_2m_max'][i]:.1f}°C</span></p>
            <p>💧 Precipitation: <strong>{daily['precipitation_sum'][i]:.1f} mm</strong></p>
            <p>☔ Probabilty: <strong>{daily['precipitation_probability_max'][i]}%</strong></p>
        """
        
        if daily['precipitation_sum'][i] > 0.5:
            html += '<div class="alerta-chuva"><strong>⚠️ PREVISÃO DE CHUVA:</strong>'
            data_str = daily['time'][i]
            
            for j, hora_str in enumerate(hourly['time']):
                if hora_str.startswith(data_str) and hourly['precipitation'][j] > 0.1:
                    hora = datetime.fromisoformat(hora_str).strftime('%H:%M')
                    html += f'<div class="horario-chuva">🕐 {hora} - {hourly["precipitation"][j]:.1f}mm</div>'
            
            html += '</div>'
        
        html += '</div>'
    
    html += '</div></body></html>'
    return html

def enviar_email(email_from, password, email_to, assunto, corpo_html):
    """Envia e-mail"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = assunto
        msg['From'] = email_from
        msg['To'] = email_to
        
        msg.attach(MIMEText(corpo_html, 'html', 'utf-8'))
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_from, password)
            server.send_message(msg)
        
        return True, "E-mail enviado com sucesso!"
    except Exception as e:
        return False, f"Erro: {str(e)}"

# Sistema de autenticação
def login_user(email, password):
    conn = sqlite3.connect('weather_alerts.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email=? AND password=?", 
              (email, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

def register_user(email, password):
    try:
        conn = sqlite3.connect('weather_alerts.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)",
                  (email, hash_password(password)))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        return True, user_id
    except sqlite3.IntegrityError:
        return False, None

# Interface principal
def main():
    st.title("🌤️ Sistema de Previsão do Tempo Automática")
    
    # Sistema de login
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if st.session_state.user_id is None:
        tab1, tab2 = st.tabs(["Login", "Cadastro"])
        
        with tab1:
            st.subheader("Faça login")
            email = st.text_input("E-mail", key="login_email")
            password = st.text_input("Senha", type="password", key="login_pass")
            
            if st.button("Entrar"):
                user_id = login_user(email, password)
                if user_id:
                    st.session_state.user_id = user_id
                    st.session_state.user_email = email
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Credenciais inválidas!")
        
        with tab2:
            st.subheader("Criar conta")
            new_email = st.text_input("E-mail", key="reg_email")
            new_password = st.text_input("Senha", type="password", key="reg_pass")
            confirm_password = st.text_input("Confirmar senha", type="password", key="reg_confirm")
            
            if st.button("Cadastrar"):
                if new_password != confirm_password:
                    st.error("As senhas não coincidem!")
                elif len(new_password) < 6:
                    st.error("A senha deve ter no mínimo 6 caracteres!")
                else:
                    success, user_id = register_user(new_email, new_password)
                    if success:
                        st.success("Conta criada com sucesso! Faça login.")
                    else:
                        st.error("E-mail já cadastrado!")
    
    else:
        # Usuário logado
        with st.sidebar:
            st.write(f"👤 **Logado como:** {st.session_state.user_email}")
            if st.button("Sair"):
                st.session_state.user_id = None
                st.rerun()
            
            st.divider()
            st.subheader("⚙️ Configurações SMTP")
            smtp_email = st.text_input("E-mail de envio", value=st.session_state.user_email)
            smtp_password = st.text_input("Senha de app Gmail", type="password",
                                         help="Use senha de app do Gmail, não sua senha normal")
            
            if 'smtp_email' not in st.session_state:
                st.session_state.smtp_email = smtp_email
                st.session_state.smtp_password = smtp_password
            
            if st.button("Salvar configurações"):
                st.session_state.smtp_email = smtp_email
                st.session_state.smtp_password = smtp_password
                st.success("Configurações salvas!")
        
        # Tabs principais
        tab1, tab2, tab3 = st.tabs(["➕ Nova Automação", "📋 Minhas Automações", "🧪 Testar"])
        
        with tab1:
            st.header("Criar Nova Automação")
            
            col1, col2 = st.columns(2)
            
            with col1:
                cidade = st.selectbox("Cidade", list(CIDADES.keys()))
                email_dest = st.text_input("E-mail de destino", value=st.session_state.user_email)
            
            with col2:
                frequency = st.selectbox("Frequência", [
                    "Toda segunda-feira",
                    "Toda terça-feira",
                    "Toda quarta-feira",
                    "Toda quinta-feira",
                    "Toda sexta-feira",
                    "Todos os dias",
                    "Segunda e quinta",
                    "Terça e sexta"
                ])
                
                time = st.time_input("Horário de envio", value=datetime.strptime("07:00", "%H:%M").time())
            
            if st.button("✅ Criar Automação", type="primary"):
                lat, lon = CIDADES[cidade]
                
                # Salvar no banco
                conn = sqlite3.connect('weather_alerts.db')
                c = conn.cursor()
                c.execute("""INSERT INTO alerts 
                            (user_id, city_name, latitude, longitude, email_dest, frequency, time, active)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                         (st.session_state.user_id, cidade, lat, lon, email_dest, 
                          frequency, time.strftime("%H:%M"), True))
                conn.commit()
                conn.close()
                
                st.success(f"✅ Automação criada! Você receberá a previsão de {cidade} {frequency.lower()} às {time.strftime('%H:%M')}")
                st.balloons()
        
        with tab2:
            st.header("Minhas Automações Ativas")
            
            conn = sqlite3.connect('weather_alerts.db')
            df = pd.read_sql_query("""SELECT id, city_name, email_dest, frequency, time, active 
                                     FROM alerts WHERE user_id=?""", 
                                   conn, params=(st.session_state.user_id,))
            conn.close()
            
            if len(df) == 0:
                st.info("Você ainda não tem automações criadas.")
            else:
                for idx, row in df.iterrows():
                    with st.expander(f"🌍 {row['city_name']} - {row['frequency']} às {row['time']}"):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.write(f"📧 **Destino:** {row['email_dest']}")
                            st.write(f"🔔 **Status:** {'🟢 Ativo' if row['active'] else '🔴 Inativo'}")
                        
                        with col2:
                            if st.button("🗑️ Deletar", key=f"del_{row['id']}"):
                                conn = sqlite3.connect('weather_alerts.db')
                                c = conn.cursor()
                                c.execute("DELETE FROM alerts WHERE id=?", (row['id'],))
                                conn.commit()
                                conn.close()
                                st.success("Automação deletada!")
                                st.rerun()
                        
                        with col3:
                            new_status = not row['active']
                            label = "▶️ Ativar" if not row['active'] else "⏸️ Pausar"
                            if st.button(label, key=f"toggle_{row['id']}"):
                                conn = sqlite3.connect('weather_alerts.db')
                                c = conn.cursor()
                                c.execute("UPDATE alerts SET active=? WHERE id=?", 
                                         (new_status, row['id']))
                                conn.commit()
                                conn.close()
                                st.rerun()
        
        with tab3:
            st.header("Testar Envio")
            st.info("Envie uma previsão de teste para verificar se está tudo funcionando")
            
            test_cidade = st.selectbox("Escolha a cidade para teste", list(CIDADES.keys()), key="test_city")
            test_email = st.text_input("E-mail de teste", value=st.session_state.user_email, key="test_email")
            
            if st.button("📨 Enviar Teste", type="primary"):
                if not hasattr(st.session_state, 'smtp_password') or not st.session_state.smtp_password:
                    st.error("Configure suas credenciais SMTP na barra lateral primeiro!")
                else:
                    with st.spinner("Buscando previsão e enviando e-mail..."):
                        lat, lon = CIDADES[test_cidade]
                        dados = obter_previsao_tempo(lat, lon)
                        html = formatar_resumo_html(dados, test_cidade)
                        
                        success, msg = enviar_email(
                            st.session_state.smtp_email,
                            st.session_state.smtp_password,
                            test_email,
                            f"🧪 TESTE - Previsão {test_cidade}",
                            html
                        )
                        
                        if success:
                            st.success(msg)
                            with st.expander("👀 Visualizar prévia do e-mail"):
                                st.components.v1.html(html, height=600, scrolling=True)
                        else:
                            st.error(msg)

if __name__ == "__main__":
    main()
