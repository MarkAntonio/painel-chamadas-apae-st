import os
import sys
import unittest
import csv
import shutil
from unittest.mock import patch, MagicMock

# Adiciona o diretório atual ao path para importação do main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import main

class TestSyncService(unittest.TestCase):
    
    def setUp(self):
        # Cria cópias dos caminhos originais para restaurar após os testes
        self.original_output_path = main.OUTPUT_PATH
        self.original_config_path = main.CONFIG_PATH
        self.original_cache_dir = main.CACHE_DIR
        self.original_frontend_public_dir = main.FRONTEND_PUBLIC_DIR
        
        # Configura caminhos temporários de teste
        self.test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_temp')
        os.makedirs(self.test_dir, exist_ok=True)
        
        main.FRONTEND_PUBLIC_DIR = os.path.join(self.test_dir, 'public')
        main.OUTPUT_PATH = os.path.join(main.FRONTEND_PUBLIC_DIR, 'atendimentos.csv')
        main.CONFIG_PATH = os.path.join(main.FRONTEND_PUBLIC_DIR, 'config.csv')
        main.CACHE_DIR = os.path.join(self.test_dir, '.cache')
        os.makedirs(main.CACHE_DIR, exist_ok=True)

    def tearDown(self):
        # Restaura caminhos originais
        main.OUTPUT_PATH = self.original_output_path
        main.CONFIG_PATH = self.original_config_path
        main.CACHE_DIR = self.original_cache_dir
        main.FRONTEND_PUBLIC_DIR = self.original_frontend_public_dir
        
        # Remove diretório temporário de testes
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_is_placeholder(self):
        self.assertTrue(main.is_placeholder(""))
        self.assertTrue(main.is_placeholder("https://docs.google.com/spreadsheets/d/e/SUA_CHAVE_AQUI/pub?output=csv"))
        self.assertTrue(main.is_placeholder("https://some-other-url.com"))
        self.assertFalse(main.is_placeholder("https://docs.google.com/spreadsheets/d/e/12345abcde/pub?output=csv"))

    def test_download_sheet_placeholder(self):
        # Deve retornar dados mockados para URLs placeholder
        data = main.download_sheet('pedagogico', "")
        self.assertEqual(data, main.MOCK_PEDAGOGICO)
        
        # O arquivo de cache deve ser criado
        cache_file = os.path.join(main.CACHE_DIR, "pedagogico_cache.csv")
        self.assertTrue(os.path.exists(cache_file))

    @patch('requests.get')
    def test_download_sheet_success(self, mock_get):
        # Configura o mock do requests para retornar um CSV válido
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"header1,header2,header3,header4,header5,header6\nval1,val2,val3,val4,val5,val6"
        mock_get.return_value = mock_response
        
        url = "https://docs.google.com/spreadsheets/d/e/12345/pub?output=csv"
        data = main.download_sheet('pedagogico', url)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], ["val1", "val2", "val3", "val4", "val5", "val6"])
        
        # O arquivo de cache correspondente deve existir
        cache_file = os.path.join(main.CACHE_DIR, "pedagogico_cache.csv")
        self.assertTrue(os.path.exists(cache_file))

    @patch('requests.get')
    def test_download_sheet_failure_with_cache(self, mock_get):
        # Simula falha na requisição
        mock_get.side_effect = Exception("Erro de rede")
        
        # Cria um arquivo de cache manualmente de antemão
        cache_file = os.path.join(main.CACHE_DIR, "saude_cache.csv")
        with open(cache_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['data', 'hora', 'sala', 'profissional', 'tipo', 'atendido'])
            writer.writerow(['03/08/2026', '14:00', 'C1', 'Dr. Teste', 'Consulta', 'Paciente Cached'])
            
        url = "https://docs.google.com/spreadsheets/d/e/12345/pub?output=csv"
        data = main.download_sheet('saude', url)
        
        # Deve carregar os dados salvos em cache
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][5], 'Paciente Cached')

    @patch('requests.get')
    def test_download_sheet_failure_no_cache_uses_mock(self, mock_get):
        # Simula falha na requisição sem cache disponível
        mock_get.side_effect = Exception("Erro de rede")
        
        url = "https://docs.google.com/spreadsheets/d/e/12345/pub?output=csv"
        data = main.download_sheet('saude', url)
        
        # Deve usar dados mockados como última barreira
        self.assertEqual(data, main.MOCK_SAUDE)

    @patch('requests.get')
    def test_sync_creates_files(self, mock_get):
        # Garante que as planilhas usem dados mockados
        # por padrão URLs são placeholders no teste se não mockados
        main.sync()
        
        # Verifica se atendimentos.csv foi criado
        self.assertTrue(os.path.exists(main.OUTPUT_PATH))
        # Verifica se config.csv foi criado
        self.assertTrue(os.path.exists(main.CONFIG_PATH))
        
        # Lê o config.csv gerado e valida valores padrão
        with open(main.CONFIG_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            values = next(reader)
            self.assertEqual(headers, ['tempo_rotacao', 'quantidade_itens_tela', 'alerta_sonoro'])
            self.assertEqual(values, ['10', '1', 'true'])

if __name__ == '__main__':
    unittest.main()
