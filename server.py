import threading
import tkinter as tk
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Flask Sunucu Ayarları ---
app = Flask(__name__)
CORS(app)

received_messages = []  # GUI'de görüntülenecek mesajlar listesi


# --- Algoritma seçici ---
def get_cipher_instance(algorithm):
    from encryption_algorithms.caesar_cipher import CaesarCipher
    from encryption_algorithms.substitution_cipher import SubstitutionCipher
    from encryption_algorithms.vigenere_cipher import VigenereCipher
    from encryption_algorithms.playfair_cipher import PlayfairCipher
    from encryption_algorithms.rail_fence_cipher import RailFenceCipher
    from encryption_algorithms.route_cipher import RouteCipher

    mapping = {
        "Caesar Cipher": CaesarCipher,
        "Substitution Cipher": SubstitutionCipher,
        "Vigenere Cipher": VigenereCipher,
        "Playfair Cipher": PlayfairCipher,
        "Rail Fence Cipher": RailFenceCipher,
        "Route Cipher": RouteCipher,
    }

    CipherClass = mapping.get(algorithm.strip())
    if CipherClass:
        return CipherClass()
    else:
        print(f"[Uyarı] Tanınmayan algoritma: {algorithm}")
        return None


# --- Şifreleme endpoint ---
@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.get_json()
    message = data.get("message", "")
    key = data.get("key", "")
    algorithm = data.get("algorithm", "Caesar Cipher")

    cipher = get_cipher_instance(algorithm)
    if cipher is None:
        return jsonify({"error": f"Geçersiz algoritma: {algorithm}"}), 400

    try:
        encrypted = cipher.encrypt(message, key)
    except Exception as e:
        encrypted = f"Hata: {str(e)}"

    received_messages.append((message, algorithm, encrypted))
    update_gui()

    return jsonify({"encrypted_message": encrypted})


# --- Flask Sunucusunu Ayrı Thread'de Çalıştır ---
def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False)


# --- GUI Fonksiyonları ---
def update_gui():
    message_list.delete(0, tk.END)
    for msg, algo, enc in received_messages:
        message_list.insert(
            tk.END, f"Gelen: {msg} | Algoritma: {algo} | Şifreli: {enc}"
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
