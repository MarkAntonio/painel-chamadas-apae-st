# 🟢🟡 Painel de Chamadas Resiliente (Versão Ultra-Leve)

[![Licença: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Vite: TypeScript](https://img.shields.io/badge/Vite-TypeScript-blueviolet.svg)](https://vitejs.dev/)

O **Painel de Chamadas Resiliente** é uma solução de sinalização digital de alta visibilidade e resiliência offline desenvolvida sob medida para a **APAE**. Projetado para rodar em hardware extremamente limitado, o sistema dispensa APIs complexas ou bancos de dados pesados, utilizando uma arquitetura ultra-leve e tolerante a falhas de conexão baseada em sincronização via **Python** e armazenamento local em **arquivos CSV**.

---

## 🧭 Visão Geral & Diferenciais

- **Resiliência Offline Total:** Após a primeira sincronização bem-sucedida, o painel funciona de forma 100% offline. Se a internet oscilar ou cair, o painel continua rodando com os últimos dados salvos.
- **Visual de Alto Contraste (Cores APAE):** Cores institucionais aplicadas estrategicamente para máxima acessibilidade e legibilidade à distância:
  - 🟢 **Verde APAE** (`#009541`)
  - 🟡 **Amarelo APAE** (`#FFCC00`)
  - ⚫ **Cinza Escuro** (`#333333`)
  - ⚪ **Branco** (`#FFFFFF`)
- **Layout Inteligente & Adaptável:** Transiciona automaticamente entre:
  - **Single Item (Padrão):** 1 pessoa por vez em tamanho gigante (ideal para salas de espera e leitura de longe).
  - **Grid/Lista:** Se configurado para exibir múltiplos itens, ajusta-se dinamicamente para uma grade organizada de alta densidade visual.
- **Sem Infraestrutura Complexa:** Um script Python unifica as planilhas do Google Sheets diretamente em arquivos CSV públicos consumidos pelo frontend SPA (Vite + TS Vanilla).

---

## 📐 Arquitetura do Sistema

```text
       ┌────────────────────────┐
       │ Google Sheets (Nuvem)  │ ◄── Cadastro/Edição de Atendimentos
       └───────────┬────────────┘
                   │ Exportação CSV (HTTP)
                   ▼
       ┌────────────────────────┐
       │   Sync Service (Py)    │ ◄── Script em loop (Tolerante a queda de rede)
       └───────────┬────────────┘
                   │ Escrita Direta Local
                   ▼
┌───────────────────────────────────────┐
│              Frontend                 │
│  ┌─────────────────────────────────┐  │
│  │     Público (public/)           │  │
│  │  - atendimentos.csv             │  │
│  │  - config.csv                   │  │
│  └────────────────┬────────────────┘  │
│                   │ Fetch Estático Local (Offline)
│                   ▼
│  ┌─────────────────────────────────┐  │
│  │   SPA (Vite + TypeScript)       │  │
│  │  - Rotação Automática (10s)     │  │
│  │  - Visual Alto Contraste APAE   │  │
│  │  - Layout Adaptativo Dinâmico   │  │
│  └─────────────────────────────────┘  │
└───────────────────────────────────────┘
```

---

## 📂 Estrutura de Diretórios

```text
/painel-de-chamadas
├── sync/                     # Sincronizador (Python)
│   ├── main.py               # Script principal de sincronização e download
│   ├── requirements.txt      # Dependências mínimas (requests)
│   └── .env                  # Variáveis de ambiente (URLs das planilhas)
│
├── frontend/                 # Painel (Vite + TS Vanilla)
│   ├── public/               # Arquivos estáticos servidos localmente
│   │   ├── atendimentos.csv  # Banco de dados de chamadas gerado pelo Sync
│   │   └── config.csv        # Parâmetros de exibição gerados pelo Sync
│   ├── src/
│   │   ├── css/
│   │   │   └── style.css     # Estilos globais e variáveis de alto contraste
│   │   ├── core/
│   │   │   ├── csv-parser.ts # Utilitário leve de parsing de arquivos CSV
│   │   │   └── types.ts      # Tipagens TypeScript do sistema
│   │   ├── main.ts           # Lógica de controle de exibição, adaptabilidade e rotação
│   │   └── index.html
│   └── package.json
```

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
- **Python 3.10+**
- **Node.js 18+** & **npm**

---

### 2. Configurando o Sincronizador (Python)

1. Navegue até a pasta de sincronização:
   ```bash
   cd sync
   ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie um arquivo `.env` baseado no modelo e configure as URLs de exportação CSV das planilhas públicas do Google Sheets:
   ```env
   URL_PLANILHA_PEDAGOGICO="https://docs.google.com/spreadsheets/d/e/CHAVE/pub?output=csv"
   URL_PLANILHA_SAUDE="https://docs.google.com/spreadsheets/d/e/CHAVE/pub?output=csv"
   ```
5. Execute o script de sincronização:
   ```bash
   python main.py
   ```

---

### 3. Configurando o Painel (Frontend)

1. Navegue até a pasta do frontend:
   ```bash
   cd ../frontend
   ```
2. Instale as dependências do projeto Vite:
   ```bash
   npm install
   ```
3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```
4. O painel estará disponível localmente no endereço exibido no terminal (geralmente `http://localhost:5173`).

---

## ⚙️ Configurações Dinâmicas (`config.csv`)

O painel é reconfigurável sem a necessidade de novos deploys através de parâmetros no arquivo `config.csv` gerado pelo sincronizador:

| Parâmetro | Descrição | Valores Padrão |
| :--- | :--- | :--- |
| `tempo_rotacao` | Tempo em segundos de exibição de cada item no modo Single. | `10` |
| `quantidade_itens_tela` | Define o modo de exibição (1 para Single, >1 para Grid de alta densidade). | `1` |
| `alerta_sonoro` | Ativa/desativa bipe de áudio ao atualizar chamadas novas. | `true` |

---

## 🎨 Cores e Estilo Visual

Desenvolvido sob rígidos padrões de acessibilidade visual de longe:
- **Fonte Padrão:** `Arial Black`, `Impact` ou fontes sans-serif robustas de alta espessura para evitar distorção à distância.
- **Tipografia Fluida:** Dimensionada com unidades responsivas (`rem` e `vh`/`vw`) para preencher telas de TVs e projetores de variadas resoluções sem quebras de layout.

---

## 📄 Licença

Este projeto está licenciado sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.
