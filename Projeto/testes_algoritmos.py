from Algoritmos_Mapeamento.Random import *
from Algoritmos_Mapeamento.Genetic_Algorithm import *
from Algoritmos_Mapeamento.Andean_condor import *
from Algoritmos_Mapeamento.Random import *
from Algoritmos_Mapeamento.SimulatedAnneling import *
from Algoritmos_Mapeamento.Cluster_Based import *
from Algoritmos_Mapeamento.PSO import *
import numpy as np

tamanho = 4

# MATRIZ ORIGINAL
matriz_cavalc = [
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

matriz_mwd = [
[  0,128, 64,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 0
[  0,  0,  0, 96,  0,  0,  0,  0,  0,  0,  0,  0],  # 1
[  0,  0,  0,  0,  0,  0,  0,  0, 64, 96,  0,  0],  # 2
[  0,  0,  0,  0, 96,  0,  0,  0,  0,  0,  0,  0],  # 3
[  0,  0,  0,  0,  0, 96,  0,  0,  0,  0,  0,  0],  # 4
[  0,  0,  0,  0,  0,  0, 64,  0,  0,  0,  0,  0],  # 5
[  0,  0,  0,  0,  0,  0,  0, 64,  0,  0,  0,  0],  # 6
[  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 7
[  0,  0,  64, 0,  0,  0,  0,  0,  0,  0,  0,  0],  # 8
[  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 96,  0],  # 9
[  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 96],  # 10
[  0,  0,  0,  0,  0, 96,  0,  0,  0,  0,  0,  0],  # 11
]

matriz_mpeg4 = [
[  0, 64,  3,  1, 20,  0,200,304,  0, 11,  0,  0],  # 0
[ 64,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 1
[  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 2
[  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 3
[ 20,  0,  0,  0,  0, 14,  0,  0,  0,  0,  0,  0],  # 4
[  0,  0,  0,  0, 14,  0, 40,  0,  0,  0,  0,  0],  # 5
[200,  0,  0,  0,  0, 40,  0,  0,  0,  0,  0,  0],  # 6
[304,  0,  0,  0,  0,  0,  0,  0,224,  0,  0,  0],  # 7
[  0,  0,  0,  0,  0,  0,  0,224,  0, 58, 84,167],  # 8
[ 11,  0,  0,  0,  0,  0,  0,  0, 58,  0,  0,  0],  # 9
[  0,  0,  0,  0,  0,  0,  0,  0, 84,  0,  0,  0],  # 10
[  0,  0,  0,  0,  0,  0,  0,  0,167,  0,  0,  0],  # 11
]

matriz_mms = [
[0,38106,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #0
[0,0,33848,0,0,0,197,106873,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
[0,0,0,33848,0,0,16591,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #2
[0,0,0,0,33848,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #3
[0,0,0,0,0,764,0,0,0,0,0,0,0,640,0,0,0,0,0,0,0,0,0,0,0], #4
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1404], #5
[0,0,0,0,0,0,0,75205,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #6
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #7
[0,0,0,0,0,0,0,0,0,7061,7061,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #8
[0,0,0,0,0,0,0,0,0,0,20348,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #9
[0,0,0,0,0,0,0,0,0,0,0,20348,0,0,0,0,0,0,0,0,0,0,0,0,0], #10
[0,0,0,0,0,0,0,0,0,0,0,0,80,640,0,0,0,0,0,0,0,0,0,0,0], #11
[0,0,0,0,0,0,0,0,0,0,0,25,0,0,0,0,0,0,0,0,0,0,0,0,0], #12
[0,0,0,0,640,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #13
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,740,0,0,0,0,641,0,0,0,0], #14
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3672,0,2672,0,0,0,0,0,0], #15
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3672,0,0,0,0,0,0,0], #16
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3672,0,0,0,0,0,0], #17
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,38016,0,0,0,0,38016], #18
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,75584,0,0,0,0,0,0], #19
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,641,0,0,0,0,0,0,80,28265,0,0], #20
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,25,0,0,0,0,0], #21
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7065,0], #22
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7065,0,0], #23
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #24
]

matriz_vopd = [
[0,70,0,0,0,0,0,0,0,0,0,0,0,0,0,0],      #0
[0,0,362,0,0,0,0,0,0,0,0,0,0,0,0,0],     #1
[0,0,0,362,0,0,0,0,0,0,0,0,0,0,0,0],     #2
[0,0,0,0,362,0,0,0,0,0,0,0,0,0,0,49],    #3
[0,0,0,0,0,357,0,0,0,0,0,0,0,0,0,0],     #4
[0,0,0,0,0,0,353,0,0,0,0,0,0,0,0,0],     #5
[0,0,0,0,0,0,0,300,0,0,0,0,0,0,0,0],     #6
[0,0,0,0,0,0,0,0,313,0,0,0,0,0,0,0],     #7
[0,0,0,0,0,0,0,313,0,94,0,0,0,0,0,0],    #8
[0,0,0,0,0,0,0,500,0,0,0,0,0,0,0,0],     #9
[0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0],      #10
[0,0,0,0,0,0,0,16,0,0,0,0,16,0,0,0],     #11
[0,0,0,0,0,0,0,0,0,0,0,0,0,157,16,0],    #12
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,0],      #13
[0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0],      #14
[0,0,0,27,0,0,0,0,0,0,0,0,0,0,0,0],      #15
]

matrizes = {
    "Cavalcanti ": matriz_cavalc,
    "MWD ": matriz_mwd,
    "MPEG4 ": matriz_mpeg4,
    "MMS ": matriz_mms,
    "VOPD ": matriz_vopd
}

   #    
# ==========================================================
# FUNÇÃO GERAL PARA CALCULAR A ENERGIA
# ==========================================================
def calcular_energia(mapeamento, matriz):
    n = len(matriz)              # número de tarefas (automático!)
    m = 16                    # tamanho da NoC (ex: 6x6)

    valor_final = 0

    # cria lista [(tarefa -> (x,y))]
    posicoes = {}
    for x in range(m):
        for y in range(m):
            posicoes[mapeamento[x][y]] = (x, y)

    # percorre todas as comunicações
    for i in range(n):
        for j in range(n):
            bw = matriz[i][j]
            if bw > 0:
                ix, iy = posicoes[i]
                jx, jy = posicoes[j]
                distancia = abs(ix - jx) + abs(iy - jy)
                valor_final += bw * distancia

    return valor_final


# ==========================================================
# EXECUÇÃO DOS EXPERIMENTOS
# ==========================================================
def rodar_experimentos():

    with open("resultados_mapeamentos16x16.txt", "w") as arquivo:

        for nome_matriz, matriz in matrizes.items():

            tamanho_noc = 16
            
            arquivo.write("\n====================================\n")
            arquivo.write(f"     RESULTADOS – {nome_matriz} \n")
            arquivo.write("====================================\n\n")

            # Vetores com todas as energias
            resultados = {
                "Genetic": [],
                "Andean": [],
                "Random": [],
                "SimulatedA": [],
                "Cluster": []
            }

            # Guardar melhor map de cada algoritmo
            melhores_mapas = {
                "Genetic": {"energia": float("inf"), "mapa": None},
                "Andean":  {"energia": float("inf"), "mapa": None},
                "Random":  {"energia": float("inf"), "mapa": None},
                "SimulatedA": {"energia": float("inf"), "mapa": None},
                "Cluster": {"energia": float("inf"), "mapa": None},
            }

            for execu in range(30):

                sol_gen = Run_Genetic_Algorithm(10000, 100, 0.5, matriz, tamanho_noc)
                sol_and = Run_Andean_condor(matriz, tamanho_noc)
                sol_rand = Run_Random(matriz, tamanho_noc)
                sol_simu = RunSimulateAnneling(matriz, tamanho_noc, 1000, 0.95, 100)

                temp_map = [['' for _ in range(tamanho_noc)] for _ in range(tamanho_noc)]
                sol_cluster = Run_Cluster_based(temp_map, matriz)

                mapas_exec = {
                    "Genetic": sol_gen,
                    "Andean": sol_and,
                    "Random": sol_rand,
                    "SimulatedA": sol_simu,
                    "Cluster": sol_cluster
                }

                # Calcular energia
                for alg, mapa in mapas_exec.items():
                    energia = calcular_energia(mapa, matriz)
                    resultados[alg].append(energia)

                    # Salvar o melhor mapa
                    if energia < melhores_mapas[alg]["energia"]:
                        melhores_mapas[alg]["energia"] = energia
                        melhores_mapas[alg]["mapa"] = [linha.copy() for linha in mapa]

            # --- SALVAR RESULTADOS NO ARQUIVO ---
            for alg, valores in resultados.items():

                arquivo.write(f"{alg}:\n")
                arquivo.write(f"  Média = {np.mean(valores):.3f}\n")
                arquivo.write(f"  Desvio = {np.std(valores):.3f}\n")
                arquivo.write(f"  Resultados = {valores}\n")

                # Melhor energia + melhor mapa
                arquivo.write(f"  Melhor Energia = {melhores_mapas[alg]['energia']}\n")
                arquivo.write("  Melhor Mapeamento:\n")

                melhor_mapa = melhores_mapas[alg]["mapa"]
                for linha in melhor_mapa:
                    arquivo.write("    " + str(linha) + "\n")

                arquivo.write("\n")

    print("\nArquivo 'resultados_mapeamentos.txt' gerado com sucesso!\n")

# ==========================================================
# RODAR
# ==========================================================
rodar_experimentos()