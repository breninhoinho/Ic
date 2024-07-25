def Engineered_Mapping(cores_noc, tam, padrao_distribuicao, traversal , transition):
    # Número de núcleos ociosos
    numero_cores_ociosos = len(cores_noc) * len(cores_noc)
    
    # Gera a distribuição dos processos de acordo com o padrão especificado
    distribuicao = gerar_distribuicao(numero_cores_ociosos, tam, padrao_distribuicao)
    
    # Coloca o resultado da distribuição de acordo com a ordem de nó seguida e retorna cada posicao de cada tarefa no dicionario
    dicionario_posicoes = ordem_nó(cores_noc, distribuicao, traversal, transition)

    # Retorna o dicionário com as posições dos processos
    return dicionario_posicoes

def ordem_nó(cores_noc, distribuicao, traversal, transition):
    dicionario_posicoes = {}
    if traversal == "horizontally" and transition == "raster":
        indice = 0
        for i in range(len(cores_noc)):
            for j in range(len(cores_noc)):
                cores_noc[i][j] = distribuicao[indice]
                indice +=1
                dicionario_posicoes[str(indice)] = (i,j)
        return dicionario_posicoes
    
    elif traversal == "horizontally" and transition == "snake":
        indice = 0
        for i in range(len(cores_noc)):
            if i%2 != 0:
                for j in range(len(cores_noc)-1,-1,-1):
                    cores_noc[i][j] = distribuicao[indice]
                    indice +=1
                    dicionario_posicoes[str(indice)] = (i,j)
            else:
                for j in range(len(cores_noc)):
                    cores_noc[i][j] = distribuicao[indice]
                    indice +=1
                    dicionario_posicoes[str(indice)] = (i,j)
        return dicionario_posicoes
    elif traversal == "diagonally" and transition == "raster":
        indice = 0
        for i in range(len(cores_noc)):
            if i == 0:
                cores_noc[0][0] = distribuicao[indice]
                indice += 1
                dicionario_posicoes[str(indice)] = (0,0)
            else:
                for j in range(i+1):
                    cores_noc[i-j][j] = distribuicao[indice]
                    indice +=1
                    dicionario_posicoes[str(indice)] = (i-j,j)
        
        for i in range(1,len(cores_noc)):
            for j in range(len(cores_noc)-i):                        
                cores_noc[len(cores_noc)-1-j][i+j] = distribuicao[indice]
                indice +=1
                dicionario_posicoes[str(indice)] = (len(cores_noc)-1-j,i+j)
                    
        return dicionario_posicoes
    elif traversal == "diagonally" and transition == "snake":
        ...


def gerar_distribuicao(numero_cores_ociosos, tam, padrao_distribuicao):
    if padrao_distribuicao == "clustered":
        # Distribuição em cluster
        distri = gerar_distribuicao_clustered(numero_cores_ociosos, tam)
    elif padrao_distribuicao == "distributed":
        # Distribuição distribuída
        distri = gerar_distribuicao_distribuida(numero_cores_ociosos, tam)

    return distri

def gerar_distribuicao_clustered(numero_cores_ociosos, tam):
    # Cria um array vazio para os núcleos ociosos
    distri = [None] * numero_cores_ociosos
    
    # Preenche os núcleos com os processos até atingir 'tam'
    for i in range(tam):
        distri[i] = i + 1  # Processos numerados a partir de 1
    
    return distri

def gerar_distribuicao_distribuida(cores, tam):
    # Cria um array vazio para os núcleos
    distri = [None] * cores
    
    # Calcula o número de núcleos ociosos
    numero_cores_ociosos = cores - tam
    
    # Calcula o tamanho do cluster
    tam_cluster = tam // numero_cores_ociosos
    if tam_cluster ==0:
        tam_cluster =1
    # Índice para controlar a posição atual no array
    indice = 0
    
    # Número do processo atual
    processo = 1
    
    for i in range(numero_cores_ociosos):
        # Preenche os processos no cluster atual
        for j in range(tam_cluster):
            if indice < cores and processo <= tam:
                distri[indice] = processo
                indice += 1
                processo += 1
        
        # Insere um núcleo ocioso
        if indice < cores:
            distri[indice] = None
            indice += 1
    
    # Preenche quaisquer processos restantes
    while processo <= tam and indice < cores:
        distri[indice] = processo
        indice += 1
        processo += 1

    return distri

#print(gerar_distribuicao_distribuida(16,14))