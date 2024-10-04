import tkinter as tk


# Dicionário global para armazenar pacotes
pacotes = {}

# Função para mover o pacote em uma direção (N, S, L, O) após chegar ao centro maior
def mover_pacote_fase2(x_inicial, y_inicial, x_final, y_final, passo, pacote_oval, pacote_texto):
    x = x_inicial
    y = y_inicial
    dx = (x_final - x_inicial) / passo
    dy = (y_final - y_inicial) / passo

    def animar():
        nonlocal x, y
        if abs(x - x_final) > abs(dx) or abs(y - y_final) > abs(dy):
            canvas.move(pacote_oval, dx, dy)
            canvas.move(pacote_texto, dx, dy)
            x += dx
            y += dy
            janela.after(20, animar)

    animar()

# Função para mover o pacote do quadrado menor para o quadrado maior
def mover_pacote_fase1(x_inicial, y_inicial, x_final, y_final, pacote_oval, pacote_texto, id_pacote, direcao):
    x = x_inicial
    y = y_inicial
    dx = (x_final - x_inicial) / 50
    dy = (y_final - y_inicial) / 50

    def animar():
        nonlocal x, y
        if abs(x - x_final) > abs(dx) or abs(y - y_final) > abs(dy):
            canvas.move(pacote_oval, dx, dy)
            canvas.move(pacote_texto, dx, dy)
            x += dx
            y += dy
            janela.after(20, animar)
        else:
            # Quando o pacote chegar ao centro do quadrado maior, iniciar a segunda fase de movimento
            mover_pacote_para_direcao(x_final, y_final, pacote_oval, pacote_texto, id_pacote, direcao)

    animar()

# Função para definir a próxima célula com base na direção (N, S, L, O)
def mover_pacote_para_direcao(x_inicial, y_inicial, pacote_oval, pacote_texto, id_pacote, direcao):
    if direcao == "N":
        x_final, y_final = x_inicial, y_inicial - 141  # Norte
    elif direcao == "S":
        x_final, y_final = x_inicial, y_inicial + 141  # Sul
    elif direcao == "L":
        x_final, y_final = x_inicial + 141, y_inicial  # Leste
    elif direcao == "O":
        x_final, y_final = x_inicial - 141, y_inicial  # Oeste
    elif direcao == "Processador":
        posicao_menor = encontrar_posicao_menor(id_pacote)
        if posicao_menor:
            x_final, y_final = posicao_menor  # Atribui a posição do quadrado menor

    mover_pacote_fase2(x_inicial, y_inicial, x_final, y_final, 50, pacote_oval, pacote_texto)

def encontrar_posicao_menor(id_pacote):
    i, j = divmod(id_pacote - 1, n)  # Assumindo que os pacotes estão indexados a partir de 1
    return centros_menores[i][j]  # Ajuste conforme a sua estrutura de dados

# Função para desenhar a matriz de quadrados
def desenhar_matriz(n):
    tamanho_quadrado = 70
    espaco = 70
    tamanho_quadrado_pequeno = 40
    tamanho_retirangulo = 15
    tamanho_total = n * (tamanho_quadrado + espaco) - espaco
    offset_x = (largura_canvas - tamanho_total) // 2
    offset_y = (altura_canvas - tamanho_total) // 2

    centros_maiores = [[None for _ in range(n)] for _ in range(n)]
    centros_menores = [[None for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            x1 = j * (tamanho_quadrado + espaco) + offset_x
            y1 = i * (tamanho_quadrado + espaco) + offset_y
            x2 = x1 + tamanho_quadrado
            y2 = y1 + tamanho_quadrado

            centro_x_maior = (x1 + x2) // 2
            centro_y_maior = (y1 + y2) // 2
            centros_maiores[i][j] = (centro_x_maior, centro_y_maior)

            canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue")

            # Norte, Sul, Leste, Oeste
            canvas.create_rectangle(centro_x_maior - tamanho_retirangulo // 2, y1, centro_x_maior + tamanho_retirangulo // 2, y1 + tamanho_retirangulo, fill="gray")
            canvas.create_text(centro_x_maior, y1 + tamanho_retirangulo // 2, text="N", fill="black", font=("Arial", 10, "bold"))
            canvas.create_rectangle(centro_x_maior - tamanho_retirangulo // 2, y2 - tamanho_retirangulo, centro_x_maior + tamanho_retirangulo // 2, y2, fill="gray")
            canvas.create_text(centro_x_maior, y2 - tamanho_retirangulo // 2, text="S", fill="black", font=("Arial", 10, "bold"))
            canvas.create_rectangle(x2 - tamanho_retirangulo, centro_y_maior - tamanho_retirangulo // 2, x2, centro_y_maior + tamanho_retirangulo // 2, fill="gray")
            canvas.create_text(x2 - tamanho_retirangulo // 2, centro_y_maior, text="L", fill="black", font=("Arial", 10, "bold"))
            canvas.create_rectangle(x1, centro_y_maior - tamanho_retirangulo // 2, x1 + tamanho_retirangulo, centro_y_maior + tamanho_retirangulo // 2, fill="gray")
            canvas.create_text(x1 + tamanho_retirangulo // 2, centro_y_maior, text="O", fill="black", font=("Arial", 10, "bold"))

            if j < n - 1:
                x1_link = x2
                y1_link = (y1 + y2) // 2
                x2_link = x2 + espaco
                y2_link = y1_link
                canvas.create_line(x1_link, y1_link, x2_link, y2_link, width=2)

            if i < n - 1:
                x1_link = (x1 + x2) // 2
                y1_link = y2
                x2_link = x1_link
                y2_link = y2 + espaco
                canvas.create_line(x1_link, y1_link, x2_link, y2_link, width=2)

            x1_diag = x1
            y1_diag = y1
            x2_diag = x1_diag - espaco // 2
            y2_diag = y1_diag - espaco // 2
            canvas.create_line(x1_diag, y1_diag, x2_diag, y2_diag, width=2)

            centro_x_menor = x2_diag
            centro_y_menor = y2_diag
            centros_menores[i][j] = (centro_x_menor, centro_y_menor)

            x1_pequeno = x2_diag - tamanho_quadrado_pequeno // 2
            y1_pequeno = y2_diag - tamanho_quadrado_pequeno // 2
            x2_pequeno = x1_pequeno + tamanho_quadrado_pequeno
            y2_pequeno = y1_pequeno + tamanho_quadrado_pequeno
            canvas.create_rectangle(x1_pequeno, y1_pequeno, x2_pequeno, y2_pequeno, fill="orange")

    # Adicionando texto no canto direito
    canvas.create_text(largura_canvas - 100, altura_canvas -600, text="Roteamento: xy", fill="black", font=("Arial", 12, "bold"), anchor="e")
    canvas.create_rectangle(largura_canvas-180, altura_canvas-560, largura_canvas + 40-180, altura_canvas + 40-560, fill="orange")
    canvas.create_text(largura_canvas + 20-180, altura_canvas + 20-560, text="CPU", fill="black", font=("Arial", 12, "bold"))
    canvas.create_text(largura_canvas + 20-180, altura_canvas + 20-500, text="Melhor Mapeamento: ", fill="black", font=("Arial", 12, "bold"))
    tamanho_matriz_mapeamento = (300-(10*3)) / 3
    for i in range(3):  # Exemplo de 3 linhas
        for j in range(3):  # Exemplo de 3 colunas
            x1_mapeamento = (largura_canvas -300) + j * (tamanho_matriz_mapeamento + 10)
            y1_mapeamento = (altura_canvas -450) + i * (tamanho_matriz_mapeamento + 10)
            canvas.create_rectangle(x1_mapeamento, y1_mapeamento, x1_mapeamento + tamanho_matriz_mapeamento, y1_mapeamento + tamanho_matriz_mapeamento, fill="lightgreen")
            canvas.create_text(x1_mapeamento + tamanho_matriz_mapeamento // 2, y1_mapeamento + tamanho_matriz_mapeamento // 2, text=f"{melhor_mapeamento[i][j]}", fill="black", font=("Arial", 10, "bold"))

    # Atualizando a margem superior para o próximo elemento
    return centros_maiores, centros_menores


# Função para criar pacotes e alocá-los com base no mapeamento e matriz de adjacência
def criar_pacotes_e_alocar():
    id_pacote = 1  # Inicia o ID dos pacotes a partir de 1
    for i in range(len(matrix_adj)):
        for j in range(len(matrix_adj[i])):
            if j > i and matrix_adj[i][j] > 0:  # Verifica se há comunicação entre i e j
                origem = encontrar_posicao(i + 1)  # +1 porque as tarefas no mapeamento começam em 1
                destino = encontrar_posicao(j + 1)
                
                if origem and destino:
                    centro_menor_origem = centros_menores[origem[0]][origem[1]]
                    
                    # Criar pacote oval e texto no centro menor da origem
                    pacote_oval = canvas.create_oval(
                        centro_menor_origem[0] - 10, centro_menor_origem[1] - 10, 
                        centro_menor_origem[0] + 10, centro_menor_origem[1] + 10, 
                        fill="red"
                    )
                    pacote_texto = canvas.create_text(
                        centro_menor_origem[0], centro_menor_origem[1], 
                        text=str(id_pacote), fill="white", font=("Arial", 12, "bold")
                    )
                    qtd_movimentos = 0
                    
                    # Armazena o pacote no dicionário usando o ID como chave
                    pacotes[id_pacote] = (pacote_oval, pacote_texto,qtd_movimentos)
                    
                    # Incrementar o ID para o próximo pacote
                    id_pacote += 1


# Função para encontrar a posição de uma tarefa no mapeamento
def encontrar_posicao(tarefa):
    for i in range(len(melhor_mapeamento)):
        for j in range(len(melhor_mapeamento[i])):
            if melhor_mapeamento[i][j] == tarefa:
                return (i, j)
    return None


# Função para animar um pacote com base no dicionário de controle
def animar_pacote():
    global direcoes
    # Passa por todos os pacotes que possuem uma direção definida no dicionário de direções
    for id_pacote, direcao in direcoes.items():
        if id_pacote in pacotes:  # Verifica se o pacote com o ID correspondente existe
            pacote_oval, pacote_texto, qtd_movimentos = pacotes[id_pacote]
            
            # Determinar a célula atual do pacote com base no ID
            i, j = divmod(id_pacote-1, n)  # Supondo que 'n' é o número de colunas
            
            # Pega as posições do centro do quadrado menor e do quadrado maior
            centro_menor = centros_menores[i][j]
            centro_maior = centros_maiores[i][j]
            
            if qtd_movimentos == 0:
                # Movimenta o pacote da fase 1 (exemplo de movimentação, pode ser ajustada)
                mover_pacote_fase1(
                    centro_menor[0], centro_menor[1], 
                    centro_maior[0], centro_maior[1], 
                    pacote_oval, pacote_texto, 
                    id_pacote, direcao
                )
                qtd_movimentos += 1
                pacotes[id_pacote] = (pacote_oval, pacote_texto,qtd_movimentos)
            else:
                mover_pacote_para_direcao(centro_maior[0], centro_maior[1], pacote_oval, pacote_texto, id_pacote, direcao)
                qtd_movimentos += 1
                pacotes[id_pacote] = (pacote_oval, pacote_texto,qtd_movimentos)
    direcoes = { 2: "Processador"}


def rodar_tela(matriz_adj, melhor_mapeamentoo, n):
    global matrix_adj, melhor_mapeamento
    # Armazena as informações passadas
    matrix_adj = matriz_adj
    melhor_mapeamento = melhor_mapeamentoo
    
    # Limpa o canvas antes de desenhar a nova matriz
    canvas.delete("all")  
    global centros_maiores, centros_menores 
    centros_maiores, centros_menores = desenhar_matriz(n)
    
    # Chama a função para criar pacotes
    criar_pacotes_e_alocar()

# Criação da janela principal e do canvas
janela = tk.Tk()
largura_canvas = 1500
altura_canvas = 900
canvas = tk.Canvas(janela, width=largura_canvas, height=altura_canvas)
canvas.pack()

# Adicionar botão para iniciar a animação
botao_animar = tk.Button(janela, text="Iniciar Animação", command=animar_pacote)
botao_animar.pack()

# Exemplo de dados para o mapeamento e a matriz de adjacência
# Você pode alterar esses dados de acordo com suas necessidades
matrix_adj = [
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]
]

melhor_mapeamento = [
    [1, 0, 0],
    [0, 2, 0],
    [0, 0, 3]
]

n = 3  # Tamanho da matriz
direcoes = { 2: "O", 3: "N"}

# Para chamar a tela a partir de outra parte do software:
rodar_tela(matrix_adj, melhor_mapeamento, n)

# Rodar a interface
janela.mainloop()


direcoes = { 2: "O", 3: "N"}


# Rodar a interface e criar pacotes
criar_pacotes_e_alocar()

janela.mainloop()
