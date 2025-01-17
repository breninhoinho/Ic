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
    """
    Verifica se todos os valores do dicionário contêm apenas o elemento 0.
    Retorna True se todos os valores forem [0], caso contrário, False.
    """
    for valores in custos_ordenado.values():
        if valores != [0]:
            return False
    return True

class Populacao:
    def __init__(self, populacao,adj_matriz):
        self.populacao = populacao  # cores do noc com o mapeamento
        self.matriz_adjacencia = adj_matriz
        self.fitness = None
        self.status = None
        
    
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
        
def Gerar_AC(tam, adj_matriz, nc):
    n = nc
    lista_AC = []
    for i in range(n):
        cores_noc =  [['' for _ in range(tam)] for _ in range(tam)]
        Cluster_based(cores_noc, adj_matriz)
        aci = Populacao(cores_noc,adj_matriz)
        aci.calcular_fitness()
        lista_AC.append(aci)

    return lista_AC


def ACA_Algorithm(AC, Nc, DP, PC):
    # Calcular o fitness usando a Eq. (4) e ordenar a população inicial do melhor para o pior
    AC.sort(key=lambda x: x.fitness)
    
    # Calcular a média de fitness usando a Eq. (9)
    AF = sum([x.fitness for x in AC]) / len(AC)
    
    # Calcular as quantidades QE e QI usando o valor de DP
    QE = Nc * DP
    QI = Nc - QE
    
    # Atualizar os estados dos condores na população para exploração e intensificação usando valores QE e QI
    update_states(AF, DP, PC, AC, Nc)

    tempo = 0
    lista_tempo = []
    tempo_tempo = 0
    lista = []
    
    while not tempo == 1000:
        for i in range(Nc):
            if AC[i].status == "exploração":
                # Movimento de exploração para AC[i]
                exploration_movement(AC[i])
            else:
                # Movimento de intensificação para AC[i]
                intensification_movement(AC[i])

        
        # Ordenar a nova população do melhor para o pior
        AC.sort(key=lambda x: x.fitness)
        
        # Calcular e atualizar os estados de cada condor usando o algoritmo 2
        update_states(AF, DP, PC, AC, Nc)
        # Atualizar o melhor AC
        if tempo == 0:
            best_AC = AC[0]
        elif AC[0].fitness < best_AC.fitness:
            tempo_tempo+=1
            best_AC = copy.copy(AC[0])
            lista.append(best_AC.fitness)
            lista_tempo.append(tempo_tempo)
        tempo += 1    
        
    # Obter a melhor solução AC_b
    AC_b = best_AC
    return AC_b ,lista,lista_tempo

def update_states(AF, DP, PC, AC, Nc):
    AFnew = sum([x.fitness for x in AC]) / len(AC)
    
    # Atualização da probabilidade de diversificação
    if AFnew > AF:
        DP = DP + PC
        if DP > 1:
            DP = 1
    else:
        DP = DP - PC
        if DP < 0:
            DP = 0

    # Cálculo da quantidade de exploração e intensificação
    QE = int(Nc * DP)
    QI = int(Nc - QE)

    # Atualização do estado dos cromossomos
    for i in range(1, QI + 1):
        AC[i].status = "intensificação"

    for i in range(QI + 1, Nc):
        AC[i].status = "exploração"

    return DP


def exploration_movement(condor):
    # Implementação do movimento de exploração para um condor
    n = len(condor.populacao)
    # Selecionar duas tarefas aleatórias para trocar de posição
    x1, y1 = random.randint(0, n - 1), random.randint(0, n - 1)

    far_positions = [
        (x1 + dx, y1 + dy)
        for dx in [-(n-1), 0, n-1]
        for dy in [-(n-1), 0, n-1]
        if 0 <= x1 + dx < n and 0 <= y1 + dy < n and (dx != 0 or dy != 0)
    ]

    while far_positions == []:
        x1, y1 = random.randint(0, n - 1), random.randint(0, n - 1)

        far_positions = [
            (x1 + dx, y1 + dy)
            for dx in [-(n-1), 0, n-1]
            for dy in [-(n-1), 0, n-1]
            if 0 <= x1 + dx < n and 0 <= y1 + dy < n and (dx != 0 or dy != 0)
        ]
    
    x2, y2 = random.choice(far_positions)
    
    
    # Trocar as tarefas de posição
    condor.populacao[x1][y1], condor.populacao[x2][y2] = condor.populacao[x2][y2], condor.populacao[x1][y1]
    
    # Recalcular o fitness após a troca
    condor.calcular_fitness()

def intensification_movement(condor):
    # Implementação do movimento de intensificação para um condor
    n = len(condor.populacao)
    # Selecionar uma tarefa aleatória
    x1, y1 = random.randint(0, n - 1), random.randint(0, n - 1)
    
    # Selecionar uma tarefa próxima para trocar de posição
    nearby_positions = [
        (x1 + dx, y1 + dy)
        for dx in [-1, 0, 1]
        for dy in [-1, 0, 1]
        if 0 <= x1 + dx < n and 0 <= y1 + dy < n and (dx != 0 or dy != 0)
    ]
    
    x2, y2 = random.choice(nearby_positions)
    
    # Trocar as tarefas de posição
    condor.populacao[x1][y1], condor.populacao[x2][y2] = condor.populacao[x2][y2], condor.populacao[x1][y1]
    
    # Recalcular o fitness após a troca
    condor.calcular_fitness()

"""
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

def Run_Andean_condor(adj_matriz, tam):
    Nc = 100

    AC = Gerar_AC(tam, adj_matriz, Nc)

    DP = 0.5

    PC = 0.1

    acb, lista , tempo = ACA_Algorithm(AC, Nc, DP, PC)

    return acb.populacao

# print()
# print("Melhor solução encontrada:")
# for linha in acb.populacao:
#     print(linha)
# print("Fitness da melhor solução: ", acb.fitness)
# print()

# plt.plot(tempo, lista, label = "Algoritmo Condores", marker='o')
# plt.xlabel('Quantidade de evoluções')
# plt.ylabel('Fitness')
# plt.title('Gráfico do do Fitness ao longo das evoluções')
# plt.legend()
# plt.show()