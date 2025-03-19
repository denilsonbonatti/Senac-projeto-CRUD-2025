import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import cv2
import os
from PIL import Image, ImageTk
import time

class FormularioFuncionario:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Funcionário")
        self.root.geometry("800x900")
        
        # Variáveis para armazenar os nomes das fotos
        self.nomes_fotos = ["", "", "", "", ""]
        
        # Frame principal
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Campos do formulário
        ttk.Label(self.frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.id_entry = ttk.Entry(self.frame)
        self.id_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.frame, text="Funcionário:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.funcionario_entry = ttk.Entry(self.frame, width=40)
        self.funcionario_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.frame, text="Cargo:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cargo_entry = ttk.Entry(self.frame, width=40)
        self.cargo_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.frame, text="Data de Contratação:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.data_contratacao = DateEntry(self.frame, width=20, locale='pt_BR')
        self.data_contratacao.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.frame, text="Salário:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.salario_entry = ttk.Entry(self.frame)
        self.salario_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Botões e labels para fotos
        for i in range(5):
            ttk.Button(
                self.frame, 
                text=f"Realizar {i+1}ª Foto", 
                command=lambda x=i: self.tirar_foto(x)
            ).grid(row=5+i, column=0, sticky=tk.W, pady=5)
            
            self.label_foto = ttk.Label(self.frame, text="Nenhuma foto tirada")
            self.label_foto.grid(row=5+i, column=1, sticky=tk.W, pady=5)
            
        # Criar pasta IMGS se não existir
        if not os.path.exists("IMGS"):
            os.makedirs("IMGS")
            
    def tirar_foto(self, numero_foto):
        # Inicializar a câmera
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            tk.messagebox.showerror("Erro", "Não foi possível acessar a webcam!")
            return
            
        # Capturar frame
        ret, frame = cap.read()
        
        if ret:
            # Gerar nome único para a foto
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"foto_{numero_foto+1}_{timestamp}.jpg"
            caminho_completo = os.path.join("IMGS", nome_arquivo)
            
            # Salvar a imagem
            cv2.imwrite(caminho_completo, frame)
            
            # Atualizar o nome da foto na interface
            label_foto = self.frame.grid_slaves(row=5+numero_foto, column=1)[0]
            label_foto.config(text=f"Foto salva: {nome_arquivo}")
            
            # Armazenar o nome da foto
            self.nomes_fotos[numero_foto] = nome_arquivo
            
        # Liberar a câmera
        cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioFuncionario(root)
    root.mainloop() 