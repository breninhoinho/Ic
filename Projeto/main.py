#Importação das bibliotecas
import tkinter as tk
from tkinter import ttk
import numpy as np
from Algoritmos_Mapeamento.Random import *
from Algoritmos_Mapeamento.Engineered_Mapping import *
from Algoritmos_Mapeamento.Genetic_Algorithm import *


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
adj_matriz = [
  [0, 8, 5, 7, 6, 4, 8, 3, 9, 2, 1, 8, 9, 6, 7, 10],
  [9, 0, 3, 2, 5, 7, 6, 10, 1, 9, 4, 5, 8, 9, 1, 2],
  [7, 2, 0, 9, 2, 10, 4, 5, 6, 8, 7, 3, 9, 7, 6, 5],
  [4, 8, 6, 0, 3, 1, 5, 7, 2, 6, 10, 4, 7, 10, 9, 8],
  [10, 5, 8, 1, 0, 9, 7, 6, 3, 1, 5, 2, 8, 4, 6, 10],
  [2, 7, 1, 9, 6, 0, 8, 5, 10, 3, 7, 6, 4, 1, 9, 7],
  [8, 6, 10, 5, 2, 9, 0, 1, 7, 4, 6, 10, 9, 5, 7, 1],
  [5, 10, 4, 2, 9, 8, 1, 0, 6, 10, 3, 9, 5, 1, 8, 6],
  [6, 1, 7, 8, 10, 7, 6, 9, 0, 5, 9, 2, 10, 3, 5, 2],
  [3, 9, 10, 7, 1, 4, 10, 6, 5, 0, 8, 1, 6, 10, 2, 7],
  [9, 4, 7, 10, 5, 7, 6, 3, 9, 8, 0, 3, 2, 9, 10, 4],
  [8, 5, 3, 4, 2, 6, 10, 9, 2, 1, 3, 0, 7, 4, 1, 9],
  [5, 8, 9, 7, 8, 4, 9, 5, 10, 6, 2, 7, 0, 5, 6, 8],
  [10, 9, 7, 10, 6, 1, 5, 1, 3, 10, 9, 4, 5, 0, 2, 9],
  [7, 1, 6, 9, 10, 9, 7, 8, 5, 2, 10, 1, 6, 2, 0, 3],
  [1, 2, 5, 8, 10, 7, 1, 6, 2, 7, 4, 9, 8, 9, 3, 0]
]

adj_matriz = [[0, 1, 2, 3, 4, 5], [0, 0, 6, 7, 8, 9], [0, 0, 0, 10, 11, 12], [0, 0, 0, 0, 13, 14], [0, 0, 0, 0, 0, 15], [0, 0, 0, 0, 0, 0]]

dicionario_posicoes = Random(cores_noc,dimensao[0]*dimensao[0])

dicionario_posicoes = Engineered_Mapping(cores_noc,dimensao[0]*dimensao[0],"clustered","horizontally","snake")


cores_noc = Run_Genetic_Algorithm(10000, 100, 0.5, adj_matriz, dimensao[0])
print(cores_noc)
# for linha in cores_noc:
#     print(linha)

