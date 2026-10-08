# Plano de Evolucao

Este plano parte do estado implementado, sem presumir que o sincronizador Python ou uma API ja existam.

## Etapa 1: consolidada

- [x] Separar HTML, CSS e TypeScript.
- [x] Remover Tailwind via CDN.
- [x] Centralizar estilos em `src/css/style.css`.
- [x] Implementar relogio.
- [x] Implementar rotacao de chamadas.
- [x] Renderizar historico dinamicamente.
- [x] Adicionar responsividade e atributos de acessibilidade.
- [x] Ajustar a escala para uso em telas de TV wall (Full HD, 2K e 4K).
- [x] Remover `clamp()` em favor de `rem` + media queries por resolucao.
- [x] Fazer o build passar com TypeScript estrito.

## Etapa 2: dados locais

- [ ] Criar `frontend/public/atendimentos.csv` com dados de exemplo.
- [ ] Ajustar `parseCSV()` para receber texto ou manter uma funcao separada de carregamento.
- [ ] Criar `data-service.ts` com validacao de campos.
- [ ] Usar CSV no carregamento inicial e manter fallback para dados locais.

## Etapa 3: modularizacao didatica

- [ ] Mover `Call` para `core/types.ts`.
- [ ] Separar relogio em `services/clock.ts`.
- [ ] Separar rotacao em `services/rotator.ts`.
- [ ] Separar atualizacao do DOM em `ui/renderer.ts`.

A modularizacao deve ser feita quando ela tornar o conceito mais facil de estudar. Nao criar modulos apenas para aumentar a quantidade de arquivos.

## Etapa 4: robustez

- [ ] Tratar CSV com campos entre aspas e virgulas internas.
- [ ] Validar dados incompletos antes de renderizar.
- [ ] Adicionar testes do parser e do limite de historico.
- [ ] Configurar o tempo de rotacao por arquivo de configuracao.
- [ ] Definir comportamento offline quando a fonte remota falhar.

## Ajuste TV wall

O painel foi ajustado para um visual mais compatvel com exibicao em parede de TV e telas grandes:

- escala visual mais compacta em Full HD;
- aumento progressivo em 2K e 4K por media query;
- uso de `rem` e resolucao fixa em vez de `clamp()`;
- espacos internos reduzidos para manter legibilidade e densidade visual sem sobrecarregar a tela.

## Validacao de cada etapa

```bash
cd frontend
npm run build
```

Tambem testar manualmente no navegador:

- chamada inicial;
- troca automatica;
- historico com no maximo quatro itens;
- relogio;
- largura de desktop, Full HD, 2K e 4K;
- ausencia de texto sobreposto.

