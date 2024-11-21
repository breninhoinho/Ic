import pygmo as pg
import numpy as np
import sys

# Adicionar o caminho absoluto do diretório onde está o arquivo
#sys.path.append('/home/breninhoinho/Desktop/Ic/Projeto/')

from Noc import *

# Definir o problema de mapeamento de objetivo único
class MappingProblemSO:
    def __init__(self, adj_matrix, num_cores, metrica):
        self.adj_matrix = adj_matrix
        self.n = len(adj_matrix)  # Número de nós/elementos
        self.num_cores = num_cores
        self.metrica = metrica


    def fitness(self, x):
        if self.metrica == "Energia":
            n = self.n  # Número de tarefas
            m = self.num_cores  # Número de roteadores
            valor_final = 0

            x = np.round(x).astype(int)  # Garantir que estamos lidando com inteiros
            if len(set(x)) != len(x):  # Verificar se há duplicação de valores
                return [float('inf')]  # Penalizar soluções inválidas

            for i in range(n):  # Percorre todas as tarefas
                for j in range(i+1, n):  # Garante que a matriz seja percorrida uma única vez (i, j) != (j, i)
                    bandwidth = self.adj_matrix[i][j]
                    if bandwidth > 0:  # Se há comunicação entre as tarefas i e j
                        # Encontra a posição de i e j no mapeamento
                        ix = x[i] // m
                        iy = x[i] % m
                        jx = x[j] // m
                        jy = x[j] % m
                        # Calcula a distância Manhattan
                        man_dist = abs(ix - jx) + abs(iy - jy)
                        # Acumula o valor da energia total
                        valor_final += bandwidth * man_dist

            return [valor_final]

        elif self.metrica == "Tolerancia":
            # Direções para as células adjacentes (cima, baixo, esquerda, direita)
            direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            tolerancia = 0

            m = int(self.num_cores**0.5)  # Número de roteadores (lado da matriz)

            x = np.round(x).astype(int)  # Garantir que estamos lidando com inteiros
            if len(set(x)) != len(x):  # Verificar se há duplicação de valores
                return [float('inf')]  # Penalizar soluções inválidas
            
            # Converte o vetor solução em uma matriz de tamanho (m x m)
            matriz = np.zeros((m, m), dtype=int)
            for i in range(len(x)):
                matriz[i // m][i % m] = x[i]
            
            for i in range(m):
                for j in range(m):
                    if matriz[i][j] != "" and int(matriz[i][j])  >= len(self.adj_matrix):
                        return [float('inf')]

            # Itera sobre cada célula da matriz
            for i in range(m):
                for j in range(m):
                    # Verifica se a célula contém uma tarefa (número diferente de 0)
                    if matriz[i][j] != 0:
                        # Verifica se há células adjacentes não vazias
                        for dx, dy in direcoes:
                            adj_x, adj_y = i + dx, j + dy
                            # Verifica se a célula adjacente está dentro dos limites da matriz
                            if 0 <= adj_x < m and 0 <= adj_y < m:
                                # Se a célula adjacente contém uma tarefa (número diferente de 0)
                                if matriz[adj_x][adj_y] != 0:
                                    tolerancia += 1

            return [tolerancia]
        elif self.metrica == "Latencia":
            x = np.round(x).astype(int)  # Garantir que estamos lidando com inteiros
            if len(set(x)) != len(x):  # Verificar se há duplicação de valores
                return [float('inf')]  # Penalizar soluções inválidas

            numero_roteadores = int(self.num_cores**0.5)  # Definir o número de roteadores (4x4)

            # Cria uma matriz 4x4 que será preenchida com valores de x ou strings vazias
            x_matrix = np.full((numero_roteadores, numero_roteadores), "", dtype=object)

            # Preenche a matriz com os valores de x (tamanhos menores que 4x4 deixam "" nos espaços vazios)
            for i in range(len(x)):
                ix = i // numero_roteadores  # Calcula a linha na matriz
                iy = i % numero_roteadores   # Calcula a coluna na matriz
                x_matrix[ix][iy] = x[i]  # Preenche a célula com o valor de x[i]
            
            for i in range(numero_roteadores):
                for j in range(numero_roteadores):
                    if x_matrix[i][j] != "" and int(x_matrix[i][j])  >= len(self.adj_matrix):
                        return [float('inf')]
                    
            # Passa a matriz preenchida para a classe Noc
            noc1 = Noc(numero_roteadores, "XY", self.adj_matrix, x_matrix)
            lat = noc1.latencia()

            return [lat]

    def get_bounds(self):
        """Definir os limites como uma permutação de [0, n-1]."""
        return ([0] * self.n, [self.num_cores - 1] * self.n)

    def get_nobj(self):
        """Número de funções objetivo (1 neste caso)."""
        return 1

    def get_name(self):
        return "Single-Objective Network Mapping Problem"

    def get_nix(self):
        """Número de variáveis de decisão (o tamanho da matriz de adjacência)."""
        return self.n

# Função para gerar uma permutação inicial para a população
def generate_initial_population(problem, size):
    population = []
    for _ in range(size):
        solution = np.random.permutation(problem.get_nix())  # Gera uma permutação aleatória
        population.append(solution)
    return np.array(population)

def Run_Single_Objective(adj_matrix, numero_roteadores, metrica):
    resultados = {}
    # Criar uma instância do problema
    problem = pg.problem(MappingProblemSO(adj_matrix, numero_roteadores**2, metrica))

    # Lista de algoritmos de otimização de objetivo único
    algorithms = {
        'DE': pg.algorithm(pg.de(gen=50)),
        'Simulated Annealing': pg.algorithm(pg.simulated_annealing()),
        'PSO': pg.algorithm(pg.pso(gen=50)),
        'GA': pg.algorithm(pg.sga(gen=50)),
        'IHS': pg.algorithm(pg.ihs()),
    }

    # Resolver o problema com diferentes algoritmos e armazenar os resultados
    for name, algo in algorithms.items():
        
        # Criar a população inicial de permutações
        initial_population = generate_initial_population(problem, size=100)
        pop = pg.population(problem)

        # Adicionar as soluções geradas na população inicial
        for individual in initial_population:
            pop.push_back(individual)

        # Resolver o problema
        algo.set_verbosity(0)  # Silenciar a saída do algoritmo
        pop = algo.evolve(pop)

        # Exibir a melhor solução encontrada
        best_solution = np.round(pop.get_x()[0]).astype(int)  # Melhor solução como array unidimensional
        best_fitness = pop.get_f()[0]  # Fitness da melhor solução

        # Verificar se o tamanho de best_solution é menor que numero_roteadores**2
        if len(best_solution) < numero_roteadores**2:
            # Preencher com strings vazias para garantir o tamanho correto
            missing_elements = numero_roteadores**2 - len(best_solution)
            best_solution = np.concatenate([best_solution, [""] * missing_elements])

        # Converter o array unidimensional em uma matriz de tamanho numero_roteadores x numero_roteadores
        best_solution_matrix = best_solution.reshape((numero_roteadores, numero_roteadores))

        # Armazenar os resultados no dicionário
        resultados[name] = {
            'matriz': best_solution_matrix,
            'fitness': best_fitness,
        }

    # Encontrar o mapeamento com o menor fitness
    melhor_algoritmo = min(resultados, key=lambda k: resultados[k]['fitness'])
    melhor_mapeamento = resultados[melhor_algoritmo]['matriz']

    return melhor_mapeamento
