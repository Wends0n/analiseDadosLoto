import pandas as pd
import os

# Caminhos dos arquivos
diretorio_base = 'dataBase'
arquivo_xlsx = os.path.join(diretorio_base, 'Lotofácil.xlsx')  # Caminho completo para o XLSX
arquivo_csv = os.path.join(diretorio_base, 'Lotofácil.csv')    # Caminho completo para o CSV

# Verificar se o arquivo XLSX existe
if not os.path.exists(arquivo_xlsx):
    print(f"Erro: O arquivo {arquivo_xlsx} não foi encontrado!")
else:
    # Ler o arquivo XLSX
    dados = pd.read_excel(arquivo_xlsx)
    
    # Salvar como CSV
    dados.to_csv(arquivo_csv, sep=';',index=False, encoding='utf-8')
    
    print(f'Arquivo {arquivo_xlsx} convertido para {arquivo_csv} com sucesso!')