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
    """Esconde todos os frames e mostra o frame desejado."""
    for frame in [frame_inicial, frame_equipas, frame_quiz, frame_resultados]:
        if frame is not None: 
            frame.pack_forget() 

    if frame_a_mostrar is not None:
        frame_a_mostrar.pack(expand=True, fill="both") 

def setup_resultados_frame():
    """Configura e mostra o frame de resultados."""
    global frame_resultados
    if frame_resultados is None:
        frame_resultados = ttk.Frame(root, padding=20)
        
        ttk.Label(frame_resultados, text="Pontuações Finais", font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        
        pontuacoes_inner_frame = ttk.Frame(frame_resultados)
        pontuacoes_inner_frame.pack(pady=10)

        for i, equipa in enumerate(equipas):
            ttk.Label(pontuacoes_inner_frame, text=f"{equipa}: {pontuacoes[i]} pontos").pack()

        # Adiciona a mensagem do vencedor
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
    """Atualiza a interface com a pergunta atual."""
    global indice_pergunta, equipa_atual, pergunta_var, opcoes_var, botoes_opcoes, label_equipa

    print(f"DEBUG: Função mostrar_pergunta() iniciada para a pergunta índice {indice_pergunta}.")
    
    if indice_pergunta >= len(perguntas): 
        print("DEBUG: Índice de pergunta fora dos limites. Quiz deveria ter terminado.")
        setup_resultados_frame() 
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
    """Verifica a resposta e avança para a próxima pergunta/equipa."""
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

    root.after(1500, avancar) 

def avancar():
    """Lógica para avançar para a próxima pergunta ou terminar o quiz."""
    global indice_pergunta, equipa_atual 

    indice_pergunta += 1
    equipa_atual = (equipa_atual + 1) % len(equipas)

    if indice_pergunta < len(perguntas):
        mostrar_pergunta()
    else:
        setup_resultados_frame() 
        
        
def setup_quiz_frame():
    """Configura o frame principal do quiz."""
    global frame_quiz, pergunta_var, opcoes_var, botoes_opcoes, label_equipa

    if frame_quiz is None: 
        frame_quiz = ttk.Frame(root, padding=30, relief="ridge")

        pergunta_var = ttk.StringVar()
        ttk.Label(frame_quiz, textvariable=pergunta_var, wraplength=550, font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))

        opcoes_var = ttk.StringVar()
        botoes_opcoes.clear() 
        for _ in range(4):
            botao = ttk.Radiobutton(
                frame_quiz, variable=opcoes_var, value="", text="", style="TRadiobutton"
            )
            botao.pack(anchor="w", pady=5)
            botoes_opcoes.append(botao)

        label_equipa = ttk.Label(frame_quiz, text="", font=("Segoe UI", 12, "italic"))
        label_equipa.pack(pady=15)

        ttk.Button(frame_quiz, text="Confirmar Resposta", command=responder).pack(pady=10)
    
    mostrar_frame(frame_quiz)
    mostrar_pergunta() 

def setup_equipas_frame(num_equipas):
    """Configura e mostra o frame para inserção dos nomes das equipas."""
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
    """Configura e mostra o frame inicial para o número de equipas."""
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
    root = ttk.Window(themename="minty")
    root.title("Quiz de Cultura Geral")
    root.geometry("650x450") 
    setup_inicial_frame() 
    root.mainloop() 