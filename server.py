# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from queue import Queue
import requests

app = Flask(__name__)
CORS(app)  # lokal testler için
msg_queue = Queue()

def caesar_encrypt(message, key):
    try:
        shift = int(key) % 26
    except:
        shift = 0
    result = []
    for ch in message:
        if 'a' <= ch <= 'z':
            result.append(chr((ord(ch)-97 + shift) % 26 + 97))
        elif 'A' <= ch <= 'Z':
            result.append(chr((ord(ch)-65 + shift) % 26 + 65))
        else:
            result.append(ch)
    return ''.join(result)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json() or {}
    message = data.get('message','')
    key = data.get('key','')
    encrypted = caesar_encrypt(message, key)
    # GUI'ye göstermek için kuyruğa ekle
    msg_queue.put(f"GELEN: '{message}' -> '{encrypted}' (key={key})")
    return jsonify({'encrypted_message': encrypted})

def run_flask():
    # ÖNEMLİ: debug=False ve use_reloader=False — Tkinter ile aynı süreçte kullanılacaksa reloader sorun çıkarır
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def start_flask_thread():
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

def gui_main():
    root = tk.Tk()
    root.title("Kriptoloji Sunucu")
    root.geometry("700x500")

    tk.Label(root, text="Sunucu - Lokal Şifreleme (Caesar)").pack(pady=5)

    frame = tk.Frame(root)
    frame.pack(pady=5, fill='x', padx=10)

    tk.Label(frame, text="Mesaj:").grid(row=0,column=0,sticky='w')
    entry_message = tk.Entry(frame, width=60)
    entry_message.grid(row=0,column=1, padx=5)

    tk.Label(frame, text="Anahtar:").grid(row=1,column=0,sticky='w')
    entry_key = tk.Entry(frame, width=10)
    entry_key.grid(row=1,column=1, sticky='w', padx=5)

    output_label = tk.Label(root, text="", fg="green")
    output_label.pack(pady=5)

    def local_encrypt():
        m = entry_message.get()
        k = entry_key.get()
        res = caesar_encrypt(m,k)
        output_label.config(text=f"Şifrelenmiş: {res}")

    tk.Button(root, text="Lokal Şifrele", command=local_encrypt).pack(pady=5)

    tk.Label(root, text="Gelen Mesajlar:").pack(pady=5)
    incoming = scrolledtext.ScrolledText(root, width=90, height=12, state='disabled')
    incoming.pack(padx=10)

    # İsteğe bağlı: sunucudan istemciye mesaj göndermek istersen kullan (istemci tarafında /receive implementasyonu olması gerekiyor)
    send_frame = tk.Frame(root)
    send_frame.pack(pady=8, fill='x', padx=10)
    tk.Label(send_frame, text="Gönderilecek IP:").grid(row=0,column=0,sticky='w')
    ip_entry = tk.Entry(send_frame, width=15); ip_entry.grid(row=0,column=1,padx=5)
    ip_entry.insert(0, "127.0.0.1")
    tk.Label(send_frame, text="Port:").grid(row=0,column=2,sticky='w')
    port_entry = tk.Entry(send_frame, width=7); port_entry.grid(row=0,column=3,padx=5)
    port_entry.insert(0, "5001")
    tk.Label(send_frame, text="Mesaj:").grid(row=1,column=0,sticky='w')
    send_message_entry = tk.Entry(send_frame, width=40); send_message_entry.grid(row=1,column=1,columnspan=3,sticky='w', padx=5)
    tk.Label(send_frame, text="Anahtar:").grid(row=2,column=0,sticky='w')
    send_key_entry = tk.Entry(send_frame, width=10); send_key_entry.grid(row=2,column=1,sticky='w', padx=5)

    def send_to_client():
        ip = ip_entry.get().strip()
        port = port_entry.get().strip()
        m = send_message_entry.get().strip()
        k = send_key_entry.get().strip()
        if not ip or not port or not m:
            messagebox.showwarning("Eksik", "IP, port ve mesaj girin.")
            return
        try:
            p = int(port)
        except ValueError:
            messagebox.showerror("Hata", "Port geçerli sayı değil.")
            return
        try:
            url = f"http://{ip}:{p}/receive"  # istemcide /receive yoksa hata verir; sonraki adımda ekleyeceğiz
            resp = requests.post(url, json={'message': m, 'key': k}, timeout=5)
            resp.raise_for_status()
            messagebox.showinfo("Başarılı", "Mesaj gönderildi. Alınan cevap: " + str(resp.text))
        except Exception as e:
            messagebox.showerror("Gönderilemedi", f"Hata: {e}")

    tk.Button(send_frame, text="İstemciye Gönder (/receive)", command=send_to_client).grid(row=2,column=2,padx=5)

    def poll_queue():
        while not msg_queue.empty():
            msg = msg_queue.get()
            incoming.configure(state='normal')
            incoming.insert('end', msg + "\n")
            incoming.configure(state='disabled')
            incoming.see('end')
        root.after(200, poll_queue)

    root.after(200, poll_queue)
    root.mainloop()

if __name__ == '__main__':
    start_flask_thread()
    gui_main()
