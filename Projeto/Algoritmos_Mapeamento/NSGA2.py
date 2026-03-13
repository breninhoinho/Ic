import random
import matplotlib
matplotlib.use('TkAgg')   # backend compatível com tkinter
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — necessário para plot 3D


# ─────────────────────────────────────────────────────────────
# Funções de métricas
# ─────────────────────────────────────────────────────────────

def calcular_energia(mapeamento, matrix, dimensao):
    n = len(matrix)
    m = len(mapeamento)
    valor_final = 0
    # Cache de posições para não recalcular O(n²·m²)
    pos = {}
    for k in range(m):
        for l in range(m):
            if mapeamento[k][l] != '':
                pos[mapeamento[k][l]] = (k, l)

    for i in range(n):
        for j in range(n):
            bw = matrix[i][j]
            if bw > 0 and i in pos and j in pos:
                ix, iy = pos[i]
                jx, jy = pos[j]
                valor_final += bw * (abs(ix - jx) + abs(iy - jy))
    return valor_final


def calcular_latencia(mapeamento, matrix, dimensao, roteamento):
    """
    Estimativa de latência: hop count máximo ponderado pela bandwidth.
    Diferente de energia (que soma todos os pares), aqui pegamos o maior
    custo individual — bottleneck de comunicação.
    """
    n = len(matrix)
    m = len(mapeamento)
    pos = {}
    for k in range(m):
        for l in range(m):
            if mapeamento[k][l] != '':
                pos[mapeamento[k][l]] = (k, l)

    max_custo = 0
    for i in range(n):
        for j in range(n):
            bw = matrix[i][j]
            if bw > 0 and i in pos and j in pos:
                ix, iy = pos[i]
                jx, jy = pos[j]
                hops = abs(ix - jx) + abs(iy - jy)
                custo = bw * hops   # latência proporcional a hops * bandwidth
                if custo > max_custo:
                    max_custo = custo
    return float(max_custo)


def calcular_tolerancia_falha(mapeamento, matrix, dimensao):
    """
    Conta pares de células vizinhas que ambas têm tarefas alocadas.
    Quanto maior, mais tarefas estão próximas — mais caminhos alternativos existem.
    Retornamos negativo porque o NSGA-II minimiza todos os objetivos.
    """
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    tolerancia = 0
    for i in range(len(mapeamento)):
        for j in range(len(mapeamento[i])):
            if mapeamento[i][j] != '':
                for dx, dy in direcoes:
                    x, y = i + dx, j + dy
                    if 0 <= x < len(mapeamento) and 0 <= y < len(mapeamento[0]):
                        if mapeamento[x][y] != '':
                            tolerancia += 1
    return tolerancia


# ─────────────────────────────────────────────────────────────
# Classe Indivíduo
# ─────────────────────────────────────────────────────────────

class Individuo:
    def __init__(self, mapeamento, matrix, dimensao, roteamento, selecao):
        self.mapeamento = mapeamento
        self.matrix = matrix
        self.dimensao = dimensao
        self.roteamento = roteamento
        self.selecao = selecao
        self.objetivos = []

        if selecao[0]:   # Energia (minimizar)
            self.objetivos.append(calcular_energia(mapeamento, matrix, dimensao))
        if selecao[1]:   # Latência (minimizar)
            self.objetivos.append(calcular_latencia(mapeamento, matrix, dimensao, roteamento))
        if selecao[2]:   # Tolerância (maximizar → negativo para minimizar)
            self.objetivos.append(-calcular_tolerancia_falha(mapeamento, matrix, dimensao))

        # Atributos de dominância — resetados antes de cada sort
        self.dominancia_count = 0
        self.dominados = []
        self.rank = 0
        self.crowding_distance = 0

    def dominates(self, other):
        better_or_equal = all(s <= o for s, o in zip(self.objetivos, other.objetivos))
        better_in_one   = any(s <  o for s, o in zip(self.objetivos, other.objetivos))
        return better_or_equal and better_in_one

    def reset_dominancia(self):
        """Deve ser chamado antes de cada fast_non_dominated_sort."""
        self.dominancia_count = 0
        self.dominados = []
        self.rank = 0
        self.crowding_distance = 0


# ─────────────────────────────────────────────────────────────
# NSGA-II — operadores
# ─────────────────────────────────────────────────────────────

def fast_non_dominated_sort(population):
    # BUGFIX: resetar estado de dominância antes de recalcular
    for p in population:
        p.reset_dominancia()

    fronts = [[]]
    for p in population:
        for q in population:
            if p is q:
                continue
            if p.dominates(q):
                p.dominados.append(q)
            elif q.dominates(p):
                p.dominancia_count += 1
        if p.dominancia_count == 0:
            p.rank = 0
            fronts[0].append(p)

    i = 0
    while fronts[i]:
        Q = []
        for p in fronts[i]:
            for q in p.dominados:
                q.dominancia_count -= 1
                if q.dominancia_count == 0:
                    q.rank = i + 1
                    Q.append(q)
        i += 1
        fronts.append(Q)
    return fronts[:-1]


def calculate_crowding_distance(front):
    if not front:
        return
    n_obj = len(front[0].objetivos)
    for ind in front:
        ind.crowding_distance = 0

    for obj in range(n_obj):
        front.sort(key=lambda x: x.objetivos[obj])
        front[0].crowding_distance  = float('inf')
        front[-1].crowding_distance = float('inf')
        if len(front) > 2:
            obj_range = front[-1].objetivos[obj] - front[0].objetivos[obj]
            if obj_range > 0:
                for k in range(1, len(front) - 1):
                    front[k].crowding_distance += (
                        front[k+1].objetivos[obj] - front[k-1].objetivos[obj]
                    ) / obj_range


def generate_random_mapping(dimensao, num_tarefas):
    # BUGFIX: parâmetros estavam trocados na versão original
    tarefas = list(range(num_tarefas))
    random.shuffle(tarefas)
    mapeamento = [['' for _ in range(dimensao)] for _ in range(dimensao)]
    idx = 0
    for i in range(dimensao):
        for j in range(dimensao):
            if idx < num_tarefas:
                mapeamento[i][j] = tarefas[idx]
                idx += 1
    return mapeamento


def crossover(parent1, parent2, dimensao):
    child1 = [row[:] for row in parent1]
    child2 = [row[:] for row in parent2]
    for i in range(dimensao // 2):
        for j in range(dimensao):
            child1[i][j], child2[i][j] = child2[i][j], child1[i][j]
    # Garantir que os filhos sejam permutações válidas (sem duplicatas)
    child1 = _reparar_mapeamento(child1, dimensao, len(parent1) * len(parent1[0]))
    child2 = _reparar_mapeamento(child2, dimensao, len(parent2) * len(parent2[0]))
    return child1, child2


def _reparar_mapeamento(mapeamento, dimensao, total_celulas):
    """
    Após crossover, pode haver tarefas duplicadas/faltando.
    Garante que cada tarefa apareça exatamente uma vez.
    """
    num_tarefas = sum(1 for row in mapeamento for v in row if v != '')
    presentes = {}
    for i in range(dimensao):
        for j in range(dimensao):
            v = mapeamento[i][j]
            if v != '':
                if v in presentes:
                    mapeamento[i][j] = ''  # duplicata → esvazia
                else:
                    presentes[v] = (i, j)

    # Tarefas que faltam
    todas = set(range(num_tarefas))
    faltando = list(todas - set(presentes.keys()))
    random.shuffle(faltando)

    idx = 0
    for i in range(dimensao):
        for j in range(dimensao):
            if mapeamento[i][j] == '' and idx < len(faltando):
                mapeamento[i][j] = faltando[idx]
                idx += 1
    return mapeamento


def mutate(mapping, dimensao, mutation_rate=0.1):
    if random.random() < mutation_rate:
        i1, j1 = random.randint(0, dimensao-1), random.randint(0, dimensao-1)
        i2, j2 = random.randint(0, dimensao-1), random.randint(0, dimensao-1)
        mapping[i1][j1], mapping[i2][j2] = mapping[i2][j2], mapping[i1][j1]
    return mapping


# ─────────────────────────────────────────────────────────────
# Algoritmo principal
# ─────────────────────────────────────────────────────────────

def Run_NSGA2(matrix, dimensao, roteamento, pop_size=20, generations=30,
              selecao=[True, True, True], plotar_pareto=True):
    """
    Executa o NSGA-II e retorna o melhor mapeamento.
    Se plotar_pareto=True, exibe o gráfico da frente de Pareto ao final.
    """
    num_objetivos = sum(selecao)
    if num_objetivos < 2:
        raise ValueError("NSGA-II requer pelo menos 2 objetivos selecionados.")

    num_tarefas = len(matrix)

    # População inicial
    population = [
        Individuo(generate_random_mapping(dimensao, num_tarefas),
                  matrix, dimensao, roteamento, selecao)
        for _ in range(pop_size)
    ]

    for gen in range(generations):
        offspring = []
        while len(offspring) < pop_size:
            # Torneio binário para seleção
            p1 = _torneio(population)
            p2 = _torneio(population)
            c1_map, c2_map = crossover(p1.mapeamento, p2.mapeamento, dimensao)
            c1_map = mutate(c1_map, dimensao)
            c2_map = mutate(c2_map, dimensao)
            offspring.append(Individuo(c1_map, matrix, dimensao, roteamento, selecao))
            if len(offspring) < pop_size:
                offspring.append(Individuo(c2_map, matrix, dimensao, roteamento, selecao))

        combined = population + offspring
        fronts   = fast_non_dominated_sort(combined)

        new_population = []
        i = 0
        while i < len(fronts) and len(new_population) + len(fronts[i]) <= pop_size:
            calculate_crowding_distance(fronts[i])
            new_population.extend(fronts[i])
            i += 1
        if len(new_population) < pop_size and i < len(fronts):
            calculate_crowding_distance(fronts[i])
            fronts[i].sort(key=lambda x: (-x.crowding_distance, x.rank))
            new_population.extend(fronts[i][:pop_size - len(new_population)])

        population = new_population

    # Frente de Pareto final (rank 0)
    fronts = fast_non_dominated_sort(population)
    pareto_front = fronts[0]

    if plotar_pareto:
        plotar_frente_pareto(pareto_front, selecao)

    # Retorna o indivíduo com maior crowding distance da frente de Pareto
    calculate_crowding_distance(pareto_front)
    best = max(pareto_front, key=lambda x: x.crowding_distance)
    return best.mapeamento


def _torneio(population, k=2):
    """Seleção por torneio binário."""
    candidatos = random.sample(population, k)
    return min(candidatos, key=lambda x: (x.rank, -x.crowding_distance))


# ─────────────────────────────────────────────────────────────
# Visualização da frente de Pareto
# ─────────────────────────────────────────────────────────────

# Nomes e rótulos para cada objetivo (índice 0, 1, 2)
_NOMES_OBJ = ["Energia", "Latência", "Tolerância"]
_LABELS_OBJ = ["Energia (bandwidth × hops)", "Latência (max hop × bw)", "Tolerância (−vizinhos)"]


def plotar_frente_pareto(pareto_front, selecao):
    """
    Plota a frente de Pareto.
    - 2 objetivos → scatter 2D
    - 3 objetivos → scatter 3D
    Cada ponto é um mapeamento não-dominado.
    """
    if not pareto_front:
        print("Frente de Pareto vazia — nada a plotar.")
        return

    # Montar lista de labels dos objetivos ativos
    labels_ativos = [_LABELS_OBJ[i] for i, s in enumerate(selecao) if s]
    n_obj = len(labels_ativos)

    # Extrair coordenadas — inverte sinal de tolerância para mostrar valor real
    coords = []
    for ind in pareto_front:
        ponto = []
        obj_idx = 0
        for i, s in enumerate(selecao):
            if s:
                v = ind.objetivos[obj_idx]
                if i == 2:   # tolerância foi negada para minimizar
                    v = -v
                ponto.append(v)
                obj_idx += 1
        coords.append(ponto)

    xs = [p[0] for p in coords]
    ys = [p[1] for p in coords]

    # Cor dos pontos proporcional ao crowding distance (diversidade)
    cd_vals = [ind.crowding_distance for ind in pareto_front]
    cd_finito = [v for v in cd_vals if v != float('inf')]
    cd_max = max(cd_finito) if cd_finito else None
    # Se cd_max é None ou 0, todos os pontos recebem a mesma cor
    if cd_max:
        cores = [min(v, cd_max) / cd_max for v in cd_vals]
    else:
        cores = [1.0] * len(cd_vals)

    fig = plt.figure(figsize=(8, 6))
    fig.patch.set_facecolor('#FAFAFA')

    if n_obj == 3:
        zs = [p[2] for p in coords]
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#FAFAFA')
        sc = ax.scatter(xs, ys, zs, c=cores, cmap='plasma', s=80, edgecolors='#333', linewidths=0.5, alpha=0.9)
        ax.set_xlabel(labels_ativos[0], fontsize=9, labelpad=8)
        ax.set_ylabel(labels_ativos[1], fontsize=9, labelpad=8)
        ax.set_zlabel(labels_ativos[2], fontsize=9, labelpad=8)
        ax.set_title("Frente de Pareto — NSGA-II", fontsize=13, fontweight='bold', pad=14)
    else:
        ax = fig.add_subplot(111)
        ax.set_facecolor('#F5F5F5')
        sc = ax.scatter(xs, ys, c=cores, cmap='plasma', s=90,
                        edgecolors='#333', linewidths=0.5, alpha=0.9, zorder=3)

        # Linha conectando os pontos da frente (ordena pelo eixo X)
        pares = sorted(zip(xs, ys))
        ax.plot([p[0] for p in pares], [p[1] for p in pares],
                color='#AAAAAA', linewidth=1, linestyle='--', zorder=2)

        ax.set_xlabel(labels_ativos[0], fontsize=10)
        ax.set_ylabel(labels_ativos[1], fontsize=10)
        ax.set_title("Frente de Pareto — NSGA-II", fontsize=13, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.4)

    cbar = fig.colorbar(sc, ax=ax, pad=0.02, fraction=0.03)
    cbar.set_label("Crowding distance (diversidade)", fontsize=8)

    plt.tight_layout()
    plt.savefig("pareto_front.png", dpi=120, bbox_inches='tight')
    plt.show()
