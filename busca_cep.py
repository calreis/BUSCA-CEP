import requests
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Aplicação criada e desenvolidade por CALREIS(Claudemir Reis) utilizando a API da VIACEP.
# Contato calreis73@gmail.com ou whatsapp (71) 981689473
class CepApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Consultor de CEP")
        self.root.geometry("500x400")
        
        self.criar_widgets()
        
    def criar_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Entrada do CEP
        ttk.Label(self.main_frame, text="CEP (sem traço ou pontos):").grid(row=0, column=0, sticky=tk.W)
        self.cep_entry = ttk.Entry(self.main_frame, width=20)
        self.cep_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Botão de consulta
        self.btn_consultar = ttk.Button(
            self.main_frame, 
            text="Consultar", 
            command=self.buscar_cep
        )
        self.btn_consultar.grid(row=0, column=2, padx=5)
        
        # Área de resultados
        self.resultados_text = tk.Text(self.main_frame, height=15, width=50, state=tk.DISABLED)
        self.resultados_text.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(self.main_frame, command=self.resultados_text.yview)
        scrollbar.grid(row=1, column=3, sticky=tk.NS)
        self.resultados_text.configure(yscrollcommand=scrollbar.set)
    
    def buscar_cep(self):
        cep = self.cep_entry.get().strip()
        
        if not cep.isdigit() or len(cep) != 8:
            messagebox.showerror("Erro", "CEP inválido! Deve conter 8 dígitos numéricos.")
            return
            
        try:
            url = f'https://viacep.com.br/ws/{cep}/json/'
            response = requests.get(url)
            
            if response.status_code != 200:
                messagebox.showerror("Erro", "Problema na conexão com a API!")
                return
                
            dados = response.json()
            
            if 'erro' in dados:
                messagebox.showinfo("Aviso", "CEP não encontrado!")
                return
                
            self.mostrar_resultados(dados)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
    
    def mostrar_resultados(self, dados):
        # Criar dicionário organizado
        info = {
            'CEP': dados.get('cep', ''),
            'Logradouro': dados.get('logradouro', ''),
            'Complemento': dados.get('complemento', ''),
            'Bairro': dados.get('bairro', ''),
            'Cidade': dados.get('localidade', ''),
            'UF': dados.get('uf', ''),
            'IBGE': dados.get('ibge', ''),
            'SIAFI': dados.get('siafi', '')
        }
        
        # Converter para DataFrame
        df = pd.DataFrame([info])
        
        # Formatar saída
        output = "Resultado da Consulta:\n\n"
        for chave, valor in info.items():
            output += f"{chave}: {valor}\n"
        
        # Atualizar a área de texto
        self.resultados_text.config(state=tk.NORMAL)
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.insert(tk.END, output)
        self.resultados_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CepApp(root)
    root.mainloop()