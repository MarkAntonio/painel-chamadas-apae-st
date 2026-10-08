# Guia de Trabalho para Pessoas e IAs

Este arquivo e a fonte principal de contexto para alteracoes no projeto. Leia-o antes de modificar codigo.

## Objetivo

O projeto e um painel de chamadas para a APAE. A tela mostra uma chamada atual em destaque, as quatro chamadas mais recentes, um relogio e uma faixa de avisos. A prioridade e legibilidade a distancia, acessibilidade e uma arquitetura simples para estudo de HTML, CSS, TypeScript e Vite.

## Estado atual

- Frontend: Vite 5 + TypeScript estrito, sem framework.
- Entrada HTML: `frontend/index.html`.
- Logica: `frontend/src/main.ts`.
- Estilos: `frontend/src/css/style.css`.
- Dados exibidos: array local de demonstracao em `main.ts`.
- Rotacao: uma chamada a cada 15 segundos.
- Historico: renderizado pelo TypeScript e limitado a quatro itens.
- Relogio: atualizado a cada segundo no fuso local do navegador.
- Parser CSV: existe em `frontend/src/core/csv-parser.ts`, mas ainda nao e usado pelo fluxo principal.
- Tipos de dominio: estao em `frontend/src/core/types.ts`, mas a interface `Call` atual ainda esta local em `main.ts`.
- Sincronizador Python: a pasta `sync/` e uma direcao planejada; nao assuma que seus arquivos ja estao implementados.
- Ajuste visual: layout otimizado para TV wall com escala compacta em Full HD e proporcional em 2K/4K.

## Estrutura

```text
projeto-painel-chamadas/
├── frontend/
│   ├── index.html              # Estrutura semantica da tela
│   ├── package.json             # Scripts npm e dependencias
│   ├── tsconfig.json            # TypeScript estrito
│   ├── vite.config.ts           # Servidor Vite na porta 5173
│   └── src/
│       ├── main.ts              # Estado de demonstracao, DOM, relogio e rotacao
│       ├── css/style.css        # Variaveis, layout, componentes e responsividade
│       └── core/
│           ├── csv-parser.ts    # Leitura basica de CSV via fetch
│           └── types.ts         # Interfaces do dominio futuro
├── sync/                        # Integracao futura com planilhas/CSV
├── DESIGN.md                    # Direcao visual
└── README.md                    # Visao geral e comandos
```

## Regras de arquitetura

1. HTML define estrutura, sem logica de negocio e sem estilos inline.
2. CSS define cores, dimensoes, responsividade e animacoes. Use as variaveis de `style.css`.
3. TypeScript controla estado, DOM e temporizadores.
4. Evite adicionar Tailwind via CDN. O projeto usa CSS tradicional para permanecer pedagogico e funcionar no build do Vite.
5. Preserve os IDs usados pelo TypeScript: `main-user-name`, `main-destination`, `main-time`, `main-professional`, `history-list`, `new-call-overlay` e `digital-clock`.
6. Prefira elementos semanticos (`main`, `section`, `aside`, `footer`, `time`, `ol`/`li`) e atributos ARIA quando houver atualizacao dinamica.
7. Nao adicione bibliotecas ou backend sem necessidade clara. O painel deve continuar leve e tolerante a uso offline.
8. Nao reverter alteracoes existentes do usuario. Mantenha mudancas pequenas e focadas.
9. Evite `clamp()` em novos ajustes; prefira `rem` e media queries por resolucao para manter previsibilidade em exibicoes de TV wall.

## Fluxo atual da aplicacao

1. O navegador carrega `frontend/index.html`.
2. O script `type="module"` importa `/src/main.ts`.
3. `main.ts` inicializa o relogio e desenha o historico inicial.
4. A cada segundo, `updateClock()` atualiza o texto e o atributo `datetime`.
5. A cada 15 segundos, `rotateCall()` chama `updateDisplay()`.
6. `updateDisplay()` atualiza a chamada principal, insere a chamada no inicio do historico, remove itens acima de quatro e exibe o overlay.

## Ajuste TV wall

A escala visual do painel deve seguir estas regras:

- 1080p: mais compacto, visando leitura a distancia sem excesso de whitespace;
- 2K: aumento suave de espaco e tipografia;
- 4K: aumento moderado para manter legibilidade sem exagerar no tamanho;
- `rem` e media queries por resolucao sao priorizados em vez de `clamp()`;
- o layout continua responsivo para mobile e telas menores.

## Comandos

Execute os comandos dentro de `frontend/`:

```bash
npm install
npm run dev
npm run build
npm run preview
```

O build executa `tsc` e depois `vite build`. O TypeScript usa `strict`, `noUnusedLocals`, `noUnusedParameters` e `noImplicitReturns`; qualquer codigo novo precisa respeitar essas regras.

## Como fazer alteracoes com seguranca

- Antes de editar, localize o elemento, funcao ou tipo que controla o comportamento.
- Para uma mudanca visual, altere `style.css` e valide em desktop e largura pequena.
- Para uma mudanca de comportamento, altere `main.ts` e preserve a renderizacao inicial.
- Ao trocar a fonte de dados para CSV, valide o formato antes de renderizar e trate falhas de rede mantendo dados locais.
- Nao use `innerHTML` com dados externos sem escapar ou validar os valores. O historico atual usa dados estaticos confiaveis; essa decisao deve ser revista ao conectar CSV real.
- Depois de editar, execute `npm run build` dentro de `frontend/`.

## Proximos passos recomendados

1. Mover `Call` para `core/types.ts` e alinhar os nomes com `IAtendimento`.
2. Criar um `data-service.ts` que use `parseCSV()` para carregar `public/atendimentos.csv`.
3. Fazer a tela usar dados CSV com fallback para dados locais quando o arquivo nao estiver disponivel.
4. Separar relogio, rotacao e renderer em modulos apenas quando isso ajudar o aprendizado.
5. Adicionar testes do parser para linhas vazias, cabecalhos e valores ausentes.
6. Adicionar controle configuravel para intervalo de rotacao e audio, sem quebrar o modo demonstracao.

## Checklist de revisao

- A alteracao atende ao objetivo do painel?
- O HTML continua sem scripts ou estilos inline?
- A responsividade evita texto cortado ou sobreposto?
- A atualizacao dinamica continua acessivel?
- O ajuste TV wall permanece legivel em Full HD, 2K e 4K?
- O build passa com `npm run build`?
- A documentacao ainda descreve o codigo real?

