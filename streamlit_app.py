"""
Aplicação Streamlit para Análise de Fluxo de Caixa do Trello

Esta aplicação fornece uma interface web interativa para visualizar
o fluxo de caixa a partir de dados do Trello.

Autor: Claude Code
Data: 2025-11-25
"""

import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Adicionar o diretório atual ao path para importar o módulo
sys.path.insert(0, str(Path(__file__).parent))

from fluxo_caixa_trello import TrelloCashFlowAnalyzer


# Configuração da página
st.set_page_config(
    page_title="Fluxo de Caixa - Contas a Pagar",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para estilo moderno
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)


def format_currency(value: float) -> str:
    """Formata valor em formato de moeda brasileira."""
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def main():
    """Função principal da aplicação Streamlit."""

    # Cabeçalho
    st.markdown('<div class="main-title">📊 Fluxo de Caixa - Contas a Pagar</div>', unsafe_allow_html=True)
    today = datetime.now()
    st.markdown(f'<div class="subtitle">Atualizado em: {today.strftime("%d/%m/%Y às %H:%M:%S")}</div>', unsafe_allow_html=True)

    # Sidebar com configurações
    with st.sidebar:
        st.header("⚙️ Configurações")

        # URL do board (com valor padrão)
        board_url = st.text_input(
            "URL do Board do Trello",
            value="https://trello.com/b/WgSarYPK/contas-a-pagar-25",
            help="Cole aqui a URL do seu board do Trello"
        )

        # Número de dias à frente
        days_ahead = st.number_input(
            "Dias à frente",
            min_value=1,
            max_value=30,
            value=7,
            help="Número de dias para análise futura"
        )

        st.divider()

        # Informações
        with st.expander("ℹ️ Sobre"):
            st.markdown("""
            **Fluxo de Caixa - Trello**

            Esta aplicação coleta automaticamente os dados de contas a pagar
            do Trello e gera análises visuais interativas.

            **Formato dos cards:**
            `DD/MM/YY - R$VALOR - NOME`

            **Exemplo:**
            `25/11/25 - R$1.500,00 - Aluguel`
            """)

        with st.expander("🔒 Credenciais"):
            st.markdown("""
            As credenciais são carregadas de:
            1. **Streamlit Cloud**: `st.secrets`
            2. **Local**: arquivo `.env`

            Certifique-se de configurar:
            - `TRELLO_API_KEY`
            - `TRELLO_TOKEN`
            """)

    # Botão principal para gerar relatório
    if st.button("🔄 Gerar Relatório", type="primary"):

        with st.spinner("🔍 Coletando dados do Trello..."):
            try:
                # Criar analisador
                analyzer = TrelloCashFlowAnalyzer()

                # Carregar credenciais (tenta st.secrets primeiro)
                success = analyzer.load_credentials(use_streamlit_secrets=True)

                if not success:
                    st.error("❌ Erro ao carregar credenciais. Verifique suas configurações.")
                    st.stop()

                # Definir datas
                today_calc = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = today_calc + timedelta(days=days_ahead - 1)

                # 1. Obter listas do board
                lists = analyzer.get_board_lists(board_url)
                if not lists:
                    st.error("❌ Não foi possível obter as listas do board. Verifique a URL e suas credenciais.")
                    st.stop()

                # 2. Identificar listas dos meses necessários
                first_day_of_month = today_calc.replace(day=1)
                list_ids = analyzer.identify_month_lists(lists, first_day_of_month, end_date)
                if not list_ids:
                    st.warning("⚠️ Nenhuma lista encontrada para o período especificado.")
                    st.stop()

                # 3. Obter cards das listas
                cards = analyzer.get_cards_from_lists(list_ids)
                if not cards:
                    st.warning("⚠️ Nenhum card encontrado nas listas.")
                    st.stop()

                # 4. Parsear TODOS os cards
                df_all_cards = analyzer.parse_all_cards(cards)
                if df_all_cards.empty:
                    st.warning("⚠️ Nenhum card foi parseado com sucesso. Verifique o formato dos títulos.")
                    st.stop()

                # 5. Calcular gastos do mês atual
                monthly_expenses = analyzer.calculate_monthly_expenses(df_all_cards, today_calc)

                # 6. Filtrar cards pelo período de 7 dias
                df_cards = analyzer.filter_cards_by_date_range(df_all_cards, today_calc, end_date)

                # 7. Calcular totais diários
                df_daily = analyzer.calculate_daily_totals(df_cards, today_calc, end_date)

                # 8. Gerar figura Plotly (sem salvar HTML)
                fig = analyzer.generate_interactive_chart(df_daily, monthly_expenses, today_calc, output_path=None)

                st.success("✅ Dados coletados com sucesso!")

                # === EXIBIÇÃO DOS RESULTADOS ===

                st.divider()

                # Métricas principais em cards
                st.subheader("📈 Métricas Principais")

                total_periodo = df_daily['total_saidas'].sum()
                saldo_final = df_daily['saldo_acumulado'].iloc[-1]

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        label=f"💰 Gastos do Mês Atual (01/{today_calc.month:02d} até Hoje)",
                        value=format_currency(monthly_expenses),
                        delta=None
                    )

                with col2:
                    st.metric(
                        label=f"📅 Total Próximos {days_ahead} Dias",
                        value=format_currency(total_periodo),
                        delta=None
                    )

                with col3:
                    st.metric(
                        label="📉 Saldo Final",
                        value=format_currency(saldo_final),
                        delta=None
                    )

                st.divider()

                # Gráfico interativo
                st.subheader("📊 Gráfico de Fluxo de Caixa")
                st.plotly_chart(fig, use_container_width=True)

                st.divider()

                # Tabela detalhada em expander
                with st.expander("📋 Detalhamento Diário", expanded=False):
                    # Formatar DataFrame para exibição
                    df_display = df_daily.copy()
                    df_display['Total Saídas'] = df_display['total_saidas'].apply(format_currency)
                    df_display['Saldo Acumulado'] = df_display['saldo_acumulado'].apply(format_currency)
                    df_display = df_display[['data_formatada', 'dia_semana', 'Total Saídas', 'Saldo Acumulado']]
                    df_display.columns = ['Data', 'Dia', 'Total Saídas', 'Saldo Acumulado']

                    st.dataframe(df_display, use_container_width=True, hide_index=True)

                # Detalhamento dos cards individuais
                if not df_cards.empty:
                    with st.expander(f"📝 Cards no Período ({len(df_cards)} cards)", expanded=False):
                        df_cards_display = df_cards.copy()
                        df_cards_display['Data'] = df_cards_display['data'].dt.strftime('%d/%m/%Y')
                        df_cards_display['Valor'] = df_cards_display['valor'].apply(format_currency)
                        df_cards_display = df_cards_display[['Data', 'Valor', 'nome']]
                        df_cards_display.columns = ['Data', 'Valor', 'Descrição']

                        st.dataframe(df_cards_display, use_container_width=True, hide_index=True)

                st.divider()

                # Botões de ação
                st.subheader("🎯 Ações")

                col_btn1, col_btn2, col_btn3 = st.columns(3)

                with col_btn1:
                    if st.button("💾 Salvar HTML Local"):
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_filename = f"fluxo_caixa_{timestamp}.html"
                        output_path = analyzer.outputs_dir / output_filename

                        # Gerar novamente com output_path
                        analyzer.generate_interactive_chart(df_daily, monthly_expenses, today_calc, str(output_path))

                        st.success(f"✅ Arquivo salvo em: {output_path}")

                        # Oferecer download
                        with open(output_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()

                        st.download_button(
                            label="⬇️ Baixar HTML",
                            data=html_content,
                            file_name=output_filename,
                            mime="text/html"
                        )

                with col_btn2:
                    if st.button("📱 Instruções WhatsApp"):
                        st.info("""
                        **Para enviar via WhatsApp:**

                        1. Clique em "💾 Salvar HTML Local"
                        2. Baixe o arquivo HTML
                        3. Abra o WhatsApp Web ou App
                        4. Anexe o arquivo como documento
                        5. Envie para o destinatário

                        Ou execute o script Python standalone:
                        ```bash
                        python fluxo_caixa_trello.py
                        ```
                        """)

                with col_btn3:
                    st.info("💡 **Dica:** Use o botão de download para compartilhar o relatório!")

                # Rodapé com informações
                st.divider()
                st.caption(f"🕐 Última atualização: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")

            except Exception as e:
                st.error(f"❌ Erro ao processar os dados: {str(e)}")
                st.exception(e)

    else:
        # Mensagem inicial quando a página carrega
        st.info("👆 Clique no botão **'Gerar Relatório'** para começar a análise!")

        # Placeholder com exemplo visual
        st.markdown("---")
        st.markdown("### 📊 Exemplo de Visualização")
        st.image("https://via.placeholder.com/1400x700/667eea/ffffff?text=Clique+em+Gerar+Relatorio+para+ver+seus+dados",
                 use_container_width=True)


if __name__ == "__main__":
    main()
