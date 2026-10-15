import './css/style.css';
// Aprendizado Marco: sigla APMC
interface Call {
  // id: string;
  name: string;
  room: string;
  time: string;
  professional: string;
}

// APMC: lista a ser preenchida pelos dados de todos os assisitidos de hoje. É imporanta que haja um filtro para consultar apenas os assistidos do dia atual.
const calls: Call[] = [
  { name: 'Jurídico Batista', room: 'Sala 08', time: '08:15', professional: 'Dra. Ana Silva' },
  { name: 'José Caruá', room: 'Triagem', time: '08:20', professional: 'Enf. Carla' },
  { name: 'Cordeiro Gomes', room: 'Sala 05', time: '08:30', professional: 'Dr. Victor Santos' },
  { name: 'Juliana Alves', room: 'Sala 02', time: '08:45', professional: 'Dra. Julia' }
];

// APMC: lista dos assistidos a serem exibidos no histórico da pilha lateral direta da tela.
const visibleHistory: Call[] = [
  { name: 'Maria Eduarda', room: 'Triagem', time: '14:25', professional: '' },
  { name: 'Ricardo Gomes', room: 'Sala 02', time: '14:18', professional: '' },
  { name: 'Ana Beatriz', room: 'Sala 05', time: '14:10', professional: '' },
  { name: 'Andreina Gomes', room: 'Sala 02', time: '14:00', professional: '' }
];

// APMC: index inicial da lista calls, que deve ser atualizado para que exiba somente o que estiver na hora atual, para que, se o sistema reiniciar, não seja exibido o primeiro assistido do dia, mas sempre o que estiver perto da hora atual (30 mitutos de janela, 15 antes e 15 depois, tendo como prioridade os que estiverem mais próximo da hora atual)
let currentIndex = 0;

// APMC: limita a quantiade de itens a serem exibidos no histórico da pilha lateral direita da tela.
const QUANTIDADE_ITENS_HISTORICO = 5;

//APMC: tempo em que cada assistido ficará no centro da tela.
const rotationTimeMilisseconds = 15000;

// APMC: função que pega o elemento DOM pelo ID. Apenas uma atualização do método built-in, levantando uma exceção personalizada.
function getElement<T extends HTMLElement>(id: string): T {
  const element = document.getElementById(id);
  if (!element)
    throw new Error(`Elemento #${id} não encontrado.`);
  return element as T;
}

//APMC: atualiza e seta o relógio com o horário atual
function updateClock(): void {
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  const clock = getElement<HTMLTimeElement>('digital-clock');
  clock.textContent = `${hours}:${minutes}:${seconds}`;
  clock.dateTime = now.toISOString();
}

// APMC:Renderiza o histórico de chamadas na pilha à direita da tela, onde o map percorre a lista visibleHistory e cria elementos HTML para cada chamada, exibindo o nome, horário e sala do assistido.
function renderHistory(): void {
  const historyList = getElement<HTMLOListElement>('history-list');
  historyList.innerHTML = visibleHistory.map((call) => `
    <li class="history-item">
      <div class="history-item__topline">
        <strong>${call.name}</strong>${call.time}
      </div>
      <span>${call.room}</span>
    </li>
  `).join('');
}

// APMC: função que exibe a div de nova chamada e o invisibiliza após 800 ms.
function showNewCall(): void {
  const overlay = getElement<HTMLDivElement>('new-call-overlay');
  overlay.classList.add('new-call-overlay--visible');
  window.setTimeout(() => overlay.classList.remove('new-call-overlay--visible'), 800);
}

//APMC: função agregadora que executa todos os outros métodos de atualização, além de atualizar o painel central da tela com os dados do assistido atual, adicionando-o ao histórico e aplicando uma animação de atualização.
function updateDisplay(call: Call): void {
  showNewCall();
  getElement('main-user-name').textContent = call.name;
  getElement('main-destination').textContent = call.room;
  getElement('main-time').textContent = call.time;
  getElement('main-professional').textContent = call.professional;
  visibleHistory.unshift(call);
  if (visibleHistory.length > QUANTIDADE_ITENS_HISTORICO) {
  visibleHistory.pop(); // Remove exatamente o último elemento (mais eficiente que splice)
  }
  renderHistory();
  const container = getElement('active-call-container');
  container.classList.remove('active-call--updated');
  void container.offsetWidth;
  container.classList.add('active-call--updated');
}

// APMC: rotaciona os itens na tela central, de acord ocom os itens disponívels naquele momento. AINDA SERÁ NECESSÁRIO CONFIGURAR A LÓGICA DA JANELA DE 15 E 15 MINUTOS (30 MINUTOS)
function rotateCall(): void {
  updateDisplay(calls[currentIndex]);
  currentIndex = (currentIndex + 1 < calls.length) ? currentIndex + 1 : 0;
}

updateClock();
renderHistory();

// estudar AINDA
window.setInterval(updateClock, 1000);
window.setInterval(rotateCall, rotationTimeMilisseconds);
