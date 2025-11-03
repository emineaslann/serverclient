import threading
import tkinter as tk
from tkinter import ttk
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Şifreleme sınıflarını içe aktar ---
from encryption_algorithms.caesar_cipher import CaesarCipher
from encryption_algorithms.substitution_cipher import SubstitutionCipher
from encryption_algorithms.vigenere_cipher import VigenereCipher
from encryption_algorithms.playfair_cipher import PlayfairCipher
from encryption_algorithms.rail_fence_cipher import RailFenceCipher


# --- Flask Sunucu Ayarları ---
app = Flask(__name__)
CORS(app)

# Gelen mesajları GUI'de gösterebilmek için global değişken
received_messages = []


# --- Şifreleme İşlemi ---
def encrypt_message(message, algorithm, key):
    if algorithm == "Caesar Cipher":
        cipher = CaesarCipher()
        return cipher.encrypt(message, key)
    elif algorithm == "Substitution Cipher":
        cipher = SubstitutionCipher()
        return cipher.encrypt(message, key)
    elif algorithm == "Vigenere Cipher":
        cipher = VigenereCipher()
        return cipher.encrypt(message, key)
    elif algorithm == "Playfair Cipher":
        cipher = PlayfairCipher()
        return cipher.encrypt(message, key)
    elif algorithm == "Rail Fence Cipher":
        cipher = RailFenceCipher()
        return cipher.encrypt(message, key)
    else:
        return message


@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    message = data.get('message', '')
    key = data.get('key', '')
    algorithm = data.get('algorithm', 'Caesar Cipher')

    encrypted = encrypt_message(message, algorithm, key)

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
root.geometry("700x500")

tk.Label(root, text="🔐 Kriptoloji Sunucu Paneli", font=("Arial", 16, "bold")).pack(pady=10)

status_label = tk.Label(root, text="Sunucu Kapalı", fg="red", font=("Arial", 12))
status_label.pack(pady=5)

start_button = tk.Button(root, text="Sunucuyu Başlat", command=start_server, bg="lightgreen", width=20)
start_button.pack(pady=10)

tk.Label(root, text="İstemciden Gelen Mesajlar:", font=("Arial", 12, "bold")).pack(pady=10)

message_list = tk.Listbox(root, width=90, height=15, font=("Consolas", 10))
message_list.pack(pady=10)

tk.Label(root, text="Sunucuda Aktif Şifreleme Algoritmaları:", font=("Arial", 12, "bold")).pack(pady=10)

algorithms = ["Caesar Cipher", "Substitution Cipher", "Vigenere Cipher", "Playfair Cipher", "Rail Fence Cipher"]

for algo in algorithms:
    tk.Label(root, text=f"• {algo}", font=("Arial", 11)).pack()

root.mainloop()
