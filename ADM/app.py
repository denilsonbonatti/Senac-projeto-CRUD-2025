import tkinter as tk
from tkinter import messagebox
import requests
import conf
import menu

root = tk.Tk()
root.title("Área de Login")
root.geometry("500x400")
root.resizable(False, False)

def verifica_usuario():
    email = entrada_usuario.get()
    senha = entrada_senha.get()
    
    url_api = f"{conf.url_api}/usuarios/login"
    
    try:
        response = requests.post(url_api, json={"email": email, "senha": senha})
        
        if response.status_code == 200:
            #messagebox.showinfo("Acesso Concedido", "Bem-vindo ao sistema!")
            root.destroy()
            menu.abrir_tela()
        else:
            data = response.json()
            messagebox.showwarning("Login Falhou", data.get("mensagem", "Erro ao autenticar usuário."))
    
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erro de Rede", "Não foi possível conectar ao servidor.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro de Requisição", f"Erro ao comunicar com o servidor: {e}")

tk.Label(root, text="Área administrativa", font=("Arial Black", 14, "bold")).pack(pady=5)

try:
    imagem = tk.PhotoImage(file="ADM/IMGS/logotipo.png")
    tk.Label(root, image=imagem).pack(pady=10)
except Exception as e:
    print(f"Erro ao carregar imagem: {e}")

tk.Label(root, text="E-mail:", font=("Arial", 12)).pack(pady=5)
entrada_usuario = tk.Entry(root, width=40)
entrada_usuario.pack(pady=5)

tk.Label(root, text="Senha:", font=("Arial", 12)).pack(pady=5)
entrada_senha = tk.Entry(root, show="*")
entrada_senha.pack(pady=5)

tk.Button(root, text="Entrar", font=("Arial", 12), command=verifica_usuario).pack(pady=15)

root.mainloop()
