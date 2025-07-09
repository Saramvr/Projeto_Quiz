import random

perguntas = [
    {
        "pergunta": "Qual é o maior oceano do mundo?",
        "opcoes": ["Atlântico", "Índico", "Pacífico", "Ártico"],
        "resposta": "Pacífico"
    },
    {
        "pergunta": "Quem escreveu “Dom Quixote”?",
        "opcoes": ["Miguel de Cervantes", "William Shakespeare", "Victor Hugo", "Fernando Pessoa"],
        "resposta": "Miguel de Cervantes"
    },
    {
        "pergunta": "Em que país se encontra a cidade de Machu Picchu?",
        "opcoes": ["Chile", "Peru", "Bolívia", "Argentina"],
        "resposta": "Peru"
    },
    {
        "pergunta": "Qual é o símbolo químico do ouro?",
        "opcoes": ["Au", "Ag", "Fe", "Pb"],
        "resposta": "Au"
    },
    {
        "pergunta": "Quem pintou o teto da Capela Sistina?",
        "opcoes": ["Leonardo da Vinci", "Michelangelo", "Rafael", "Donatello"],
        "resposta": "Michelangelo"
    },
    {
        "pergunta": "Qual é a capital do Canadá?",
        "opcoes": ["Toronto", "Vancouver", "Montreal", "Ottawa"],
        "resposta": "Ottawa"
    },
    {
        "pergunta": "Em que ano ocorreu a queda do Muro de Berlim?",
        "opcoes": ["1987", "1989", "1991", "1993"],
        "resposta": "1989"
    },
    {
        "pergunta": "Qual é o planeta mais próximo do Sol?",
        "opcoes": ["Vénus", "Marte", "Mercúrio", "Júpiter"],
        "resposta": "Mercúrio"
    },
    {
        "pergunta": "Qual é o maior animal terrestre?",
        "opcoes": ["Rinoceronte", "Elefante-africano", "Hipopótamo", "Girafa"],
        "resposta": "Elefante-africano"
    },
    {
        "pergunta": "Quem foi o primeiro homem a pisar a Lua?",
        "opcoes": ["Yuri Gagarin", "Neil Armstrong", "Buzz Aldrin", "Michael Collins"],
        "resposta": "Neil Armstrong"
    },
    {
        "pergunta": "Qual a capital de França?",
        "opcoes": ["Londres", "Berlim", "Paris", "Madrid"],
        "resposta": "Paris"
    },
    {
        "pergunta": "Quem pintou a Mona Lisa?",
        "opcoes": ["Rembrant", "Leonardo Da Vinci", "Picasso", "Van Gogh"],
        "resposta": "Leonardo Da Vinci"
    },
    {
        "pergunta": "Quem escreveu 'Os Lusíadas'?",
        "opcoes": ["Fernando Pessoa", "José Saramago", "Camões", "Eça de Queirós"],
        "resposta": "Camões"
    },
    {
        "pergunta": "Em que ano o homem pisou a Lua pela primeira vez?",
        "opcoes": ["1969", "1972", "1958", "1980"],
        "resposta": "1969"
    },
    {
        "pergunta": "Qual é o símbolo químico da água?",
        "opcoes": ["CO2", "H2O", "NaCl", "O2"],
        "resposta": "H2O"
    },
    {
        "pergunta": "Qual o país com maior população do mundo?",
        "opcoes": ["China", "EUA", "Índia", "Brasil"],
        "resposta": "Índia"
    },
    {
        "pergunta": "Quantos planetas há no sistema solar?",
        "opcoes": ["8", "9", "7", "10"],
        "resposta": "8"
    },
    {
        "pergunta": "Qual é a língua mais falada no mundo?",
        "opcoes": ["Inglês", "Hindi", "Mandarim", "Espanhol"],
        "resposta": "Mandarim"
    }
]
random.shuffle(perguntas)