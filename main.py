import requests
import random
import datetime
import asyncio
import nest_asyncio

nest_asyncio.apply()

TOKEN = "TOKEN DISCORD"

# IDs dos canais e intervalo de tempo de espera
canais = [
    {"id": "880415511173804083", "nome": "Primeiro Chat", "url_enviar": "https://discord.com/api/v9/channels/IDCANAL/messages", "tempo_min": 60, "tempo_max": 180},
    {"id": "896616891206995978", "nome": "Segundo Chat", "url_enviar": "https://discord.com/api/v9/channels/IDCANAL/messages", "tempo_min": 60, "tempo_max": 300}
]

emojis = ["😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😊"]

headers = {
    "Authorization" : TOKEN
}

def log_message(message):
    agora_utc3 = datetime.datetime.now() - datetime.timedelta(hours=3)
    print(f"{agora_utc3.strftime('%Y-%m-%d %H:%M:%S')} - {message}")

async def enviar_mensagem(canal):
    while True:
        agora_utc3 = datetime.datetime.now() - datetime.timedelta(hours=3)
        
        # Verificar se é hora de parar o envio de mensagens
        if agora_utc3.hour >= 22 or agora_utc3.hour < 7:
            log_message("Script pausado. Próximo reinício entre 7:00 e 10:00.")
            reinicio = agora_utc3.replace(hour=random.randint(7, 9), minute=random.randint(0, 59), second=random.randint(0, 59))
            tempo_espera = (reinicio - agora_utc3).total_seconds()
            await asyncio.sleep(tempo_espera)
            log_message("Reiniciando o script.")
            continue
        
        proximo_horario = agora_utc3 + datetime.timedelta(seconds=random.randint(canal["tempo_min"], canal["tempo_max"]))
        log_message(f"Próxima mensagem para {canal['nome']} será enviada em {proximo_horario.hour}:{proximo_horario.minute}:{proximo_horario.second}")

        # Calcular o tempo até a próxima mensagem
        tempo_espera = (proximo_horario - agora_utc3).total_seconds()
        await asyncio.sleep(tempo_espera - 5)  # Dormir até 5 segundos antes da próxima mensagem
        
        # Contagem regressiva de 5 segundos
        log_message(f"A mensagem do {canal['nome']} será enviada em 5 segundos!")
        for i in range(5, 0, -1):
            log_message(str(i))
            await asyncio.sleep(1)
        
        # Enviar a mensagem
        payload = {
            "content" : random.choice(emojis)
        }
        res_enviar = requests.post(canal["url_enviar"], json=payload, headers=headers)
        if res_enviar.status_code == 200:
            log_message(f"Mensagem enviada com sucesso para o canal {canal['nome']}!")
        else:
            log_message(f"Falha ao enviar mensagem para o canal {canal['nome']}. Status code: {res_enviar.status_code}")

async def main():
    tasks = [enviar_mensagem(canal) for canal in canais]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    log_message("Iniciando o script")
    asyncio.run(main())