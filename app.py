# Gold RSI Alert Bot — Webhook Server
from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# ===== PASTE YOUR VALUES BELOW =====
TOKEN = "8656898499:AAGcRU-wilwH4uewA4Uru1mTecKWYpGKG0s"
CHAT_ID = "716797698"
# ===================================

def send_telegram(msg):
  url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
  payload = {
    "chat_id": CHAT_ID,
    "text": msg,
    "parse_mode": "HTML"
  }
  requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
  d = request.get_json(force=True)
  if not d:
    return jsonify({"error":"no data"}), 400

  sym = d.get("symbol", "XAUUSD")
  signal = d.get("signal", "SIGNAL")
  rsi = d.get("rsi", "N/A")
  price = d.get("price", "N/A")
  tf = d.get("tf", "15m")
  note = d.get("note", "")
  emoji = "🟢" if "OVERSOLD" in signal else "🔴"
  t = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

  msg = (
    f"{emoji} <b>{sym} — {signal}</b>\n\n"
    f"RSI: <b>{rsi}</b>\n"
    f"Price: <b>${price}</b>\n"
    f"Timeframe: <b>{tf}</b>\n"
    f"Time: {t}\n\n"
    f"<i>{note}</i>\n"
    "<i>Not financial advice.</i>"
  )
  send_telegram(msg)
  return jsonify({"status": "ok"}), 200

@app.route("/")
def health():
  return "Gold Alert Bot is running!", 200

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)