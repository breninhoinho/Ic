from Algoritmos_Mapeamento.Random import *
from Algoritmos_Mapeamento.Genetic_Algorithm import *
from Algoritmos_Mapeamento.Andean_condor import *
from Algoritmos_Mapeamento.Random import *
from Algoritmos_Mapeamento.SimulatedAnneling import *
from Algoritmos_Mapeamento.Cluster_Based import *
from Algoritmos_Mapeamento.PSO import *
import numpy as np


tamanho =6

matriz = [
    [0.0, 3.0, 712.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 6.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 712.0, 30.0, 15.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 712.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 30.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 20.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 15.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 712.0, 712.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1424.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 45.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 45.0, 0.0, 1424.0, 4.0, 4.0, 8.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
]


def calcular_energia(mapeamento,matriz):
        n =  16 # Número de tarefas
        m = 6  # Dimensão da NoC
        valor_final = 0

        for i in range(n):  # Percorre todas as tarefas
            for j in range(n):  # Garante que a matriz seja percorrida uma única vez (i, j) != (j, i)
                bandwidth = matriz[i][j]
                if bandwidth > 0 :  # Se há comunicação entre as tarefas i e j
                    # Encontra a posição de i no mapeamento
                    ix, iy = [(k, l) for k in range(m) for l in range(m) if mapeamento[k][l] == i][0]
                    jx, jy = [(k, l) for k in range(m) for l in range(m) if mapeamento[k][l] == j][0]
                    # Calcula a distância Manhattan
                    man_dist = abs(ix - jx) + abs(iy - jy)
                    # Acumula o valor da energia total
                    valor_final += bandwidth * man_dist


        return valor_final



# Inicializar as variáveis de soma e listas para armazenar os resultados
soma_gen = 0
soma_andean = 0
soma_ramd = 0
soma_simu = 0
soma_cluster = 0
soma_PSO = 0

resultados_gen = []
resultados_andean = []
resultados_ramd = []
resultados_simu = []
resultados_cluster = []
resultados_PSO = []


# Loop para as 30 iterações
for i in range(30):
    # Executar os algoritmos
    cores_noc = Run_Genetic_Algorithm(100, 100, 0.5, matriz, tamanho)

    cores_noc2 = Run_Andean_condor(matriz, tamanho)

    cores_noc3 = Run_Random(matriz, tamanho)

    cores_noc4 = RunSimulateAnneling(matriz, tamanho,1000, 0.95, 100)

    cores_noc5 =  [['' for _ in range(tamanho)] for _ in range(tamanho)]
    cores_noc5 = Run_Cluster_based(cores_noc5, matriz)

    cores_noc6 = Run_pso(matriz,tamanho)

    
    
    
    # Calcular energia e armazenar resultados para os outros algoritmos
    energia_gen = calcular_energia(cores_noc, matriz)
    energia_andean = calcular_energia(cores_noc2, matriz)
    energia_ramd = calcular_energia(cores_noc3, matriz)
    energia_simu = calcular_energia(cores_noc4, matriz)
    energia_cluster = calcular_energia(cores_noc5, matriz)
    energia_PSO = calcular_energia(cores_noc6, matriz)

    soma_gen += energia_gen
    soma_andean += energia_andean
    soma_ramd += energia_ramd
    soma_simu+= energia_simu
    soma_cluster += energia_cluster
    soma_PSO += energia_PSO

    #print(energia_andean,energia_cluster,energia_gen,energia_simu, energia_ramd)


    resultados_gen.append(energia_gen)
    resultados_andean.append(energia_andean)
    resultados_ramd.append(energia_ramd)
    resultados_simu.append(energia_simu)
    resultados_cluster.append(energia_cluster)
    resultados_PSO.append(energia_PSO)


# Calcular a média e o desvio padrão para os outros algoritmos
estatisticas_outros = {
    'Genetic Algorithm': {
        'Média': np.mean(resultados_gen),
        'Desvio Padrão': np.std(resultados_gen)
    },
    'Andean Condor': {
        'Média': np.mean(resultados_andean),
        'Desvio Padrão': np.std(resultados_andean)
    },
    'Random': {
        'Média': np.mean(resultados_ramd),
        'Desvio Padrão': np.std(resultados_ramd)
    },
    'Simulated Anneling': {
        'Média': np.mean(resultados_simu),
        'Desvio Padrão': np.std(resultados_simu)
    },
    'Cluster Based': {
        'Média': np.mean(resultados_cluster),
        'Desvio Padrão': np.std(resultados_cluster)
    },
    'PSO': {
        'Média': np.mean(resultados_PSO),
        'Desvio Padrão': np.std(resultados_PSO)
    },
}

print("Estatísticas dos algoritmos:")
for chave, stats in estatisticas_outros.items():
    print(f"Algoritmo: {chave}")
    print(f"  Média: {stats['Média']:.3f}")
    print(f"  Desvio Padrão: {stats['Desvio Padrão']:.3f}")
    print()

