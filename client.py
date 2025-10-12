import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as st
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
from queue import Queue

# === Flask mini server for incoming messages ===
app = Flask(__name__)
CORS(app)
msg_queue = Queue()

@app.route('/receive', methods=['POST'])
def receive_message():
    """
    Server bu endpoint'e POST isteği gönderdiğinde,
    mesaj GUI'de görüntülenecek şekilde kuyruğa alınır.
    """
    data = request.get_json() or {}
    message = data.get('message', '')
    key = data.get('key', '')
    msg_queue.put(f"SUNUCU'DAN GELEN: {message} (key={key})")
    return jsonify({'status': 'ok'})

def run_flask():
    """
    Flask sunucusunu ayrı bir thread'de başlatır.
    5001 portunda dinler, böylece server bu porta mesaj gönderebilir.
    """
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)

def start_flask_thread():
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

# === Mesaj gönderme (Client → Server) ===
def send_message():
    ip = ip_entry.get()
    port = port_entry.get()
    message = message_entry.get()
    key = key_entry.get()

    if not ip or not port or not message:
        messagebox.showwarning("Eksik Bilgi", "Lütfen IP, port ve mesaj alanlarını doldurun!")
        return

    url = f"http://{ip}:{port}/encrypt"

    try:
        response = requests.post(url, json={'message': message, 'key': key})
        if response.status_code == 200:
            data = response.json()
            result_label.config(text=f"Sunucudan Gelen (şifreli):\n{data['encrypted_message']}")
        else:
            messagebox.showerror("Hata", f"Sunucudan geçersiz yanıt alındı: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Bağlantı Hatası", f"Sunucuya bağlanılamadı:\n{e}")

# === Flask'ı başlat ===
start_flask_thread()

# === Tkinter GUI ===
root = tk.Tk()
root.title("Kriptoloji İstemci")
root.geometry("500x600")

tk.Label(root, text="Sunucu IP Adresi:").pack(pady=5)
ip_entry = tk.Entry(root)
ip_entry.pack()
ip_entry.insert(0, "127.0.0.1")

tk.Label(root, text="Port:").pack(pady=5)
port_entry = tk.Entry(root)
port_entry.pack()
port_entry.insert(0, "5000")

tk.Label(root, text="Mesaj:").pack(pady=5)
message_entry = tk.Entry(root, width=40)
message_entry.pack()

tk.Label(root, text="Anahtar:").pack(pady=5)
key_entry = tk.Entry(root, width=20)
key_entry.pack()

tk.Button(root, text="Sunucuya Gönder", command=send_message).pack(pady=10)

result_label = tk.Label(root, text="", fg="blue", wraplength=450, justify="center")
result_label.pack(pady=10)

# === Gelen mesajları gösterme alanı ===
tk.Label(root, text="Sunucudan Gelen Mesajlar:").pack(pady=5)
incoming_box = st.ScrolledText(root, width=60, height=12, state='disabled')
incoming_box.pack(padx=10, pady=5)

# === Flask'tan gelen mesajları GUI'ye aktarma ===
def poll_messages():
    while not msg_queue.empty():
        msg = msg_queue.get()
        incoming_box.configure(state='normal')
        incoming_box.insert('end', msg + "\n")
        incoming_box.configure(state='disabled')
        incoming_box.see('end')
    root.after(200, poll_messages)

root.after(200, poll_messages)

root.mainloop()
