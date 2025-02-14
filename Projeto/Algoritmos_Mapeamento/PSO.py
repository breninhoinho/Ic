import random
import numpy as np
import matplotlib.pyplot as plt
import copy

def calcular_energia(mapeamento, matriz):
    n = len(matriz)
    m = len(mapeamento)
    valor_final = 0

    for i in range(n):
        for j in range(n):
            bandwidth = matriz[i][j]
            if bandwidth > 0:
                ix, iy = np.argwhere(np.array(mapeamento) == i)[0]
                jx, jy = np.argwhere(np.array(mapeamento) == j)[0]
                man_dist = abs(ix - jx) + abs(iy - jy)
                valor_final += bandwidth * man_dist

    return valor_final

def inicializar_particula(n, tamanho_noc):
    mapeamento = [[-1 for _ in range(tamanho_noc)] for _ in range(tamanho_noc)]
    posicoes = [(i, j) for i in range(tamanho_noc) for j in range(tamanho_noc)]
    random.shuffle(posicoes)
    tarefas = list(range(n))
    random.shuffle(tarefas)
    for idx, (i, j) in enumerate(posicoes[:n]):
        mapeamento[i][j] = tarefas[idx]
    return mapeamento

def atualizar_velocidade(posicao, velocidade, pbest, gbest, w, c1, c2):
    novas_permutacoes = []
    tamanho_noc = len(posicao)
    velocidade_atualizada = [troca for troca in velocidade if random.random() < w]

    if random.random() < c1:
        for i in range(tamanho_noc):
            for j in range(tamanho_noc):
                if posicao[i][j] != pbest[i][j]:
                    indices_pbest = np.argwhere(np.array(pbest) == posicao[i][j])
                    if len(indices_pbest) > 0:
                        i_pbest, j_pbest = indices_pbest[0]
                        novas_permutacoes.append(((i, j), (i_pbest, j_pbest)))

    if random.random() < c2:
        for i in range(tamanho_noc):
            for j in range(tamanho_noc):
                if posicao[i][j] != gbest[i][j]:
                    indices_gbest = np.argwhere(np.array(gbest) == posicao[i][j])
                    if len(indices_gbest) > 0:
                        i_gbest, j_gbest = indices_gbest[0]
                        novas_permutacoes.append(((i, j), (i_gbest, j_gbest)))

    velocidade_atualizada += novas_permutacoes
    return velocidade_atualizada

def atualizar_posicao(posicao, velocidade):
    nova_posicao = copy.deepcopy(posicao)
    for troca in velocidade:
        (i1, j1), (i2, j2) = troca
        nova_posicao[i1][j1], nova_posicao[i2][j2] = nova_posicao[i2][j2], nova_posicao[i1][j1]
    return nova_posicao

def Run_pso(matriz_adjacencia, tamanho_noc, num_particulas=1000, max_iter=1000, w=0.8, c1=1.6, c2=1.8):
    n = len(matriz_adjacencia)
    particulas = [inicializar_particula(n, tamanho_noc) for _ in range(num_particulas)]
    velocidades = [[] for _ in range(num_particulas)]
    pbest = [copy.deepcopy(p) for p in particulas]
    pbest_valores = [calcular_energia(p, matriz_adjacencia) for p in particulas]
    gbest = copy.deepcopy(particulas[np.argmin(pbest_valores)])
    gbest_valor = min(pbest_valores)
    fitness_values = []
    
    for _ in range(max_iter):
        print(gbest_valor)
        for i in range(num_particulas):
            velocidades[i] = atualizar_velocidade(particulas[i], velocidades[i], pbest[i], gbest, w, c1, c2)
            particulas[i] = atualizar_posicao(particulas[i], velocidades[i])
            fitness = calcular_energia(particulas[i], matriz_adjacencia)

            if fitness < pbest_valores[i]:
                pbest[i] = copy.deepcopy(particulas[i])
                pbest_valores[i] = fitness

            if fitness < gbest_valor:
                gbest = copy.deepcopy(particulas[i])
                gbest_valor = fitness
                print("Melhor valor encontrado:", gbest_valor)
                fitness_values.append(gbest_valor)

    for i in range(tamanho_noc):
        for j in range(tamanho_noc):
            if gbest[i][j] == -1:
                gbest[i][j] = ''
                
    plt.plot(fitness_values)
    plt.xlabel("Iteração")
    plt.ylabel("Melhor Fitness (Custo)")
    plt.title("Evolução do Fitness ao Longo das Iterações")
    plt.show()
    return gbest, gbest_valor

# Exemplo de uso
tam = 4
adj_matriz = [
  [0, 8, 5, 7, 6, 4, 8, 3, 9, 2, 1, 8, 9, 6, 7, 10],
  [9, 0, 3, 2, 5, 7, 6, 10, 1, 9, 4, 5, 8, 9, 1, 2],
  [7, 2, 0, 9, 2, 10, 4, 5, 6, 8, 7, 3, 9, 7, 6, 5],
  [4, 8, 6, 0, 3, 1, 5, 7, 2, 6, 10, 4, 7, 10, 9, 8],
  [10, 5, 8, 1, 0, 9, 7, 6, 3, 1, 5, 2, 8, 4, 6, 10],
  [2, 7, 1, 9, 6, 0, 8, 5, 10, 3, 7, 6, 4, 1, 9, 7],
  [8, 6, 10, 5, 2, 9, 0, 1, 7, 4, 6, 10, 9, 5, 7, 1],
  [5, 10, 4, 2, 9, 8, 1, 0, 6, 10, 3, 9, 5, 1, 8, 6],
  [6, 1, 7, 8, 10, 7, 6, 9, 0, 5, 9, 2, 10, 3, 5, 2],
  [3, 9, 10, 7, 1, 4, 10, 6, 5, 0, 8, 1, 6, 10, 2, 7],
  [9, 4, 7, 10, 5, 7, 6, 3, 9, 8, 0, 3, 2, 9, 10, 4],
  [8, 5, 3, 4, 2, 6, 10, 9, 2, 1, 3, 0, 7, 4, 1, 9],
  [5, 8, 9, 7, 8, 4, 9, 5, 10, 6, 2, 7, 0, 5, 6, 8],
  [10, 9, 7, 10, 6, 1, 5, 1, 3, 10, 9, 4, 5, 0, 2, 9],
  [7, 1, 6, 9, 10, 9, 7, 8, 5, 2, 10, 1, 6, 2, 0, 3],
  [1, 2, 5, 8, 10, 7, 1, 6, 2, 7, 4, 9, 8, 9, 3, 0]
]
final_mapping, cost = Run_pso(adj_matriz, tam)
print("Melhor solução encontrada:")
for linha in final_mapping:
    print(linha)
print("Fitness da melhor solução:", cost)
print()
