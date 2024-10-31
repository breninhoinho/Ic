import random 

def Run_Random(adj_matriz, tam):
    # Cria uma matriz 2D de listas vazias
    cores_noc =  [['' for _ in range(tam)] for _ in range(tam)]
    tam_cores = tam
    
    # Preenche a matriz aleatoriamente com os índices da adj_matriz
    for i in range(len(adj_matriz)):
        posicao_x = random.randint(0, tam_cores-1)
        posicao_y = random.randint(0, tam_cores-1)
        
        # Adiciona o valor na posição sorteada
        cores_noc[posicao_x][posicao_y] = i
    
    return cores_noc


