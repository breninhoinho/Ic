import random

def Run_Cluster_based(cores_noc, adj_matriz):
    import random

    def tarefa_esta_no_noc(t, noc):
        return any(t in linha for linha in noc)

    def tiles_livres(noc):
        return [(i, j) for i in range(len(noc)) for j in range(len(noc)) if noc[i][j] == '' or noc[i][j] is None]

    n = len(cores_noc)

    # -------------------------------------------------------
    # 1) CALCULA CUSTO DE COMUNICAÇÃO POR TAREFA
    # -------------------------------------------------------
    custos = {}
    for linha in range(len(adj_matriz)):
        soma = sum(adj_matriz[linha])
        conectados = [i for i, v in enumerate(adj_matriz[linha]) if v != 0]
        custos[str(linha)] = conectados + [soma]

    # ordena do maior custo para o menor
    custos_ordenado = dict(sorted(custos.items(), key=lambda x: x[1][-1], reverse=True))

    # -------------------------------------------------------
    # 2) POSIÇÃO INICIAL
    # -------------------------------------------------------
    rot = (random.randint(0, n - 1), random.randint(0, n - 1))
    assigned_tiles = {rot}

    primeira_tarefa = int(list(custos_ordenado.keys())[0])
    cores_noc[rot[0]][rot[1]] = primeira_tarefa
    custos_ordenado[str(primeira_tarefa)].pop()
    tarefas_adicionadas = {primeira_tarefa}

    # -------------------------------------------------------
    # 3) INSERE TAREFAS DO CLUSTER INICIAL
    # -------------------------------------------------------
    for tarefa in custos_ordenado[str(primeira_tarefa)]:
        if tarefa in tarefas_adicionadas:
            continue

        livres = tiles_livres(cores_noc)
        if not livres:
            break

        tile = random.choice(livres)
        cores_noc[tile[0]][tile[1]] = int(tarefa)
        tarefas_adicionadas.add(int(tarefa))
        assigned_tiles.add(tile)

    del custos_ordenado[str(primeira_tarefa)]

    # -------------------------------------------------------
    # 4) INSERE RESTANTE DOS CLUSTERS
    # -------------------------------------------------------
    for key, valores in list(custos_ordenado.items()):

        tarefa_principal = int(key)
        if tarefa_principal not in tarefas_adicionadas:
            livres = tiles_livres(cores_noc)
            if not livres:
                break
            tile = random.choice(livres)
            cores_noc[tile[0]][tile[1]] = tarefa_principal
            tarefas_adicionadas.add(tarefa_principal)
            assigned_tiles.add(tile)

        # adiciona conectadas
        for tarefa in valores[:-1]:
            tarefa = int(tarefa)
            if tarefa in tarefas_adicionadas:
                continue

            livres = tiles_livres(cores_noc)
            if not livres:
                break

            tile = random.choice(livres)
            cores_noc[tile[0]][tile[1]] = tarefa
            tarefas_adicionadas.add(tarefa)
            assigned_tiles.add(tile)

        del custos_ordenado[key]

    # -------------------------------------------------------
    # 5) CORREÇÃO FINAL (REMOVE DUPLICADOS E PREENCHE FALTANDO)
    # -------------------------------------------------------
    total_tarefas = len(adj_matriz)
    mapa = [cores_noc[i][j] for i in range(n) for j in range(n)]

    # remove duplicados mantendo o primeiro
    vistos = set()
    duplicados = []
    for t in mapa:
        if t in vistos:
            duplicados.append(t)
        else:
            vistos.add(t)

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