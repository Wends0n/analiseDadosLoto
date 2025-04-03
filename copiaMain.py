from array import array
import pandas as pd
import os
from itertools import combinations
from collections import defaultdict
import random

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
        for pair, count in top_pares[:10]:
            num1, num2 = pair
            print(f"({num1}, {num2}): {count} vezes - Frequência: {(count/len(df))*100:.2f}%")
        
        # GERANDO OS 6 NÚMEROS RECOMENDADOS
        print("\nGERANDO NÚMEROS RECOMENDADOS...")
        
        # Estratégia 1: Pegar os números mais frequentes
        top_frequentes = sorted(contagem.items(), key=lambda x: x[1], reverse=True)[:15]
        
        # Estratégia 2: Pegar os números com maior atraso
        top_atrasados = sorted(atraso.items(), key=lambda x: x[1], reverse=True)[:15]
        
        # Estratégia 3: Pegar números que formam os pares mais frequentes
        numeros_pares = []
        for pair, _ in top_pares[:50]:
            numeros_pares.extend(pair)
        contagem_pares = {num: numeros_pares.count(num) for num in set(numeros_pares)}
        top_pares_numeros = sorted(contagem_pares.items(), key=lambda x: x[1], reverse=True)[:15]
        
        # Combinando as estratégias com pesos diferentes
        candidatos = defaultdict(int)
        
        for num, freq in top_frequentes:
            candidatos[num] += freq * 1.0  # Peso para frequência
        
        for num, atraso in top_atrasados:
            candidatos[num] += atraso * 0.7  # Peso para atraso (quanto maior o atraso, mais pontos)
        
        for num, freq in top_pares_numeros:
            candidatos[num] += freq * 1.2  # Peso maior para números que aparecem em pares frequentes
        
        # Ordena os candidatos por pontuação
        candidatos_ordenados = sorted(candidatos.items(), key=lambda x: x[1], reverse=True)
        
        # Seleciona os 15 melhores candidatos
        melhores_candidatos = [num for num, score in candidatos_ordenados[:15]]
        
        # Seleciona aleatoriamente 6 números entre os melhores candidatos
        numeros_recomendados = random.sample(melhores_candidatos, 6)
        
        print("\n6 NÚMEROS RECOMENDADOS PARA O PRÓXIMO SORTEIO:")
        print(sorted(numeros_recomendados))
                
        return {
            'contagem': contagem,
            'ultimo_sorteio': ultimo_sorteio,
            'atraso': atraso,
            'sorteios_analisados': len(df),
            'pares_juntos': dict(top_pares),
            'numeros_recomendados': sorted(numeros_recomendados)
        }

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {os.path.abspath(caminho)}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

if __name__ == "__main__":
    resultado = analisar_mega_sena()