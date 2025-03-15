import tkinter as tk
from tkinter import messagebox
import edit_usuarios

def janela_usuarios():
    edit_usuarios.criar_tela()



def abrir_tela():

    def sair():
            resposta = messagebox.askyesno("Sair", "Tem certeza que deseja sair?")
            if resposta:
                menu.destroy()

    menu = tk.Tk()
    menu.title("Menu Principal")

    # Maximizar a janela
    menu.state('zoomed')

    menu_bar = tk.Menu(menu)
    menu.config(menu=menu_bar)

    menu_usuarios = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Usuários", menu=menu_usuarios)
    menu_usuarios.add_command(label="Edição", command=janela_usuarios)
    menu_usuarios.add_command(label="Relatório")

    menu_produtos = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Produtos", menu=menu_produtos)
    menu_produtos.add_command(label="Edição")
    menu_produtos.add_command(label="Relatório")

    menu_bar.add_command(label="Sair", command=sair)

    menu.mainloop()