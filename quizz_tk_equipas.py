import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import random

try:
    from dados_perguntas import perguntas
    print(f"DEBUG: Perguntas carregadas com sucesso. Total: {len(perguntas)}")
    if not perguntas:
        print("DEBUG: A lista 'perguntas' está vazia!")
        messagebox.showerror("Erro", "O ficheiro de perguntas foi encontrado, mas a lista 'perguntas' está vazia!")
        exit()
except ImportError:
    messagebox.showerror("Erro", "O ficheiro 'dados_perguntas.py' não foi encontrado ou está mal formatado. Certifica-te de que está no mesmo diretório e tem a estrutura correta.")
    exit()
except Exception as e:
    messagebox.showerror("Erro", f"Ocorreu um erro inesperado ao carregar as perguntas: {e}")
    exit()


equipas = []
pontuacoes = []


indice_pergunta = 0
equipa_atual = 0
janela_quiz = None 
botoes_opcoes = []
opcoes_var = None
pergunta_var = None
label_equipa = None


def mostrar_resultados():
    janela = ttk.Window(themename="minty")
    janela.title("Resultado Final")
    janela.geometry("400x300")

    frame = ttk.Frame(janela, padding=20)
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="Pontuações Finais", font=("Segoe UI", 14, "bold")).pack(pady=10)
    for i, equipa in enumerate(equipas):
        ttk.Label(frame, text=f"{equipa}: {pontuacoes[i]} pontos").pack()

    
    if pontuacoes:
        max_pontos = max(pontuacoes)
        vencedores = [equipas[i] for i, p in enumerate(pontuacoes) if p == max_pontos]
        if len(vencedores) == 1:
            msg = f"A equipa vencedora é: {vencedores[0]}"
        else:
            msg = "Empate entre: " + ", ".join(vencedores)
    else:
        msg = "Nenhuma equipa jogou." 

    ttk.Label(frame, text=msg, font=("Segoe UI", 12, "italic"), padding=10).pack(pady=20)

    janela.mainloop()

def iniciar_quiz():
    
    global indice_pergunta, equipa_atual, janela_quiz, botoes_opcoes, opcoes_var, pergunta_var, label_equipa
    
    indice_pergunta = 0
    equipa_atual = 0
    print("DEBUG: Função iniciar_quiz() iniciada.")
    print(f"DEBUG: Total de perguntas disponíveis: {len(perguntas)}")

    
    janela_quiz = ttk.Window(themename="minty")
    janela_quiz.title("Quiz de Cultura Geral")
    janela_quiz.geometry("650x450")

    frame = ttk.Frame(janela_quiz, padding=30, relief="ridge")
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    pergunta_var = ttk.StringVar()
    ttk.Label(frame, textvariable=pergunta_var, wraplength=550, font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))

    opcoes_var = ttk.StringVar()
    botoes_opcoes = []

    for _ in range(4):
        botao = ttk.Radiobutton(
            frame, variable=opcoes_var, value="", text="", style="TRadiobutton"
            
        )
        botao.pack(anchor="w", pady=5)
        botoes_opcoes.append(botao)

    label_equipa = ttk.Label(frame, text="", font=("Segoe UI", 12, "italic"))
    label_equipa.pack(pady=15)

    def mostrar_pergunta():
        global indice_pergunta, equipa_atual, pergunta_var, opcoes_var, botoes_opcoes, label_equipa, perguntas
        print(f"DEBUG: Função mostrar_pergunta() iniciada para a pergunta índice {indice_pergunta}.")
        
        if indice_pergunta >= len(perguntas): 
            print("DEBUG: Índice de pergunta fora dos limites. Quiz deveria ter terminado.")
            janela_quiz.destroy() 
            mostrar_resultados()  
            return 
        
        pergunta_atual = perguntas[indice_pergunta]
        print("DEBUG: Pergunta atual a ser carregada:", pergunta_atual["pergunta"])
        pergunta_var.set(pergunta_atual["pergunta"])
        print("DEBUG: pergunta_var (depois de setar):", pergunta_var.get())

        opcoes = pergunta_atual["opcoes"].copy()
        random.shuffle(opcoes) 
        opcoes_var.set("")  
        print("DEBUG: Opções embaralhadas:", opcoes)

        for i in range(4):
            botoes_opcoes[i]["text"] = opcoes[i]
            botoes_opcoes[i]["value"] = opcoes[i]
            botoes_opcoes[i]["state"] = "normal"
            botoes_opcoes[i].config(fg="black")
            print(f"DEBUG: Botão {i} setado para: {botoes_opcoes[i]['text']}")

        label_equipa.config(text=f"É a vossa vez de jogar: {equipas[equipa_atual]}")
        print("DEBUG: Label equipa atualizado para:", label_equipa["text"])

    def responder():
        global indice_pergunta, equipa_atual 
        if opcoes_var.get() == "":
            messagebox.showwarning("Aviso", "Seleciona uma resposta.")
            return

        resposta_certa = perguntas[indice_pergunta]["resposta"]
        resposta_escolhida = opcoes_var.get()

        for botao in botoes_opcoes:
            botao.config(state="disabled")

        for botao in botoes_opcoes:
            if botao["value"] == resposta_certa:
                botao.config(fg="green")
            elif botao["value"] == resposta_escolhida:
                botao.config(fg="red")

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
    
    botao_confirmar = ttk.Button(frame, text="Confirmar Resposta", command=responder)
    botao_confirmar.pack(pady=10)

    janela_quiz.mainloop() 


def criar_interface_equipas(num):
    
    janela_equipas = ttk.Toplevel(janela_inicial, themename="minty") 
    janela_equipas.title("Nomes das Equipas")
    janela_equipas.geometry("400x500")
    
    
    janela_equipas.grab_set() 
    janela_inicial.withdraw() 
    
    frame = ttk.Frame(janela_equipas, padding=20)
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
            janela_equipas.destroy() 
            janela_inicial.deiconify() 
            
            

    ttk.Button(frame, text="Iniciar Quiz", command=confirmar).pack(pady=20)
    
    
    def ao_fechar_equipas():
        janela_equipas.destroy()
        janela_inicial.destroy() 
        exit() 

    janela_equipas.protocol("WM_DELETE_WINDOW", ao_fechar_equipas)
    janela_equipas.transient(janela_inicial) 

    janela_equipas.wait_window() 

    
    janela_inicial.destroy() 
    iniciar_quiz() 


def iniciar_jogo():
    try:
        num = int(entry_num_equipas.get())
        if num < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Insere um número válido de equipas.")
        return
    
    
    criar_interface_equipas(num) 
    

janela_inicial = ttk.Window(themename="minty")
janela_inicial.title("Configuração do Quiz")
janela_inicial.geometry("350x250")

frame_inicial = ttk.Frame(janela_inicial, padding=20)
frame_inicial.pack(expand=True)

ttk.Label(frame_inicial, text="Quantas equipas vão jogar?", font=("Segoe UI", 13, "bold")).pack(pady=10)
entry_num_equipas = ttk.Entry(frame_inicial, width=5, justify="center")
entry_num_equipas.pack(pady=5)

ttk.Button(frame_inicial, text="Começar Quiz", command=iniciar_jogo).pack(pady=20)

janela_inicial.mainloop() 