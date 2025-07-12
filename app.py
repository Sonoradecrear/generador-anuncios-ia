import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
except Exception as e:
    model = None

def construir_prompt(producto, publico, tono, plataforma):
    return f"""
    Actúa como un Director Creativo experto de Sonora de Crear. Genera 3 conceptos de anuncios únicos basados en:
    - Producto: "{producto}"
    - Público: "{publico}"
    - Tono: "{tono}"
    - Plataforma: "{plataforma}"
    Usa formato Markdown con ### para títulos y * para bullet points.
    """

@app.route('/generar-conceptos', methods=['POST'])
def generar_conceptos_api():
    if not model: return jsonify({"error": "El cerebro IA no está conectado."}), 503
    data = request.get_json()
    prompt = construir_prompt(
        producto=data.get('producto'),
        publico=data.get('publico'),
        tono=data.get('tono'),
        plataforma=data.get('plataforma')
    )
    try:
        response = model.generate_content(prompt)
        return jsonify({"conceptos_markdown": response.text})
    except Exception as e:
        return jsonify({"error": f"Error de la IA: {e}"}), 500

@app.route('/')
def health_check():
    return "El cerebro del generador de anuncios está online."