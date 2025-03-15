import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk  # Importando a biblioteca Pillow para manipulação de imagens
import conf
import requests
import os
import shutil

def criar_tela():
    janela = tk.Toplevel()
    janela.title("Gerenciamento de Produtos")
    janela.configure(padx=20, pady=20)

    labels = ["ID:", "Produto:", "Quantidade:", "Imagem:", "Validade:", "Thumbnail:"]
    entradas = {}

    imagem_label = tk.Label(janela)
    imagem_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")


    for i, texto in enumerate(labels):
        tk.Label(janela, text=texto, width=15, anchor="e").grid(row=i, column=0, padx=5, pady=5, sticky="e")
        if texto == "Imagem:":
            entrada = tk.Entry(janela, width=30)
            entrada.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            botao_upload = tk.Button(janela, text="Upload", command=lambda e=entrada: upload_imagem(e, imagem_label))
            botao_upload.grid(row=i, column=2, padx=5, pady=5)
        elif texto == "Thumbnail:":
            imagem_label = tk.Label(janela)
            imagem_label.grid(row=i, column=1, padx=5, pady=5, sticky="w")
        else:
            entrada = tk.Entry(janela, width=40)
            entrada.grid(row=i, column=1, padx=5, pady=5, sticky="w")
        entradas[texto] = entrada

    entradas["ID:"].config(state="normal")
    for campo in ["Produto:", "Quantidade:", "Imagem:", "Validade:"]:
        entradas[campo].config(state="disabled")

    def upload_imagem(entrada, imagem_label):
        caminho_imagem = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if caminho_imagem:
            nome_arquivo = os.path.basename(caminho_imagem)
            destino = os.path.join("ADM/IMGS/", nome_arquivo)
            shutil.copy(caminho_imagem, destino)
            entrada.delete(0, tk.END)
            entrada.insert(0, destino)
            janela.lift()
            # Exibir a imagem como thumbnail
            img = Image.open(destino)
            print(f"Imagem carregada: {destino}")
            img.thumbnail((300, 300)) # Redimensiona a imagem para 300x300
            img_tk = ImageTk.PhotoImage(img) # Converte para formato compatível com tkinter
            imagem_label.config(image=img_tk)
            imagem_label.image = img_tk # Mantém uma referência à imagem
            imagem_label.update_idletasks() # Atualiza a janela
        
    def consultar():
        id_produto = entradas["ID:"].get()
        if not id_produto:
            messagebox.showwarning("Erro", "Informe o ID do produto para consultar.")
            janela.lift()
            return

        try:
            url = f"{conf.url_api}/produtos/{id_produto}"
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                if dados:
                    entradas["Produto:"].config(state="normal")
                    entradas["Quantidade:"].config(state="normal")
                    entradas["Imagem:"].config(state="normal")
                    entradas["Validade:"].config(state="normal")

                    entradas["Produto:"].delete(0, tk.END)
                    entradas["Produto:"].insert(0, dados["produto"])
                    entradas["Quantidade:"].delete(0, tk.END)
                    entradas["Quantidade:"].insert(0, dados["quantidade"])
                    entradas["Imagem:"].delete(0, tk.END)
                    entradas["Imagem:"].insert(0, dados["imagem"])
                    entradas["Validade:"].delete(0, tk.END)
                    entradas["Validade:"].insert(0, dados["validade"])

                    # Habilitar / Desabilitar botões
                    botao_consultar.config(state="normal")
                    botao_atualizar.config(state="normal")
                    botao_novo.config(state="disabled")
                    botao_consultar.config(state="disabled")
                    botao_excluir.config(state="normal")
                else:
                    messagebox.showwarning("Erro", "Produto não encontrado.")
                    janela.lift()
            else:
                messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
                janela.lift()
        except Exception as e:
            messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")
            janela.lift()

    def novo():
        entradas["ID:"].config(state="normal")
        entradas["Produto:"].config(state="normal")
        entradas["Quantidade:"].config(state="normal")
        entradas["Imagem:"].config(state="normal")
        entradas["Validade:"].config(state="normal")
        limpar()
        entradas["ID:"].config(state="disabled")

        # Habilitar/desabilitar botões
        botao_salvar.config(state="normal")
        botao_consultar.config(state="disabled")
        botao_novo.config(state="disabled")

    def salvar():
        dados = {
            "produto": entradas["Produto:"].get(),
            "quantidade": int(entradas["Quantidade:"].get()),
            "imagem": entradas["Imagem:"].get(),
            "validade": entradas["Validade:"].get()
        }

        try:
            url = f"{conf.url_api}/produtos"
            response = requests.post(url, json=dados)

            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
                janela.lift()

                # Habilitar/desabilitar botões
                botao_salvar.config(state="disabled")
                botao_consultar.config(state="disabled")
                botao_novo.config(state="normal")
            else:
                messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
                janela.lift()
        except Exception as e:
            messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")
            janela.lift()

    def atualizar():
        id_produto = entradas["ID:"].get()
        if not id_produto:
            messagebox.showwarning("Erro", "Informe o ID do produto para atualizar.")
            janela.lift()
            return

        dados = {
            "produto": entradas["Produto:"].get(),
            "quantidade": int(entradas["Quantidade:"].get()),
            "imagem": entradas["Imagem:"].get(),
            "validade": entradas["Validade:"].get()
        }

        try:
            url = f"{conf.url_api}/produtos/{id_produto}"
            response = requests.put(url, json=dados)

            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                janela.lift()
            else:
                messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
                janela.lift()
        except Exception as e:
            messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")
            janela.lift()

    def excluir():
        id_produto = entradas["ID:"].get()
        if not id_produto:
            messagebox.showwarning("Erro", "Informe o ID do produto para excluir.")
            janela.lift()
            return

        resposta = messagebox.askyesno("Excluir", "Tem certeza que deseja excluir o registro?")
        if resposta:

            try:
                url = f"{conf.url_api}/produtos/{id_produto}"
                response = requests.delete(url)

                if response.status_code == 200:
                    messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                    entradas["ID:"].config(state="normal")
                    entradas["Produto:"].config(state="normal")
                    entradas["Quantidade:"].config(state="normal")
                    entradas["Imagem:"].config(state="normal")
                    entradas["Validade:"].config(state="normal")
                    limpar()
                    entradas["ID:"].config(state="disabled")

                    # Habilitar/desabilitar botões
                    botao_salvar.config(state="normal")
                    botao_consultar.config(state="disabled")
                    botao_novo.config(state="disabled")
                    botao_atualizar.config(state="disabled")
                    janela.lift()
                else:
                    messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
                    janela.lift()
            except Exception as e:
                messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")
                janela.lift()

    def limpar():
        for entrada in entradas.values():
            entrada.delete(0, tk.END)

    def sair():
        janela.destroy()

    frame_botoes = tk.Frame(janela)
    frame_botoes.grid(row=len(labels), column=0, columnspan=2, pady=10)

    # Criando os botões
    botao_consultar = tk.Button(frame_botoes, text="Consultar", command=consultar, width=12)
    botao_consultar.pack(side="left", padx=5)
    botao_novo = tk.Button(frame_botoes, text="Novo", command=novo, width=12)
    botao_novo.pack(side="left", padx=5)
    botao_salvar = tk.Button(frame_botoes, text="Salvar", command=salvar, width=12, state="disabled")
    botao_salvar.pack(side="left", padx=5)
    botao_atualizar = tk.Button(frame_botoes, text="Atualizar", command=atualizar, width=12, state="disabled")
    botao_atualizar.pack(side="left", padx=5)
    botao_excluir = tk.Button(frame_botoes, text="Excluir", command=excluir, width=12, state="disabled")
    botao_excluir.pack(side="left", padx=5)
    botao_sair = tk.Button(frame_botoes, text="Sair", command=sair, width=12)
    botao_sair.pack(side="left", padx=5)

    janela.mainloop()
