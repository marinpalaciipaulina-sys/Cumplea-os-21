from flask import Flask, render_template, jsonify
import json
import random

app = Flask(__name__)

# Mensajes románticos para cada vela
LOVE_MESSAGES = [
    "Eres mi lugar seguro 💕",
    "Gracias por existir en mi vida",
    "Contigo todo es más bonito",
    "Eres mi sueño hecho realidad",
    "Cada día a tu lado es un regalo",
    "Me haces mejor persona",
    "Tu sonrisa es mi sol ☀️",
    "Eres mi historia de amor favorita",
    "Mi corazón late por ti",
    "Para siempre empezó cuando te conocí 💖"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/message/<int:candle>')
def get_message(candle):
    """Retorna un mensaje romántico para cada vela apagada"""
    if 0 <= candle < len(LOVE_MESSAGES):
        return jsonify({
            'message': LOVE_MESSAGES[candle],
            'candle': candle
        })
    return jsonify({'message': 'Te amo 💕', 'candle': candle})

@app.route('/api/messages')
def get_all_messages():
    return jsonify(LOVE_MESSAGES)

if __name__ == '__main__':
    app.run(debug=True, port=5000)