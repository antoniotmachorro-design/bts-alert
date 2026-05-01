import requests
import time
import asyncio
from telegram import Bot

TG_TOKEN   = "8786809670:AAGv4mqPNcLfTFZlOLdgAg7VtUoaX8kyD7A"
TG_CHAT_ID = "8662544541"
INTERVALO  = 60

EVENTOS = {
    "BTS CDMX - 7 mayo":  "https://www.ticketmaster.com.mx/bts-world-tour-arirang-in-mexico-ciudad-de-mexico-07-05-2026/event/1400642AA1B78268",
    "BTS CDMX - 9 mayo":  "https://www.ticketmaster.com.mx/bts-world-tour-arirang-in-mexico-ciudad-de-mexico-09-05-2026/event/1400642AA32C84D5",
    "BTS CDMX - 10 mayo": "https://www.ticketmaster.com.mx/bts-world-tour-arirang-in-mexico-ciudad-de-mexico-10-05-2026/event/1400642AA32D84D7",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

async def enviar_mensaje(bot, chat_id, texto):
    await bot.send_message(chat_id=chat_id, text=texto)

def hay_boletos(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        texto = r.text
        no_disponible = (
            "Boletos no disponibles por INTERNET" in texto or
            "ya no existe" in texto or
            "no existe en nuestra base de datos" in texto
        )
        return not no_disponible
    except:
        return False

async def main():
    bot = Bot(token=TG_TOKEN)
    print("Monitoreando boletos de BTS en Mexico...")
    notificados = {nombre: False for nombre in EVENTOS}

    while True:
        for nombre, url in EVENTOS.items():
            try:
                disponible = hay_boletos(url)
                if disponible and not notificados[nombre]:
                    await enviar_mensaje(
                        bot, TG_CHAT_ID,
                        f"🚨 BOLETOS DISPONIBLES!\n{nombre}\n\n👉 {url}"
                    )
                    notificados[nombre] = True
                    print(f"Alerta enviada: {nombre}")
                elif not disponible and notificados[nombre]:
                    notificados[nombre] = False
                    print(f"Sin boletos: {nombre}")
                else:
                    print(f"Revisando: {nombre} - disponible: {disponible}")
            except Exception as e:
                print(f"Error en {nombre}: {e}")
        time.sleep(INTERVALO)

if __name__ == "__main__":
    asyncio.run(main())
