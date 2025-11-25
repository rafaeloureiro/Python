# 📊 Análise de Fluxo de Caixa do Trello

Aplicação Python para análise automatizada de contas a pagar do Trello, gerando relatórios visuais interativos em HTML com opção de envio automático via WhatsApp.

## 🎯 Funcionalidades

### ✅ Análise de Dados
- Conexão automática com API do Trello
- Identificação inteligente de listas por mês (ex: "Outubro/25", "Novembro/25")
- Coleta de cards dos próximos 7 dias (range configurável)
- Parser robusto de títulos no formato: `DD/MM/YY - R$VALOR - NOME`
- Cálculo de totais diários e saldo acumulado

### 💰 Métricas Financeiras
- **NOVO**: Gastos do Mês Atual (do dia 01 até hoje)
- Total do Período (próximos 7 dias)
- Saldo acumulado com visualização gráfica

### 📱 Envio Automático
- **NOVO**: Integração com WhatsApp Web via pywhatkit
- Pergunta condicional antes de enviar (confirmação do usuário)
- Envio automático com mensagem personalizada e data
- Tratamento robusto de erros

### 📈 Visualização
- Gráfico HTML interativo com Plotly
- Design moderno e responsivo
- Dimensões otimizadas (1400x700px) para melhor visualização
- Margens ajustadas para título e métricas sempre visíveis
- Exportável para imagem PNG/PDF
- Hover interativo com detalhes

### 📁 Organização
- Estrutura de pastas organizada
- Outputs salvos com timestamp: `fluxo_caixa_YYYYMMDD_HHMMSS.html`
- Arquivo .env local na pasta do projeto
- Logs detalhados de todas as operações

## 📋 Requisitos

- Python 3.8 ou superior
- Arquivo `.env` na pasta do projeto com:
  ```env
  TRELLO_API_KEY=sua_api_key_aqui
  TRELLO_TOKEN=seu_token_aqui
  ```

## 🚀 Instalação

1. **Clone ou navegue até a pasta do projeto:**
   ```bash
   cd C:\Users\rafae\fluxo_caixa_trello_app
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o arquivo .env:**
   - O arquivo `.env` já está na pasta do projeto (copiado de motoboy_automation)
   - Certifique-se de que contém as credenciais válidas do Trello:
     - `TRELLO_API_KEY`
     - `TRELLO_TOKEN`

## 💻 Como Usar

### Execução Básica

1. **Execute o script:**
   ```bash
   python fluxo_caixa_trello.py
   ```

2. **O script irá:**
   - ✅ Carregar credenciais do arquivo `.env` local
   - ✅ Conectar ao board: https://trello.com/b/WgSarYPK/contas-a-pagar-25
   - ✅ Identificar listas dos meses necessários
   - ✅ Coletar todos os cards das listas
   - ✅ Calcular gastos do mês atual (01/[MÊS] até hoje)
   - ✅ Filtrar cards dos próximos 7 dias
   - ✅ Gerar gráfico HTML na pasta `outputs/`
   - ✅ Exibir resumo completo no console
   - ✅ Perguntar se deseja enviar via WhatsApp

3. **Confirmação de Envio via WhatsApp:**
   ```
   📱 Deseja enviar o relatório para o sócio via WhatsApp? (s/n):
   ```
   - Digite `s`, `S`, `sim` ou `SIM` para enviar
   - Digite `n`, `N`, `não` ou qualquer outra coisa para cancelar
   - **Destinatário**: +5521991998872
   - **Mensagem**: "📊 Fluxo de Caixa Atualizado - DD/MM/YYYY"

## 📊 Formato dos Cards no Trello

Os títulos dos cards devem seguir o padrão:
```
DD/MM/YY - R$VALOR - NOME
```

### Exemplos válidos:
- `20/10/25 - R$150,50 - Fornecedor A`
- `05/11/25 - R$791,36 - Packlog`
- `15/10/25 - R$ 1.500,00 - Aluguel`
- `01/12/25 - R$6.136,28 - Folha de Pagamento`

## 📤 Saída do Programa

### 1. Console (Terminal)

```
🚀 Iniciando análise de fluxo de caixa...
📅 Data de hoje: 24/11/2025
📆 Período de análise: 7 dias

📂 Carregando credenciais de: C:\Users\rafae\fluxo_caixa_trello_app\.env
✅ Credenciais carregadas com sucesso
✅ 12 listas encontradas no board
📅 Meses necessários: {('novembro', '25')}
✅ Lista encontrada: 'Novembro/25' (ID: xxx)
✅ 45 cards obtidos da lista xxx
✅ Total de 45 cards coletados
🔍 Parseando 45 cards...
✅ 42 cards parseados com sucesso

💰 Gastos do mês atual (01/11 até 24/11): R$ 125.432,50

✅ 15 cards no período de 24/11/2025 a 30/11/2025
✅ Gráfico salvo em: C:\Users\rafae\fluxo_caixa_trello_app\outputs\fluxo_caixa_20251124_143022.html

======================================================================
📊 RESUMO DA ANÁLISE DE FLUXO DE CAIXA
======================================================================

📦 Total de cards nas listas: 42
🎯 Cards no período de 7 dias: 15
📅 Range de datas nas listas: 01/11/2025 até 30/11/2025

💰 GASTOS DO MÊS ATUAL (01/11 até 24/11): R$ 125.432,50

📅 TOTAL POR DIA (Próximos 7 dias):
----------------------------------------------------------------------
24/11/2025 (Dom):     R$ 1.500,00 | Saldo:     R$ -1.500,00
25/11/2025 (Seg):       R$ 350,00 | Saldo:     R$ -1.850,00
...
----------------------------------------------------------------------
💰 TOTAL CONSOLIDADO DO PERÍODO (7 dias): R$ 8.432,50
📉 SALDO FINAL ACUMULADO: R$ -8.432,50

📋 DETALHAMENTO DOS CARDS NO PERÍODO:
----------------------------------------------------------------------
24/11/2025:  R$ 1.500,00 - Aluguel
25/11/2025:    R$ 350,00 - Fornecedor A
...
======================================================================

✅ Análise concluída! Gráfico disponível em: C:\Users\rafae\fluxo_caixa_trello_app\outputs\fluxo_caixa_20251124_143022.html

======================================================================
📱 Deseja enviar o relatório para o sócio via WhatsApp? (s/n):
```

### 2. HTML Interativo

Arquivo salvo em `outputs/fluxo_caixa_YYYYMMDD_HHMMSS.html` com:

- **Título**: Fluxo de Caixa - Próximos 7 dias
- **Métrica Principal**: Gastos do Mês Atual (01/[MÊS] até Hoje): R$ XX.XXX,XX *(destacado em vermelho)*
- **Métricas Secundárias**:
  - Total do Período: R$ XX.XXX,XX
  - Saldo Final: R$ XX.XXX,XX
- **Gráfico**:
  - Barras verticais com valores de saídas diárias
  - Linha de saldo acumulado
  - Hover interativo com detalhes
  - Botões de zoom, pan, reset
  - Exportável para PNG

### 3. Envio via WhatsApp

Quando confirmado (`s`):
- Abre WhatsApp Web automaticamente
- Envia mensagem: "📊 Fluxo de Caixa Atualizado - DD/MM/YYYY"
- **NOTA**: O arquivo HTML precisa ser anexado manualmente (instruções aparecem no console)

## ⚙️ Configurações

### Alterar Período de Análise

Edite o arquivo `fluxo_caixa_trello.py`:

```python
# Linha ~801
DAYS_AHEAD = 7  # Alterar para o número de dias desejado (ex: 14, 30)
```

### Alterar Board do Trello

Edite o arquivo `fluxo_caixa_trello.py`:

```python
# Linha ~800
BOARD_URL = "https://trello.com/b/SEU_BOARD_ID/nome-do-board"
```

### Alterar Número de WhatsApp

Edite o arquivo `fluxo_caixa_trello.py`:

```python
# Linha ~633 (dentro do método send_whatsapp_report)
phone_number = "+55219XXXXXXXX"  # Novo número no formato internacional
```

## 📁 Estrutura do Projeto

```
C:\Users\rafae\fluxo_caixa_trello_app\
│
├── fluxo_caixa_trello.py    # Script principal
├── .env                       # Credenciais do Trello (NÃO COMMITAR!)
├── requirements.txt           # Dependências Python
├── README.md                  # Este arquivo
│
└── outputs\                   # Pasta com relatórios gerados
    ├── fluxo_caixa_20251124_143022.html
    ├── fluxo_caixa_20251123_091245.html
    └── ...
```

## 🔧 Estrutura do Código

```
fluxo_caixa_trello.py
│
├── TrelloCashFlowAnalyzer (classe principal)
│   ├── __init__()                    # Inicializa com .env local
│   ├── load_credentials()            # Carrega .env da pasta do projeto
│   ├── get_board_lists()             # Obtém listas do board
│   ├── identify_month_lists()        # Identifica listas por mês
│   ├── get_cards_from_lists()        # Coleta cards
│   ├── parse_card_title()            # Parser de títulos
│   ├── parse_all_cards()             # Parseia todos os cards
│   ├── filter_cards_by_date_range()  # Filtra por período
│   ├── calculate_monthly_expenses()  # 🆕 Calcula gastos do mês
│   ├── calculate_daily_totals()      # Calcula totais diários
│   ├── generate_interactive_chart()  # 🆕 Gera HTML (dimensões ajustadas)
│   ├── send_whatsapp_report()        # 🆕 Envia via WhatsApp
│   ├── print_summary()               # 🆕 Imprime resumo (com gastos mensais)
│   └── run_analysis()                # Executa análise completa
│
└── main()                             # Função principal
```

## 🛠️ Tratamento de Erros

O script possui tratamento robusto para:

- ❌ Credenciais ausentes ou inválidas
- ❌ Arquivo .env não encontrado
- ❌ Falhas na API do Trello
- ❌ Cards com formato inválido
- ❌ Listas de mês não encontradas
- ❌ Erros de parsing de datas/valores
- ❌ Falhas no envio via WhatsApp
- ❌ Problemas de conexão com WhatsApp Web

## 🔐 Segurança

- **IMPORTANTE**: Nunca commite o arquivo `.env` em repositórios públicos!
- O arquivo `.env` contém credenciais sensíveis (API Key e Token do Trello)
- Mantenha as credenciais seguras e não as compartilhe

## 📝 Notas Importantes

### WhatsApp Web
- O envio via WhatsApp requer que o WhatsApp Web esteja **conectado e funcional**
- A biblioteca `pywhatkit` abrirá uma nova aba do navegador automaticamente
- **Não feche a aba** enquanto o envio estiver em progresso
- O arquivo HTML deve ser **anexado manualmente** após a mensagem ser enviada

### Dependências
- Todas as dependências estão listadas em `requirements.txt`
- A instalação via `pip install -r requirements.txt` instala tudo automaticamente
- `pywhatkit` pode solicitar permissões adicionais no primeiro uso

### Performance
- O script é otimizado para coletar cards de múltiplas listas em paralelo
- O tempo de execução depende do número de cards e listas
- Gráficos interativos são gerados rapidamente (< 2 segundos)

## 🐛 Troubleshooting

### Problema: "Credenciais não encontradas"
**Solução**: Verifique se o arquivo `.env` está na pasta `C:\Users\rafae\fluxo_caixa_trello_app\` e contém:
```env
TRELLO_API_KEY=sua_chave_aqui
TRELLO_TOKEN=seu_token_aqui
```

### Problema: "Nenhuma lista encontrada"
**Solução**: Verifique se as listas no Trello seguem o formato `Mês/Ano` (ex: "Novembro/25", "novembro/25")

### Problema: "Erro ao enviar WhatsApp"
**Soluções**:
- Verifique se o WhatsApp Web está conectado
- Certifique-se de ter conexão com internet
- Tente enviar manualmente (caminho do arquivo é mostrado no console)
- Verifique se o navegador padrão está configurado corretamente

### Problema: "Cards não parseados"
**Solução**: Verifique se os títulos dos cards seguem o formato exato: `DD/MM/YY - R$VALOR - NOME`

## 🌐 Interface Web com Streamlit (NOVO!)

### Visão Geral

Além do script Python standalone, o projeto agora inclui uma interface web interativa desenvolvida com Streamlit, permitindo análise visual em tempo real através do navegador.

### 🎨 Características da Interface Streamlit

- **Interface Moderna**: Design responsivo com tema personalizado
- **Métricas em Cards**: Visualização clara dos principais indicadores
- **Gráficos Interativos**: Plotly integrado para máxima interatividade
- **Configurações Dinâmicas**: Ajuste URL do board e período diretamente na interface
- **Download de Relatórios**: Geração e download de HTML com um clique
- **Sem Duplicação de Código**: Reutiliza toda a lógica existente de `fluxo_caixa_trello.py`

### 🚀 Como Rodar Localmente

1. **Instale as dependências (se ainda não fez):**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure as credenciais:**

   **Opção 1 - Usando .env (recomendado para local):**
   - O arquivo `.env` já existe na pasta do projeto
   - Certifique-se de que contém `TRELLO_API_KEY` e `TRELLO_TOKEN`

   **Opção 2 - Usando Streamlit secrets:**
   ```bash
   # Copie o exemplo
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml

   # Edite com suas credenciais
   # Adicione:
   # TRELLO_API_KEY = "sua_api_key"
   # TRELLO_TOKEN = "seu_token"
   ```

3. **Execute o Streamlit:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Acesse no navegador:**
   - O Streamlit abrirá automaticamente em: http://localhost:8501
   - Se não abrir, acesse manualmente o endereço acima

### ☁️ Deploy no Streamlit Cloud

#### Passo 1: Preparar Repositório

1. **Crie um repositório no GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Fluxo de Caixa Trello"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/fluxo-caixa-trello.git
   git push -u origin main
   ```

2. **Verifique que o `.gitignore` está configurado:**
   - O arquivo `.gitignore` já está configurado para não commitar:
     - `.env`
     - `.streamlit/secrets.toml`
     - `__pycache__/`
     - `outputs/`

#### Passo 2: Deploy no Streamlit Cloud

1. **Acesse**: https://share.streamlit.io

2. **Faça login com GitHub**

3. **Clique em "New app"**

4. **Configure:**
   - **Repository**: `SEU_USUARIO/fluxo-caixa-trello`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: `seu-app-nome` (personalize)

5. **Clique em "Deploy!"**

#### Passo 3: Configurar Secrets no Streamlit Cloud

1. **Na página do seu app, clique em "⚙️ Settings"**

2. **Vá em "Secrets"**

3. **Adicione suas credenciais:**
   ```toml
   TRELLO_API_KEY = "sua_api_key_aqui"
   TRELLO_TOKEN = "seu_token_aqui"
   ```

4. **Clique em "Save"**

5. **O app reiniciará automaticamente**

### 🔄 Compatibilidade entre Modo CLI e Streamlit

Ambos os modos funcionam simultaneamente:

| Funcionalidade | CLI (Python) | Streamlit |
|----------------|--------------|-----------|
| Coleta de dados | ✅ | ✅ |
| Cálculos | ✅ | ✅ |
| Gráficos Plotly | ✅ | ✅ |
| Salvar HTML local | ✅ | ✅ |
| Envio WhatsApp | ✅ (automático) | ⚠️ (manual)* |
| Interface visual | ❌ | ✅ |
| Configuração dinâmica | ❌ | ✅ |

\* *No Streamlit, o envio via WhatsApp é feito manualmente através do download do HTML*

### 📱 Como Usar a Interface Streamlit

1. **Acesse a aplicação** (local ou cloud)

2. **Configure na Sidebar:**
   - URL do Board do Trello (pré-preenchida)
   - Número de dias à frente (padrão: 7)

3. **Clique em "🔄 Gerar Relatório"**

4. **Visualize os resultados:**
   - Métricas principais em cards destacados
   - Gráfico interativo de fluxo de caixa
   - Tabela detalhada (expandível)
   - Lista de cards individuais (expandível)

5. **Ações disponíveis:**
   - **💾 Salvar HTML Local**: Gera arquivo e oferece download
   - **📱 Instruções WhatsApp**: Mostra como enviar manualmente
   - **⬇️ Baixar HTML**: Download direto do relatório

### 🎯 Diferenças entre CLI e Streamlit

#### Use o CLI (`python fluxo_caixa_trello.py`) quando:
- Quiser automação completa (scripts, cron jobs, etc.)
- Precisar enviar automaticamente via WhatsApp
- Preferir trabalhar no terminal
- Quiser logs detalhados no console

#### Use o Streamlit (`streamlit run streamlit_app.py`) quando:
- Quiser interface visual e moderna
- Precisar demonstrar para outras pessoas
- Quiser ajustar configurações sem editar código
- Preferir interação via navegador
- Quiser compartilhar um link público (Streamlit Cloud)

### 🔒 Segurança no Streamlit Cloud

- **Nunca commite** arquivos `.env` ou `.streamlit/secrets.toml`
- Use sempre o gerenciador de secrets do Streamlit Cloud
- As credenciais são criptografadas pelo Streamlit
- Não exponha credenciais em logs ou mensagens de erro

### 📂 Estrutura Atualizada do Projeto

```
C:\Users\rafae\fluxo_caixa_trello_app\
│
├── fluxo_caixa_trello.py    # Script principal (CLI)
├── streamlit_app.py          # 🆕 Interface Streamlit
├── .env                       # Credenciais (LOCAL - NÃO COMMITAR!)
├── requirements.txt           # Dependências (inclui streamlit)
├── .gitignore                 # 🆕 Configurado para não commitar secrets
├── README.md                  # Este arquivo
│
├── .streamlit/                # 🆕 Configurações do Streamlit
│   ├── config.toml           # Tema e configurações gerais
│   └── secrets.toml.example  # Exemplo de secrets (copiar e preencher)
│
└── outputs/                   # Pasta com relatórios gerados
    ├── fluxo_caixa_20251124_143022.html
    └── ...
```

### 🆘 Troubleshooting Streamlit

#### Problema: "ModuleNotFoundError: No module named 'streamlit'"
**Solução**:
```bash
pip install streamlit
# ou
pip install -r requirements.txt
```

#### Problema: "TRELLO_API_KEY not found in secrets"
**Solução**:
- **Local**: Verifique se o arquivo `.env` existe e está preenchido
- **Cloud**: Configure os secrets na interface do Streamlit Cloud

#### Problema: "App não carrega no Streamlit Cloud"
**Solução**:
1. Verifique os logs do Streamlit Cloud
2. Certifique-se de que todos os arquivos necessários estão no repositório
3. Verifique se `requirements.txt` está atualizado
4. Confirme que os secrets estão configurados

#### Problema: "Gráfico não aparece"
**Solução**:
- Certifique-se de clicar em "🔄 Gerar Relatório"
- Verifique se as credenciais estão corretas
- Confirme que o board URL está acessível

## 👨‍💻 Autor

Desenvolvido por Claude Code em 24-25/11/2025

## 📜 Licença

Uso interno. Todos os direitos reservados.
