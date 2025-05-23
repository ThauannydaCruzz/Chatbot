import os
import json
import random
from datetime import datetime
import pywhatkit as kit
from rapidfuzz import process, fuzz
try:
    from googlesearch import search
except ImportError:
    search = None

# Utilitários de leitura e escrita
def ler_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

# Arquivos de dados
FAQ_FILE = "faq_memoria.json"
AMEACAS_FILE = "ameacas_explicacoes_solucoes.json"
SITES_FILE = "sites_maliciosos.json"
LOGS_FILE = "logs.json"

faq = ler_json(FAQ_FILE)
ameacas = ler_json(AMEACAS_FILE)
sites = ler_json(SITES_FILE)
logs = ler_json(LOGS_FILE)
historico = []

# Respostas básicas
cumprimentos = [
    "Oi! Tudo bem por aí? 😊",
    "Olá! Como posso ajudar hoje?",
    "E aí, tranquilo? Em que posso te ajudar?"
]
despedidas = [
    "Tchau! Fique seguro(a)! 👋",
    "Até mais! Proteja seus dados! 🛡️",
    "Se cuida! Qualquer coisa, só chamar. 😄"
]
respostas_basicas = {
    "como você está": [
        "Estou ótimo, obrigado por perguntar! E você?",
        "Funcionando a todo vapor! E contigo?",
        "De boas, sempre pronto pra ajudar."
    ],
    "quem é você": [
        "Sou o Aegis, especialista em segurança virtual! Pronto para proteger você e sua loja. 😎",
        "Eu sou o Aegis, seu consultor digital para cibersegurança.",
        "Aegis na área! Seu escudeiro virtual contra ameaças."
    ],
    "qual seu nome": [
        "Meu nome é Aegis!",
        "Pode me chamar de Aegis.",
        "Sou o Aegis, prazer!"
    ],
    "qual sua função": [
        "Minha missão é ajudar você a entender e se proteger de ameaças digitais, explicar boas práticas, analisar riscos e orientar em emergências.",
        "Sou seu assistente especialista em cibersegurança, pronto para explicar, proteger e agir junto com sua equipe.",
    ],
    "obrigado": [
        "Por nada! 😉",
        "Disponha!",
        "Tamo junto!"
    ],
    "qual o dia de hoje": [
        f"Hoje é {datetime.now().strftime('%d/%m/%Y')}.",
        f"Estamos no dia {datetime.now().strftime('%d/%m/%Y')}.",
        f"O calendário diz: {datetime.now().strftime('%d/%m/%Y')}."
    ],
    "que dia é hoje": [
        f"Hoje é {datetime.now().strftime('%d/%m/%Y')}.",
        f"Estamos no dia {datetime.now().strftime('%d/%m/%Y')}.",
        f"O calendário diz: {datetime.now().strftime('%d/%m/%Y')}."
    ],
    "que horas são": [
        f"Agora são {datetime.now().strftime('%H:%M')} (horário do servidor).",
        "Deixa eu ver... são " + datetime.now().strftime('%H:%M') + "!",
        f"Relógio marcando: {datetime.now().strftime('%H:%M')}."
    ],
    "qual a temperatura": [
        "Eu ainda não sei ver previsão do tempo 😅, mas posso te ajudar com cibersegurança!",
        "Ainda não tenho acesso à temperatura, mas posso proteger seus dados!",
        "Se quiser saber sobre ameaças, tô afiado! Mas temperatura ainda não é comigo."
    ],
    "como está o tempo": [
        "Infelizmente não consigo ver o clima lá fora, só o clima virtual aqui! 🌤️",
        "Tempo? Só se for o tempo de resposta dos meus alertas 😁",
        "Ainda não sei o clima, mas posso te atualizar sobre ameaças digitais!"
    ]
}

def resposta_varias(opcoes):
    return random.choice(opcoes)

def responder(msg):
    print(f"🛡️  Aegis: {msg}")
    historico.append({"bot": msg})
    if len(historico) > 20:
        historico.pop(0)

def verificar_basico(pergunta):
    pergunta_low = pergunta.lower().strip()
    for chave, respostas in respostas_basicas.items():
        if chave in pergunta_low:
            return resposta_varias(respostas)
    if any(x in pergunta_low for x in ["oi", "olá", "bom dia", "boa tarde", "boa noite"]):
        return resposta_varias(cumprimentos)
    if any(x in pergunta_low for x in ["tchau", "adeus", "até mais", "falou", "até logo"]):
        return resposta_varias(despedidas)
    return None

def fuzzy_search(query, data, key):
    termos = [item.get(key, "") for item in data]
    if not termos:
        return None, None
    match, score, idx = process.extractOne(query, termos, scorer=fuzz.token_sort_ratio)
    if score > 70:
        return data[idx], score
    return None, None

def buscar_resposta_faq(pergunta):
    perguntas = [item["pergunta"] for item in faq]
    if not perguntas:
        return None
    match, score, idx = process.extractOne(pergunta, perguntas, scorer=fuzz.token_sort_ratio)
    if score > 80:
        return faq[idx]["resposta"]
    return None

def pesquisar_google(query, num=2):
    links = []
    if search:
        try:
            for url in search(query, num_results=num, lang="pt"):
                links.append(url)
        except Exception as e:
            links.append(f"Erro ao pesquisar no Google: {e}")
    else:
        links.append("Nenhuma biblioteca de pesquisa instalada.")
    return links

def acionar_equipe_aegis(prioridade, resumo_situacao):
    numero = "+5514996609040"
    mensagem = f"""⚠️ Alerta Aegis [{prioridade.upper()} PRIORIDADE]:
Usuário solicitou atendimento presencial.

Resumo da situação:
{resumo_situacao}

Por favor, entrem em contato imediatamente conforme o nível de prioridade."""
    agora = datetime.now()
    hora = agora.hour
    minuto = agora.minute + 1
    kit.sendwhatmsg(numero, mensagem, hora, minuto, wait_time=10, tab_close=True)

def formatar_resumo_para_formal(situacao):
    resumo = situacao.strip().capitalize()
    frases = resumo.split('.')
    frases = [f.strip().capitalize() for f in frases if f.strip()]
    return '. '.join(frases) + '.'

emergencia_keywords = ["emergência", "socorro", "urgente", "atendimento presencial", "acidente", "chame a equipe", "preciso de ajuda presencial"]

saudacoes = [
    "Oi! Sou o Aegis 🛡️, especialista em cibersegurança. Pergunte sobre ameaças, golpes, proteção ou dúvidas de tecnologia!",
    "Olá! Posso explicar riscos, analisar suspeitas, sugerir boas práticas e te orientar em emergências digitais.",
    "E aí! Sou expert em segurança virtual, pronto pra proteger você e sua loja. O que precisa saber?"
]
respostas_nao_sei = [
    "Essa não sei de cabeça, mas estou pesquisando pra você!",
    "Ainda não sei responder isso, mas vou buscar a melhor resposta.",
    "Não tenho certeza, mas vou pesquisar na internet pra te ajudar."
]

responder(resposta_varias(saudacoes))
ultima_pergunta_sem_resposta = None

while True:
    user = input("Você: ").strip()
    if not user:
        continue
    historico.append({"user": user})
    if len(historico) > 20:
        historico.pop(0)

    # Despedida
    if any(x in user.lower() for x in ["sair", "exit", "quit", "tchau", "adeus"]):
        responder(resposta_varias(despedidas))
        break

    # Emergência
    if any(kw in user.lower() for kw in emergencia_keywords):
        responder("Entendi que você pode precisar de atendimento presencial.")
        responder("Qual o nível de prioridade do seu pedido?\n[1] Baixo\n[2] Médio\n[3] Alto")
        prioridade_map = {"1": "Baixo", "2": "Médio", "3": "Alto"}
        prioridade = ""
        while prioridade not in prioridade_map:
            prioridade = input("Escolha o nível de prioridade (1/2/3): ").strip()
        prioridade_str = prioridade_map[prioridade]
        responder(f"Por favor, explique brevemente a situação. Quanto mais detalhes, melhor para a equipe atender:")
        situacao = input("Explique a situação: ").strip()
        resumo_formal = formatar_resumo_para_formal(situacao)
        if prioridade_str == "Alto":
            responder("Situação entendida como ALTA PRIORIDADE. Estou acionando a equipe Aegis agora mesmo!")
            acionar_equipe_aegis(prioridade_str, resumo_formal)
            responder("Equipe notificada. Em breve alguém deve entrar em contato. Precisa de mais alguma coisa?")
        else:
            responder(f"Você marcou prioridade {prioridade_str}. Confirma o envio do chamado à equipe? (sim/não)")
            confirma = input("Você: ").strip().lower()
            if confirma in ["sim", "s", "confirmo"]:
                responder("Chamado enviado à equipe Aegis!")
                acionar_equipe_aegis(prioridade_str, resumo_formal)
                responder("Equipe notificada. Precisa de mais alguma coisa?")
            else:
                responder("Ok, não acionei a equipe. Posso ajudar de outra forma?")
        continue

    # Respostas básicas
    resposta_basico = verificar_basico(user)
    if resposta_basico:
        responder(resposta_basico)
        ultima_pergunta_sem_resposta = None
        continue

    # Perguntas sobre ameaças
    ameaca, score_a = fuzzy_search(user, ameacas, "Ameaças")
    if ameaca:
        responder(f"Sobre '{ameaca['Ameaças']}':\n{ameaca['Explicações das Ameaças']}\nSolução recomendada: {ameaca['Soluções']}")
        responder("Se quiser exemplos, dicas de proteção ou saber como agir, é só pedir!")
        ultima_pergunta_sem_resposta = None
        responder("Posso ajudar em mais alguma coisa? 😊")
        continue

    # Perguntas sobre sites maliciosos
    site, score_s = fuzzy_search(user, sites, "URL")
    if site:
        responder(f"Cuidado! O site {site['URL']} é malicioso: {site['Descrição']}")
        ultima_pergunta_sem_resposta = None
        responder("Mais alguma dúvida ou posso ajudar com outra coisa?")
        continue

    # Perguntas sobre logs
    if "hoje" in user.lower() or "recentes" in user.lower():
        hoje = datetime.now().strftime("%d/%b/%Y")
        logs_hoje = [l for l in logs if l.get("Data") == hoje]
        if logs_hoje:
            responder(f"Foram detectados {len(logs_hoje)} eventos hoje:")
            for log in logs_hoje[:5]:
                responder(f"- {log['Hora']} | IP: {log['IP Atacante']} | {', '.join(log['Títulos do Ataque'])}")
            if len(logs_hoje) > 5:
                responder(f"...e mais {len(logs_hoje)-5} eventos! Quer ver tudo?")
        else:
            responder("Por enquanto, tudo tranquilo nos registros de hoje.")
        ultima_pergunta_sem_resposta = None
        responder("Posso ajudar em mais alguma coisa? 😊")
        continue

    # Busca no FAQ
    resposta_faq = buscar_resposta_faq(user)
    if resposta_faq:
        responder(resposta_faq)
        ultima_pergunta_sem_resposta = None
        responder("Se quiser saber mais, só perguntar! 😁")
        continue

    # Pesquisa Google se não souber
    responder(resposta_varias(respostas_nao_sei))
    links_achados = pesquisar_google(user, num=2)
    if links_achados and links_achados[0]:
        responder("Pesquisei na web pra você, olha só o que achei:")
        for link in links_achados:
            responder(link)
    else:
        responder("Não encontrei nada relevante nas buscas, mas se quiser pode tentar perguntar de outro jeito!")

    ultima_pergunta_sem_resposta = user
    responder("Precisa de mais alguma coisa? Se sim, pode perguntar! 😉")