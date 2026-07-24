# Diretrizes do Projeto - Painel de Chamadas Resiliente (Versão Ultra-Leve)

## 1. Arquitetura do Sistema

O sistema foi simplificado para rodar em hardware limitado, utilizando arquivos CSV como "banco de dados" e sem a necessidade de um servidor de API ativo.

1.  **Sync Service (Python):** Script autônomo que roda em loop (ex: a cada 5 min). Ele baixa as planilhas do Google (CSV), unifica os dados e salva os arquivos `atendimentos.csv` e `configuracoes.csv` diretamente na pasta pública do frontend.
2.  **Armazenamento (CSV):** Arquivos locais simples que garantem o funcionamento offline total após a primeira sincronização.
3.  **Frontend (Painel):** Aplicação Single Page (Vite + TS Vanilla) que consome os arquivos CSV locais como recursos estáticos e renderiza a interface.

---

## 2. Padrões de Desenvolvimento

### Python (Sincronizador)
- **Simplicidade:** Usar bibliotecas nativas (`csv`, `urllib`) ou `requests` para minimizar o peso da instalação.
- **Robustez:** O script deve ignorar erros de conexão e manter os arquivos locais se a internet cair.

### TypeScript e JavaScript
- **Consumo de CSV:** Utilizar `fetch()` para carregar os arquivos estáticos e um parser leve.
- **Nomenclatura:** `camelCase` para variáveis/funções, `PascalCase` para classes/interfaces.

### Visual (Alto Contraste)
- **Cores APAE:** Verde (`#009541`), Amarelo (`#FFCC00`), Cinza (`#555555`), Branco (`#FFFFFF`).
- **Fundo:** Claro (Branco ou Cinza muito claro) para máxima visibilidade em ambientes iluminados.
- **Tipografia:** Fontes grandes e negritas para leitura à distância.

---

## 3. Plano de Desenvolvimento (Sprints)

### Sprint 1: Sincronização e Estrutura CSV
**Backend (Python):**
- Script de download de Google Sheets via URL de exportação CSV.
- Lógica de unificação (Merge) de múltiplas planilhas em um único `atendimentos.csv`.
- Geração do arquivo `configuracoes.csv` com parâmetros de exibição.

**Frontend (Base):**
- Setup do projeto Vite + TypeScript.
- Configuração do CSS base com as cores de alto contraste e variáveis.
- Implementação do Relógio de alta visibilidade.

### Sprint 2: Lógica de Exibição Dinâmica
**Frontend:**
- Lógica para carregar e parsear CSVs da pasta `/public`.
- Implementação da visualização "Single Item" (1 pessoa por vez) como padrão.
- Lógica de rotação automática (10 segundos) lendo do `configuracoes.csv`.
- Mecanismo de auto-ajuste: se `quantidade_itens_tela > 1`, o layout muda para grade/lista automaticamente.

### Sprint 3: Resiliência e Polimento
**Sincronizador:**
- Implementação de log de status (última sincronização bem-sucedida).
- Script de inicialização automática ao ligar o computador (ex: .bat ou .sh).

**Frontend:**
- Animações de transição suaves (fade-in/out) para evitar "piscadas" na troca de nomes.
- Ajustes finos de contraste e tamanhos de fonte baseados em testes reais.
- Placeholder para avisos institucionais.
