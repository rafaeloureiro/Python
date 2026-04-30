# Streamlit App

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Sidebar configuration
st.sidebar.title('Configuraciones')

# New period selection logic
period = st.sidebar.radio('Selecciona el periodo:', ('Futuro', 'Passado', 'Ambos'))
if period == 'Futuro':
    dias_a_frente = st.sidebar.number_input('Dias à frente:', min_value=1, value=1)
    start_date = datetime.now() + timedelta(days=dias_a_frente)
    end_date = start_date
elif period == 'Passado':
    dias_atras = st.sidebar.number_input('Dias atrás:', min_value=1, value=1)
    start_date = datetime.now() - timedelta(days=dias_atras)
    end_date = start_date
else:
    dias_a_frente = st.sidebar.number_input('Dias à frente:', min_value=1, value=1)
    dias_atras = st.sidebar.number_input('Dias atrás:', min_value=1, value=1)
    start_date = datetime.now() - timedelta(days=dias_atras)
    end_date = datetime.now() + timedelta(days=dias_a_frente)

# Update metric labels and period display
st.write('Desde:', start_date.date(), 'Até:', end_date.date())

# Remaining application logic here...