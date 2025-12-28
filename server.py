print(">>> DOĞRU SERVER.PY ÇALIŞIYOR <<<")

import threading
import tkinter as tk
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Flask Sunucu Ayarları ---
app = Flask(__name__)
CORS(app)

received_messages = []  # GUI'de görüntülenecek mesajlar listesi

@app.route("/")
def home():
    return "SERVER CALISIYOR"



# --- Algoritma seçici ---
def get_cipher_instance(algorithm):
    from encryption_algorithms.aes_cipher import AESCipher
    from encryption_algorithms.des_cipher import DESCipher
    from encryption_algorithms.rsa_cipher import RSACipher

    from encryption_algorithms.caesar_cipher import CaesarCipher
    from encryption_algorithms.substitution_cipher import SubstitutionCipher
    from encryption_algorithms.vigenere_cipher import VigenereCipher
    from encryption_algorithms.playfair_cipher import PlayfairCipher
    from encryption_algorithms.rail_fence_cipher import RailFenceCipher
    from encryption_algorithms.route_cipher import RouteCipher
    from encryption_algorithms.columnar_transposition_cipher import ColumnarTranspositionCipher
    from encryption_algorithms.pigpen_cipher import PigpenCipher
    from encryption_algorithms.hill_cipher import HillCipher 

    from encryption_algorithms.manual_aes import ManualAES
    from encryption_algorithms.manual_des import ManualDES

    mapping = {
        "Caesar Cipher": CaesarCipher,
        "Substitution Cipher": SubstitutionCipher,
        "Vigenere Cipher": VigenereCipher,
        "Playfair Cipher": PlayfairCipher,
        "Rail Fence Cipher": RailFenceCipher,
        "Route Cipher": RouteCipher,
        "Columnar Transposition Cipher": ColumnarTranspositionCipher,
        "Pigpen Cipher": PigpenCipher,
        "Hill Cipher": HillCipher, 

        "AES-128 (kütüphaneli)": AESCipher,
        "DES (kütüphaneli)": DESCipher,
        "RSA (kütüphaneli)": RSACipher,

        "AES-128 (manuel)": ManualAES,
        "DES (manuel)": ManualDES,
    }

    CipherClass = mapping.get(algorithm.strip())
    return CipherClass() if CipherClass else None


# --- Şifreleme / Deşifreleme endpoint ---
@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.get_json()
    message = data.get("message", "")
    key = data.get("key", "")
    algorithm = data.get("algorithm", "Caesar Cipher")
    operation = data.get("operation", "Encrypt")  # <--- YENİ EKLENDİ

    cipher = get_cipher_instance(algorithm)
    if cipher is None:
        return jsonify({"error": f"Geçersiz algoritma: {algorithm}"}), 400

    try:
        if operation == "Encrypt":
            result = cipher.encrypt(message, key)
        else:
            result = cipher.decrypt(message, key)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # --- GUI Güncelleme ---
    if operation == "Encrypt":
        if isinstance(result, dict):
            enc = result.get("encrypted_message", "")
        else:
            enc = result
        received_messages.append((f"[Encrypt] {message}", algorithm, enc))
    else:
        if isinstance(result, dict):
            dec = result.get("decrypted_message", "")
        else:
            dec = result
        received_messages.append((f"[Decrypt] {message}", algorithm, dec))

    update_gui()

    # --- JSON Döndür ---
    if isinstance(result, dict):
        return jsonify(result)
    else:
        if operation == "Encrypt":
            return jsonify({"encrypted_message": result})
        else:
            return jsonify({"decrypted_message": result})


# --- Flask Sunucusu Thread ---
def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False)


# --- GUI Fonksiyonları ---
def update_gui():
    message_list.delete(0, tk.END)
    for msg, algo, res in received_messages:
        message_list.insert(
            tk.END, f"{msg} | Algoritma: {algo} | Sonuç: {res}"
        )


def start_server():
    start_button.config(state=tk.DISABLED)
    status_label.config(text="Sunucu Çalışıyor (Port 5000)...", fg="green")
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()


# --- Tkinter GUI ---
root = tk.Tk()
root.title("Kriptoloji Sunucu")
root.geometry("650x420")

tk.Label(root, text="Sunucu Kontrol Paneli", font=("Arial", 14, "bold")).pack(pady=10)

status_label = tk.Label(root, text="Sunucu Kapalı", fg="red", font=("Arial", 11))
status_label.pack(pady=5)

start_button = tk.Button(root, text="Sunucuyu Başlat", command=start_server, bg="lightgreen", width=20)
start_button.pack(pady=5)

tk.Label(root, text="İstemciden Gelen Mesajlar:", font=("Arial", 11)).pack(pady=10)

message_list = tk.Listbox(root, width=90, height=12)
message_list.pack(pady=5)

root.mainloop()
