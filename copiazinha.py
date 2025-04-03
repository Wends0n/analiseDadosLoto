from array import array
import pandas as pd
import os
from itertools import combinations
from collections import defaultdict
import random
import numpy as np

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
        atrasos = {num: 0 for num in range(1, 61)}
        pares_juntos = defaultdict(int)

        for idx, sorteio in enumerate(sorteios):
            numeros_sorteados = df[df[df.columns[0]] == sorteio][colunas].values[0]
            
            for num in numeros_sorteados:
                contagem[num] += 1
                if ultimo_sorteio[num] is None:
                    ultimo_sorteio[num] = sorteio
                    if idx == 0:
                        atrasos[num] = 0
            
            for pair in combinations(sorted(numeros_sorteados), 2):
                pares_juntos[pair] += 1

        ultimo_sorteio_realizado = sorteios[0]
        for num in range(1, 61):
            if ultimo_sorteio[num] is not None and ultimo_sorteio[num] != ultimo_sorteio_realizado:
                posicao = list(sorteios).index(ultimo_sorteio[num])
                atrasos[num] = posicao

        top_pares = sorted(pares_juntos.items(), key=lambda x: x[1], reverse=True)[:200]

        print("\nBOLA;OCORRENCIAS;TAXA_OCORRENCIA;ULTIMO_SORTEIO;ATRASO")
        for num in range(1, 61):
            if contagem[num] != 0:
                taxa_ocorrencia = (contagem[num]/len(df))*100
                print(f"{num};{contagem[num]};{taxa_ocorrencia:.2f}%;{ultimo_sorteio[num]};{atrasos[num]}")
            else:
                print(f"{num};0;0.00%;Nunca sorteado;N/A")
        
        print("\nTOP 10 PARES QUE MAIS SAEM JUNTOS:")
        for pair, count in top_pares[:10]:
            num1, num2 = pair
            print(f"({num1}, {num2}): {count} vezes - Frequência: {(count/len(df))*100:.2f}%")
        
        # Função para gerar números recomendados com imprevisibilidade
        def gerar_numeros_recomendados():
            # Estratégia 1: Pegar os números mais frequentes
            top_frequentes = sorted(contagem.items(), key=lambda x: x[1], reverse=True)[:20]
            
            # Estratégia 2: Pegar os números com maior atraso
            top_atrasados = sorted(atrasos.items(), key=lambda x: x[1], reverse=True)[:20]
            
            # Estratégia 3: Pegar números que formam os pares mais frequentes
            numeros_pares = []
            for pair, _ in top_pares[:50]:
                numeros_pares.extend(pair)
            contagem_pares = {num: numeros_pares.count(num) for num in set(numeros_pares)}
            top_pares_numeros = sorted(contagem_pares.items(), key=lambda x: x[1], reverse=True)[:20]
            
            # Combinando as estratégias com pesos diferentes
            candidatos = defaultdict(float)
            
            # Adiciona imprevisibilidade nos pesos
            peso_frequencia = random.uniform(0.8, 1.2)
            peso_atraso = random.uniform(0.5, 0.9)
            peso_pares = random.uniform(1.0, 1.4)
            
            for num, freq in top_frequentes:
                candidatos[num] += freq * peso_frequencia
            
            for num, atraso_count in top_atrasados:
                candidatos[num] += atraso_count * peso_atraso
            
            for num, freq in top_pares_numeros:
                candidatos[num] += freq * peso_pares
            
            # Adiciona alguns números aleatórios com pequena probabilidade
            for num in random.sample(range(1, 61), 5):
                candidatos[num] += random.uniform(0.1, 0.5) * max(candidatos.values())
            
            # Ordena os candidatos por pontuação
            candidatos_ordenados = sorted(candidatos.items(), key=lambda x: x[1], reverse=True)
            
            # Seleciona os 20 melhores candidatos
            melhores_candidatos = [num for num, score in candidatos_ordenados[:20]]
            
            # Cria grupos de números por faixa (1-10, 11-20, etc.)
            grupos = [list(range(i, i+10)) for i in range(1, 51, 10)]
            
            # Garante que pelo menos 1 número de cada grupo esteja nos candidatos
            for grupo in grupos:
                if not set(grupo) & set(melhores_candidatos):
                    melhores_candidatos.append(random.choice(grupo))
            
            # Seleciona 6 números com uma distribuição que favorece os melhores mas permite surpresas
            selecionados = []
            for i in range(6):
                # Usa uma distribuição exponencial para selecionar os números
                prob = np.array([1/(i+1) for i in range(len(melhores_candidatos))])
                prob = prob / prob.sum()
                
                escolhido = np.random.choice(melhores_candidatos, p=prob)
                selecionados.append(escolhido)
                melhores_candidatos.remove(escolhido)
            
            return sorted(selecionados)
        
        # GERANDO OS 6 NÚMEROS RECOMENDADOS
        print("\n6 NÚMEROS RECOMENDADOS PARA O PRÓXIMO SORTEIO (COM IMPREVISIBILIDADE):")
        numeros_recomendados = gerar_numeros_recomendados()
        print(numeros_recomendados)
        
        # FUNÇÃO PARA TESTAR CONTRA UM SORTEIO ESPECÍFICO
        def testar_contra_sorteio(sorteio_especifico):
            try:
                numeros_sorteio = df[df[df.columns[0]] == sorteio_especifico][colunas].values[0]
                print(f"\nTestando contra o sorteio {sorteio_especifico}: {numeros_sorteio}")
                
                tentativas = 0
                acertos = 0
                melhor_resultado = 0
                
                while acertos < 4:
                    tentativas += 1
                    numeros_gerados = gerar_numeros_recomendados()
                    acertos = len(set(numeros_gerados) & set(numeros_sorteio))
                    
                    if acertos > melhor_resultado:
                        melhor_resultado = acertos
                        print(f"Novo recorde: {acertos} acertos na tentativa {tentativas}")
                    
                    if tentativas % 1000 == 0:
                        print(f"Tentativa {tentativas}: Melhor até agora - {melhor_resultado} acertos")
                
                print(f"\nACERTOU {acertos} NÚMEROS APÓS {tentativas} TENTATIVAS!")
                print(f"Números sorteados: {sorted(numeros_sorteio)}")
                print(f"Números gerados:   {numeros_gerados}")
                print(f"Acertos: {sorted(set(numeros_gerados) & set(numeros_sorteio))}")
                
            except Exception as e:
                print(f"Erro ao testar sorteio {sorteio_especifico}: {e}")
        
        # Opção para testar contra um sorteio específico
        if input("\nDeseja testar contra um sorteio específico? (s/n): ").lower() == 's':
            sorteio_teste = input("Digite o número do concurso para testar: ")
            testar_contra_sorteio(int(sorteio_teste))
                
        return {
            'contagem': contagem,
            'ultimo_sorteio': ultimo_sorteio,
            'atrasos': atrasos,
            'sorteios_analisados': len(df),
            'pares_juntos': dict(top_pares),
            'numeros_recomendados': numeros_recomendados
        }

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {os.path.abspath(caminho)}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

if __name__ == "__main__":
    resultado = analisar_mega_sena()