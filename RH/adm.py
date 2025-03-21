import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import cv2
import os
from PIL import Image, ImageTk
import requests
from email.utils import parsedate_to_datetime

class FormularioFuncionario:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Funcionário")
        self.root.geometry("800x900")
        
        # Variáveis para armazenar os nomes das fotos
        self.nomes_fotos = ["", "", "", "", ""]
        self.fotos_temporarias = ["", "", "", "", ""]
        self.funcionario_atual = None
        
        # Frame principal
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame para botões de ação
        frame_botoes = ttk.Frame(self.frame)
        frame_botoes.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Botões de ação
        ttk.Button(frame_botoes, text="Incluir", command=self.incluir_funcionario).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Salvar", command=self.salvar_funcionario).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Alterar", command=self.alterar_funcionario).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Excluir", command=self.excluir_funcionario).pack(side=tk.LEFT, padx=5)
        
        # Frame para ID e Consulta
        frame_id = ttk.Frame(self.frame)
        frame_id.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(frame_id, text="ID:").pack(side=tk.LEFT, padx=5)
        self.id_entry = ttk.Entry(frame_id)
        self.id_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_id, text="Consultar", command=self.consultar_funcionario).pack(side=tk.LEFT, padx=5)
        
        # Campos do formulário
        ttk.Label(self.frame, text="Funcionário:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.funcionario_entry = ttk.Entry(self.frame, width=40)
        self.funcionario_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.frame, text="Cargo:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cargo_entry = ttk.Entry(self.frame, width=40)
        self.cargo_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.frame, text="Data de Contratação:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.data_contratacao = DateEntry(self.frame, width=20, locale='pt_BR')
        self.data_contratacao.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.frame, text="Salário:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.salario_entry = ttk.Entry(self.frame)
        self.salario_entry.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Botões e labels para fotos
        for i in range(5):
            ttk.Button(
                self.frame, 
                text=f"Realizar {i+1}ª Foto", 
                command=lambda x=i: self.tirar_foto(x)
            ).grid(row=6+i, column=0, sticky=tk.W, pady=5)
            
            # Criar um frame para conter o label e o nome do arquivo
            frame_foto = ttk.Frame(self.frame)
            frame_foto.grid(row=6+i, column=1, sticky=tk.W, pady=5)
            
            # Label para indicar o status
            self.label_foto = ttk.Label(frame_foto, text="Nenhuma foto tirada")
            self.label_foto.pack(side=tk.LEFT, padx=5)
            
            # Label para mostrar o nome do arquivo
            self.label_nome_arquivo = ttk.Label(frame_foto, text="")
            self.label_nome_arquivo.pack(side=tk.LEFT, padx=5)
        
        # Criar pasta IMGS se não existir
        if not os.path.exists("IMGS"):
            os.makedirs("IMGS")
            
        # Desabilitar campos inicialmente
        self.desabilitar_campos()
            
    def desabilitar_campos(self):
        self.funcionario_entry.config(state='disabled')
        self.cargo_entry.config(state='disabled')
        self.data_contratacao.config(state='disabled')
        self.salario_entry.config(state='disabled')
        
        # Desabilitar botões de foto
        for i in range(5):
            btn = self.frame.grid_slaves(row=6+i, column=0)[0]
            btn.config(state='disabled')
            
    def habilitar_campos(self):
        self.funcionario_entry.config(state='normal')
        self.cargo_entry.config(state='normal')
        self.data_contratacao.config(state='normal')
        self.salario_entry.config(state='normal')
        
        # Habilitar botões de foto
        for i in range(5):
            btn = self.frame.grid_slaves(row=6+i, column=0)[0]
            btn.config(state='normal')
            
    def incluir_funcionario(self):
        self.limpar_campos()
        self.funcionario_atual = None
        self.id_entry.config(state='disabled')
        self.habilitar_campos()
        
    def consultar_funcionario(self):
        try:
            id = self.id_entry.get()
            if not id:
                messagebox.showwarning("Aviso", "Digite o ID do funcionário para consultar!")
                return
                
            response = requests.get(f'http://localhost:5000/funcionarios/{id}')
            if response.status_code == 200:
                funcionario = response.json()
                self.funcionario_atual = funcionario
                
                # Preencher campos
                self.funcionario_entry.config(state='normal')
                self.funcionario_entry.delete(0, tk.END)
                self.funcionario_entry.insert(0, funcionario['funcionario'])
                
                self.cargo_entry.config(state='normal')
                self.cargo_entry.delete(0, tk.END)
                self.cargo_entry.insert(0, funcionario['cargo'])
                
                try:
                    data = parsedate_to_datetime(funcionario['data_contratacao'])
                except Exception:
                    messagebox.showerror("Erro", f"Formato de data inválido: {funcionario['data_contratacao']}")
                    return

                self.data_contratacao.set_date(data)
                
                self.salario_entry.config(state='normal')
                self.salario_entry.delete(0, tk.END)
                self.salario_entry.insert(0, str(funcionario['salario']))
                
                # Atualizar labels das fotos
                for i in range(5):
                    foto = funcionario[f'foto{i+1}']
                    label_foto = self.frame.grid_slaves(row=6+i, column=1)[0]
                    label_foto.winfo_children()[0].config(text="Foto salva:")
                    label_foto.winfo_children()[1].config(text=foto)
                    self.nomes_fotos[i] = foto
                    
                # Habilitar campos para edição
                self.habilitar_campos()
            else:
                messagebox.showerror("Erro", "Funcionário não encontrado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar funcionário: {str(e)}")
            
    def salvar_funcionario(self):
        try:
            dados = {
                'funcionario': self.funcionario_entry.get(),
                'cargo': self.cargo_entry.get(),
                'data_contratacao': self.data_contratacao.get_date().strftime('%Y-%m-%d'),
                'salario': float(self.salario_entry.get()),
                'foto1': self.nomes_fotos[0],
                'foto2': self.nomes_fotos[1],
                'foto3': self.nomes_fotos[2],
                'foto4': self.nomes_fotos[3],
                'foto5': self.nomes_fotos[4]
            }
            
            if self.funcionario_atual:
                # Atualizar funcionário existente
                response = requests.put(f'http://localhost:5000/funcionarios/{self.funcionario_atual["id"]}', json=dados)
                if response.status_code == 200:
                    messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
            else:
                # Criar novo funcionário
                response = requests.post('http://localhost:5000/funcionarios', json=dados)
                if response.status_code == 201:
                    messagebox.showinfo("Sucesso", "Funcionário criado com sucesso!")
                    
            self.limpar_campos()
            self.desabilitar_campos()
            self.id_entry.config(state='normal')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar funcionário: {str(e)}")
            
    def alterar_funcionario(self):
        if not self.funcionario_atual:
            messagebox.showwarning("Aviso", "Consulte um funcionário primeiro!")
            return
            
    def excluir_funcionario(self):
        if not self.funcionario_atual:
            messagebox.showwarning("Aviso", "Consulte um funcionário primeiro!")
            return
            
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este funcionário?"):
            try:
                response = requests.delete(f'http://localhost:5000/funcionarios/{self.funcionario_atual["id"]}')
                if response.status_code == 200:
                    messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
                    self.limpar_campos()
                    self.desabilitar_campos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir funcionário: {str(e)}")
                
    def limpar_campos(self):
        self.funcionario_entry.config(state='normal')
        self.funcionario_entry.delete(0, tk.END)
        
        self.cargo_entry.config(state='normal')
        self.cargo_entry.delete(0, tk.END)
        
        self.salario_entry.config(state='normal')
        self.salario_entry.delete(0, tk.END)
        
        self.data_contratacao.delete(0, tk.END)
        
        for i in range(5):
            label_foto = self.frame.grid_slaves(row=6+i, column=1)[0]
            label_foto.winfo_children()[0].config(text="Nenhuma foto tirada")
            label_foto.winfo_children()[1].config(text="")
            self.nomes_fotos[i] = ""
            
        self.funcionario_atual = None
            
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
            label_foto = self.frame.grid_slaves(row=6+numero_foto, column=1)[0]
            label_foto.winfo_children()[0].config(text="Foto salva:")
            label_foto.winfo_children()[1].config(text=nome_arquivo)
            
            # Armazenar o nome da foto temporária
            self.nomes_fotos[numero_foto] = nome_arquivo
            
            # Liberar a câmera e fechar a janela
            self.cap.release()
            janela_camera.destroy()
            
            messagebox.showinfo("Sucesso", "Foto capturada com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioFuncionario(root)
    root.mainloop()