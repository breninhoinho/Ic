import random 

def Random(cores_noc,tam):
    dicionario_posicoes = {}
    tam_cores = len(cores_noc)
    for i in range (tam):
        posicao_x = random.randint(0,tam_cores-1)
        posicao_y = random.randint(0,tam_cores-1)
        if cores_noc[posicao_x][posicao_y] != '':
            cores_noc[posicao_x][posicao_y].append(i)
        elif cores_noc[posicao_x][posicao_y] == '':
            cores_noc[posicao_x][posicao_y] = [i]
        dicionario_posicoes[str(i+1)] = (posicao_x,posicao_y)
    return dicionario_posicoes


