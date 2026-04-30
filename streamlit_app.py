import streamlit as st
import pandas as pd
from trello_cash_flow_analyzer import TrelloCashFlowAnalyzer  # Assume this is the correct import for your analyzer class

# Função para gerar relatório com base na seleção do período
def gerar_relatorio(periodo, dias_atras, dias_a_frente):
    analyzer = TrelloCashFlowAnalyzer()
    # Use o analyzer para obter dados com base no período e dias selecionados
    dados = analyzer.analyze(periodo, dias_atras, dias_a_frente)
    return dados

# Interface do Streamlit
st.title("Análise de Fluxo de Caixa")

# Sidebar para seleção de período
a_periodo = st.sidebar.selectbox("Selecione o Período:", ["Futuro", "Passado", "Ambos"])

# Inputs dinâmicos para dias
if a_periodo == "Passado":
    dias_atras = st.sidebar.number_input("Dias para trás:", min_value=1, value=7)
    dias_a_frente = 0
elif a_periodo == "Futuro":
    dias_atras = 0
    dias_a_frente = st.sidebar.number_input("Dias para frente:", min_value=1, value=7)
else:
    dias_atras = st.sidebar.number_input("Dias para trás:", min_value=1, value=7)
    dias_a_frente = st.sidebar.number_input("Dias para frente:", min_value=1, value=7)

# Botão para gerar relatório
if st.sidebar.button("🔄 Gerar Relatório"):
    relatorio = gerar_relatorio(a_periodo, dias_atras, dias_a_frente)
    st.write(relatorio)  # Exibir dados do relatório em tabelas ou gráficos
    st.line_chart(relatorio['metricas'])  # Exemplo de gráfico de métricas
    st.dataframe(relatorio['tabela'])  # Exemplo de tabela
