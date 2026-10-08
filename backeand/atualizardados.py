# Importa a biblioteca para trabalhar com tempo (usada para o intervalo de 5 minutos)
import time 
# Importa ferramentas para fazer requisições na internet (acessar os links)
from urllib.request import urlopen, Request
# Importa o Path para lidar com caminhos de pastas e arquivos de forma mais segura.
from pathlib import Path
# Importa o Pandas, uma biblioteca poderosa para manipular e juntar tabelas de dados
import pandas as pd

# Descobre o caminho absoluto da pasta onde este script (o arquivo .py) está salvo
BASE_DIR = Path(__file__).resolve().parent

# Define onde os arquivos CSV individuais baixados serão guardados
PASTA_DOWNLOAD = BASE_DIR / "planilhas_setores"

# Define o nome e o local do arquivo final (a planilha que junta tudo)
ARQUIVO_MERGE = BASE_DIR / "agenda_unificada.xlsx"

URLS_SETOR = [
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQtsxHNzeKQ8Jsk3HnUNFR-NzrplWHJdz4fMr4IRH5gHoOVuD9Msq2dtHIKz3EE0QkiXo5Xo2sJnoyf/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vSa1C-gR98OD-Xq6-QHb_FgZ5M4xXhVvoJfrPJogESKPifXUIVlD9xde-BXcJjL0yh4dxR7BzqI3v7X/pub?output=csv"
]

def internet_disponivel() -> bool:
    """Função para verificar se o computador está conectado à internet."""
    try:
        # Tenta acessar o site do Google com um limite de tempo (timeout) de 5 segundos
        req = Request("https://www.google.com", headers={"User-Agent": "Mozilla/5.0"})
        urlopen(req, timeout=5)
        # Se não der erro, significa que há internet. Retorna Verdadeiro.
        return True
    except Exception:
        # Se der qualquer erro (cair a rede, site fora do ar), retorna Falso.
        return False

def atualizar_arquivos() -> None:
    """Função principal que gerencia o download e a união das planilhas."""
    
    # 1. VERIFICAÇÃO DE INTERNET
    if not internet_disponivel():
        # Se a função retornar False, avisa no terminal e encerra a execução desta rodada.
        # Ao encerrar com 'return', os arquivos antigos continuam intactos na pasta.
        print(f"[{time.strftime('%H:%M:%S')}] Sem internet. Mantendo os arquivos anteriores e aguardando 5 minutos...")
        return

    # Se passou da verificação acima, é porque tem internet.
    print(f"[{time.strftime('%H:%M:%S')}] Internet disponível. Iniciando o processo de atualização...")
    
    # Cria a pasta 'planilhas_setores' se ela ainda não existir
    PASTA_DOWNLOAD.mkdir(parents=True, exist_ok=True)

    # Lista vazia que vai guardar os dados (DataFrames) de cada CSV que for lido
    dfs = []
    
    # 2. DOWNLOAD DOS ARQUIVOS
    # Passa por cada link na lista URLS_SETOR. O 'enumerate' ajuda a numerar os arquivos (1, 2, 3...)
    for index, url in enumerate(URLS_SETOR, start=1):
        # Define o nome do arquivo que será salvo (ex: setor_1.csv, setor_2.csv)
        destino = PASTA_DOWNLOAD / f"setor_{index}.csv"
        
        try:
            # Prepara a requisição fingindo ser um navegador (Mozilla) para o Google não bloquear
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            
            # Abre o link e lê o conteúdo dele
            with urlopen(req, timeout=20) as response:
                conteudo = response.read()
                
            # Abre o arquivo local no modo 'wb' (write binary) e salva o que baixou
            with open(destino, "wb") as arquivo:
                arquivo.write(conteudo)
            
            # Pega o arquivo que acabou de ser salvo e lê usando o Pandas
            tabela = pd.read_csv(destino)
            # Adiciona essa tabela na nossa lista 'dfs'
            dfs.append(tabela)
            
            print(f" - Arquivo baixado e processado: {destino.name}")
            
        except Exception as exc:
            # Se algum link falhar (link quebrado, erro de permissão), avisa o erro mas continua tentando os próximos
            print(f" - Erro ao baixar ou processar {url}: {exc}")

    # 3. UNIÃO E SALVAMENTO DOS ARQUIVOS
    # Verifica se a lista 'dfs' tem algum dado (ou seja, se conseguiu baixar e ler pelo menos uma planilha)
    if dfs:
        try:
            # Junta (concatena) todas as tabelas da lista em uma só
            # ignore_index=True refaz a numeração das linhas. sort=False evita que o Pandas misture a ordem das colunas
            agenda_unificada = pd.concat(dfs, ignore_index=True, sort=False)
            
            # Salva a tabela final como um arquivo de Excel no caminho definido lá em cima
            agenda_unificada.to_excel(ARQUIVO_MERGE, index=False)
            
            print(f"[{time.strftime('%H:%M:%S')}] Sucesso! Agenda unificada salva em: {ARQUIVO_MERGE}\n")
        except Exception as exc:
            print(f"[{time.strftime('%H:%M:%S')}] Erro ao salvar a agenda unificada: {exc}\n")
    else:
        # Se a lista 'dfs' estiver vazia (a internet caiu no meio do processo ou todos os links deram erro)
        print(f"[{time.strftime('%H:%M:%S')}] Falha ao baixar todos os arquivos. Os arquivos anteriores foram mantidos.\n")


# 4. LOOP INFINITO DE EXECUÇÃO
# Verifica se o script está sendo executado diretamente (e não importado por outro programa)
if __name__ == "__main__":
    # Laço de repetição infinito (roda para sempre enquanto o programa estiver aberto)
    while True:
        # Chama a função principal
        atualizar_arquivos()
        
        # Pausa a execução do programa por 300 segundos (5 minutos) antes de repetir o ciclo
        time.sleep(300)