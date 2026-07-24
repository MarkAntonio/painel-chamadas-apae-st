// Definições de tipos e interfaces do sistema
export interface IAtendimento {
  data: string;
  hora: string;
  sala: string;
  profissional: string;
  tipo: string;
  atendido: string;
  setor: 'pedagogico' | 'saude';
}

export interface IConfig {
  tempo_rotacao: number;
  quantidade_itens_tela: number;
  alerta_sonoro: boolean;
}
