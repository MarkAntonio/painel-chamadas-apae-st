# Explicacao Didatica do Frontend

Este documento acompanha o codigo atual. A aplicacao usa HTML semantico, CSS tradicional e TypeScript compilado pelo Vite.

## 1. HTML: estrutura

`index.html` define apenas a estrutura da pagina e importa o ponto de entrada:

```html
<script type="module" src="/src/main.ts"></script>
```

As areas principais sao:

- `.main-stage`: chamada atual;
- `.history-sidebar`: historico;
- `.new-call-overlay`: aviso visual de nova chamada;
- `.footer`: relogio e ticker.

Os elementos que recebem dados possuem IDs. Por exemplo, `#main-user-name` e atualizado pelo TypeScript.

## 2. CSS: apresentacao

`src/css/style.css` concentra:

- variaveis de cor em `:root`;
- escala visual por `rem` e media queries em resolucoes fixas;
- layout de 70% para a chamada e 30% para o historico;
- media query em `768px` para mobile;
- breakpoint extra para televisores e telas grandes em `1800px`, `2560px` e `3840px`;
- animacoes de entrada e ticker.

A estrategia atual evita `clamp()` para tornar o comportamento mais previsivel em exibicoes de TV wall e facilitar a manutencao do painel em HD, 2K e 4K.

Para praticar CSS, altere uma variavel como `--primary` ou ajuste uma regra de `.detail-card` e observe o efeito no navegador.

## 3. TypeScript: comportamento

`src/main.ts` possui quatro ideias importantes:

### Dados

`calls` e uma lista de chamadas de demonstracao. Cada item tem `id`, `name`, `room`, `time` e `professional`.

### DOM tipado

`getElement()` procura um elemento por ID e gera um erro claro se ele nao existir. O tipo generico ajuda o TypeScript a entender que o elemento e, por exemplo, um `HTMLTimeElement`.

### Relogio

`updateClock()` le a hora do navegador, atualiza o texto de `#digital-clock` e registra o valor ISO no atributo `datetime`. O `setInterval` executa a funcao a cada segundo.

### Rotacao e historico

`rotateCall()` escolhe o proximo item. `updateDisplay()` atualiza a chamada principal, coloca o item no inicio de `visibleHistory` e limita a lista a quatro registros. `renderHistory()` transforma os dados em elementos `li`.

## 4. Ajuste TV wall

O layout foi desenhado para ficar compacto em Full HD e aumentar progressivamente em telas maiores. O objetivo e manter:

- leitura facil a distancia;
- densidade visual aceitavel;
- proporcao adequada para TV wall;
- responsividade sem perder consistencia visual em resolucoes diferentes.

Em termos práticos, a escala base de fontes e espacos e definida em `rem` e os ajustes de tela grande ficam em media queries bem definidas, em vez de `clamp()`.

## 5. CSV

`src/core/csv-parser.ts` carrega um arquivo por `fetch`, usa a primeira linha como cabecalho e retorna objetos. Ele ainda nao esta conectado ao fluxo da tela. Essa separacao permite estudar o parser antes de integrar uma fonte de dados real.

O parser atual assume CSV simples, sem virgulas internas entre aspas. O proximo exercicio e tratar corretamente campos escapados e validar cabecalhos.

## 6. Acessibilidade

A pagina usa `main`, `section`, `aside`, `footer`, `time`, `h1` e `h2`. As areas que mudam possuem `aria-live`, e os icones decorativos possuem `aria-hidden`.

Ao alterar o projeto, mantenha contraste alto, evite texto cortado e nao remova os nomes acessiveis das regioes.

## 7. Exercicios sugeridos

1. Troque o intervalo de `15000` para `5000` e observe a rotacao.
2. Adicione uma propriedade `sector` e mostre-a no historico.
3. Crie um arquivo CSV em `public/` e use `parseCSV()` no console.
4. Separe `updateClock()` em um modulo proprio.
5. Adicione um teste para uma linha CSV vazia.

Depois de qualquer alteracao, execute `npm run build` dentro de `frontend/`.
