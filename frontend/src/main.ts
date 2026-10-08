import './css/style.css';

interface Call {
  id: string;
  name: string;
  room: string;
  time: string;
  professional: string;
}

const calls: Call[] = [
  { id: 'P043', name: 'Marcos Oliveira', room: 'Sala 08', time: '08:15', professional: 'Dra. Ana Silva' },
  { id: 'A119', name: 'Beatriz Santos', room: 'Triagem', time: '08:20', professional: 'Enf. Carla' },
  { id: 'P044', name: 'Fernando Costa', room: 'Sala 05', time: '08:30', professional: 'Dr. Victor Santos' },
  { id: 'C013', name: 'Juliana Alves', room: 'Sala 02', time: '08:45', professional: 'Dra. Julia' }
];

const visibleHistory: Call[] = [
  { id: 'H001', name: 'Maria Eduarda', room: 'Triagem', time: '14:25', professional: '' },
  { id: 'H002', name: 'Ricardo Gomes', room: 'Sala 02', time: '14:18', professional: '' },
  { id: 'H003', name: 'Ana Beatriz', room: 'Sala 05', time: '14:10', professional: '' },
  { id: 'H004', name: 'Andreina Gomes', room: 'Sala 02', time: '14:00', professional: '' }
];

let currentIndex = 0;
const rotationTime = 15000;

function getElement<T extends HTMLElement>(id: string): T {
  const element = document.getElementById(id);
  if (!element) throw new Error(`Elemento #${id} não encontrado.`);
  return element as T;
}

function updateClock(): void {
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const clock = getElement<HTMLTimeElement>('digital-clock');
  clock.textContent = `${hours}:${minutes}`;
  clock.dateTime = now.toISOString();
}

function renderHistory(): void {
  const historyList = getElement<HTMLOListElement>('history-list');
  historyList.innerHTML = visibleHistory.map((call) => `
    <li class="history-item">
      <div class="history-item__topline"><strong>${call.name}</strong><time datetime="${call.time}">${call.time}</time></div>
      <span>${call.room}</span>
    </li>
  `).join('');
}

function showNewCall(): void {
  const overlay = getElement<HTMLDivElement>('new-call-overlay');
  overlay.classList.add('new-call-overlay--visible');
  window.setTimeout(() => overlay.classList.remove('new-call-overlay--visible'), 800);
}

function updateDisplay(call: Call): void {
  showNewCall();
  getElement('main-user-name').textContent = call.name;
  getElement('main-destination').textContent = call.room;
  getElement('main-time').textContent = call.time;
  getElement('main-professional').textContent = call.professional;
  visibleHistory.unshift(call);
  visibleHistory.splice(4);
  renderHistory();
  const container = getElement('active-call-container');
  container.classList.remove('active-call--updated');
  void container.offsetWidth;
  container.classList.add('active-call--updated');
}

function rotateCall(): void {
  updateDisplay(calls[currentIndex]);
  currentIndex = (currentIndex + 1) % calls.length;
}

updateClock();
renderHistory();
window.setInterval(updateClock, 1000);
window.setInterval(rotateCall, rotationTime);
