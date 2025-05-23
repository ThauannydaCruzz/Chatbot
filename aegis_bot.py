import random
import json
import os
from datetime import datetime
import pywhatkit
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import matplotlib.pyplot as plt

try:
    from googlesearch import search
except ImportError:
    search = None

CHAMADOS_FILE = "chamados.json"
LOGS_FILE = "logs.json"

dialogos = [
    "O que é phishing?",
    "Phishing é um golpe para roubar seus dados usando e-mails ou sites falsos.",
    "Como proteger meu site?",
    "Use senhas fortes, autenticação em dois fatores e mantenha tudo atualizado.",
    "Como sei se meu site foi atacado?",
    "Verifique notificações de sua plataforma, acessos suspeitos e mantenha monitoramento ativo.",
    "Quais boas práticas de segurança?",
    "Senhas fortes, autenticação em dois fatores, backups e cuidado com links e e-mails suspeitos.",
    "O que é DDoS?",
    "É um ataque que sobrecarrega seu site até ele sair do ar.",
    "Como criar senhas seguras?",
    "Misture letras, números e símbolos. Evite datas ou nomes comuns.",
    "É seguro usar Wi-Fi público?",
    "Evite acessar informações sensíveis e prefira usar uma VPN."
]
bot = ChatBot("AegisExpert", logic_adapters=["chatterbot.logic.BestMatch"])
ListTrainer(bot).train(dialogos)

def responder(msg):
    print(f"\n🛡️  Aegis: {msg}")

def pesquisar_google(query, num=2):
    links = []
    if search:
        try:
            for url in search(query, num_results=num, lang="pt"):
                links.append(url)
        except Exception:
            links.append("Erro ao pesquisar no Google.")
    else:
        links.append("Nenhuma biblioteca de pesquisa instalada.")
    return links

def acionar_equipe_aegis(prioridade, resumo):
    numero = "+5514996609040"
    mensagem = f"""⚠️ Alerta Aegis [{prioridade.upper()} PRIORIDADE]:
Usuário solicitou atendimento técnico.

Resumo do problema:
{resumo}

Por favor, entrem em contato conforme prioridade."""
    agora = datetime.now()
    hora = agora.hour
    minuto = agora.minute + 2
    responder("Acionando a equipe Aegis via WhatsApp...")
    pywhatkit.sendwhatmsg(numero, mensagem, hora, minuto, wait_time=30, tab_close=True)
    responder("Equipe notificada! Você receberá contato em breve.")

def salvar_chamado(prioridade, resumo, status="aberto"):
    chamado = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "prioridade": prioridade,
        "resumo": resumo,
        "status": status
    }
    if not os.path.exists(CHAMADOS_FILE):
        chamados = []
    else:
        with open(CHAMADOS_FILE, "r", encoding="utf-8") as f:
            chamados = json.load(f)
    chamados.append(chamado)
    with open(CHAMADOS_FILE, "w", encoding="utf-8") as f:
        json.dump(chamados, f, ensure_ascii=False, indent=2)

def registrar_pesquisa(usuario, pergunta, links):
    registro = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "usuario": usuario,
        "pergunta": pergunta,
        "links": links
    }
    if not os.path.exists("pesquisas.json"):
        pesquisas = []
    else:
        with open("pesquisas.json", "r", encoding="utf-8") as f:
            pesquisas = json.load(f)
    pesquisas.append(registro)
    with open("pesquisas.json", "w", encoding="utf-8") as f:
        json.dump(pesquisas, f, ensure_ascii=False, indent=2)

def gerar_relatorio_ataques():
    if not os.path.exists(LOGS_FILE):
        responder("Nenhum log de ataque registrado ainda.")
        return
    with open(LOGS_FILE, "r", encoding="utf-8") as f:
        logs = json.load(f)
    if not logs:
        responder("Nenhum log de ataque registrado ainda.")
        return
    print("\n=== Relatório de Ataques ===")
    for log in logs:
        print(f"{log['Data']} {log['Hora']} | IP: {log['IP Atacante']} | {', '.join(log['Títulos do Ataque'])}")
    # Gera gráfico simples por tipo de ataque
    tipos = {}
    for log in logs:
        for titulo in log.get("Títulos do Ataque", []):
            tipos[titulo] = tipos.get(titulo, 0) + 1
    if tipos:
        plt.bar(tipos.keys(), tipos.values())
        plt.title("Quantidade de Ataques por Tipo")
        plt.xlabel("Tipo de Ataque")
        plt.ylabel("Frequência")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig("grafico_ataques.png")
        plt.show()
        responder("Gráfico gerado: grafico_ataques.png")
    else:
        responder("Não foi possível gerar gráfico: tipos de ataque não identificados.")

def main():
    usuario = input("Seu nome ou login: ").strip() or "usuário"
    responder("Olá! Sou o assistente Aegis 👋. Tire dúvidas de segurança ou peça suporte técnico.")
    while True:
        user = input("\nVocê: ").strip()
        if not user:
            continue

        if user.lower() in ["sair", "exit", "quit", "tchau", "adeus"]:
            responder("Até mais! Fique seguro(a)!")
            break

        # Emergência/suporte para equipe técnica
        if any(palavra in user.lower() for palavra in ["ajuda", "suporte", "urgente", "emergência", "quero falar com a equipe", "atendimento"]):
            responder("Qual o nível de prioridade do seu chamado?\n[1] Baixo\n[2] Médio\n[3] Alto")
            prioridade_map = {"1": "Baixo", "2": "Médio", "3": "Alto"}
            prioridade = ""
            while prioridade not in prioridade_map:
                prioridade = input("Escolha (1/2/3): ").strip()
            prioridade_str = prioridade_map[prioridade]
            responder("Descreva resumidamente o problema ou dúvida para que a equipe possa te ajudar melhor:")
            resumo = input("Resumo: ").strip()
            responder(f"Confirmando: prioridade {prioridade_str}. Posso acionar a equipe? (sim/não)")
            confirma = input().strip().lower()
            if confirma in ["sim", "s"]:
                acionar_equipe_aegis(prioridade_str, resumo)
                salvar_chamado(prioridade_str, resumo)
            else:
                responder("Ok, chamado não enviado. Precisa de mais alguma coisa?")
            continue

        # Relatório de ataques/gráficos
        if "relatório de ataques" in user.lower() or "gráfico de ataques" in user.lower():
            gerar_relatorio_ataques()
            continue

        # Resposta do ChatterBot
        resposta = str(bot.get_response(user))
        if resposta and resposta.strip() and resposta.lower() != user.lower():
            responder(resposta)
            continue

        # Pesquisa no Google se não souber responder
        responder("Não tenho certeza. Pesquisando na internet para te ajudar...")
        links = pesquisar_google(user, num=2)
        responder("Veja o que encontrei:")
        for link in links:
            responder(link)
        registrar_pesquisa(usuario, user, links)

if __name__ == "__main__":
    main()