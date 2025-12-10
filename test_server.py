from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/encrypt", methods=["POST"])
def encrypt_test():
    data = request.json
    print("Sunucu Veriyi Aldı:", data)
    return jsonify({
        "ok": True,
        "received": data
    })

app.run(host="127.0.0.1", port=5000, debug=False)

