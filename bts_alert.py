import requests
import time
import asyncio
from telegram import Bot

TM_API_KEY = "jxPyLtP0TLrgfnILSm0FclwyG7vf9aAK"
TG_TOKEN   = "8786809670:AAGv4mqPNcLfTFZlOLdgAg7VtUoaX8kyD7A"
TG_CHAT_ID = "8662544541"
INTERVALO  = 60

EVENTOS = {
    "BTS CDMX - 7 mayo":  "1Av8Z_eGkn-czaI",
    "BTS CDMX - 9 mayo":  "1Av8Z_eGknN5FK4",
    "BTS CDMX - 10 mayo": "1Av8Z_eGknN5bK9",
}

def verificar_evento(event_id):
    url = f"https://app.ticketmaster.com/discovery/v2/events/{event_id}"
    r = requests.get(url, params={"apikey": TM_API_KEY, "locale": "es-mx"}, timeout=10)
    data = r.json()
    status = data.get("dates", {}).get("status", {}).get("code", "offsale")
    tiene_precio = "_embedded" in data and "priceRanges" in data
    print(f"Status: {status}, tiene_precio: {tiene_precio}")
    return status == "onsale" and tiene_precio

async def enviar_mensaje(bot, chat_id, texto):
    await bot.send_message(chat_id=chat_id, text=texto)

async def main():
    bot = Bot(token=TG_TOKEN)
    print("Monitoreando boletos de BTS en Mexico...")
    notificados = {nombre: False for nombre in EVENTOS}

    while True:
        for nombre, event_id in EVENTOS.items():
            try:
                disponible = verificar_evento(event_id)
                if disponible and not notificados[nombre]:
                    await enviar_mensaje(
                        bot, TG_CHAT_ID,
                        f"🚨 BOLETOS DISPONIBLES!\n{nombre}\n\n"
                        f"👉 https://www.ticketmaster.com.mx/event/{event_id}"
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
