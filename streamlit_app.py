"""
Aplicação Streamlit para Análise de Fluxo de Caixa
Integração com Trello para visualização e análise de dados financeiros
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional
from trello_cash_flow_analyzer import TrelloCashFlowAnalyzer


# Configuração da página
st.set_page_config(
    page_title="Análise de Fluxo de Caixa",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data(ttl=300)  # Cache por 5 minutos
def obter_dados_fluxo_caixa(
    periodo: str, 
    dias_atras: int, 
    dias_a_frente: int
) -> Optional[Dict[str, Any]]:
    """
    Obtém dados de fluxo de caixa do Trello com cache.
    
    Args:
        periodo: Tipo de período ('Futuro', 'Passado', 'Ambos')
        dias_atras: Número de dias para análise retroativa
        dias_a_frente: Número de dias para projeção futura
        
    Returns:
        Dicionário com dados do relatório ou None em caso de erro
    """
    try:
        analyzer = TrelloCashFlowAnalyzer()
        dados = analyzer.analyze(periodo, dias_atras, dias_a_frente)
        return dados
    except Exception as e:
        st.error(f"❌ Erro ao obter dados: {str(e)}")
        return None


def renderizar_sidebar() -> tuple[str, int, int]:
    """
    Renderiza a barra lateral com controles de filtro.
    
    Returns:
        Tupla com (periodo, dias_atras, dias_a_frente)
    """
    st.sidebar.title("⚙️ Configurações")
    st.sidebar.markdown("---")
    
    # Seleção de período
    periodo = st.sidebar.selectbox(
        "📅 Período de Análise:",
        options=["Futuro", "Passado", "Ambos"],
        help="Escolha o intervalo temporal para análise"
    )
    
    st.sidebar.markdown("---")
    
    # Inputs dinâmicos baseados no período selecionado
    if periodo == "Passado":
        dias_atras = st.sidebar.number_input(
            "⏪ Dias para trás:",
            min_value=1,
            max_value=365,
            value=7,
            help="Quantos dias anteriores analisar"
        )
        dias_a_frente = 0
        
    elif periodo == "Futuro":
        dias_atras = 0
        dias_a_frente = st.sidebar.number_input(
            "⏩ Dias para frente:",
            min_value=1,
            max_value=365,
            value=7,
            help="Quantos dias futuros projetar"
        )
        
    else:  # Ambos
        col1, col2 = st.sidebar.columns(2)
        with col1:
            dias_atras = st.number_input(
                "⏪ Dias atrás:",
                min_value=1,
                max_value=365,
                value=7
            )
        with col2:
            dias_a_frente = st.number_input(
                "⏩ Dias à frente:",
                min_value=1,
                max_value=365,
                value=7
            )
    
    return periodo, dias_atras, dias_a_frente


def renderizar_metricas(dados: Dict[str, Any]) -> None:
    """
    Renderiza métricas principais em cards.
    
    Args:
        dados: Dicionário com dados do relatório
    """
    if 'metricas' not in dados:
        st.warning("⚠️ Métricas não disponíveis nos dados")
        return
    
    metricas = dados['metricas']
    
    # Cria colunas para métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💵 Receita Total",
            value=f"R$ {metricas.get('receita_total', 0):,.2f}",
            delta=metricas.get('variacao_receita', 0)
        )
    
    with col2:
        st.metric(
            label="💸 Despesa Total",
            value=f"R$ {metricas.get('despesa_total', 0):,.2f}",
            delta=metricas.get('variacao_despesa', 0),
            delta_color="inverse"
        )
    
    with col3:
        saldo = metricas.get('saldo', 0)
        st.metric(
            label="💰 Saldo",
            value=f"R$ {saldo:,.2f}",
            delta=metricas.get('variacao_saldo', 0)
        )
    
    with col4:
        st.metric(
            label="📊 Transações",
            value=metricas.get('total_transacoes', 0)
        )


def renderizar_graficos(dados: Dict[str, Any]) -> None:
    """
    Renderiza gráficos de análise.
    
    Args:
        dados: Dicionário com dados do relatório
    """
    if 'metricas' not in dados or not isinstance(dados['metricas'], pd.DataFrame):
        if 'metricas' in dados:
            st.info("ℹ️ Dados de métricas não estão em formato de DataFrame")
        return
    
    st.subheader("📈 Evolução Temporal")
    
    try:
        # Gráfico de linha para métricas ao longo do tempo
        st.line_chart(dados['metricas'])
    except Exception as e:
        st.error(f"Erro ao renderizar gráfico: {str(e)}")


def renderizar_tabela(dados: Dict[str, Any]) -> None:
    """
    Renderiza tabela de dados detalhados.
    
    Args:
        dados: Dicionário com dados do relatório
    """
    if 'tabela' not in dados:
        st.warning("⚠️ Tabela de dados não disponível")
        return
    
    st.subheader("📋 Detalhamento de Transações")
    
    tabela = dados['tabela']
    
    if isinstance(tabela, pd.DataFrame):
        # Configurações de exibição
        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=False
        )
        
        # Opção de download
        csv = tabela.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar dados (CSV)",
            data=csv,
            file_name="fluxo_caixa.csv",
            mime="text/csv"
        )
    else:
        st.write(tabela)


def main():
    """Função principal da aplicação."""
    
    # Título e descrição
    st.title("💰 Análise de Fluxo de Caixa")
    st.markdown("""
    Dashboard interativo para análise de fluxo de caixa com integração ao Trello.
    Configure os parâmetros na barra lateral e clique em **Gerar Relatório**.
    """)
    
    st.markdown("---")
    
    # Renderiza sidebar e obtém parâmetros
    periodo, dias_atras, dias_a_frente = renderizar_sidebar()
    
    # Botão de geração de relatório
    st.sidebar.markdown("---")
    gerar = st.sidebar.button(
        "🔄 Gerar Relatório",
        type="primary",
        use_container_width=True
    )
    
    # Adiciona botão de limpar cache
    if st.sidebar.button("🗑️ Limpar Cache", use_container_width=True):
        st.cache_data.clear()
        st.sidebar.success("✅ Cache limpo!")
    
    # Processamento quando botão é clicado
    if gerar:
        with st.spinner("⏳ Processando dados..."):
            # Obtém dados
            relatorio = obter_dados_fluxo_caixa(periodo, dias_atras, dias_a_frente)
        
        if relatorio is None:
            st.error("❌ Não foi possível gerar o relatório. Verifique os logs acima.")
            return
        
        # Valida estrutura dos dados
        if not isinstance(relatorio, dict):
            st.error("❌ Formato de dados inválido retornado pelo analisador")
            return
        
        # Renderiza componentes
        st.success("✅ Relatório gerado com sucesso!")
        
        # Métricas principais
        renderizar_metricas(relatorio)
        
        st.markdown("---")
        
        # Gráficos
        renderizar_graficos(relatorio)
        
        st.markdown("---")
        
        # Tabela detalhada
        renderizar_tabela(relatorio)
        
    else:
        # Estado inicial - exibe instruções
        st.info("""
        👆 **Primeiros passos:**
        1. Configure o período de análise na barra lateral
        2. Ajuste a quantidade de dias conforme necessário
        3. Clique em **Gerar Relatório** para visualizar os dados
        """)


if __name__ == "__main__":
    main()
