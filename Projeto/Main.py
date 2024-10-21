import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from Algoritmos_Mapeamento.Random import *
from Algoritmos_Mapeamento.Genetic_Algorithm import *
from Algoritmos_Mapeamento.Andean_condor import *
from Noc import *
import json
from time import sleep



class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matriz de Adjacência para Grafo")

        # Variáveis globais do programa
        self.selecao = None
        self.roteamento = None
        self.dimensao = None
        self.matrix = []
        

        # Configurações da janela
        self.setup_ui()

    def setup_ui(self):
        # Definir o tamanho inicial da janela (largura x altura)
        largura = 400
        altura = 500
        self.root.geometry(f"{largura}x{altura}")

        # Rótulo para o título "Métricas"
        rotulo_metricas = tk.Label(self.root, text="Métricas", font=("Arial", 16, "bold"), pady=10, padx=40)
        rotulo_metricas.grid(row=0, column=0, columnspan=2)

        # Lista de itens para a lista
        lista_metricas = ["Energia", "Latência", "Tolerância a falha"]

        # Variáveis para armazenar os estados das checkboxes
        self.variaveis_checkbox = [tk.IntVar() for _ in range(len(lista_metricas))]

        # Criar checkboxes para cada item na lista
        for i, item in enumerate(lista_metricas):
            checkbox = tk.Checkbutton(self.root, text=item, variable=self.variaveis_checkbox[i], font=("Arial", 16))
            checkbox.grid(row=i + 1, column=0, sticky=tk.W, padx=5, pady=5)

        # Rótulo para o título "Grid"
        rotulo_grid = tk.Label(self.root, text="Grid (nxn)", font=("Arial", 16, "bold"), pady=10, padx=40)
        rotulo_grid.grid(row=len(lista_metricas) + 2, column=0, columnspan=2)

        # Entrada para o novo valor
        self.entrada_novo_valor = tk.Entry(self.root, font=("Arial", 12))
        self.entrada_novo_valor.grid(row=len(lista_metricas) + 3, column=0, pady=5, padx=5, sticky=tk.W)

        # Rótulo para o título "Roteamento"
        rotulo_roteamento = tk.Label(self.root, text="Roteamento", font=("Arial", 16, "bold"), pady=10, padx=40)
        rotulo_roteamento.grid(row=len(lista_metricas) + 4, column=0, columnspan=2)

        # ComboBox para capturar o tipo de roteamento desejado
        opcoes = ["XY", "XYX", "Negative First"]
        self.valor_selecionado = tk.StringVar()
        self.combo = ttk.Combobox(self.root, values=opcoes, textvariable=self.valor_selecionado, state="readonly")
        self.combo.grid(row=len(lista_metricas) + 5, column=0, padx=10, pady=10)

        # Botão para atualizar o valor
        botao_atualizar_valor = tk.Button(self.root, text="Calcular", command=self.atualizar_valores, font=("Arial", 14, "italic"), pady=10)
        botao_atualizar_valor.grid(row=len(lista_metricas) + 6, column=0, sticky=tk.W, padx=5, pady=5)

    def atualizar_valores(self):
        # Seleção valores das Métricas
        self.selecao = [var.get() for var in self.variaveis_checkbox]

        # Seleção do Roteamento
        self.roteamento = self.combo.get()

        # Seleção da dimensão do SoC
        dim = self.entrada_novo_valor.get()
        try:
            self.dimensao = (int(dim), int(dim))
            self.root.destroy()
            self.get_matrix_size()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico.")

    def get_matrix_size(self):
        self.matrix_window = tk.Tk()
        self.matrix_window.title("Entrada da Matriz de Adjacência")
        
        self.label = tk.Label(self.matrix_window, text="Insira a dimensão da matriz de adjacência:")
        self.label.pack()
        
        self.entry = tk.Entry(self.matrix_window)
        self.entry.pack()
        
        self.button = tk.Button(self.matrix_window, text="OK", command=self.get_matrix_entries)
        self.button.pack()

    def get_matrix_entries(self):
        try:
            self.size = int(self.entry.get())
            if self.size <= 0:
                raise ValueError("Dimensão deve ser maior que 0.")
            
            self.matrix_window.destroy()
            self.matrix_input_window = tk.Tk()
            self.matrix_input_window.title("Entrada da Matriz de Adjacência")
            self.matrix = []
            self.matrix_entry_widgets = []

            # Configurar as linhas e colunas para se expandirem
            for i in range(self.size):
                self.matrix_input_window.rowconfigure(i, weight=1)
                self.matrix_input_window.columnconfigure(i, weight=1)

                row_entries = []
                for j in range(self.size):
                    entry = tk.Entry(self.matrix_input_window, width=3)
                    entry.grid(row=i, column=j, padx=20, pady=20, sticky="nsew")
                    row_entries.append(entry)
                self.matrix_entry_widgets.append(row_entries)

            # Configurar o botão de submit
            submit_button = tk.Button(self.matrix_input_window, text="Submit", command=self.submit_matrix)
            submit_button.grid(row=self.size, columnspan=self.size)

            # Configurar a linha e coluna do botão de submit para expandirem
            self.matrix_input_window.rowconfigure(self.size, weight=1)
            self.matrix_input_window.columnconfigure(0, weight=1)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))


    def submit_matrix(self):
        try:
            self.matrix = []
            for row_entries in self.matrix_entry_widgets:
                row = []
                for entry in row_entries:
                    value = int(entry.get())
                    row.append(value)
                self.matrix.append(row)

            self.matrix_input_window.destroy()
            self.create_graph()
            #self.calculate_best_solution() proximo passo
        except ValueError as e:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

    def create_graph(self):
        G = nx.Graph()
        
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] != 0:
                    G.add_edge(i, j, weight=self.matrix[i][j])
        
        pos = nx.spring_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.savefig("grafo.png", format="PNG")
        plt.show()
        
        self.verificação_da_corretude()


    def verificação_da_corretude(self):
        response = messagebox.askyesno("Confirmação", "O grafo está correto?")
        if response:
            # Prosseguir com o cálculo ou a próxima etapa
            self.mapeamentos()
        else:
            # Reabrir a janela para que o usuário insira a matriz novamente
            self.perguntar_novamente_matrix()


    def perguntar_novamente_matrix(self):
        # Reabre a janela de entrada da matriz sem precisar de self.entry
        self.matrix_input_window = tk.Tk()
        self.matrix_input_window.title("Entrada da Matriz de Adjacência")
        self.matrix = []
        self.matrix_entry_widgets = []

        # Configurar as linhas e colunas para se expandirem
        for i in range(self.size):
            self.matrix_input_window.rowconfigure(i, weight=1)
            self.matrix_input_window.columnconfigure(i, weight=1)

            row_entries = []
            for j in range(self.size):
                entry = tk.Entry(self.matrix_input_window, width=3)
                entry.grid(row=i, column=j, padx=20, pady=20, sticky="nsew")
                row_entries.append(entry)
            self.matrix_entry_widgets.append(row_entries)

        # Configurar o botão de submit
        submit_button = tk.Button(self.matrix_input_window, text="Submit", command=self.submit_matrix)
        submit_button.grid(row=self.size, columnspan=self.size)

        # Configurar a linha e coluna do botão de submit para expandirem
        self.matrix_input_window.rowconfigure(self.size, weight=1)
        self.matrix_input_window.columnconfigure(0, weight=1)

    def mapeamentos(self):
        
        cores_noc = Run_Genetic_Algorithm(10000, 100, 0.5, self.matrix, self.dimensao[0])
        print(cores_noc)
        print(self.calcular_energia(cores_noc))
        
        print(self.dimensao[0] , self.roteamento, self.matrix, cores_noc)
        noc1 = Noc(self.dimensao[0] , self.roteamento, self.matrix, cores_noc)
        latencia = noc1.latencia()
        print(latencia)
        for i in range(self.dimensao[0]):
           for j in range(self.dimensao[0]):
               print(noc1.matriz_roteadores[i][j].buffers)
        

        data = {
            "matriz_adj": self.matrix,
            "melhor_mapeamento": cores_noc,
            "n": self.dimensao,
            "roteamento":self.roteamento
        }
        
        # Salvar em um arquivo JSON
        with open('config.json', 'w') as f:
            json.dump(data, f)

    def calcular_energia(self, mapeamento):
        n = len(self.matrix)  # Número de tarefas
        m = len(mapeamento)  # Dimensão da NoC
        valor_final = 0

        for i in range(n):  # Percorre todas as tarefas
            for j in range(i+1, n):  # Garante que a matriz seja percorrida uma única vez (i, j) != (j, i)
                bandwidth = self.matrix[i][j]
                if bandwidth > 0 :  # Se há comunicação entre as tarefas i e j
                    # Encontra a posição de i no mapeamento
                    ix, iy = [(k, l) for k in range(m) for l in range(m) if mapeamento[k][l] == i][0]
                    # Encontra a posição de j no mapeamento
                    jx, jy = [(k, l) for k in range(m) for l in range(m) if mapeamento[k][l] == j][0]
                    # Calcula a distância Manhattan
                    man_dist = abs(ix - jx) + abs(iy - jy)
                    # Acumula o valor da energia total
                    valor_final += bandwidth * man_dist

        return valor_final
    
    def calcular_tolerancia_falha(matriz):
        # Direções para as células adjacentes (cima, baixo, esquerda, direita)
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        tolerancia = 0

        # Itera sobre cada célula da matriz
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                # Verifica se a célula contém uma tarefa (número diferente de 0)
                if matriz[i][j] != 0:
                    # Verifica se há células adjacentes vazias que têm uma tarefa adjacente
                    for dx, dy in direcoes:
                        x, y = i + dx, j + dy
                        # Verifica se a posição está dentro dos limites da matriz
                        if 0 <= x < len(matriz) and 0 <= y < len(matriz[0]):
                            # Se a célula adjacente estiver vazia (0)
                            if matriz[x][y] != 0:
                                tolerancia += 1
                                
        return tolerancia
    

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
    sleep(1)
    from Tela import *

