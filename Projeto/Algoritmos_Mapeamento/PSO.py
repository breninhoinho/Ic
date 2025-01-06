import random
import numpy as np

def calcular_energia(mapeamento, matriz):
    n = len(matriz)  # Número de tarefas
    m = len(mapeamento)  # Dimensão da NoC
    valor_final = 0

    for i in range(n):  # Percorre todas as tarefas
        for j in range(n):  # Garante que a matriz seja percorrida uma única vez (i, j) != (j, i)
            bandwidth = matriz[i][j]
            if bandwidth > 0:  # Se há comunicação entre as tarefas i e j
                # Encontra a posição de i no mapeamento
                ix, iy = [(k, l) for k in range(m) for l in range(m) if mapeamento[k][l] == i][0]
                jx, jy = [(k, l) for k in range(m) for l in range(m) if mapeamento[k][l] == j][0]
                # Calcula a distância Manhattan
                man_dist = abs(ix - jx) + abs(iy - jy)
                # Acumula o valor da energia total
                valor_final += bandwidth * man_dist

    return valor_final

def inicializar_particula(n, tamanho_noc):

    mapeamento = [[-1 for _ in range(tamanho_noc)] for _ in range(tamanho_noc)]
    tarefas = list(range(n))
    random.shuffle(tarefas)

    idx = 0
    for i in range(tamanho_noc):
        for j in range(tamanho_noc):
            if idx < len(tarefas):
                mapeamento[i][j] = tarefas[idx]
                idx += 1

    return mapeamento

def atualizar_velocidade(posicao, velocidade, pbest, gbest, w, c1, c2):
    novas_permutacoes = []
    tamanho_noc = len(posicao)

    for _ in range(tamanho_noc**2):  # Gera várias trocas possíveis
        if random.random() < c1:
            # Troca baseada em pBest
            i1, j1 = random.choice(range(tamanho_noc)), random.choice(range(tamanho_noc))
            i2, j2 = random.choice(range(tamanho_noc)), random.choice(range(tamanho_noc))
            novas_permutacoes.append(((i1, j1), (i2, j2)))
        if random.random() < c2:
            # Troca baseada em gBest
            i1, j1 = random.choice(range(tamanho_noc)), random.choice(range(tamanho_noc))
            i2, j2 = random.choice(range(tamanho_noc)), random.choice(range(tamanho_noc))
            novas_permutacoes.append(((i1, j1), (i2, j2)))

    velocidade_atualizada = velocidade + novas_permutacoes

    return velocidade_atualizada

def atualizar_posicao(posicao, velocidade):
    nova_posicao = [linha[:] for linha in posicao]  # Faz uma cópia profunda

    for troca in velocidade:
        (i1, j1), (i2, j2) = troca  # Troca definida como pares de índices
        nova_posicao[i1][j1], nova_posicao[i2][j2] = nova_posicao[i2][j2], nova_posicao[i1][j1]

    return nova_posicao

def Run_pso(matriz_adjacencia, tamanho_noc, num_particulas=1000, max_iter=100, w=0.6, c1=1.4, c2=1.6):
    n = len(matriz_adjacencia)  # Número de tarefas

    # Inicializa partículas
    particulas = [inicializar_particula(n, tamanho_noc) for _ in range(num_particulas)]
    velocidades = [[] for _ in range(num_particulas)]

    # Inicializa pBest e gBest
    pbest = particulas[:]
    pbest_valores = [calcular_energia(p, matriz_adjacencia) for p in particulas]

    gbest = particulas[np.argmin(pbest_valores)]
    gbest_valor = min(pbest_valores)

    for _ in range(max_iter):
        for i in range(num_particulas):
            # Atualiza velocidade e posição
            velocidades[i] = atualizar_velocidade(particulas[i], velocidades[i], pbest[i], gbest, w, c1, c2)
            particulas[i] = atualizar_posicao(particulas[i], velocidades[i])

            # Recalcula fitness
            fitness = calcular_energia(particulas[i], matriz_adjacencia)

            # Atualiza pBest
            if fitness < pbest_valores[i]:
                pbest[i] = particulas[i]
                pbest_valores[i] = fitness

            # Atualiza gBest
            if fitness < gbest_valor:
                gbest = particulas[i]
                gbest_valor = fitness

    for i in range(tamanho_noc):
        for j in range(tamanho_noc):
            if gbest[i][j] == -1:
                gbest[i][j] = ''
    return gbest

