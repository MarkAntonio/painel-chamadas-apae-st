import os
import sys
import csv
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"[AVISO] Arquivo .env não encontrado em: {dotenv_path}")
    print("Usando valores padrão de configuração.")

# Caminhos de saída definidos dinamicamente e com fallback robusto
FRONTEND_PUBLIC_DIR = os.path.abspath(os.path.join(script_dir, '..', 'frontend', 'public'))
OUTPUT_PATH = os.path.join(FRONTEND_PUBLIC_DIR, 'atendimentos.csv')
CONFIG_PATH = os.path.join(FRONTEND_PUBLIC_DIR, 'config.csv')

# Diretório para cache local de resiliência caso a rede caia
CACHE_DIR = os.path.join(script_dir, '.cache')
os.makedirs(CACHE_DIR, exist_ok=True)

# Dados Mock estruturados para quando os links forem os padrões (.env com placeholders)
# ou caso o download falhe e não haja cache local anterior.
MOCK_PEDAGOGICO = [
    ["03/08/2026", "08:15", "Sala 03", "Prof. Ana Souza (Psicopedagoga)", "Atendimento Individual", "João Silva Santos"],
    ["03/08/2026", "09:00", "Sala 01", "Prof. Marcos Lima (Pedagogo)", "Avaliação Pedagógica", "Maria Eduarda Alves"],
    ["03/08/2026", "10:15", "Sala 03", "Prof. Ana Souza (Psicopedagoga)", "Atendimento Individual", "Lucas Ferreira Costa"],
    ["03/08/2026", "11:00", "Sala 02", "Prof. Beatriz Costa (Pedagoga)", "Atividade Psicomotora", "Pedro Oliveira Santos"],
    ["03/08/2026", "13:30", "Sala 01", "Prof. Marcos Lima (Pedagogo)", "Atendimento Individual", "Gabriel Souza Ramos"],
    ["03/08/2026", "14:15", "Sala 05", "Prof. Beatriz Costa (Pedagoga)", "Atendimento Coletivo", "Ana Beatriz Pinheiro"]
]

MOCK_SAUDE = [
    ["03/08/2026", "08:00", "Consultório 1", "Dra. Patrícia Alves (Fisioterapeuta)", "Fisioterapia Motora", "Juliana Ribeiro Dias"],
    ["03/08/2026", "08:45", "Consultório 2", "Dr. Roberto Melo (Fonoaudiólogo)", "Terapia de Linguagem", "Enzo Rodrigues Lima"],
    ["03/08/2026", "09:30", "Consultório 1", "Dra. Patrícia Alves (Fisioterapeuta)", "Terapia Ocupacional", "Sofia Castro Mendes"],
    ["03/08/2026", "10:30", "Consultório 3", "Dra. Camila Duarte (Neuropediatra)", "Consulta Clínica", "Arthur Almeida Prado"],
    ["03/08/2026", "14:00", "Consultório 2", "Dr. Roberto Melo (Fonoaudiólogo)", "Audiometria", "Matheus Vieira Rocha"],
    ["03/08/2026", "15:00", "Consultório 3", "Dra. Camila Duarte (Neuropediatra)", "Avaliação de Desenvolvimento", "Laura Castro Ferreira"]
]

def is_placeholder(url):
    """Verifica se a URL configurada é apenas um placeholder do .env.example."""
    return not url or "SUA_CHAVE_AQUI" in url or "pub?output=csv" not in url

def download_sheet(setor, url):
    """
    Baixa o CSV correspondente ao setor do Google Sheets.
    Implementa um mecanismo de cache em arquivo local e fallback para mock.
    """
    cache_file = os.path.join(CACHE_DIR, f"{setor}_cache.csv")
    
    if is_placeholder(url):
        print(f"[{setor.upper()}] URL do Google Sheets é um placeholder ou vazia. Carregando dados Mock de demonstração.")
        mock_data = MOCK_PEDAGOGICO if setor == 'pedagogico' else MOCK_SAUDE
        # Salva o mock no cache local para resiliência consistente
        try:
            with open(cache_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['data', 'hora', 'sala', 'profissional', 'tipo', 'atendido'])
                writer.writerows(mock_data)
        except Exception as e:
            print(f"[{setor.upper()}] Erro ao gravar cache local do mock: {e}")
        return mock_data

    # Tentativa de download da planilha real
    print(f"[{setor.upper()}] Baixando planilha de: {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        decoded_content = response.content.decode('utf-8')
        # Faz parse simples para validar se é de fato um CSV
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        rows = list(cr)
        
        if not rows:
            raise ValueError("Planilha baixada está vazia.")
            
        # Salva a cópia com sucesso no cache de resiliência local
        with open(cache_file, 'w', newline='', encoding='utf-8') as f:
            f.write(decoded_content)
            
        print(f"[{setor.upper()}] Download concluído com sucesso e armazenado em cache.")
        
        # Ignora a linha de cabeçalho do CSV baixado e filtra linhas em branco
        data_rows = []
        for row in rows[1:]:
            if row and any(cell.strip() for cell in row):
                data_rows.append(row[:6]) # Limita a 6 colunas padrão
        return data_rows

    except Exception as e:
        print(f"[ERRO - {setor.upper()}] Falha na sincronização online: {e}")
        
        # Tenta carregar do cache local
        if os.path.exists(cache_file):
            print(f"[{setor.upper()}] RESILIÊNCIA: Carregando dados armazenados em cache local...")
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cr = csv.reader(f, delimiter=',')
                    rows = list(cr)
                    data_rows = []
                    for row in rows[1:]:
                        if row and any(cell.strip() for cell in row):
                            data_rows.append(row[:6])
                    return data_rows
            except Exception as cache_err:
                print(f"[{setor.upper()}] Erro crítico ao ler o arquivo de cache local: {cache_err}")
        
        # Caso não haja cache, usa os dados Mock padrão como última barreira para o painel não abrir em branco
        print(f"[{setor.upper()}] Sem cache disponível. Carregando dados Mock de emergência.")
        mock_data = MOCK_PEDAGOGICO if setor == 'pedagogico' else MOCK_SAUDE
        return mock_data

def sync():
    """Executa o processo principal de sincronização de dados e gravação de parâmetros."""
    print(f"\n--- Iniciando Sincronização em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ---")
    
    # 1. Obter URLs do ambiente
    url_pedagogico = os.environ.get('URL_PLANILHA_PEDAGOGICO', '')
    url_saude = os.environ.get('URL_PLANILHA_SAUDE', '')
    
    # 2. Baixar dados de ambos os setores
    dados_pedagogico = download_sheet('pedagogico', url_pedagogico)
    dados_saude = download_sheet('saude', url_saude)
    
    # 3. Unificar dados rotulando com o respectivo setor
    all_data = []
    
    # Adiciona dados pedagógicos
    for row in dados_pedagogico:
        # Preenche com vazios caso a linha tenha menos colunas que o esperado
        row_filled = row + [''] * (6 - len(row))
        all_data.append(row_filled + ['pedagogico'])
        
    # Adiciona dados de saúde
    for row in dados_saude:
        row_filled = row + [''] * (6 - len(row))
        all_data.append(row_filled + ['saude'])
        
    # Ordena os atendimentos por hora para exibição cronológica
    try:
        all_data.sort(key=lambda x: x[1])
    except Exception as sort_err:
        print(f"[AVISO] Erro ao ordenar por hora: {sort_err}")

    # 4. Gravar o arquivo unificado atendimentos.csv na pasta do frontend
    os.makedirs(FRONTEND_PUBLIC_DIR, exist_ok=True)
    
    try:
        with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['data', 'hora', 'sala', 'profissional', 'tipo', 'atendido', 'setor'])
            writer.writerows(all_data)
        print(f"[SUCESSO] Arquivo de atendimentos unificado gravado em: {OUTPUT_PATH} ({len(all_data)} registros)")
    except Exception as write_err:
        print(f"[ERRO CRÍTICO] Falha ao gravar 'atendimentos.csv': {write_err}")
        
    # 5. Ler e gravar arquivo de configurações config.csv
    try:
        tempo_rotacao = int(os.environ.get('TEMPO_ROTACAO', 10))
        quantidade_itens_tela = int(os.environ.get('QUANTIDADE_ITENS_TELA', 1))
        alerta_sonoro = os.environ.get('ALERTA_SONORO', 'true').lower() == 'true'
        
        with open(CONFIG_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['tempo_rotacao', 'quantidade_itens_tela', 'alerta_sonoro'])
            writer.writerow([tempo_rotacao, quantidade_itens_tela, str(alerta_sonoro).lower()])
        print(f"[SUCESSO] Arquivo de configurações gravado em: {CONFIG_PATH}")
    except Exception as config_err:
        print(f"[ERRO CRÍTICO] Falha ao gravar 'config.csv': {config_err}")
        
    print(f"--- Sincronização finalizada em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ---\n")

if __name__ == "__main__":
    # Verifica parâmetros de execução
    run_once = "--once" in sys.argv
    
    interval_sec = 300
    try:
        interval_sec = int(os.environ.get('INTERVALO_SINC_SEGUNDOS', 300))
    except Exception:
        pass
        
    if run_once or interval_sec <= 0:
        sync()
    else:
        print(f"Sincronizador ativo. Executando em loop a cada {interval_sec} segundos.")
        print("Pressione Ctrl+C para encerrar o processo.")
        try:
            while True:
                sync()
                time.sleep(interval_sec)
        except KeyboardInterrupt:
            print("\n[INFO] Sincronizador encerrado pelo usuário.")
