import tkinter as tk
from tkinter import ttk, messagebox
import requests

def send_message():
    ip = ip_entry.get()
    port = port_entry.get()
    message = message_entry.get()
    key = key_entry.get()
    algorithm = algorithm_var.get()

    if not ip or not port or not message:
        messagebox.showwarning("Eksik Bilgi", "Lütfen IP, port ve mesaj alanlarını doldurun!")
        return

    url = f"http://{ip}:{port}/encrypt"

    try:
        response = requests.post(url, json={
            'message': message,
            'key': key,
            'algorithm': algorithm
        })
        if response.status_code == 200:
            data = response.json()
            result_label.config(
                text=f"Sunucudan Gelen:\n{data['encrypted_message']}",
                fg="blue"
            )
        else:
            messagebox.showerror("Hata", f"Sunucudan geçersiz yanıt alındı: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Bağlantı Hatası", f"Sunucuya bağlanılamadı:\n{e}")

# --- GUI ---

root = tk.Tk()
root.title("Kriptoloji İstemci")
root.geometry("420x480")

tk.Label(root, text="🔐 Kriptoloji Şifreleme Arayüzü", font=("Arial", 14, "bold")).pack(pady=10)

# IP ve Port Girişi
frame_conn = tk.Frame(root)
frame_conn.pack(pady=5)

tk.Label(frame_conn, text="Sunucu IP:").grid(row=0, column=0, padx=5, pady=5)
ip_entry = tk.Entry(frame_conn)
ip_entry.grid(row=0, column=1)
ip_entry.insert(0, "127.0.0.1")

tk.Label(frame_conn, text="Port:").grid(row=1, column=0, padx=5, pady=5)
port_entry = tk.Entry(frame_conn)
port_entry.grid(row=1, column=1)
port_entry.insert(0, "5000")

# Mesaj ve Anahtar
tk.Label(root, text="Mesaj:").pack(pady=5)
message_entry = tk.Entry(root, width=40)
message_entry.pack()

tk.Label(root, text="Anahtar:").pack(pady=5)
key_entry = tk.Entry(root, width=40)
key_entry.pack()

# Algoritma Seçimi
tk.Label(root, text="Şifreleme Algoritması Seç:").pack(pady=5)

algorithm_var = tk.StringVar()
algorithm_combobox = ttk.Combobox(root, textvariable=algorithm_var, width=37, state="readonly")
algorithm_combobox['values'] = [
    "Caesar Cipher",
    "Substitution Cipher",
    "Vigenere Cipher",
    "Playfair Cipher"
]
algorithm_combobox.current(0)
algorithm_combobox.pack(pady=5)

# Gönder Butonu
tk.Button(root, text="Sunucuya Gönder", command=send_message, bg="lightgreen", width=20).pack(pady=15)

# Sonuç
result_label = tk.Label(root, text="", wraplength=380, justify="center", font=("Arial", 10))
result_label.pack(pady=10)

root.mainloop()
