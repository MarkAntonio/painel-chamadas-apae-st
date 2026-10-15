# Especificação Técnica Detalhada (Versão Ultra-Leve)

Este documento detalha a implementação do **Painel de Chamadas Resiliente** usando Python para sincronização e arquivos CSV para armazenamento de dados, focado em alta performance em hardware limitado.

---

## 1. Estrutura de Diretórios

```text
/painel-de-chamadas
├── sync/                     # Sincronizador (Python)
│   ├── main.py               # Script principal de sincronização
│   ├── requirements.txt      # Dependências (requests)
│   └── .env                  # URLs das planilhas Google
│
├── frontend/                 # Painel (Vite + TS Vanilla)
│   ├── public/               # Arquivos servidos estaticamente
│   │   ├── atendimentos.csv  # Gerado pelo script Python
│   │   └── config.csv        # Gerado pelo script Python
│   ├── src/
│   │   ├── css/
│   │   │   └── style.css     # Estilos de alto contraste
│   │   ├── core/
│   │   │   ├── csv-parser.ts # Utilitário para ler CSV
│   │   │   └── types.ts      # Interfaces TS
│   │   ├── main.ts           # Lógica de rotação e renderização
│   │   └── index.html
│   └── package.json
```

---

## 2. Especificação do Sincronizador (Python)

O script `main.py` será responsável por consolidar os dados.

### Exemplo de Lógica (`sync/main.py`):
```python
import requests
import csv
import os
import time
from datetime import datetime

# Configurações via variáveis de ambiente ou arquivo direto
SHEET_URLS = {
    'pedagogico': 'URL_CSV_1',
    'saude': 'URL_CSV_2'
}
OUTPUT_PATH = '../frontend/public/atendimentos.csv'
CONFIG_PATH = '../frontend/public/config.csv'

def sync():
    all_data = []
    for setor, url in SHEET_URLS.items():
        try:
            response = requests.get(url)
            decoded_content = response.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            rows = list(cr)
            # Pula cabeçalho e adiciona o setor
            for row in rows[1:]:
                if any(row): # Evita linhas vazias
                    all_data.append(row + [setor])
        except Exception as e:
            print(f"Erro ao sincronizar {setor}: {e}")

    if all_data:
        with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['data', 'hora', 'sala', 'profissional', 'tipo', 'atendido', 'setor'])
            writer.writerows(all_data)
        print(f"Sincronização concluída: {datetime.now()}")

# Loop infinito simples (opcional, pode ser via Task Scheduler)
if __name__ == "__main__":
    while True:
        sync()
        time.sleep(300) # 5 minutos
```

---

## 3. Especificação do Frontend (Alto Contraste)

### Cores e Variáveis CSS (`frontend/src/css/style.css`)
```css
:root {
  /* Cores APAE - Alto Contraste */
  --color-green: #009541;
  --color-yellow: #FFCC00;
  --color-gray-dark: #333333;
  --color-gray-light: #F4F4F4;
  --color-white: #FFFFFF;
  
  --bg-primary: var(--color-white);
  --text-primary: var(--color-gray-dark);
  --accent-primary: var(--color-green);
  --accent-secondary: var(--color-yellow);
}

body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-family: 'Arial Black', sans-serif; /* Fonte robusta para distância */
  margin: 0;
  overflow: hidden;
}

/* Modo Single Item (1 pessoa) */
.layout-single .card {
  height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 15px solid var(--accent-primary);
  margin: 20px;
  text-align: center;
}

.layout-single .card__name {
  font-size: 8rem; /* Nome gigante */
  color: var(--accent-primary);
}

/* Modo Grid (Várias pessoas) */
.layout-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  padding: 20px;
}

.layout-grid .card {
  border-left: 20px solid var(--accent-secondary);
  background: var(--color-gray-light);
  padding: 20px;
}
```

---

## 4. Lógica de Adaptabilidade (Frontend)

O arquivo `main.ts` deve ler a configuração e decidir como renderizar:

```typescript
async function render() {
    const config = await loadConfig(); // Lê config.csv
    const atendimentos = await loadAtendimentos(); // Lê atendimentos.csv
    
    const container = document.getElementById('app');
    
    if (config.quantidade_itens_tela === 1) {
        container.className = 'layout-single';
        renderSingle(atendimentos[currentIndex]);
    } else {
        container.className = 'layout-grid';
        renderGrid(atendimentos.slice(offset, offset + config.quantidade_itens_tela));
    }
}
```

---

## 5. Divisão de Tarefas por Desenvolvedor

Esta divisão assume que o **Dev 1 foca no Backend (Python)** e o **Dev 2 foca no Frontend (TS/CSS)**.

### Sprint 1: Infraestrutura e Dados
*   **Dev 1 (Backend):**
    *   Setup do ambiente Python e arquivo `requirements.txt`.
    *   Desenvolvimento do script `main.py` para download e unificação de CSVs do Google Sheets.
    *   Lógica de proteção: manter CSV local caso o download falhe.
*   **Dev 2 (Frontend):**
    *   Setup do projeto com Vite + TypeScript.
    *   Configuração do sistema de cores e variáveis CSS (Alto Contraste).
    *   Criação do componente de Relógio Digital de alta visibilidade.

### Sprint 2: Dinâmica e Exibição
*   **Dev 1 (Backend):**
    *   Criação da lógica de geração do `config.csv` (parametrizável).
    *   Refinamento do script para rodar em loop silencioso (background).
*   **Dev 2 (Frontend):**
    *   Implementação do parser de CSV (leitura dos arquivos na pasta `public`).
    *   Desenvolvimento dos layouts "Single Item" e "Grid".
    *   Lógica de rotação automática de pacientes a cada 10 segundos.

### Sprint 3: Resiliência e Entrega
*   **Dev 1 (Backend):**
    *   Criação do script de inicialização automática (ex: `.bat` para Windows ou `.sh` para Linux).
    *   Documentação de como atualizar as URLs das planilhas no `.env`.
*   **Dev 2 (Frontend):**
    *   Implementação de animações suaves de transição (fade).
    *   Testes de responsividade para diferentes tamanhos de TV/Monitor.

---

## 6. Boas Práticas de Engenharia de Software

### Python e Backend (Sincronizador)
*   **Tratamento de Exceções:** Nunca deixe o script travar. Use blocos `try-except` em chamadas de rede e leitura de arquivos.
*   **Logs Claros:** O script deve imprimir no terminal o que está fazendo (ex: "Sincronizando setor Saúde...", "Sucesso: 10 pacientes encontrados").
*   **Variáveis de Ambiente:** URLs sensíveis ou mutáveis devem ficar no arquivo `.env`, nunca fixas no código (Hardcoded).

### TypeScript e Frontend
*   **Tipagem Estrita:** Defina interfaces para tudo. Ex: `interface IPaciente { nome: string; sala: string; }`.
*   **Componentização:** Separe a lógica (ex: parser de CSV) da visualização (ex: renderização do card).
*   **Performance:** Não faça requisições ao CSV a cada segundo. Carregue os dados em memória e atualize a memória a cada 5 minutos.

### Git e GitHub (Workflow)
*   **Branches:**
    *   `main`: Código estável, idêntico ao que está na TV da APAE.
    *   `develop`: Integração de novas funcionalidades.
    *   `feat/nome-da-task`: Branches temporárias para cada desenvolvedor.
*   **Commits:** Devem ser descritivos e em português. Ex: `feat: adiciona lógica de rotação de 10s`.
*   **Pull Requests (PRs):**
    *   Ao terminar uma task, abra um PR da sua `feat` para a `develop`.
    *   **Revisão:** O outro desenvolvedor DEVE revisar o código e aprovar antes do merge.
    *   **Critérios de Aprovação:** O código segue os padrões? As cores estão corretas? Não há erros no console?
*   **Merge:** Após aprovado, o merge deve ser feito na `develop`. O merge para `main` ocorre apenas no fim da Sprint após testes finais.

