# client.py
import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as st
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
from queue import Queue

# --------------------------
# Mini Flask (Client-side) to receive messages
# --------------------------
app = Flask(__name__)
CORS(app)
msg_queue = Queue()

@app.route('/receive', methods=['POST'])
def receive_message():
    data = request.get_json() or {}
    message = data.get('message', '')
    key = data.get('key', '')
    algorithms = data.get('algorithms', [])
    msg_queue.put(f"SUNUCU'DAN GELEN [{', '.join(algorithms)} | key={key}]: {message}")
    return jsonify({'status': 'ok'})

def run_flask():
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)

def start_flask_thread():
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

# --------------------------
# GUI ve gönderme işlemi
# --------------------------
def thread_send(server_ip, server_port, message, key, selected_algorithms):
    try:
        url = f"http://{server_ip}:{server_port}/encrypt"
        payload = {'message': message, 'key': key, 'algorithms': selected_algorithms}
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        encrypted = data.get('encrypted_message') or data.get('error') or str(data)
        root.after(0, lambda: result_label.config(text=f"Sunucudan Gelen (şifreli):\n{encrypted}"))
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Bağlantı Hatası", f"Sunucuya bağlanılamadı:\n{e}"))
    finally:
        root.after(0, lambda: send_button.config(state='normal'))

def send_message():
    server_ip = ip_entry.get().strip()
    server_port = port_entry.get().strip()
    message = message_entry.get().strip()
    key = key_entry.get().strip()

    # Seçili algoritmaları liste olarak al
    selected_algorithms = [alg for alg, var in algorithm_vars.items() if var.get() == 1]

    if not server_ip or not server_port or not message:
        messagebox.showwarning("Eksik Bilgi", "Lütfen IP, port ve mesaj alanlarını doldurun!")
        return

    if not selected_algorithms:
        messagebox.showwarning("Eksik Seçim", "Lütfen en az bir şifreleme algoritması seçin!")
        return

    try:
        int(server_port)
    except ValueError:
        messagebox.showerror("Hata", "Port numarası geçerli bir sayı değil.")
        return

    send_button.config(state='disabled')
    threading.Thread(
        target=thread_send,
        args=(server_ip, server_port, message, key, selected_algorithms),
        daemon=True
    ).start()

# --------------------------
# Flask thread başlat
# --------------------------
start_flask_thread()

# --------------------------
# Tkinter GUI
# --------------------------
root = tk.Tk()
root.title("Kriptoloji İstemci")
root.geometry("540x680")

tk.Label(root, text="Sunucu IP Adresi:").pack(pady=5)
ip_entry = tk.Entry(root)
ip_entry.pack()
ip_entry.insert(0, "127.0.0.1")

tk.Label(root, text="Port:").pack(pady=5)
port_entry = tk.Entry(root)
port_entry.pack()
port_entry.insert(0, "5000")

# Checkbox kısmı
tk.Label(root, text="Şifreleme Algoritmaları:").pack(pady=5)

# Buraya ekleyerek çoğaltabilirsin
ALGORITHMS = ["Caesar", "Vigenere", "XOR", "Affine"]
algorithm_vars = {}

frame = tk.Frame(root)
frame.pack(pady=5)

for alg in ALGORITHMS:
    var = tk.IntVar()
    chk = tk.Checkbutton(frame, text=alg, variable=var)
    chk.pack(anchor='w')
    algorithm_vars[alg.lower()] = var  # küçük harfli anahtar kaydı

tk.Label(root, text="Mesaj:").pack(pady=5)
message_entry = tk.Entry(root, width=60)
message_entry.pack()

tk.Label(root, text="Anahtar:").pack(pady=5)
key_entry = tk.Entry(root, width=20)
key_entry.pack()

send_button = tk.Button(root, text="Sunucuya Gönder", command=send_message)
send_button.pack(pady=10)

result_label = tk.Label(root, text="", fg="blue", wraplength=480, justify="center")
result_label.pack(pady=10)

tk.Label(root, text="Sunucudan Gelen Mesajlar:").pack(pady=5)
incoming_box = st.ScrolledText(root, width=65, height=18, state='disabled')
incoming_box.pack(padx=10, pady=5)

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
