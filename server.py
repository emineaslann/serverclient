from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    message = data.get('message', '')
    key = data.get('key', '')

    # Şimdilik sadece test: mesajı büyük harfe çeviriyoruz
    encrypted = message.upper()

    return jsonify({'encrypted_message': encrypted})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
