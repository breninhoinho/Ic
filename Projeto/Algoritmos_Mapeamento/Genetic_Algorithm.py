import random
import copy
import matplotlib.pyplot as plt

def Cluster_based(cores_noc, adj_matriz):
    custos = {}
    soma = 0

    # Calcula os custos de comunicação para cada tarefa
    for linha in range(len(adj_matriz)):
        soma = 0
        custos[str(linha)] = []
        for coluna in range(len(adj_matriz)):
            if adj_matriz[linha][coluna] != 0:
                soma += adj_matriz[linha][coluna]
                custos[str(linha)].append(coluna)
        custos[str(linha)].append(soma)

    # Ordena as tarefas por custo total de comunicação (maior para menor)
    custos_ordenado = dict(sorted(custos.items(), key=lambda item: item[1][-1], reverse=True))

    n = len(cores_noc)
    rot = (random.randint(0, n - 1), random.randint(0, n - 1))  # Escolhe um núcleo inicial aleatório

    assigned_tiles = set()
    assigned_tiles.add(rot)

    # Atribui a primeira tarefa ao núcleo inicial
    primeira_tarefa = list(custos_ordenado.keys())[0]
    cores_noc[rot[0]][rot[1]] = int(primeira_tarefa)
    custos_ordenado[primeira_tarefa].pop()
    tarefas_adicionadas = [int(primeira_tarefa)]

    # Atribui as tarefas conectadas próximas à primeira tarefa
    for tarefa in custos_ordenado[primeira_tarefa]:
        nearby_tiles = [
            (rot[0] + dx, rot[1] + dy)
            for dx in range(-1, 2)
            for dy in range(-1, 2)
            if (0 <= rot[0] + dx < n) and (0 <= rot[1] + dy < n) and (rot[0] + dx, rot[1] + dy) not in assigned_tiles
        ]

        if nearby_tiles:
            tarefa_tile = random.choice(nearby_tiles)
            cores_noc[tarefa_tile[0]][tarefa_tile[1]] = int(tarefa)
            tarefas_adicionadas.append(tarefa)
            assigned_tiles.add(tarefa_tile)
        else:
            # Expande a busca para tiles mais distantes
            expanded_tiles = [
                (rot[0] + dx, rot[1] + dy)
                for dx in range(-2, 3)
                for dy in range(-2, 3)
                if (0 <= rot[0] + dx < n) and (0 <= rot[1] + dy < n) and (rot[0] + dx, rot[1] + dy) not in assigned_tiles
            ]

            if expanded_tiles:
                tarefa_tile = random.choice(expanded_tiles)
                cores_noc[tarefa_tile[0]][tarefa_tile[1]] = int(tarefa)
                tarefas_adicionadas.append(tarefa)
                assigned_tiles.add(tarefa_tile)
    del custos_ordenado[primeira_tarefa]


    # Continua o mapeamento para as demais tarefas
    while list(custos_ordenado.keys()) != []:
        
        for key in list(custos_ordenado.keys()):
            if verificar_elementos_zero(custos_ordenado):
                

                # Adiciona tarefas restantes de forma aleatória
                remaining_tiles =  [
                        (px + dx, py + dy)
                        for (px, py) in assigned_tiles
                        for dx in range(-1, 2)
                        for dy in range(-1, 2)
                        if (0 <= px + dx < n) and (0 <= py + dy < n) and (px + dx, py + dy) not in assigned_tiles
                    ]
                
                for tarefa in custos_ordenado.keys():
                    if not tarefa_esta_no_noc(tarefa,n,cores_noc):
                        if remaining_tiles:
                            tarefa_tile = random.choice(remaining_tiles)
                            cores_noc[tarefa_tile[0]][tarefa_tile[1]] = int(tarefa)
                            assigned_tiles.add(tarefa_tile)
                            remaining_tiles.remove(tarefa_tile)
                custos_ordenado.clear()
                break

            if any(custo in tarefas_adicionadas for custo in custos_ordenado[key][0:-1]):
                # Verifica se a tarefa principal do cluster está mapeada
                
                tarefa_principal = int(key)
                if not tarefa_esta_no_noc(tarefa_principal,n,cores_noc):
                    tarefas_adicionadas.append(tarefa_principal)
                    nearby_tiles = [
                        (px + dx, py + dy)
                        for (px, py) in assigned_tiles
                        for dx in range(-1, 2)
                        for dy in range(-1, 2)
                        if (0 <= px + dx < n) and (0 <= py + dy < n) and (px + dx, py + dy) not in assigned_tiles
                    ]

                    if nearby_tiles:
                        tarefa_tile = random.choice(nearby_tiles)
                        cores_noc[tarefa_tile[0]][tarefa_tile[1]] = tarefa_principal
                        assigned_tiles.add(tarefa_tile)
                    else:
                        # Expande a busca para tiles mais distantes
                        expanded_tiles = [
                            (px + dx, py + dy)
                            for (px, py) in assigned_tiles
                            for dx in range(-2, 3)
                            for dy in range(-2, 3)
                            if (0 <= px + dx < n) and (0 <= py + dy < n) and (px + dx, py + dy) not in assigned_tiles
                        ]

                        if expanded_tiles:
                            tarefa_tile = random.choice(expanded_tiles)
                            cores_noc[tarefa_tile[0]][tarefa_tile[1]] = tarefa_principal
                            assigned_tiles.add(tarefa_tile)
                


                if all(custo in tarefas_adicionadas for custo in custos_ordenado[key][0:-1]):
                    del custos_ordenado[key]
                else:
                    for tarefa in custos_ordenado[key][0:-1]:
                        if not tarefa_esta_no_noc(tarefa_principal,n,cores_noc):
                            tarefas_adicionadas.append(tarefa)
                            nearby_tiles = [
                                (px + dx, py + dy)
                                for (px, py) in assigned_tiles
                                for dx in range(-1, 2)
                                for dy in range(-1, 2)
                                if (0 <= px + dx < n) and (0 <= py + dy < n) and (px + dx, py + dy) not in assigned_tiles
                            ]

                            if nearby_tiles:
                                tarefa_tile = random.choice(nearby_tiles)
                                cores_noc[tarefa_tile[0]][tarefa_tile[1]] = int(tarefa)
                                assigned_tiles.add(tarefa_tile)
                            else:
                                # Expande a busca para tiles mais distantes
                                expanded_tiles = [
                                    (px + dx, py + dy)
                                    for (px, py) in assigned_tiles
                                    for dx in range(-2, 3)
                                    for dy in range(-2, 3)
                                    if (0 <= px + dx < n) and (0 <= py + dy < n) and (px + dx, py + dy) not in assigned_tiles
                                ]

                                if expanded_tiles:
                                    tarefa_tile = random.choice(expanded_tiles)
                                    cores_noc[tarefa_tile[0]][tarefa_tile[1]] = int(tarefa)
                                    assigned_tiles.add(tarefa_tile)
                    del custos_ordenado[key]
            else:
                
                 # Adiciona o cluster de maior valor em uma posição próxima às já mapeadas
                cluster_valor = max(custos_ordenado.items(), key=lambda item: item[1][-1])
                cluster_key = int(cluster_valor[0])
                nearby_tiles = [
                    (px + dx, py + dy)
                    for (px, py) in assigned_tiles
                    for dx in range(-1, 2)
                    for dy in range(-1, 2)
                    if (0 <= px + dx < n) and (0 <= py + dy < n) and (px + dx, py + dy) not in assigned_tiles
                    ]

                if nearby_tiles and not tarefa_esta_no_noc(cluster_key,n,cores_noc):
                    tarefa_tile = random.choice(nearby_tiles)
                    cores_noc[tarefa_tile[0]][tarefa_tile[1]] = cluster_key
                    assigned_tiles.add(tarefa_tile)

                                   
                    for tarefa in custos_ordenado[str(cluster_key)][:-1]:
                        nearby_tiles = [
                            (px + dx, py + dy)
                            for (px, py) in assigned_tiles
                            for dx in range(-1, 2)
                            for dy in range(-1, 2)
                            if (0 <= px + dx < n) and (0 <= py + dy < n) and (px + dx, py + dy) not in assigned_tiles
                        ]

                        if nearby_tiles:
                            tarefa_tile = random.choice(nearby_tiles)
                            cores_noc[tarefa_tile[0]][tarefa_tile[1]] = int(tarefa)
                            assigned_tiles.add(tarefa_tile)
                else:
                    for tarefa in custos_ordenado[str(cluster_key)][:-1]:
                        nearby_tiles = [
                            (px + dx, py + dy)
                            for (px, py) in assigned_tiles
                            for dx in range(-1, 2)
                            for dy in range(-1, 2)
                            if (0 <= px + dx < n) and (0 <= py + dy < n) and (px + dx, py + dy) not in assigned_tiles
                        ]

                        if nearby_tiles:
                            tarefa_tile = random.choice(nearby_tiles)
                            cores_noc[tarefa_tile[0]][tarefa_tile[1]] = int(tarefa)
                            assigned_tiles.add(tarefa_tile)
                del custos_ordenado[str(cluster_key)]
                        
    return cores_noc

def tarefa_esta_no_noc(tarefa,n,cores_noc):
    for i in range(n):
        for j in range (n):
            if cores_noc[i][j] == int(tarefa):
                return True
    return False

def verificar_elementos_zero(custos_ordenado):
    for valores in custos_ordenado.values():
        if valores != [0]:
            return False
    return True

def Gerar_AC(tam, adj_matriz, nc):
    n = nc
    lista_AC = []
    for i in range(n):
        cores_noc =  [['' for _ in range(tam)] for _ in range(tam)]
        Cluster_based(cores_noc, adj_matriz)
        aci = Populacao(cores_noc, adj_matriz)
        aci.calcular_fitness()
        lista_AC.append(aci)

    return lista_AC

class Populacao:
    def __init__(self, cores, adj_matriz):
        self.populacao = cores
        self.matriz_adjacencia = adj_matriz
        self.fitness = None
    
    def calcular_fitness(self):
        
        n = len(self.matriz_adjacencia)  # Número de tarefas
        m = len(self.populacao)  # Dimensão da NoC
        valor_final = 0
        for i in range(n):  # Percorre todas as tarefas
            for j in range(n):  # Garante que a matriz seja percorrida uma única vez (i, j) != (j, i)
                bandwidth = self.matriz_adjacencia[i][j]

                if bandwidth > 0 :  # Se há comunicação entre as tarefas i e j
                    # Encontra a posição de i no self.populacao
                    ix, iy = [(k, l) for k in range(m) for l in range(m) if self.populacao[k][l] == i][0]
                    # Encontra a posição de j no self.populacao
                    jx, jy = [(k, l) for k in range(m) for l in range(m) if self.populacao[k][l] == j][0]
                    # Calcula a distância Manhattan
                    man_dist = abs(ix - jx) + abs(iy - jy)
                    # Acumula o valor da energia total
                    valor_final += bandwidth * man_dist

        self.fitness = valor_final

def Genetic_Algorithm(populacao, geracoes, tamanho_populacao, adj_matriz, pc_mutar,tam):
    def selecionar(populacao):
        return min(random.sample(populacao, k=3), key=aptidao)
    
    def cruzar(pai1, pai2):
        # Colocar os genes em um array 
        arr_pai1 = []
        arr_pai2 = []

        for i in range(len(pai1.populacao)):
            for j in range(len(pai1.populacao)):
                arr_pai1.append(pai1.populacao[i][j])
                arr_pai2.append(pai2.populacao[i][j])

        # Seleciona dois pontos de cruzamento aleatórios
        ponto1, ponto2 = sorted(random.sample(range(len(arr_pai1)), 2))
        
        # Inicializa os filhos com -1 (indicando genes não atribuídos)
        filho1 = [-1] * len(arr_pai1)

        # Copia a subsequência entre os pontos de cruzamento do pai1 para o filho1
        filho1[ponto1:ponto2] = arr_pai1[ponto1:ponto2]

        pointer = ponto2
        for gene in arr_pai2:
            if gene not in filho1:
                if pointer >= len(filho1):
                    pointer = 0
                if -1 not in filho1:
                    break
                while filho1[pointer] != -1:
                    pointer += 1
                    if pointer >= len(filho1):
                        pointer = 0
                filho1[pointer] = gene
                pointer += 1
        
        # Reconstruir matriz 
        k=0
        cores_noc =  [['' for _ in range(tam)] for _ in range(tam)]
        for i in range(len(pai1.populacao)):
            for j in range(len(pai1.populacao)):
                cores_noc[i][j] = filho1[k]
                k += 1
        
        filho = Populacao(cores_noc, adj_matriz)

        return filho

    def mutar(individuo,pc_mutar):
        if random.random() > pc_mutar:
            for _ in range(1):  # número de mutações
                x1, y1 = random.randint(0, len(individuo.populacao) - 1), random.randint(0, len(individuo.populacao) - 1)
                x2, y2 = random.randint(0, len(individuo.populacao) - 1), random.randint(0, len(individuo.populacao) - 1)
                individuo.populacao[x1][y1], individuo.populacao[x2][y2] = individuo.populacao[x2][y2], individuo.populacao[x1][y1]
            return individuo
        return individuo
    def aptidao(individuo):
        if individuo.fitness is None:
            individuo.calcular_fitness()
        return individuo.fitness

    melhor_aptidao = float('inf')
    melhor_solucao = None
    geracoes_estagnadas = 0
    lista = []
    tempo = []
    t = 0
    for geracao in range(geracoes):
        nova_populacao = []
        for _ in range(tamanho_populacao ):
            pai1 = selecionar(populacao)
            pai2 = selecionar(populacao)
            filho = cruzar(pai1, pai2)
            nova_populacao.append(mutar(filho, pc_mutar))

        populacao = nova_populacao
        melhor_atual = min(populacao, key=aptidao)
        melhor_aptidao_atual = aptidao(melhor_atual)

        if melhor_aptidao_atual < melhor_aptidao:
            melhor_aptidao = melhor_aptidao_atual
            melhor_solucao = melhor_atual
            lista.append(melhor_aptidao)
            tempo.append(t)
            t += 1 
            geracoes_estagnadas = 0
        else:
            geracoes_estagnadas += 1

        if geracoes_estagnadas >= 1000:
            break

    return melhor_solucao, lista, tempo


def Run_Genetic_Algorithm(qtd_geracao, qtd_tamanho_populacao, taxa_mutacao, adj_matriz,tamanho):
    geracoes = qtd_geracao  # Número de gerações
    tamanho_populacao = qtd_tamanho_populacao  # Tamanho da população
    pc_mutar = taxa_mutacao
    tam = tamanho

    populacao_inicial = Gerar_AC(tam, adj_matriz, tamanho_populacao)

    melhor_solucao, lista , tempo = Genetic_Algorithm(populacao_inicial, geracoes, tamanho_populacao, adj_matriz, pc_mutar,tam)
    for i in range(len(melhor_solucao.populacao)):
        for j in range(len(melhor_solucao.populacao)):
            if melhor_solucao.populacao[i][j] == -1:
                melhor_solucao.populacao[i][j] = ''
    return melhor_solucao.populacao

"""
# Exemplo de uso
tam = 4  # Tamanho da matriz cores_noc (4x4)
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
"""
"""print()
print("Melhor solução encontrada:")
for linha in melhor_solucao.populacao:
    print(linha)
print("Fitness da melhor solução:", melhor_solucao.fitness)
print()
plt.plot(tempo, lista, label = "Algoritmo Genético", marker='o')
plt.xlabel('Quantidade de evoluções')
plt.ylabel('Fitness')
plt.title('Gráfico do do Fitness ao longo das evoluções')
plt.legend()
plt.show()
"""