import pygmo as pg
import numpy as np

# Definir a matriz de adjacência (exemplo)
adj_matrix = np.array([
    [0, 1, 0, 1, 0, 0, 0, 1, 0],  # Tarefa 0 está conectada a 1, 3, 7
    [1, 0, 1, 0, 1, 0, 0, 0, 0],  # Tarefa 1 está conectada a 0, 2, 4
    [0, 1, 0, 0, 0, 1, 0, 0, 0],  # Tarefa 2 está conectada a 1, 5
    [1, 0, 0, 0, 1, 0, 0, 0, 0],  # Tarefa 3 está conectada a 0, 4
    [0, 1, 0, 1, 0, 0, 1, 0, 0],  # Tarefa 4 está conectada a 1, 3, 6
    [0, 0, 1, 0, 0, 0, 0, 0, 1],  # Tarefa 5 está conectada a 2, 8
    [0, 0, 0, 0, 1, 0, 0, 1, 0],  # Tarefa 6 está conectada a 4, 7
    [1, 0, 0, 0, 0, 0, 1, 0, 0],  # Tarefa 7 está conectada a 0, 6
    [0, 0, 0, 0, 0, 1, 0, 0, 0],  # Tarefa 8 está conectada a 5
])
# Definir o problema de mapeamento de objetivo único
class MappingProblemSO:
    def __init__(self, adj_matrix, num_cores):
        self.adj_matrix = adj_matrix
        self.n = len(adj_matrix)  # Número de nós/elementos
        self.num_cores = num_cores

    def fitness(self, x):
        """
        Função de aptidão. Retorna um valor representando a função objetivo.
        1. Minimizar o número de comunicações entre nodos não adjacentes.
        """
        x = np.round(x).astype(int)  # Garantir que estamos lidando com inteiros
        if len(set(x)) != len(x):  # Verificar se há duplicação de valores
            return [float('inf')]  # Penalizar soluções inválidas

        # Função objetivo: Penalidade por comunicação entre nodos não adjacentes
        penalty = 0
        for i in range(len(x)):
            for j in range(i + 1, len(x)):
                if self.adj_matrix[i][j] == 1 and abs(x[i] - x[j]) > 1:
                    # Penalidade se as tarefas adjacentes estiverem em cores não adjacentes
                    penalty += 1

        return [penalty]

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

numero_roteadores = 3

resultados = {}

# Criar uma instância do problema
problem = pg.problem(MappingProblemSO(adj_matrix, numero_roteadores**2))

# Lista de algoritmos de otimização de objetivo único
algorithms = {
    'DE': pg.algorithm(pg.de(gen=50)),
    'Simulated Annealing': pg.algorithm(pg.simulated_annealing()),
    'PSO': pg.algorithm(pg.pso(gen=50)),
    'GA': pg.algorithm(pg.sga(gen=50)),
    'IHS': pg.algorithm(pg.ihs()),
}



# Resolver o problema com diferentes algoritmos e exibir uma solução para cada um
for name, algo in algorithms.items():
    print(f"Executando o algoritmo: {name}")
    
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
