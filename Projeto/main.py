#Importação das bibliotecas
import tkinter as tk
from tkinter import ttk
import numpy as np
from Algoritmos_Mapeamento.Random import *
from Algoritmos_Mapeamento.Engineered_Mapping import *


# Variaveis globais do programa
selecao = None
roteamento = None
dimensao = None

def atualizar_valores(): 
    #Variaveis globais
    global selecao
    global roteamento
    global dimensao

    # Seleção valores das Métricas
    selecao = [var.get() for var in variaveis_checkbox]

    #Seleção do Roteamento
    roteamento = combo.get()

    #Seleção da dimensão do Soc
    dim = entrada_novo_valor.get()
    try:
        dimensao = (int(dim), int(dim))
        janela.destroy()
    except ValueError:
        print("Por favor, insira um valor numérico.")
    

# Criar uma instância da classe Tk, que representa a janela principal
janela = tk.Tk()

# Definir o tamanho inicial da janela (largura x altura)
largura = 400
altura =500
janela.geometry(f"{largura}x{altura}")

# Rótulo para o título "Métricas"
rotulo_metricas = tk.Label(janela, text="Métricas", font=("Arial", 16, "bold"), pady=10, padx=40)
rotulo_metricas.grid(row=0, column=0, columnspan=2)  # Adicionado grid ao rótulo

# Lista de itens para a lista
lista_metricas = ["Energia", "Latência", "Tolerância a falha"]

# Variáveis para armazenar os estados das checkboxes
variaveis_checkbox = [tk.IntVar() for _ in range(len(lista_metricas))]

# Criar checkboxes para cada item na lista
for i, item in enumerate(lista_metricas):
    checkbox = tk.Checkbutton(janela, text=item, variable=variaveis_checkbox[i], font=("Arial", 16))
    checkbox.grid(row=i + 1, column=0, sticky=tk.W, padx=5, pady=5)  # Adicionado grid às checkboxes

# Rótulo para o título "Grid"
rotulo_metricas = tk.Label(janela, text="Grid (nxn)", font=("Arial", 16, "bold"), pady=10, padx=40)
rotulo_metricas.grid(row=len(lista_metricas) + 2, column=0, columnspan=2)  # Adicionado grid ao rótulo

# Entrada para o novo valor
entrada_novo_valor = tk.Entry(janela, font=("Arial", 12))
entrada_novo_valor.grid(row=len(lista_metricas) + 3, column=0, pady=5, padx=5, sticky=tk.W)

# Rótulo para o título "Roteamento"
rotulo_metricas = tk.Label(janela, text="Roteamento", font=("Arial", 16, "bold"), pady=10, padx=40)
rotulo_metricas.grid(row=len(lista_metricas) + 4, column=0, columnspan=2)

# ComboBox para capturar o tipo de roteamento desejado
opcoes = ["XY", "XYX", "Negative First"]
valor_selecionado = tk.StringVar()
combo = ttk.Combobox(janela, values=opcoes, textvariable=valor_selecionado, state="readonly")
combo.grid(row=len(lista_metricas) + 5, column=0, padx=10, pady=10)

# Botão para atualizar o valor
botao_atualizar_valor = tk.Button(janela, text="Calcular", command=atualizar_valores, font=("Arial", 14, "italic"), pady=10)
botao_atualizar_valor.grid(row=len(lista_metricas) + 6, column=0, sticky=tk.W, padx=5, pady=5)  # Adicionado grid ao botão de atualização

# Loop principal da interface gráfica (GUI)
janela.mainloop()

############################################################################################################################################################

#gerando matriz vazia do tamanho da dimensao do noc passada pelo usuario
cores_noc =  [['' for _ in range(dimensao[1])] for _ in range(dimensao[0])]

# gerar grafo para teste
tam = 13
adj_matriz = np.zeros((tam,tam), dtype=int)
edges = [(0, 1, 5), (0, 3 ,4), (1, 2 ,3), (1, 4 ,2 ), (2, 3, 1), (3, 4, 8)]

# Atualizando a matriz de adjacência com as arestas
for edge in edges:
    adj_matriz[edge[0]][edge[1]] = edge[2]
    adj_matriz[edge[1]][edge[0]] = edge[2]


#dicionario_posicoes = Random(cores_noc,tam)
dicionario_posicoes = Engineered_Mapping(cores_noc,tam,"distributed","horizontally","snake")

for linha in cores_noc:
    print(linha)
    
