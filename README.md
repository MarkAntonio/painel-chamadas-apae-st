# Painel de Chamadas APAE

Comece pelo [GUIA_DO_PROJETO.md](GUIA_DO_PROJETO.md). Ele apresenta o mapa da documentacao, o fluxo da aplicacao e quais arquivos devem ser alterados em cada tipo de tarefa.

Painel de sinalizacao digital para uma sala de espera da APAE. O projeto foi mantido pequeno de proposito: ele serve como laboratorio pratico para aprender HTML, CSS, TypeScript e Vite.

## Estado atual

A aplicacao e um frontend Vite com TypeScript vanilla. Ela exibe:

- uma chamada atual em destaque;
- destino, horario e profissional;
- as quatro ultimas chamadas;
- relogio atualizado a cada segundo;
- faixa de avisos animada;
- layout responsivo para telas menores;
- dados locais de demonstracao, rotacionados a cada 15 segundos.

A orientacao detalhada para pessoas e IAs esta em [AGENTS.md](AGENTS.md). O design esta documentado em [DESIGN.md](DESIGN.md).

## Estrutura principal

```text
frontend/
├── index.html              # Estrutura semantica
├── package.json             # Scripts e dependencias
├── tsconfig.json            # TypeScript estrito
├── vite.config.ts          # Configuracao do servidor Vite
└── src/
    ├── main.ts              # Relogio, rotacao, historico e DOM
    ├── css/style.css        # Variaveis, layout e responsividade
    └── core/
        ├── csv-parser.ts    # Parser CSV independente
        └── types.ts         # Tipos do dominio em evolucao
```

## Executar

Entre na pasta `frontend/` antes de executar os comandos:

```bash
cd frontend
npm install
npm run dev
```

O Vite normalmente abre `http://localhost:5173`.

Para validar o projeto:

```bash
npm run build
```

O build executa o compilador TypeScript e gera a versao de producao em `frontend/dist/`.

## Como estudar o projeto

1. Comece pelo `index.html` e identifique os elementos com IDs.
2. Leia `style.css` e associe cada classe a uma parte visual.
3. Acompanhe em `main.ts` como `getElement()`, `updateClock()`, `renderHistory()` e `updateDisplay()` alteram o DOM.
4. Altere uma chamada no array local e observe a rotacao.
5. Depois estude `csv-parser.ts` e conecte uma fonte CSV como exercicio.

## Proximas evolucoes

- carregar chamadas de `public/atendimentos.csv`;
- usar um servico de dados com fallback offline;
- mover tipos e responsabilidades para modulos separados;
- adicionar testes para o parser;
- permitir configuracao do intervalo de rotacao.

Consulte [AGENTS.md](AGENTS.md) antes de fazer mudancas maiores.
