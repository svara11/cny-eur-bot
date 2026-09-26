import os
import requests
from datetime import datetime

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID        = os.environ["CHAT_ID"]

TARGET    = 0.1294
TOLERANCE = 0.0002

API_URL = "https://api.frankfurter.app/latest?from=CNY&to=EUR"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
    r.raise_for_status()

def main():
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    data = r.json()
    rate = data["rates"]["EUR"]
    date = data["date"]

    now = datetime.utcnow().strftime("%d.%m.%Y %H:%M UTC")
    print(f"[{now}] {date}: 1 CNY = {rate:.5f} EUR")

    if abs(rate - TARGET) <= TOLERANCE:
        send_telegram(
            f"🔔 Курс достиг цели!\n"
            f"1 CNY = {rate:.5f} EUR ({date})\n"
            f"Цель: {TARGET}"
        )
        print("Уведомление отправлено в Telegram.")
    else:
        print("Курс ещё не достиг цели. Уведомление не отправлено.")

if __name__ == "__main__":
    main()
