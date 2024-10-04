import tkinter as tk

# Função para mover o pacote entre dois pontos (x_inicial, y_inicial) e (x_final, y_final)
def mover_pacote(x_inicial, y_inicial, x_final, y_final, passo):
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

# Função para desenhar a matriz de quadrados, links e conexões diagonais com quadrados pequenos
def desenhar_matriz(n):
    tamanho_quadrado = 70  # Tamanho de cada quadrado maior
    espaco = 70  # Espaço entre quadrados
    tamanho_quadrado_pequeno = 40  # Tamanho dos quadrados pequenos
    tamanho_retirangulo = 15  # Tamanho dos retângulos de entrada

    # Tamanho total da matriz
    tamanho_total = n * (tamanho_quadrado + espaco) - espaco

    # Calcula o offset inicial para centralizar a matriz
    offset_x = (largura_canvas - tamanho_total) // 2
    offset_y = (altura_canvas - tamanho_total) // 2

    # Matriz para armazenar as coordenadas do centro dos quadrados maiores e menores
    centros_maiores = [[None for _ in range(n)] for _ in range(n)]
    centros_menores = [[None for _ in range(n)] for _ in range(n)]

    # Loop para desenhar os quadrados e os links
    for i in range(n):
        for j in range(n):
            x1 = j * (tamanho_quadrado + espaco) + offset_x
            y1 = i * (tamanho_quadrado + espaco) + offset_y
            x2 = x1 + tamanho_quadrado
            y2 = y1 + tamanho_quadrado

            # Coordenadas do centro do quadrado maior
            centro_x_maior = (x1 + x2) // 2
            centro_y_maior = (y1 + y2) // 2
            centros_maiores[i][j] = (centro_x_maior, centro_y_maior)

            # Desenhar o quadrado maior
            quadrado = canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue")

            # Desenhar retângulos de entrada nas direções N, S, L e O
            # Norte
            canvas.create_rectangle(centro_x_maior - tamanho_retirangulo // 2, y1, centro_x_maior + tamanho_retirangulo // 2, y1 + tamanho_retirangulo, fill="gray")
            canvas.create_text(centro_x_maior, y1 + tamanho_retirangulo // 2, text="N", fill="black", font=("Arial", 10, "bold"))
            # Sul
            canvas.create_rectangle(centro_x_maior - tamanho_retirangulo // 2, y2 - tamanho_retirangulo, centro_x_maior + tamanho_retirangulo // 2, y2, fill="gray")
            canvas.create_text(centro_x_maior, y2 - tamanho_retirangulo // 2, text="S", fill="black", font=("Arial", 10, "bold"))
            # Leste
            canvas.create_rectangle(x2 - tamanho_retirangulo, centro_y_maior - tamanho_retirangulo // 2, x2, centro_y_maior + tamanho_retirangulo // 2, fill="gray")
            canvas.create_text(x2 - tamanho_retirangulo // 2, centro_y_maior, text="L", fill="black", font=("Arial", 10, "bold"))
            # Oeste
            canvas.create_rectangle(x1, centro_y_maior - tamanho_retirangulo // 2, x1 + tamanho_retirangulo, centro_y_maior + tamanho_retirangulo // 2, fill="gray")
            canvas.create_text(x1 + tamanho_retirangulo // 2, centro_y_maior, text="O", fill="black", font=("Arial", 10, "bold"))

            # Desenhar links para o vizinho da direita
            if j < n - 1:
                x1_link = x2
                y1_link = (y1 + y2) // 2
                x2_link = x2 + espaco
                y2_link = y1_link
                canvas.create_line(x1_link, y1_link, x2_link, y2_link, width=2)

            # Desenhar links para o vizinho de baixo
            if i < n - 1:
                x1_link = (x1 + x2) // 2
                y1_link = y2
                x2_link = x1_link
                y2_link = y2 + espaco
                canvas.create_line(x1_link, y1_link, x2_link, y2_link, width=2)

            # Desenhar ligação saindo da ponta superior esquerda em uma diagonal
            x1_diag = x1
            y1_diag = y1
            x2_diag = x1_diag - espaco // 2
            y2_diag = y1_diag - espaco // 2
            canvas.create_line(x1_diag, y1_diag, x2_diag, y2_diag, width=2)

            # Coordenadas do centro do quadrado menor
            centro_x_menor = x2_diag
            centro_y_menor = y2_diag
            centros_menores[i][j] = (centro_x_menor, centro_y_menor)

            # Desenhar quadrado pequeno na ponta da ligação diagonal
            x1_pequeno = x2_diag - tamanho_quadrado_pequeno // 2
            y1_pequeno = y2_diag - tamanho_quadrado_pequeno // 2
            x2_pequeno = x1_pequeno + tamanho_quadrado_pequeno
            y2_pequeno = y1_pequeno + tamanho_quadrado_pequeno
            canvas.create_rectangle(x1_pequeno, y1_pequeno, x2_pequeno, y2_pequeno, fill="orange")

    return centros_maiores, centros_menores

# Função para iniciar a animação do pacote entre um quadrado menor e maior
def enviar_pacote_menor_para_maior(i, j):
    centro_menor = centros_menores[i][j]
    centro_maior = centros_maiores[i][j]
    mover_pacote(centro_menor[0], centro_menor[1], centro_maior[0], centro_maior[1], 50)

# Criar a interface Tkinter
janela = tk.Tk()
janela.title("Matriz de Quadrados e Envio de Pacotes")

# Definir o tamanho do canvas
largura_canvas = 1000
altura_canvas = 900

# Canvas para desenhar a matriz
canvas = tk.Canvas(janela, width=largura_canvas, height=altura_canvas)
canvas.pack()

# Tamanho da matriz (n x n)
n = 6
centros_maiores, centros_menores = desenhar_matriz(n)

# Criar o "pacote" como um pequeno círculo
pacote_oval = canvas.create_oval(centros_menores[0][0][0]-10, centros_menores[0][0][1]-10, centros_menores[0][0][0]+10, centros_menores[0][0][1]+10, fill="red")
# Adicionar número dentro do pacote
pacote_texto = canvas.create_text(centros_menores[0][0][0], centros_menores[0][0][1], text="1", fill="white", font=("Arial", 12, "bold"))

# Botão para iniciar a animação do pacote de um quadrado menor para o maior
botao = tk.Button(janela, text="Enviar Pacote", command=lambda: enviar_pacote_menor_para_maior(0, 0))
botao.pack()

janela.mainloop()
