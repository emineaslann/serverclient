import tkinter as tk
from tkinter import messagebox
import requests

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
            result_label.config(text=f"Sunucudan Gelen:\n{data['encrypted_message']}")
        else:
            messagebox.showerror("Hata", f"Sunucudan geçersiz yanıt alındı: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Bağlantı Hatası", f"Sunucuya bağlanılamadı:\n{e}")

# Tkinter arayüzü
root = tk.Tk()
root.title("Kriptoloji İstemci")
root.geometry("400x400")

tk.Label(root, text="Sunucu IP Adresi:").pack(pady=5)
ip_entry = tk.Entry(root)
ip_entry.pack()

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

result_label = tk.Label(root, text="", fg="blue", wraplength=350, justify="center")
result_label.pack(pady=10)

root.mainloop()
