import tkinter as tk
from tkinter import messagebox
import conf
import requests

def criar_tela():
    janela = tk.Toplevel()
    janela.title("Gerenciamento de Usuários")
    janela.configure(padx=20, pady=20)

    labels = ["ID:", "Nome:", "Cargo:", "Email:", "Senha:", "Confirmar Senha:"]
    entradas = {}

    for i, texto in enumerate(labels):
        tk.Label(janela, text=texto, width=15, anchor="e").grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entrada = tk.Entry(janela, width=40, show="*" if "Senha" in texto else "")
        entrada.grid(row=i, column=1, padx=5, pady=5, sticky="w")
        entradas[texto] = entrada
    
    entradas["ID:"].config(state="normal")
    for campo in ["Nome:", "Cargo:", "Email:", "Senha:", "Confirmar Senha:"]:
        entradas[campo].config(state="disabled")

    def consultar():
        id_usuario = entradas["ID:"].get()
        if not id_usuario:
            messagebox.showwarning("Erro", "Informe o ID do usuário para consultar.")
            return

        try:
            url = f"{conf.url_api}/usuarios/{id_usuario}"
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                if dados:
                    entradas["Nome:"].config(state="normal")
                    entradas["Cargo:"].config(state="normal")
                    entradas["Email:"].config(state="normal")
                    entradas["Senha:"].config(state="normal")
                    entradas["Confirmar Senha:"].config(state="normal")
                    
                    entradas["Nome:"].delete(0, tk.END)
                    entradas["Nome:"].insert(0, dados["nome"])
                    entradas["Cargo:"].delete(0, tk.END)
                    entradas["Cargo:"].insert(0, dados["cargo"])
                    entradas["Email:"].delete(0, tk.END)
                    entradas["Email:"].insert(0, dados["email"])
                else:
                    messagebox.showwarning("Erro", "Usuário não encontrado.")
            else:
                messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
        except Exception as e:
            messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")
    
    def novo():
        entradas["ID:"].config(state="normal")
        entradas["Nome:"].config(state="normal")
        entradas["Cargo:"].config(state="normal")
        entradas["Email:"].config(state="normal")
        entradas["Senha:"].config(state="normal")
        entradas["Confirmar Senha:"].config(state="normal")
        limpar()
        entradas["ID:"].config(state="disabled")

        # Habilitar o botão "Salvar"
        botao_salvar.config(state="normal")

    def salvar():
        if entradas["Senha:"].get() != entradas["Confirmar Senha:"].get():
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
        
        dados = {
            "nome": entradas["Nome:"].get(),
            "cargo": entradas["Cargo:"].get(),
            "email": entradas["Email:"].get(),
            "senha": entradas["Senha:"].get()
        }
        
        try:
            url = f"{conf.url_api}/usuarios"
            response = requests.post(url, json=dados)
            
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Usuário salvo com sucesso!")
            else:
                messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
        except Exception as e:
            messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")
    
    def atualizar():
        id_usuario = entradas["ID:"].get()
        if not id_usuario:
            messagebox.showwarning("Erro", "Informe o ID do usuário para atualizar.")
            return

        dados = {
            "nome": entradas["Nome:"].get(),
            "cargo": entradas["Cargo:"].get(),
            "email": entradas["Email:"].get(),
            "senha": entradas["Senha:"].get()
        }
        
        try:
            url = f"{conf.url_api}/usuarios/{id_usuario}"
            response = requests.put(url, json=dados)
            
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            else:
                messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
        except Exception as e:
            messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")
    
    def excluir():
        id_usuario = entradas["ID:"].get()
        if not id_usuario:
            messagebox.showwarning("Erro", "Informe o ID do usuário para excluir.")
            return
        
        try:
            url = f"{conf.url_api}/usuarios/{id_usuario}"
            response = requests.delete(url)
            
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
            else:
                messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
        except Exception as e:
            messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")
    
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

    botao_sair = tk.Button(frame_botoes, text="Sair", command=sair, width=12, state="disabled")
    botao_sair.pack(side="left", padx=5)

    janela.mainloop()
