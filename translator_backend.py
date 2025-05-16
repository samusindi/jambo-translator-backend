from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend to connect

openai.api_key = 'your-openai-api-key-here'

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text', '').strip()
    direction = data.get('direction', 'rw-en')
    paid = data.get('paid', False)

    words = text.split()
    word_count = len(words)

    if word_count <= 30 or paid:
        prompt = f"Translate this text from {'Kinyarwanda to English' if direction == 'rw-en' else 'English to Kinyarwanda'}:\n\n{text}"
        try:
            response = openai.ChatCompletion.create(
                model='gpt-4',
                messages=[
                    {'role': 'system', 'content': 'You are a professional translator.'},
                    {'role': 'user', 'content': prompt}
                ]
            )
            translation = response['choices'][0]['message']['content']
            return jsonify({'success': True, 'translation': translation})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    else:
        return jsonify({
            'success': False,
            'message': 'Text exceeds 30 words. Please pay to continue.',
            'word_count': word_count,
            'cost': round((word_count - 30) * 0.01, 2)
        }), 402

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
