import threading
import tkinter as tk
from flask import Flask, request, jsonify
from flask_cors import CORS
from encryption_algorithms.caesar_cipher import CaesarCipher

# --- Flask Sunucu Ayarları ---
app = Flask(__name__)
CORS(app)

# Gelen mesajları GUI'de gösterebilmek için global değişken
received_messages = []

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    message = data.get('message', '')
    key = data.get('key', '')
    algorithm = data.get('algorithm', 'Caesar Cipher')

    if algorithm == "Caesar Cipher":
       from encryption_algorithms.caesar_cipher import CaesarCipher
       cipher = CaesarCipher()
       encrypted = cipher.encrypt(message, key)

    elif algorithm == "Substitution Cipher":
       encrypted = message[::-1]

    elif algorithm == "Vigenere Cipher":
       from encryption_algorithms.vigenere_cipher import VigenereCipher
       cipher = VigenereCipher()
       encrypted = cipher.encrypt(message, key)

    elif algorithm == "Playfair Cipher":
       from encryption_algorithms.playfair_cipher import PlayfairCipher
       cipher = PlayfairCipher(key)
       encrypted = cipher.encrypt(message)


    else:
       encrypted = message


    received_messages.append((message, algorithm, encrypted))
    update_gui()

    return jsonify({'encrypted_message': encrypted})

# --- Flask Sunucusunu Ayrı Thread'de Çalıştır ---
def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

# --- GUI Kısmı ---
def update_gui():
    """GUI'deki mesaj listesini günceller."""
    message_list.delete(0, tk.END)
    for msg, algo, enc in received_messages:
        message_list.insert(tk.END, f"Gelen: {msg} | Algoritma: {algo} | Şifreli: {enc}")

def start_server():
    """Flask sunucusunu başlatır."""
    start_button.config(state=tk.DISABLED)
    status_label.config(text="Sunucu Çalışıyor (Port 5000)...", fg="green")

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

# --- Tkinter GUI ---
root = tk.Tk()
root.title("Kriptoloji Sunucu")
root.geometry("600x400")

tk.Label(root, text="Sunucu Kontrol Paneli", font=("Arial", 14, "bold")).pack(pady=10)

status_label = tk.Label(root, text="Sunucu Kapalı", fg="red", font=("Arial", 11))
status_label.pack(pady=5)

start_button = tk.Button(root, text="Sunucuyu Başlat", command=start_server, bg="lightgreen", width=20)
start_button.pack(pady=5)

tk.Label(root, text="İstemciden Gelen Mesajlar:", font=("Arial", 11)).pack(pady=10)

message_list = tk.Listbox(root, width=80, height=12)
message_list.pack(pady=5)

root.mainloop()
