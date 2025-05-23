import pywhatkit
from datetime import datetime

numero = "+5514996609040"
mensagem = "Teste de mensagem automática pelo pywhatkit."
agora = datetime.now()
hora = agora.hour
minuto = agora.minute + 2  # Adicione pelo menos 2 minutos para abrir, logar e enviar

pywhatkit.sendwhatmsg(numero, mensagem, hora, minuto, wait_time=30, tab_close=True)