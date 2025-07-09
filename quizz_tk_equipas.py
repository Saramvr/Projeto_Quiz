import tkinter as tk
from tkinter import ttk, messagebox
import random
from perguntas import perguntas



equipas = []
pontuacoes = []

def aplicar_estilo(janela):
    style = ttk.Style(janela)
    style.theme_use("clam")
    style.configure("TLabel", font=("Segoe UI", 12))
    style.configure("TButton", font=("Segoe UI", 12), padding=6)
    style.configure("TRadiobutton", font=("Segoe UI", 11))
    janela.configure(bg="#f7f9fc")

def mostrar_resultados():
    janela = tk.Tk()
    janela.title("Resultado Final")
    janela.geometry("400x300")
    janela.configure(bg="#eaf6ff")

    frame = ttk.Frame(janela, padding=20)
    frame.pack(expand=True)

    ttk.Label(frame, text="Pontuações Finais", font=("Segoe UI", 14, "bold")).pack(pady=10)
    for i, equipa in enumerate(equipas):
        ttk.Label(frame, text=f"{equipa}: {pontuacoes[i]} pontos").pack()

    max_pontos = max(pontuacoes)
    vencedores = [equipas[i] for i, p in enumerate(pontuacoes) if p == max_pontos]
    if len(vencedores) == 1:
        msg = f"A equipa vencedora é: {vencedores[0]}"
    else:
        msg = "Empate entre: " + ", ".join(vencedores)

    ttk.Label(frame, text=msg, font=("Segoe UI", 12, "italic"), padding=10).pack(pady=20)
    janela.mainloop()

def iniciar_quiz():
    global indice_pergunta, equipa_atual, janela_quiz, botoes_opcoes, opcoes_var, pergunta_var, label_equipa
    indice_pergunta = 0
    equipa_atual = 0

    janela_quiz = tk.Tk()
    janela_quiz.title("Quiz de Cultura Geral")
    janela_quiz.geometry("650x450")
    janela_quiz.configure(bg="#d6bbd3")

    frame = ttk.Frame(janela_quiz, padding=30, relief="ridge")
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    pergunta_var = tk.StringVar()
    ttk.Label(frame, textvariable=pergunta_var, wraplength=550, font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))

    opcoes_var = tk.StringVar()
    botoes_opcoes = []

    for _ in range(4):
        botao = tk.Radiobutton(
            frame, variable=opcoes_var, value="", text="", font=("Segoe UI", 12), anchor="w",
            justify="left", width=50, wraplength=500, bg=janela_quiz.cget("bg"), indicatoron=1
        )
        botao.pack(anchor="w", pady=5)
        botoes_opcoes.append(botao)

    label_equipa = ttk.Label(frame, text="", font=("Segoe UI", 12, "italic"))
    label_equipa.pack(pady=15)

    def mostrar_pergunta():
        pergunta_atual = perguntas[indice_pergunta]
        pergunta_var.set(pergunta_atual["pergunta"])
        opcoes = pergunta_atual["opcoes"].copy()
        random.shuffle(opcoes)

        opcoes_var.set("")  # limpa seleção

        for i in range(4):
            botoes_opcoes[i]["text"] = opcoes[i]
            botoes_opcoes[i]["value"] = opcoes[i]
            botoes_opcoes[i]["state"] = "normal"
            botoes_opcoes[i].config(bg=janela_quiz.cget("bg"), fg="black")

        label_equipa.config(text=f"É a vossa vez de jogar: {equipas[equipa_atual]}")

    def responder():
        if opcoes_var.get() == "":
            messagebox.showwarning("Aviso", "Seleciona uma resposta.")
            return

        resposta_certa = perguntas[indice_pergunta]["resposta"]
        resposta_escolhida = opcoes_var.get()

        for botao in botoes_opcoes:
            botao.config(state="disabled")

        for botao in botoes_opcoes:
            if botao["value"] == resposta_certa:
                botao.config(bg="#d4eeda", fg="green")
            elif botao["value"] == resposta_escolhida:
                botao.config(bg="#f8cace", fg="red")

        if resposta_escolhida == resposta_certa:
            pontuacoes[equipa_atual] += 1

        janela_quiz.after(1500, avancar)

    def avancar():
        global indice_pergunta, equipa_atual
        indice_pergunta += 1
        equipa_atual = (equipa_atual + 1) % len(equipas)

        if indice_pergunta < len(perguntas):
            mostrar_pergunta()
        else:
            janela_quiz.destroy()
            mostrar_resultados()

    mostrar_pergunta()

    botao_confirmar = tk.Button(frame, text="Confirmar Resposta", font=("Segoe UI", 12, "bold"), bg="#cc0099", fg="white", command=responder)
    botao_confirmar.pack(pady=10)

    janela_quiz.mainloop()

def criar_interface_equipas(num):
    janela = tk.Tk()
    janela.title("Nomes das Equipas")
    janela.geometry("400x500")
    aplicar_estilo(janela)

    frame = ttk.Frame(janela, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Insere o nome de cada equipa:", font=("Segoe UI", 14, "bold")).pack(pady=(0, 10))
    entradas = []

    for i in range(num):
        ttk.Label(frame, text=f"Equipa {i+1}:").pack(anchor="w", pady=(5, 0))
        entrada = ttk.Entry(frame, width=30)
        entrada.pack(pady=5)
        entradas.append(entrada)

    def confirmar():
        nomes = [e.get().strip() for e in entradas]
        if "" in nomes:
            messagebox.showwarning("Atenção", "Todas as equipas devem ter um nome.")
        else:
            global equipas, pontuacoes
            equipas = nomes
            pontuacoes = [0] * len(equipas)
            janela.destroy()
            iniciar_quiz()

    ttk.Button(frame, text="Iniciar Quiz", command=confirmar).pack(pady=20)
    janela.mainloop()

def iniciar_jogo():
    try:
        num = int(entry_num_equipas.get())
        if num < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Insere um número válido de equipas.")
        return
    janela_inicial.destroy()
    criar_interface_equipas(num)

janela_inicial = tk.Tk()
janela_inicial.title("Configuração do Quiz")
janela_inicial.geometry("350x250")
aplicar_estilo(janela_inicial)

frame_inicial = ttk.Frame(janela_inicial, padding=20)
frame_inicial.pack(expand=True)

ttk.Label(frame_inicial, text="Quantas equipas vão jogar?", font=("Segoe UI", 13, "bold")).pack(pady=10)
entry_num_equipas = ttk.Entry(frame_inicial, width=5, justify="center")
entry_num_equipas.pack(pady=5)

ttk.Button(frame_inicial, text="Começar Quiz", command=iniciar_jogo).pack(pady=20)

janela_inicial.mainloop()

