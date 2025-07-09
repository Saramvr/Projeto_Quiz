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
resposta_selecionada_idx = -1


pergunta_var = None
opcoes_var = None
botoes_opcoes = []
label_equipa = None


root = None


frame_inicial = None
frame_equipas = None
frame_quiz = None
frame_resultados = None



def mostrar_frame(frame_a_mostrar):
    
    for frame in [frame_inicial, frame_equipas, frame_quiz, frame_resultados]:
        if frame is not None: 
            frame.pack_forget() 

    if frame_a_mostrar is not None:
        frame_a_mostrar.pack(expand=True, fill="both") 

def setup_resultados_frame():
    
    global frame_resultados
    if frame_resultados is None:
        frame_resultados = ttk.Frame(root, padding=20)
        
        ttk.Label(frame_resultados, text="Pontuações Finais", font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        
        pontuacoes_inner_frame = ttk.Frame(frame_resultados)
        pontuacoes_inner_frame.pack(pady=10)

        for i, equipa in enumerate(equipas):
            ttk.Label(pontuacoes_inner_frame, text=f"{equipa}: {pontuacoes[i]} pontos").pack()

        
        max_pontos = max(pontuacoes) if pontuacoes else 0
        vencedores = [equipas[i] for i, p in enumerate(pontuacoes) if p == max_pontos]
        
        if len(vencedores) == 1:
            msg = f"A equipa vencedora é: {vencedores[0]}!"
        elif vencedores:
            msg = "Empate entre: " + ", ".join(vencedores) + "!"
        else:
            msg = "Nenhuma equipa jogou."

        ttk.Label(frame_resultados, text=msg, font=("Segoe UI", 12, "italic"), padding=10).pack(pady=20)

        ttk.Button(frame_resultados, text="Sair", command=root.destroy).pack(pady=10)

    mostrar_frame(frame_resultados)

def mostrar_pergunta():
    global indice_pergunta, equipa_atual, pergunta_var, botoes_opcoes, label_equipa, resposta_selecionada_idx

    if indice_pergunta >= len(perguntas):
        setup_resultados_frame()
        return
    
    resposta_selecionada_idx = -1

    pergunta_atual = perguntas[indice_pergunta]
    pergunta_var.set(pergunta_atual["pergunta"])

    opcoes = pergunta_atual["opcoes"].copy()
    random.shuffle(opcoes)

    for i in range(4):
        botoes_opcoes[i]["text"] = opcoes[i]
        botoes_opcoes[i]["state"] = "normal"
        botoes_opcoes[i].config(bootstyle="secondary")

    label_equipa.config(text=f"É a vossa vez de jogar: {equipas[equipa_atual]}")
    print("DEBUG: Label equipa atualizado para:", label_equipa["text"])

    
def selecionar_resposta(idx):
    global resposta_selecionada_idx
    resposta_selecionada_idx = idx

    for i, botao in enumerate(botoes_opcoes):
        if i == idx:
            botao.config(bootstyle="warning")
        else:
            botao.config(bootstyle="secondary")

def responder(resposta_idx):
    global indice_pergunta, equipa_atual, resposta_selecionada_idx

    pergunta_atual = perguntas[indice_pergunta]
    resposta_certa = pergunta_atual["resposta"]
    resposta_escolhida = botoes_opcoes[resposta_idx]["text"]

    
  
    for i, botao in enumerate(botoes_opcoes):
        if botao["text"] == resposta_certa:
            botao.config(bootstyle="success")
        elif i == resposta_selecionada_idx and resposta_escolhida != resposta_certa:
            botao.config(bootstyle="danger")
        else:
            botao.config(bootstyle="secondary")

    root.after(1500, lambda: [botao.config(state="disabled") for botao in botoes_opcoes])
    
    if resposta_escolhida == resposta_certa:
        pontuacoes[equipa_atual] += 1

    
    
    def desativar_e_avancar(correta):
        for botao in botoes_opcoes:
            botao.config(state="disabled")
        if correta:
            pontuacoes[equipa_atual] += 1
            
    root.after(1500, desativar_e_avancar)
    
    root.after(2000, avancar)

def avancar():
    
    global indice_pergunta, equipa_atual 

    indice_pergunta += 1
    equipa_atual = (equipa_atual + 1) % len(equipas)

    if indice_pergunta < len(perguntas):
        mostrar_pergunta()
    else:
        setup_resultados_frame() 
        
        
def setup_quiz_frame():
    global frame_quiz, pergunta_var, botoes_opcoes, label_equipa

    if frame_quiz is None:
        frame_quiz = ttk.Frame(root, padding=30, relief="ridge")

        pergunta_var = ttk.StringVar()
        ttk.Label(frame_quiz, textvariable=pergunta_var, wraplength=550, font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))

        botoes_opcoes.clear()

        for i in range(4):
            botao = ttk.Button(frame_quiz, text="", command=lambda idx=i: selecionar_resposta(idx))
            botao.pack(fill="x", pady=5)
            botoes_opcoes.append(botao)
            
        ttk.Button(frame_quiz, text="Confirmar Resposta", command=lambda: responder(resposta_selecionada_idx)).pack(pady=10)

        label_equipa = ttk.Label(frame_quiz, text="", font=("Segoe UI", 12, "italic"))
        label_equipa.pack(pady=15)

    mostrar_frame(frame_quiz)
    mostrar_pergunta()

def setup_equipas_frame(num_equipas):
    
    global frame_equipas, equipas, pontuacoes

    
    if frame_equipas:
        for widget in frame_equipas.winfo_children():
            widget.destroy()
    else:
        frame_equipas = ttk.Frame(root, padding=20)

    ttk.Label(frame_equipas, text="Insere o nome de cada equipa:", font=("Segoe UI", 14, "bold")).pack(pady=(0, 10))
    entradas = []

    for i in range(num_equipas):
        ttk.Label(frame_equipas, text=f"Equipa {i+1}:").pack(anchor="w", pady=(5, 0))
        entrada = ttk.Entry(frame_equipas, width=30)
        entrada.pack(pady=5)
        entradas.append(entrada)

    def confirmar_nomes():
        global equipas, pontuacoes
        nomes = [e.get().strip() for e in entradas]
        if "" in nomes:
            messagebox.showwarning("Atenção", "Todas as equipas devem ter um nome.")
        else:
            equipas = nomes
            pontuacoes = [0] * len(equipas)
            print(f"DEBUG: Equipas definidas: {equipas}")
            setup_quiz_frame() 
            
    ttk.Button(frame_equipas, text="Iniciar Quiz", command=confirmar_nomes).pack(pady=20)
    mostrar_frame(frame_equipas)

def setup_inicial_frame():
    
    global frame_inicial

    frame_inicial = ttk.Frame(root, padding=20)

    ttk.Label(frame_inicial, text="Quantas equipas vão jogar?", font=("Segoe UI", 13, "bold")).pack(pady=10)
    entry_num_equipas = ttk.Entry(frame_inicial, width=5, justify="center")
    entry_num_equipas.pack(pady=5)

    def iniciar_jogo_callback():
        try:
            num = int(entry_num_equipas.get())
            if num < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Insere um número válido de equipas (mínimo 1).")
            return
        setup_equipas_frame(num)

    ttk.Button(frame_inicial, text="Começar Quiz", command=iniciar_jogo_callback).pack(pady=20)
    mostrar_frame(frame_inicial)


if __name__ == "__main__":
    root = ttk.Window(themename="solar")
    root.title("Quiz de Cultura Geral")
    root.geometry("650x450") 
    setup_inicial_frame() 
    root.mainloop() 