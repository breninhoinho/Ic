import random 

def Run_Random(adj_matriz, tam):
    # Cria uma matriz 2D de listas vazias
    cores_noc = [['' for _ in range(tam)] for _ in range(tam)]
    tam_cores = tam * tam  # Total de posições na matriz

    # Gera uma lista de índices de adj_matriz embaralhados
    indices = list(range(len(adj_matriz)))
    random.shuffle(indices)

    # Preenche a matriz sequencialmente com os índices embaralhados
    k = 0
    for i in range(tam):
        for j in range(tam):
            if k < len(indices):
                cores_noc[i][j] = indices[k]
                k += 1

    return cores_noc

