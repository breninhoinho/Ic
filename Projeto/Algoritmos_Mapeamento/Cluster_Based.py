import random

def Run_Cluster_based(cores_noc, adj_matriz):
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