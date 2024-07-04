import random

def Cluster_based(cores_noc, adj_matriz):
    # 1,2,3,4 calcular o custo de comunicação de cada tarefa com seus parentes e rankear

    # Dicionário para armazenar os custos de comunicação para cada tarefa
    custos = {}
    soma = 0

    # Iterar sobre a matriz de adjacência para calcular o custo de comunicação
    for linha in range(len(adj_matriz)):
        soma = 0
        custos[str(linha)] = []
        for coluna in range(len(adj_matriz)):
            if adj_matriz[linha][coluna] != 0:
                soma += adj_matriz[linha][coluna]
                custos[str(linha)].append(coluna)
        custos[str(linha)].append(soma)

    # Ordenar o dicionário com base no custo de comunicação (último elemento de cada lista)
    custos_ordenado = dict(sorted(custos.items(), key=lambda item: item[1][-1], reverse=True))
    # 5 selecionar um espaço aleatório para colocar a primeira tarefa
    n = len(cores_noc)
    rot = (random.randint(0, n - 1), random.randint(0, n - 1))

    # Adiciona o tile inicial ao conjunto de tiles atribuídos
    assigned_tiles = set()
    assigned_tiles.add(rot)
    
    # Coloca a primeira tarefa no tile selecionado aleatoriamente
    primeira_tarefa = list(custos_ordenado.keys())[0]
    cores_noc[rot[0]][rot[1]] = int(primeira_tarefa)
    custos_ordenado[primeira_tarefa].pop()
    tarefas_adicionadas = [int(primeira_tarefa)]

    # 6 Mapear as tarefas restantes
    for tarefa in custos_ordenado[primeira_tarefa]:
        # Encontrar tiles disponíveis próximos ao tile da primeira tarefa
        nearby_tiles = [
            (rot[0] + dx, rot[1] + dy)
            for dx in range(-1, 2)
            for dy in range(-1, 2)
            if (0 <= rot[0] + dx < n) and (0 <= rot[1] + dy < n) and (rot[0] + dx, rot[1] + dy) not in assigned_tiles
        ]

        if nearby_tiles:
            # Selecionar um tile próximo disponível
            tarefa_tile = random.choice(nearby_tiles)
            cores_noc[tarefa_tile[0]][tarefa_tile[1]] = int(tarefa)
            tarefas_adicionadas.append(tarefa)
            assigned_tiles.add(tarefa_tile)
    del custos_ordenado[primeira_tarefa]


    
    # 7 e 8: Mapear as tarefas restantes baseado na comunicação com tarefas já mapeadas
    while list(custos_ordenado.keys()) != []:
        for key in list(custos_ordenado.keys()):
            if any(custo in tarefas_adicionadas for custo in custos_ordenado[key][0:-1]):
                if all(custo in tarefas_adicionadas for custo in custos_ordenado[key][0:-1]):
                    del custos_ordenado[key]
                else:
                    for tarefa in custos_ordenado[key][0:-1]:
                        if tarefa not in tarefas_adicionadas:
                            tarefas_adicionadas.append(tarefa)
                            # Encontrar tiles disponíveis próximos a tiles já mapeados
                            nearby_tiles = [
                                (px + dx, py + dy)
                                for (px, py) in assigned_tiles
                                for dx in range(-1, 2)
                                for dy in range(-1, 2)
                                if (0 <= px + dx < n) and (0 <= py + dy < n) and (px + dx, py + dy) not in assigned_tiles
                            ]

                            if nearby_tiles:
                                # Selecionar um tile próximo disponível
                                tarefa_tile = random.choice(nearby_tiles)
                                cores_noc[tarefa_tile[0]][tarefa_tile[1]] = int(tarefa)
                                assigned_tiles.add(tarefa_tile)
                    del custos_ordenado[key]
                       
        # Retornar a matriz cores_noc com o mapeamento final
    return cores_noc

# Exemplo de uso:
cores_noc = [[None] * 4 for _ in range(4)]
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

#adj_matriz = [[0, 5, 0, 4, 0],[5 ,0 ,3 ,0 ,2],[0, 3, 0 ,1 ,0],[4 ,0 ,1 ,0, 8],[0, 2 ,0 ,8 ,0]]

class Populacao:
    def __init__(self, populacao,adj_matriz):
        self.populacao = populacao  # cores do noc com o mapeamento
        self.matriz_adjacencia = adj_matriz
        self.fitness = None
        
    
    def calcular_fitness(self):
        n = len(self.matriz_adjacencia)
        m = len(self.populacao)
        valor_final = 0
        bandwidth = 0
        man_dist = 0
        for i in range(n):
            for j in range(n):
                bandwidth = self.matriz_adjacencia[i][j]
                if bandwidth == 0:
                    pass
                else:
                    ix = 0
                    iy = 0
                    jx = 0
                    jy = 0
                    for k in range(m):
                        for l in range(m):
                            if self.populacao[k][l] == i:
                                ix = k
                                iy = l
                            if self.populacao[k][l] == j:
                                jx = k
                                jy = l    
                    man_dist = abs(ix-jx) + abs(iy-jy)

                    valor_final += bandwidth * man_dist
                    self.fitness = valor_final

    
def Gerar_AC(tam, adj_matriz):
    n = 10
    lista_AC = []
    for i in range(n):
        cores_noc =  [['' for _ in range(tam)] for _ in range(tam)]
        Cluster_based(cores_noc, adj_matriz)
        aci = Populacao(cores_noc,adj_matriz)
        aci.calcular_fitness()
        lista_AC.append(aci)
    return lista_AC

lista = Gerar_AC(4,adj_matriz)
lista.sort(key=lambda x: x.fitness)
AF = sum([x.fitness for x in lista]) / len(lista)
print(AF)
for i in lista:
    print(i.populacao)
