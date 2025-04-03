from array import array
import pandas as pd
import os
from itertools import combinations
from collections import defaultdict

caminho = 'dataBase/Mega-Sena.csv'

def analisar_mega_sena(quantidade_sorteios=None):
    try:
        df = pd.read_csv(
            caminho,
            sep=';',  
            encoding='utf-8'
        )
        print("Arquivo lido com sucesso!")
        
        df = df.sort_values(by=df.columns[0], ascending=False)
        
        if quantidade_sorteios is not None and quantidade_sorteios > 0:
            df = df.head(quantidade_sorteios)
            print(f"\nAnalisando os últimos {quantidade_sorteios} sorteios...")
        else:
            print("\nAnalisando todos os sorteios disponíveis...")
        
        sorteios = df[df.columns[0]].values
        colunas = df.columns[2:8]

        # Inicialização correta para números de 1 a 60
        contagem = {num: 0 for num in range(1, 61)}
        ultimo_sorteio = {num: None for num in range(1, 61)}
        atraso = {num: 0 for num in range(1, 61)}
        pares_juntos = defaultdict(int)

        for idx, sorteio in enumerate(sorteios):
            numeros_sorteados = df[df[df.columns[0]] == sorteio][colunas].values[0]
            
            for num in numeros_sorteados:
                contagem[num] += 1
                if ultimo_sorteio[num] is None:
                    ultimo_sorteio[num] = sorteio
                    if idx == 0:
                        atraso[num] = 0
            
            for pair in combinations(sorted(numeros_sorteados), 2):
                pares_juntos[pair] += 1

        ultimo_sorteio_realizado = sorteios[0]
        for num in range(1, 61):
            if ultimo_sorteio[num] is not None and ultimo_sorteio[num] != ultimo_sorteio_realizado:
                posicao = list(sorteios).index(ultimo_sorteio[num])
                atraso[num] = posicao

        top_pares = sorted(pares_juntos.items(), key=lambda x: x[1], reverse=True)[:200]

        print("\nBOLA;OCORRENCIAS;TAXA_OCORRENCIA;ULTIMO_SORTEIO;ATRASO")
        for num in range(1, 61):
            if contagem[num] != 0:
                taxa_ocorrencia = (contagem[num]/len(df))*100
                print(f"{num};{contagem[num]};{taxa_ocorrencia:.2f}%;{ultimo_sorteio[num]};{atraso[num]}")
            else:
                print(f"{num};0;0.00%;Nunca sorteado;N/A")
        
        print("\nTOP 10 PARES QUE MAIS SAEM JUNTOS:")
        for pair, count in top_pares:
            num1, num2 = pair
            print(f"({num1}, {num2}): {count} vezes - Frequência: {(count/len(df))*100:.2f}%")
                
        return {
            'contagem': contagem,
            'ultimo_sorteio': ultimo_sorteio,
            'atraso': atraso,
            'sorteios_analisados': len(df),
            'pares_juntos': dict(top_pares)
        }

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {os.path.abspath(caminho)}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

if __name__ == "__main__":
    resultado = analisar_mega_sena()