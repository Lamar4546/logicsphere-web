from flask import Blueprint, request, jsonify
import requests as http_requests
from ..config import Config

ai_bp = Blueprint('ai', __name__)

SYSTEM_PROMPT = """You are LogiSphere AI, an intelligent logistics assistant. 
You help users optimize supply chains, reduce freight costs, manage shipments, 
and improve logistics efficiency. Be concise, professional, and data-driven."""

@ai_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'Message required'}), 400
    if Config.OPENAI_API_KEY:
        return chat_with_openai(user_message)
    if Config.HUGGINGFACE_API_KEY:
        return chat_with_huggingface(user_message)

    return jsonify({'error': 'AI provider is not configured. Set OPENAI_API_KEY or HUGGINGFACE_API_KEY.'}), 500


def chat_with_openai(user_message):
    try:
        response = http_requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {Config.OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': Config.OPENAI_MODEL,
                'messages': [
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': user_message}
                ],
                'max_tokens': 500
            },
            timeout=30
        )
        if not response.ok:
            return jsonify({
                'error': 'OpenAI request failed',
                'details': response.text
            }), response.status_code

        result = response.json()
        reply = result.get('choices', [{}])[0].get('message', {}).get('content')
        if not reply:
            return jsonify({'error': 'OpenAI returned an empty response'}), 502
        return jsonify({'reply': reply}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def chat_with_huggingface(user_message):
    try:
        response = http_requests.post(
            'https://router.huggingface.co/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {Config.HUGGINGFACE_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'moonshotai/Kimi-K2-Instruct',
                'messages': [
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': user_message}
                ],
                'max_tokens': 500
            },
            timeout=30
        )
        if not response.ok:
            return jsonify({
                'error': 'Hugging Face request failed',
                'details': response.text
            }), response.status_code

        result = response.json()
        reply = result.get('choices', [{}])[0].get('message', {}).get('content')
        if not reply:
            return jsonify({'error': 'Hugging Face returned an empty response'}), 502
        return jsonify({'reply': reply}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
