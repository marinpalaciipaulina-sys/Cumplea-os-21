from flask import Flask, jsonify, render_template
import os
from pathlib import Path

app = Flask(__name__, template_folder='templates')

# Mensajes románticos para las velas
LOVE_MESSAGES = [
    "Eres mi lugar seguro",
    "Gracias por existir en mi vida",
    "Contigo todo es más bonito",
    "Eres mi sueño hecho realidad",
    "Cada día a tu lado es un regalo",
    "Me haces mejor persona",
    "Tu sonrisa es mi sol",
    "Eres mi historia de amor favorita",
    "Mi corazón late por ti",
    "Para siempre empezó cuando te conocí 💖"
]

@app.route('/')
def index():
    """Sirve la página principal con la experiencia de cumpleaños"""
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
    """Retorna todos los mensajes románticos"""
    return jsonify(LOVE_MESSAGES)

# Handler para Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)