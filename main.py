from tkinter import simpledialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from datetime import datetime, timedelta

class Livro:
    def __init__(self, tema, nome, edicao):
        self.tema = tema
        self.nome = nome
        self.edicao = edicao
        self.disponivel = True
        self.data_emprestimo = None
        self.data_devolucao = None

class Usuario:
    def __init__(self, nome):
        self.nome = nome
        self.livros_emprestados = []

class Biblioteca:
    def __init__(self):
        self.livros = []
        self.usuarios = []

    def adicionar_livro(self, livro):
        self.livros.append(livro)
        return f"Livro '{livro.nome}' adicionado à biblioteca."

    def cadastrar_usuario(self, usuario):
        self.usuarios.append(usuario)
        return f"Usuário {usuario.nome} cadastrado."

    def realizar_emprestimo(self, usuario, livro, data_inicial, data_final):
        if livro in self.livros and livro.disponivel:
            usuario.livros_emprestados.append(livro)
            livro.disponivel = False
            livro.data_emprestimo = data_inicial
            livro.data_devolucao = data_final
            return f"{usuario.nome} pegou emprestado o livro '{livro.nome}'."
        else:
            return "Livro não disponível para empréstimo."

    def realizar_devolucao(self, usuario, livro):
        if livro in usuario.livros_emprestados:
            usuario.livros_emprestados.remove(livro)
            livro.disponivel = True
            livro.data_emprestimo = None
            livro.data_devolucao = None
            return f"{usuario.nome} devolveu o livro '{livro.nome}'."
        else:
            return "Este livro não foi emprestado para este usuário."

class BibliotecaGUI:
    def __init__(self, master):
        self.master = ThemedTk(theme="equilux")  # Escolha um tema, neste caso, "equilux"
        self.master.title("Sistema de Gerenciamento de Biblioteca")

        self.biblioteca = Biblioteca()

        self.frame = ttk.Frame(self.master)
        self.frame.pack()

        self.label = ttk.Label(self.frame, text="Bem-vindo ao Sistema de Gerenciamento de Biblioteca", font=("Helvetica", 14))
        self.label.grid(row=0, column=0, pady=10)

        self.button_add_user = ttk.Button(self.frame, text="Cadastrar Usuário", command=self.cadastrar_usuario)
        self.button_add_user.grid(row=1, column=0, pady=5)

        self.button_add_book = ttk.Button(self.frame, text="Adicionar Livro", command=self.adicionar_livro)
        self.button_add_book.grid(row=2, column=0, pady=5)

        self.button_borrow = ttk.Button(self.frame, text="Realizar Empréstimo", command=self.realizar_emprestimo)
        self.button_borrow.grid(row=3, column=0, pady=5)

        self.button_return = ttk.Button(self.frame, text="Realizar Devolução", command=self.realizar_devolucao)
        self.button_return.grid(row=4, column=0, pady=5)

        self.button_exit = ttk.Button(self.frame, text="Sair", command=self.master.destroy)
        self.button_exit.grid(row=5, column=0, pady=10)

    def cadastrar_usuario(self):
        user_name = self.get_input("Digite o nome do usuário:")
        if user_name:
            usuario = Usuario(user_name)
            mensagem = self.biblioteca.cadastrar_usuario(usuario)
            messagebox.showinfo("Cadastro de Usuário", mensagem)

    def adicionar_livro(self):
        tema = self.get_input("Digite o tema do livro:")
        nome = self.get_input("Digite o nome do livro:")
        edicao = self.get_input("Digite a edição do livro:")
        livro = Livro(tema, nome, edicao)
        mensagem = self.biblioteca.adicionar_livro(livro)
        messagebox.showinfo("Adição de Livro", mensagem)

    def realizar_emprestimo(self):
        user_name = self.get_input("Digite o nome do usuário:")
        book_name = self.get_input("Digite o nome do livro:")
        initial_date = self.get_input("Digite a data inicial do empréstimo (DD/MM/AAAA):")
        final_date = self.get_input("Digite a data final do empréstimo (DD/MM/AAAA):")

        usuario = next((u for u in self.biblioteca.usuarios if u.nome == user_name), None)
        livro = next((l for l in self.biblioteca.livros if l.nome == book_name), None)

        if usuario and livro:
            try:
                initial_date = datetime.strptime(initial_date, "%d/%m/%Y")
                final_date = datetime.strptime(final_date, "%d/%m/%Y")
                mensagem = self.biblioteca.realizar_emprestimo(usuario, livro, initial_date, final_date)
                messagebox.showinfo("Empréstimo de Livro", mensagem)
            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido. Utilize DD/MM/AAAA.")
        else:
            messagebox.showerror("Erro", "Usuário ou livro não encontrado.")

    def realizar_devolucao(self):
        user_name = self.get_input("Digite o nome do usuário:")
        book_name = self.get_input("Digite o nome do livro:")

        usuario = next((u for u in self.biblioteca.usuarios if u.nome == user_name), None)
        livro = next((l for l in self.biblioteca.livros if l.nome == book_name), None)

        if usuario and livro:
            mensagem = self.biblioteca.realizar_devolucao(usuario, livro)
            messagebox.showinfo("Devolução de Livro", mensagem)
        else:
            messagebox.showerror("Erro", "Usuário ou livro não encontrado.")

    def get_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

if __name__ == "__main__":
    app = BibliotecaGUI(tk.Tk())
    app.master.mainloop()
