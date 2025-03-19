import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import cv2
import os
from PIL import Image, ImageTk
import time
import shutil

class FormularioFuncionario:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Funcionário")
        self.root.geometry("800x900")
        
        # Variáveis para armazenar os nomes das fotos
        self.nomes_fotos = ["", "", "", "", ""]
        self.fotos_temporarias = ["", "", "", "", ""]
        
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
            
            # Criar um frame para conter o label e o nome do arquivo
            frame_foto = ttk.Frame(self.frame)
            frame_foto.grid(row=5+i, column=1, sticky=tk.W, pady=5)
            
            # Label para indicar o status
            self.label_foto = ttk.Label(frame_foto, text="Nenhuma foto tirada")
            self.label_foto.pack(side=tk.LEFT, padx=5)
            
            # Label para mostrar o nome do arquivo
            self.label_nome_arquivo = ttk.Label(frame_foto, text="")
            self.label_nome_arquivo.pack(side=tk.LEFT, padx=5)
        
        # Botão Salvar
        self.btn_salvar = ttk.Button(self.frame, text="Salvar", command=self.salvar_funcionario)
        self.btn_salvar.grid(row=10, column=0, columnspan=2, pady=20)
            
        # Criar pasta IMGS se não existir
        if not os.path.exists("IMGS"):
            os.makedirs("IMGS")
            
    def tirar_foto(self, numero_foto):
        # Criar uma nova janela para visualização da câmera
        janela_camera = tk.Toplevel(self.root)
        janela_camera.title("Captura de Foto")
        janela_camera.geometry("640x480")
        
        # Label para exibir a imagem da câmera
        label_camera = ttk.Label(janela_camera)
        label_camera.pack(pady=10)
        
        # Botão para capturar a foto
        btn_capturar = ttk.Button(janela_camera, text="Capturar Foto", command=lambda: self.capturar_foto(numero_foto, janela_camera, label_camera))
        btn_capturar.pack(pady=10)
        
        # Inicializar a câmera
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            messagebox.showerror("Erro", "Não foi possível acessar a webcam!")
            janela_camera.destroy()
            return
            
        def atualizar_camera():
            ret, frame = self.cap.read()
            if ret:
                # Converter frame para formato PIL
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                imagem_pil = Image.fromarray(frame_rgb)
                # Redimensionar para caber na janela
                imagem_pil = imagem_pil.resize((640, 360), Image.Resampling.LANCZOS)
                # Converter para PhotoImage
                imagem_tk = ImageTk.PhotoImage(image=imagem_pil)
                label_camera.configure(image=imagem_tk)
                label_camera.image = imagem_tk
            janela_camera.after(10, atualizar_camera)
            
        atualizar_camera()
        
        # Configurar o que acontece quando a janela é fechada
        def on_closing():
            self.cap.release()
            janela_camera.destroy()
            
        janela_camera.protocol("WM_DELETE_WINDOW", on_closing)
        
    def capturar_foto(self, numero_foto, janela_camera, label_camera):
        # Capturar frame atual
        ret, frame = self.cap.read()
        
        if ret:
            # Gerar nome único para a foto
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"foto_{numero_foto+1}_{timestamp}.jpg"
            caminho_completo = os.path.join("IMGS", nome_arquivo)
            
            # Salvar a imagem
            cv2.imwrite(caminho_completo, frame)
            
            # Atualizar os labels na interface principal
            label_foto = self.frame.grid_slaves(row=5+numero_foto, column=1)[0]
            label_foto.winfo_children()[0].config(text="Foto salva:")
            label_foto.winfo_children()[1].config(text=nome_arquivo)
            
            # Armazenar o nome da foto temporária
            self.fotos_temporarias[numero_foto] = nome_arquivo
            
            # Liberar a câmera e fechar a janela
            self.cap.release()
            janela_camera.destroy()
            
            messagebox.showinfo("Sucesso", "Foto capturada com sucesso!")
            
    def salvar_funcionario(self):
        # Verificar se o ID foi preenchido
        id_funcionario = self.id_entry.get().strip()
        if not id_funcionario:
            messagebox.showerror("Erro", "Por favor, preencha o ID do funcionário!")
            return
            
        # Criar diretório para o funcionário
        diretorio_funcionario = os.path.join("IMGS", id_funcionario)
        if not os.path.exists(diretorio_funcionario):
            os.makedirs(diretorio_funcionario)
            
        # Mover as fotos para o diretório do funcionário
        for i, foto_temp in enumerate(self.fotos_temporarias):
            if foto_temp:
                origem = os.path.join("IMGS", foto_temp)
                if os.path.exists(origem):
                    # Gerar novo nome para a foto no diretório do funcionário
                    novo_nome = f"foto_{i+1}.jpg"
                    destino = os.path.join(diretorio_funcionario, novo_nome)
                    
                    # Mover a foto
                    shutil.move(origem, destino)
                    
                    # Atualizar o nome da foto na lista
                    self.nomes_fotos[i] = novo_nome
                    
                    # Atualizar o label com o novo nome
                    label_foto = self.frame.grid_slaves(row=5+i, column=1)[0]
                    label_foto.winfo_children()[1].config(text=novo_nome)
        
        # Limpar as fotos temporárias
        self.fotos_temporarias = ["", "", "", "", ""]
        
        messagebox.showinfo("Sucesso", "Funcionário salvo com sucesso!")
        
        # Limpar os campos do formulário
        self.id_entry.delete(0, tk.END)
        self.funcionario_entry.delete(0, tk.END)
        self.cargo_entry.delete(0, tk.END)
        self.salario_entry.delete(0, tk.END)
        self.data_contratacao.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioFuncionario(root)
    root.mainloop()