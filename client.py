import tkinter as tk
from tkinter import ttk, messagebox
import requests


# --- Mesajı Sunucuya Gönderme Fonksiyonu ---
def send_message():
    ip = ip_entry.get()
    port = port_entry.get()
    message = message_entry.get()
    key = key_entry.get()
    algorithm = algorithm_combo.get()

    if not ip or not port or not message:
        messagebox.showwarning("Eksik Bilgi", "Lütfen IP, port ve mesaj alanlarını doldurun!")
        return

    url = f"http://{ip}:{port}/encrypt"
    data = {
        'message': message,
        'key': key,
        'algorithm': algorithm
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            data = response.json()
            result_label.config(
                text=f"Sunucudan Gelen Şifreli Mesaj:\n{data['encrypted_message']}",
                fg="blue"
            )
        else:
            messagebox.showerror("Sunucu Hatası", f"Geçersiz yanıt alındı: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Bağlantı Hatası", f"Sunucuya bağlanılamadı:\n{e}")


# --- Tkinter GUI ---
root = tk.Tk()
root.title("Kriptoloji İstemci")
root.geometry("500x500")

tk.Label(root, text="🔐 Kriptoloji İstemci Uygulaması", font=("Arial", 16, "bold")).pack(pady=15)

# Sunucu IP ve Port Girişi
tk.Label(root, text="Sunucu IP Adresi:", font=("Arial", 11)).pack(pady=5)
ip_entry = tk.Entry(root, width=30)
ip_entry.insert(0, "127.0.0.1")  # varsayılan olarak localhost
ip_entry.pack()

tk.Label(root, text="Port:", font=("Arial", 11)).pack(pady=5)
port_entry = tk.Entry(root, width=10)
port_entry.insert(0, "5000")
port_entry.pack()

# Mesaj Girişi
tk.Label(root, text="Mesaj:", font=("Arial", 11)).pack(pady=5)
message_entry = tk.Entry(root, width=40)
message_entry.pack()

# Anahtar Girişi
tk.Label(root, text="Anahtar:", font=("Arial", 11)).pack(pady=5)
key_entry = tk.Entry(root, width=20)
key_entry.pack()

# Algoritma Seçimi
tk.Label(root, text="Şifreleme Algoritması:", font=("Arial", 11)).pack(pady=5)
algorithm_combo = ttk.Combobox(root, width=30, state="readonly")
algorithm_combo['values'] = [
    "Caesar Cipher",
    "Substitution Cipher",
    "Vigenere Cipher",
    "Playfair Cipher",
    "Rail Fence Cipher",
    "Route Cipher",
    "Columnar Transposition Cipher",
    "Pigpen Cipher"
]
algorithm_combo.current(0)
algorithm_combo.pack(pady=5)

# Gönder Butonu
tk.Button(root, text="Sunucuya Gönder", command=send_message, bg="lightgreen", font=("Arial", 11)).pack(pady=15)

# Sonuç Gösterimi
result_label = tk.Label(root, text="", font=("Consolas", 11), fg="blue", wraplength=400, justify="center")
result_label.pack(pady=15)

root.mainloop()