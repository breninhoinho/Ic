from random import randint
import matplotlib.pyplot as plt
import numpy as np

class Noc:
    def __init__(self, dimensao):
        self.dimensao = dimensao
        self.matriz_roteadores = self.criar_matriz_roteadores(dimensao)
        self.total_pacotes = 0
        self.total_pacotes_recebidos = [0]
        self.total_pacotes_chegos = [0]
        self.total_pacotes_perdidos = [0]
        self.chegos = 0
    
    def criar_matriz_roteadores(self, dimensao):
        tamanho = dimensao

        matriz = [['' for _ in range(tamanho)] for _ in range(tamanho)] # matriz vazia

        for i in range(tamanho):
            for j in range(tamanho):
                matriz[i][j] = Roteador((i,j), self)  # passando a instância de Noc para Roteador

        return matriz

    def alocar_pacotes(self,pacote):
        x,y = pacote.posicao_inicial 
        self.total_pacotes += 1
        self.matriz_roteadores[x][y].buffers["Processador"].append(pacote)

    def rodar_simulacao(self, qtd_max_pacotes):
        input = [0]
        paramentro = [0]
        tempo = 0
        media = 0
        for i in range(1,qtd_max_pacotes): 
            # marcar tempo
            tempo +=1
            input.append(tempo)
            # criar pacotes
            self.criar_pacotes_ef(tempo,i)
            # ver paraemtro
            media = self.Efficiency(i)
            paramentro.append(media)       
        return input, paramentro
        

    def criar_pacotes(self,tempo,qtd_pacotes_max):
            rot = (randint(0,self.dimensao-1),randint(0,self.dimensao-1))
            for _ in range(self.dimensao*self.dimensao):
                pacote = Pacote(rot,(randint(0,self.dimensao-1),randint(0,self.dimensao-1)),tempo)
                self.alocar_pacotes(pacote)    

    def criar_pacotes_ef(self,tempo,qtd_pacotes_max):
            for i in range(qtd_pacotes_max):
                for j in range(self.dimensao):
                    for k in range(self.dimensao):
                        pacote = Pacote((j,k),(randint(0,self.dimensao-1),randint(0,self.dimensao-1)),tempo)
                        self.alocar_pacotes(pacote) 


    def Total_Throughput(self, qtd_pacotes):
        tempo =qtd_pacotes
        total_rodada = 0
        for i in range(tempo): 
            if i%2==0:
                for j in range(self.dimensao):
                    for k in range(self.dimensao):
                        self.matriz_roteadores[j][k].enviar_pacote_RR()
            else:
                for j in range(self.dimensao):
                    for k in range(self.dimensao):
                        self.matriz_roteadores[j][k].ajustar_pacotes()
        self.ajusta_pacotes_recebidos()
        total_rodada = self.total_pacotes_recebidos[-1] - self.total_pacotes_recebidos[-2]
        if tempo > self.dimensao*self.dimensao:
            return total_rodada/(self.dimensao*self.dimensao)
        else:
            return total_rodada/(tempo)

    def Node_Throughput(self,qtd_pacotes):
        #Node throughput =(total arrived packets)/(Rows × Column)
        total_rodada = self.Total_Throughput(qtd_pacotes)
        return total_rodada/(self.dimensao*self.dimensao)


    def Packet_Latency(self,i):
        total_rodada = 0
        for i in range(self.dimensao*4): 
            if i%2==0:
                for j in range(self.dimensao):
                    for k in range(self.dimensao):
                        self.matriz_roteadores[j][k].enviar_pacote_RR()
            else:
                for j in range(self.dimensao):
                    for k in range(self.dimensao):
                        self.matriz_roteadores[j][k].ajustar_pacotes()
        
        for j in range(self.dimensao):
            for k in range(self.dimensao):
                while len(self.matriz_roteadores[j][k].buffers["Pacotes_entregues"]) > 0:
                    self.chegos +=1
                    pacote = self.matriz_roteadores[j][k].buffers["Pacotes_entregues"].pop(0)
                    tempo_criacao = pacote.tempo_criação
                    tempo_chegada = pacote.tempo_chegada
                    total_rodada += tempo_chegada - tempo_criacao
        if self.chegos== 0 :
            return 0
        else:
            return total_rodada/self.chegos

    def Extra_Delay(self,i):
        total_rodada = 0
        for i in range(self.dimensao*4): 
            if i%2==0:
                for j in range(self.dimensao):
                    for k in range(self.dimensao):
                        self.matriz_roteadores[j][k].enviar_pacote_RR()
            else:
                for j in range(self.dimensao):
                    for k in range(self.dimensao):
                        self.matriz_roteadores[j][k].ajustar_pacotes()
        
        for j in range(self.dimensao):
            for k in range(self.dimensao):
                while len(self.matriz_roteadores[j][k].buffers["Pacotes_entregues"]) > 0:
                    pacote = self.matriz_roteadores[j][k].buffers["Pacotes_entregues"].pop(0)
                    tempo_criacao = pacote.tempo_criação
                    tempo_chegada = pacote.tempo_chegada
                    origem = pacote.posicao_inicial
                    destino = pacote.posicao_destino
                    diferenca1 = abs(origem[0] - destino[0])
                    diferenca2 = abs(origem[1] - destino[1])
                    soma_diferencas = diferenca1 + diferenca2
                    total_rodada += (tempo_chegada - tempo_criacao) - (soma_diferencas*5)
        return total_rodada

    def Efficiency(self,qtd_pacotes):

        for i in range(120): 
            if i%2==0:
                for j in range(self.dimensao):
                    for k in range(self.dimensao):
                        self.matriz_roteadores[j][k].enviar_pacote_RR()
            else:
                for j in range(self.dimensao):
                    for k in range(self.dimensao):
                        self.matriz_roteadores[j][k].ajustar_pacotes()
        self.ajusta_pacotes_chegos()
        #self.ajusta_pacote_total()
        print(self.total_pacotes_chegos[-1],self.total_pacotes)
        return  (100*((self.total_pacotes_chegos[-1] / self.total_pacotes)))
        

    def Packet_Lost(self,i):
        for i in range(8): 
            if i%2==0:
                for j in range(self.dimensao):
                    for k in range(self.dimensao):
                        self.matriz_roteadores[j][k].enviar_pacote_RR()
            else:
                for j in range(self.dimensao):
                    for k in range(self.dimensao):
                        self.matriz_roteadores[j][k].ajustar_pacotes()
        self.ajusta_pacotes_perdido()
        return 100*self.total_pacotes_perdidos[-1] / self.total_pacotes

    def ajusta_pacotes_perdido(self):
        soma_rodada = 0
        for j in range(self.dimensao):
            for k in range(self.dimensao):
                soma_rodada += self.matriz_roteadores[j][k].total_pacotes_perdidos
        self.total_pacotes_perdidos.append(soma_rodada) 


    def ajusta_pacote_total(self):
        soma_rodada = 0
        for j in range(self.dimensao):
            for k in range(self.dimensao):
                soma_rodada += self.matriz_roteadores[j][k].total_pacotes_criados
        self.total_pacotes = soma_rodada

    def ajusta_pacotes_recebidos(self):
        soma_rodada = 0
        for j in range(self.dimensao):
            for k in range(self.dimensao):
                soma_rodada += self.matriz_roteadores[j][k].total_pacotes_recebidos
        self.total_pacotes_recebidos.append(soma_rodada)

    def ajusta_pacotes_chegos(self):
            soma_rodada = 0
            for j in range(self.dimensao):
                for k in range(self.dimensao):
                    soma_rodada += self.matriz_roteadores[j][k].total_pacotes_chegos
            self.total_pacotes_chegos.append(soma_rodada)

    

    ...

class Roteador:

    max_packets_buffer = 8 # variável global para definir a quantidade máxima de itens

    def __init__(self, posicao, noc):
        self.posicao = posicao
        self.noc = noc  # armazenando a instância de Noc
        self.buffers = {
            "Norte": [],
            "Sul": [],
            "Leste": [],
            "Oeste": [],
            "Processador": [],
            "Pacotes_entregues": [], #pacotes que chegaram ao seu destino final
            "Pacotes_recebidos": [],
        }
        self.buffer_atual = "Oeste"
        self.tempo = 0
        self.total_pacotes_criados = 0
        self.total_pacotes_perdidos = 0
        self.total_pacotes_chegos = 0 #chegaram ao seu destino final
        self.total_pacotes_recebidos = 0 # quantos chegaram no roteador 

    def enviar_pacote_RR(self):
        buffer_pacote_para_enviar = self.selecionar_buffer() # seleciona qual buffer do roteador eu vou pegar o pacote
        
        self.tempo = self.tempo + 1 

        if self.buffers[buffer_pacote_para_enviar] == []:
            return
        else:
            if buffer_pacote_para_enviar == "Processador":
                self.total_pacotes_criados += 1
            pacote = self.buffers[buffer_pacote_para_enviar].pop(0) # seleciona o primeiro pacote do buffer selecionado
        
        roteador_destino, buffer_destino = self.seleciona_roteador_destino(pacote) #seleciona qual roteador de destino do pacote    

        if roteador_destino == self: 
            self.buffers["Pacotes_entregues"].append(pacote)
            pacote.tempo_chegada = self.tempo
            self.total_pacotes_chegos += 1

        else:
            roteador_destino.buffers["Pacotes_recebidos"].append((pacote,buffer_destino))
        
    def ajustar_pacotes(self):
        tamanho = len(self.buffers["Pacotes_recebidos"])
        for i in range(tamanho):
            pacote , endereço = self.buffers["Pacotes_recebidos"].pop(0)
            qtd_dados = self.contar_dados(endereço)
            if pacote.peso <= (self.max_packets_buffer - qtd_dados):
                self.buffers[endereço].append(pacote)
                self.total_pacotes_recebidos += 1
            else:
                self.total_pacotes_perdidos += 1

    def contar_dados(self,endereço):
        dados = 0
        if self.buffers[endereço] == []:
            return 0 
        else :
            for pacote in self.buffers[endereço]:
                dados = dados + pacote.peso
            return dados

    def selecionar_buffer(self):
        # pelo algoritmo round robin, inicialmente
        if self.buffer_atual == "Norte":
            self.buffer_atual = "Leste"
            return "Leste"
            
        if self.buffer_atual == "Leste":
            self.buffer_atual = "Sul"
            return "Sul"
        
        if self.buffer_atual == "Sul":
            self.buffer_atual = "Oeste"
            return "Oeste"
            
        if self.buffer_atual == "Oeste":
            self.buffer_atual = "Processador"
            return "Processador"
            
        if self.buffer_atual == "Processador":
            self.buffer_atual = "Norte"
            return "Norte"
             
    def seleciona_roteador_destino(self,pacote):
        x_destino,y_destino = pacote.posicao_destino #posicao destino
        x_atual , y_atual = self.posicao  #posicao atual do roteador
        delta_x = x_destino-x_atual #deslocamento em x
        delta_y = y_destino-y_atual # deslocamento em y
        if delta_x == 0 and delta_y == 0:
            return self ,  "Nada"
        if delta_y > 0:
            return self.noc.matriz_roteadores[x_atual][y_atual+1] , "Oeste" #.buffers["Oeste"]
        if delta_y < 0:
            return self.noc.matriz_roteadores[x_atual][y_atual-1] , "Leste"#.buffers["Leste"]
        if delta_x > 0:
            return self.noc.matriz_roteadores[x_atual+1][y_atual] , "Norte"#.buffers["Norte"]
        if delta_x < 0:
            return self.noc.matriz_roteadores[x_atual-1][y_atual] , "Sul"#.buffers["Sul"]

class Pacote():
    contador_global = 1

    def __init__(self,  posicao_inicial, posicao_destino, tempo_criacao , peso = 1):
        self.id = Pacote.contador_global
        Pacote.contador_global += 1
        self.peso = peso
        self.tempo_criação = tempo_criacao
        self.tempo_chegada = 0
        self.posicao_inicial = posicao_inicial
        self.posicao_destino = posicao_destino
    
    def __repr__(self):
        return f'Pacote {self.id}'



qtd_linhas = 2
qtd_colunas = 2
tempo_simulacao = 100

noc1 = Noc(4)
instante_tempos1,total_thru1 = noc1.rodar_simulacao(tempo_simulacao)

# Grau do polinômio
degree =5

# Coeficientes da regressão polinomial
coefficients = np.polyfit(instante_tempos1, total_thru1, degree)

# Cria o polinômio a partir dos coeficientes
polynomial = np.poly1d(coefficients)

# Valores de x para a linha de regressão (usando uma faixa mais suave)
x_fit = np.linspace(min(instante_tempos1), max(instante_tempos1), 100)

# Valores de y correspondentes aos x_fit
y_fit = polynomial(x_fit)

# Plotar a linha de regressão
plt.plot(x_fit, y_fit, color='blue', label=' 4x4')

noc2 = Noc(8)
instante_tempos2,total_thru2 = noc2.rodar_simulacao(tempo_simulacao)

# Grau do polinômio
degree = 5

# Coeficientes da regressão polinomial
coefficients = np.polyfit(instante_tempos2, total_thru2, degree)

# Cria o polinômio a partir dos coeficientes
polynomial = np.poly1d(coefficients)

# Valores de x para a linha de regressão (usando uma faixa mais suave)
x_fit = np.linspace(min(instante_tempos2), max(instante_tempos2), 100)

# Valores de y correspondentes aos x_fit
y_fit = polynomial(x_fit)

# Plotar a linha de regressão
plt.plot(x_fit, y_fit, color='red', label=' 8x8')

# Adicionando rótulos e título
plt.xlabel('Tempo')
plt.ylabel('Eficiência ')
plt.title('Gráfico da Eficiência ao Longo do Tempo')

plt.legend()
# Exibindo o gráfico
plt.show()


'''
                 ---------------------       ---------------------       ---------------------
                ||p|     |n|          |     ||p|      |n|         |     ||p|     |n|          |
                |                     |     |                     |     |                     |
                ||o|               |l||     ||o|               |l||     ||o|               |l||
                |                     |     |                     |     |                     |
                |         |s|         |     |         |s|         |     |        |n|          |
                ---------------------       ---------------------       ---------------------


                 ---------------------       ---------------------       ---------------------
                ||p|      |n|         |     ||p|      |n|         |     ||p|     |n|          |
                |                     |     |                     |     |                     |
                ||o|               |l||     ||o|               |l||     ||o|               |l||
                |                     |     |                     |     |                     |
                |         |s|         |     |         |s|         |     |         |s|         |
                ---------------------       ---------------------       ---------------------


                 ---------------------       ---------------------       ---------------------
                ||p|     |n|          |     ||p|      |n|         |     ||p|      |n|         |
                |                     |     |                     |     |                     |
                ||o|               |l||     ||o|               |l||     ||o|               |l||
                |                     |     |                     |     |                     |
                |        |s|          |     |         |s|         |     |         |s|         |
                ---------------------       ---------------------       ---------------------
                
'''

