# server.py
"""
Server with Tkinter GUI + Flask backend.

Features:
 - GUI to start/stop the server
 - Algorithm checkboxes (currently supports 'Caesar')
 - /encrypt endpoint to accept {"message","key","algorithms":[...]}
 - Incoming requests shown in the GUI (thread-safe via Queue)
 - Local encrypt button for testing via GUI
"""
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from queue import Queue
import requests
import time

# Flask imports
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import cipher implementations
from encryption_algorithms import CaesarCipher, VigenereCipher


# ---------- Flask app and inter-thread queue ----------
app = Flask(__name__)
CORS(app)
msg_queue = Queue()

# We'll keep a flag to indicate whether the server thread was started
server_thread = None
server_running = False

# ---------- Helper: choose cipher instance ----------
def get_cipher_instance(name, key):
    name = (name or "").lower()
    if name == "caesar":
        return CaesarCipher(key)
    elif name == "vigenere":
        return VigenereCipher(key)
    # future: add xor, affine, ...
    return None


# ---------- Flask endpoints ----------
@app.route('/encrypt', methods=['POST'])
def encrypt_endpoint():
    """
    Expected JSON:
    {
      "message": "hello",
      "key": "3",
      "algorithms": ["caesar", "vigenere"]
    }
    """
    data = request.get_json() or {}
    message = data.get('message', '')
    key = data.get('key', '')
    algorithms = data.get('algorithms', [])

    if not message:
        return jsonify({'error': 'Mesaj boş olamaz!'}), 400
    if not algorithms:
        return jsonify({'error': 'Algoritma listesi boş!'}), 400

    try:
        encrypted = message
        applied = []
        for alg in algorithms:
            cipher = get_cipher_instance(alg, key)
            if cipher is None:
                return jsonify({'error': f'{alg} algoritması desteklenmiyor!'}), 400
            encrypted = cipher.encrypt(encrypted)
            applied.append(alg)
        # push to GUI queue for display
        msg_queue.put(f"GELEN: '{message}' -> '{encrypted}' (algoritmalar: {applied}, key={key})")
        return jsonify({'encrypted_message': encrypted})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the Werkzeug server (only for development/testing)."""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        return jsonify({'error': 'Server shutdown not available.'}), 500
    func()
    return jsonify({'status': 'shutting down'})

# ---------- Function to run Flask in thread ----------
def run_flask_app():
    # Note: debug=False and use_reloader=False to avoid reloader thread conflicts
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# ---------- Tkinter GUI ----------
class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kriptoloji Sunucu")
        self.root.geometry("800x600")

        # Top frame: control buttons and algorithm checkboxes
        top_frame = tk.Frame(root, pady=6)
        top_frame.pack(fill='x')

        # Start / Stop buttons
        self.start_btn = tk.Button(top_frame, text="Sunucuyu Başlat", command=self.start_server)
        self.start_btn.pack(side='left', padx=6)
        self.stop_btn = tk.Button(top_frame, text="Sunucuyu Durdur", command=self.stop_server, state='disabled')
        self.stop_btn.pack(side='left', padx=6)

        # Local encrypt test (in GUI)
        tk.Label(top_frame, text="  Lokal Mesaj:").pack(side='left', padx=(12,0))
        self.local_message_entry = tk.Entry(top_frame, width=25)
        self.local_message_entry.pack(side='left', padx=4)
        tk.Label(top_frame, text="Anahtar:").pack(side='left', padx=(8,0))
        self.local_key_entry = tk.Entry(top_frame, width=6)
        self.local_key_entry.pack(side='left', padx=4)
        tk.Button(top_frame, text="Lokal Şifrele (Caesar)", command=self.local_encrypt).pack(side='left', padx=6)

        # Algorithm checkboxes (visual)
        alg_frame = tk.Frame(root, pady=6)
        alg_frame.pack(fill='x', padx=10)
        tk.Label(alg_frame, text="Şifreleme Algoritmaları (Sunucu tarafında kullanılacak):").pack(anchor='w')

        self.alg_vars = {}
        # Put the same algorithm set as client GUI (so they match visually)
        available = ["Caesar", "Vigenere", "XOR", "Affine"]
        cb_frame = tk.Frame(alg_frame)
        cb_frame.pack(anchor='w')
        for alg in available:
            var = tk.IntVar(value=1 if alg.lower()=="caesar" else 0)  # default Caesar on
            chk = tk.Checkbutton(cb_frame, text=alg, variable=var)
            chk.pack(side='left', padx=6)
            self.alg_vars[alg.lower()] = var

        # Middle: incoming messages
        mid_frame = tk.Frame(root)
        mid_frame.pack(fill='both', expand=True, padx=10, pady=8)

        tk.Label(mid_frame, text="Gelen Mesajlar (Client -> Server):").pack(anchor='w')
        self.incoming_box = scrolledtext.ScrolledText(mid_frame, state='disabled', wrap='word')
        self.incoming_box.pack(fill='both', expand=True)

        # Bottom: status and instructions
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill='x', padx=10, pady=6)
        self.status_label = tk.Label(bottom_frame, text="Sunucu: Durdu", anchor='w')
        self.status_label.pack(anchor='w')

        tk.Label(bottom_frame, text="Not: Sunucuyu durdurmak uygulamayı kapatmaz; restart için tekrar Start tuşuna kullanın.").pack(anchor='w')

        # Poll the msg_queue to show incoming messages in GUI
        self.root.after(200, self.poll_queue)

    def start_server(self):
        global server_thread, server_running
        if server_running:
            messagebox.showinfo("Bilgi", "Sunucu zaten çalışıyor.")
            return
        # Start Flask thread
        server_thread = threading.Thread(target=run_flask_app, daemon=True)
        server_thread.start()
        # small wait to let server come up (not strictly necessary)
        time.sleep(0.3)
        server_running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_label.config(text="Sunucu: Çalışıyor (http://127.0.0.1:5000)")

    def stop_server(self):
        global server_running
        if not server_running:
            messagebox.showinfo("Bilgi", "Sunucu zaten durdurulmuş.")
            return
        try:
            # call our shutdown endpoint
            requests.post('http://127.0.0.1:5000/shutdown', timeout=2)
        except Exception:
            # shutdown will close the server, which may raise a connection error here
            pass
        server_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="Sunucu: Durduruldu")

    def local_encrypt(self):
        """Simple local test using selected algorithms (applies CAESAR only for now)."""
        text = self.local_message_entry.get()
        k = self.local_key_entry.get()
        if not text:
            messagebox.showwarning("Uyarı", "Lütfen lokal mesaj girin.")
            return
        # build algorithms list from checkboxes (but for local test we'll apply same pipeline)
        algorithms = [name for name, var in self.alg_vars.items() if var.get() == 1]
        try:
            encrypted = text
            for alg in algorithms:
                cipher = get_cipher_instance(alg, k)
                if cipher is None:
                    messagebox.showerror("Hata", f"{alg} algoritması desteklenmiyor (henüz).")
                    return
                encrypted = cipher.encrypt(encrypted)
            messagebox.showinfo("Lokal Şifreleme Sonucu", encrypted)
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def poll_queue(self):
        """Move messages from the Flask thread into the ScrolledText widget."""
        while not msg_queue.empty():
            msg = msg_queue.get()
            self.incoming_box.configure(state='normal')
            self.incoming_box.insert('end', msg + "\n")
            self.incoming_box.configure(state='disabled')
            self.incoming_box.see('end')
        self.root.after(200, self.poll_queue)


# ---------- Main ----------
if __name__ == '__main__':
    root = tk.Tk()
    gui = ServerGUI(root)
    root.mainloop()
