from flask import Flask, render_template, jsonify
import os

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

LOVE_MESSAGES = [
    "Eres mi lugar seguro",
    "Gracias por existir en mi vida",
    "Contigo todo es mas bonito",
    "Eres mi sueno hecho realidad",
    "Cada dia a tu lado es un regalo",
    "Me haces mejor persona",
    "Tu sonrisa es mi sol",
    "Eres mi historia de amor favorita",
    "Mi corazon late por ti",
    "Para siempre empezo cuando te conoci"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/message/<int:candle>')
def get_message(candle):
    if 0 <= candle < len(LOVE_MESSAGES):
        return jsonify({'message': LOVE_MESSAGES[candle], 'candle': candle})
    return jsonify({'message': 'Te amo', 'candle': candle})

handler = app
