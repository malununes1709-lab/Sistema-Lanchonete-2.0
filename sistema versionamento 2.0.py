import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# Configuração inicial da janela
janela = ctk.CTk()
janela.title("Sistema de Cadastro de Produtos")
janela.geometry("500x600")


# Função para conectar ao banco de dados
def conectar():
    conexao = sqlite3.connect("produtos.db")
    cursor = conexao.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            nome TEXT PRIMARY KEY,
            preco REAL,
            quantidade INTEGER
        )
    """
    )
    conexao.commit()
    return conexao, cursor


# Bloco 4 & Proteção de Dados (Regras de Negócio): Cadastrar Produto
def cadastrar_produto():
    nome = entry_nome.get().strip()
    preco_str = entry_preco.get().strip()
    quantidade_str = entry_quantidade.get().strip()

    # Tratamento de erro de conversão de dados
    try:
        preco = float(preco_str)
        quantidade = int(quantidade_str)
    except ValueError:
        messagebox.showerror(
            "Erro de Digitação", "Digite valores numéricos válidos!"
        )  #[cite: 18]
        return

    # 1. Barreira Matemática: Bloqueia valores menores que zero[cite: 19]
    if preco < 0 or quantidade < 0:
        messagebox.showwarning(
            "Aviso", "Valores não podem ser negativos!"
        )  #[cite: 19]
        return  # 'return' expulsa o usuário da função antes de salvar[cite: 19]

    conexao, cursor = conectar()  #[cite: 18]

    # 2. Checagem de Duplicidade: Procura no banco se o nome já existe[cite: 19]
    cursor.execute(
        "SELECT * FROM produtos WHERE nome = ?", (nome,)
    )  #[cite: 19]

    # Se o fetchone() encontrar algo, significa que já tem cadastro[cite: 19]
    if cursor.fetchone():
        messagebox.showwarning(
            "Aviso", "Este produto já está cadastrado!"
        )  #[cite: 19]
        entry_nome.delete(0, "end")  # Limpa o campo para a nova tentativa[cite: 19]
        conexao.close()
        return

    # Gravação no Banco de Dados[cite: 18]
    cursor.execute(
        "INSERT INTO produtos VALUES (?, ?, ?)", (nome, preco, quantidade)
    )  #[cite: 18]
    conexao.commit()  #[cite: 18]
    conexao.close()  #[cite: 18]

    messagebox.showinfo(
        "Sucesso", f"Produto '{nome}' cadastrado!"
    )  #[cite: 18]

    # Limpar campos após o sucesso
    entry_nome.delete(0, "end")
    entry_preco.delete(0, "end")
    entry_quantidade.delete(0, "end")


# Bloco 6: Função para consultar produtos salvos
def consultar_produtos():
    conexao, cursor = conectar()  #[cite: 22]
    cursor.execute("SELECT * FROM produtos")  #[cite: 22]
    itens = cursor.fetchall()  #[cite: 22]
    conexao.close()  #[cite: 22]

    caixa_resultados.configure(state="normal")  #[cite: 22]
    caixa_resultados.delete("1.0", "end")  #[cite: 22]

    for linha in itens:  #[cite: 22]
        texto = f"Produto: {linha[0]:<15} | Preço: R$ {linha[1]:>6.2f} | Estoque: {linha[2]}\n"  #[cite: 22]
        caixa_resultados.insert("end", texto)  #[cite: 22]

    caixa_resultados.configure(state="disabled")  #[cite: 22]


# UI: Campos de Entrada
lbl_nome = ctk.CTkLabel(janela, text="Nome do Produto:")
lbl_nome.pack(pady=(10, 0))
entry_nome = ctk.CTkEntry(janela, width=300)
entry_nome.pack(pady=5)

lbl_preco = ctk.CTkLabel(janela, text="Preço (R$):")
lbl_preco.pack(pady=(10, 0))
entry_preco = ctk.CTkEntry(janela, width=300)
entry_preco.pack(pady=5)

lbl_quantidade = ctk.CTkLabel(janela, text="Quantidade:")
lbl_quantidade.pack(pady=(10, 0))
entry_quantidade = ctk.CTkEntry(janela, width=300)
entry_quantidade.pack(pady=5)

# Bloco 7: Botões de Ação[cite: 21]
btn_salvar = ctk.CTkButton(
    janela,
    text="Salvar Produto",
    fg_color="green",
    command=cadastrar_produto,  #[cite: 21]
)
btn_salvar.pack(pady=15)  #[cite: 21]

btn_consultar = ctk.CTkButton(
    janela,
    text="Consultar Produtos Salvos",
    command=consultar_produtos,  #[cite: 21]
)
btn_consultar.pack(pady=10)  #[cite: 21]

# Área para exibição dos resultados da consulta
caixa_resultados = ctk.CTkTextbox(janela, width=420, height=180)
caixa_resultados.pack(pady=10)
caixa_resultados.configure(state="disabled")

# Inicialização da aplicação
janela.mainloop()