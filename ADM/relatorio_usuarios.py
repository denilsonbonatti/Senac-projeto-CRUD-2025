import requests
import tkinter as tk
from tkinter import ttk
import conf


def criar_janela():

    # URL da API Flask
    API_URL = f"{conf.url_api}/usuarios" 

    # Criar janela principal
    root = tk.Tk()
    root.title("Relatório de Usuários")

    # Criar frame para organizar a tabela e a barra de rolagem
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Criar Treeview para exibir os dados
    tree = ttk.Treeview(frame, columns=("ID", "Nome", "Cargo", "Email"), show="headings")

    # Definir os cabeçalhos das colunas
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Cargo", text="Cargo")
    tree.heading("Email", text="Email")

    # Ajustar tamanho das colunas
    tree.column("ID", width=50, anchor="center")
    tree.column("Nome", width=200)
    tree.column("Cargo", width=150)
    tree.column("Email", width=250)

    # Adicionar barra de rolagem vertical
    scroll_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)

    # Posicionar os widgets
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    # Buscar dados da API e preencher a tabela
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            usuarios = response.json()
            for usuario in usuarios:
                tree.insert("", tk.END, values=usuario)
        else:
            print("Erro ao buscar dados:", response.json())
    except Exception as e:
        print("Erro na requisição:", e)

    # Rodar a interface gráfica
    root.mainloop()
