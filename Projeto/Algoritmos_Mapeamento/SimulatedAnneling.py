import numpy as np
import random

class TaskMapping:
    def __init__(self, matrix):
        self.matrix = matrix

    def calcular_energia(self, mapeamento):
        n = len(self.matrix)  # Número de tarefas
        m = len(mapeamento)  # Dimensão da NoC
        valor_final = 0

        for i in range(n):  # Percorre todas as tarefas
            for j in range( n):  # Garante que a matriz seja percorrida uma única vez (i, j) != (j, i)
                bandwidth = self.matrix[i][j]
                if bandwidth > 0:  # Se há comunicação entre as tarefas i e j
                    # Encontra a posição de i no mapeamento
                    ix, iy = [(k, l) for k in range(m) for l in range(m) if mapeamento[k][l] == i][0]
                    jx, jy = [(k, l) for k in range(m) for l in range(m) if mapeamento[k][l] == j][0]
                    # Calcula a distância Manhattan
                    man_dist = abs(ix - jx) + abs(iy - jy)
                    # Acumula o valor da energia total
                    valor_final += bandwidth * man_dist

        return valor_final

def RunSimulateAnneling(task_adjacency_matrix, num_nodes, initial_temp, cooling_rate, max_iterations):
    
    
    num_tasks = len(task_adjacency_matrix)
    grid_size = num_nodes


    # inicializar
    current_mapping =  np.full((grid_size, grid_size), '', dtype=object)
    task_positions = random.sample(range(num_nodes**2), num_tasks)
    for idx, pos in enumerate(task_positions):
        x, y = divmod(pos, grid_size)
        current_mapping[x, y] = idx

    best_mapping = np.copy(current_mapping)
    best_cost = TaskMapping(task_adjacency_matrix).calcular_energia(best_mapping)

    temperature = initial_temp

    while temperature > 1e-3:
        for _ in range(max_iterations):
            # gerar a vizinhança

            new_mapping = np.copy(current_mapping)
            x1, y1, x2, y2 = [random.randint(0, grid_size - 1) for _ in range(4)]
            new_mapping[x1, y1], new_mapping[x2, y2] = new_mapping[x2, y2], new_mapping[x1, y1]

            # calcular custo
            task_mapper = TaskMapping(task_adjacency_matrix)
            current_cost = task_mapper.calcular_energia(current_mapping)
            new_cost = task_mapper.calcular_energia(new_mapping)

            #aceitacao da probabilidade
            if new_cost < current_cost or random.random() < np.exp((current_cost - new_cost) / temperature):
                current_mapping = np.copy(new_mapping)

                # update melhor solucao
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_mapping = np.copy(new_mapping)

        # refriamento
        temperature *= cooling_rate

    return best_mapping.tolist()

# task_adjacency_matrix = [
#     [0, 3, 2, 0],  
#     [3, 0, 0, 1],  
#     [2, 0, 0, 1],  
#     [0, 1, 1, 0]
# ] 
# num_nodes = 3
# initial_temp = 1000
# cooling_rate = 0.95
# max_iterations = 100

# final_mapping = RunSimulateAnneling(task_adjacency_matrix, num_nodes, 1000, 0.95, 100)

