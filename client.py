import tkinter as tk
from tkinter import ttk, messagebox
import requests
from Crypto.PublicKey import RSA
import time
from tkinter import filedialog
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
import os



def generate_rsa_keypair():
    key = RSA.generate(2048)
    private_pem = key.export_key().decode('utf-8')
    public_pem = key.publickey().export_key().decode('utf-8')
    key_entry.delete(0, tk.END)
    key_entry.insert(0, public_pem)
    messagebox.showinfo("RSA Anahtar Çifti Üretildi",
                        "Public key gönderime eklendi.\nPrivate key'i kaydedin!\n\n" + private_pem)


def send_message(operation):
    ip = ip_entry.get()
    port = port_entry.get()
    message = message_entry.get()
    key = key_entry.get()
    algorithm = algorithm_combo.get()

    if not ip or not port or not message:
        messagebox.showwarning("Eksik Bilgi", "IP, port ve mesaj alanları zorunludur!")
        return

    url = f"http://{ip}:{port}/encrypt"
    data = {
        'message': message,
        'key': key,
        'algorithm': algorithm,
        'operation': operation
    }

    try:
        start_time = time.perf_counter()   # ⏱️ BAŞLA
        response = requests.post(url, json=data)
        total_time = time.perf_counter() - start_time  # ⏱️ BİT

        if response.status_code != 200:
            messagebox.showerror(
                "Sunucu Hatası",
                f"Status Code: {response.status_code}\n\n{response.text}"
            )
            return

        data = response.json()

        if "encrypted_message" in data:
            result_label.config(
                text=(
                    "Sunucudan Gelen Şifreli Mesaj:\n"
                    + data["encrypted_message"]
                    + f"\n\n⏱️ Toplam Süre: {total_time:.6f} saniye"
                ),
                fg="blue"
            )

        elif "decrypted_message" in data:
            result_label.config(
                text=(
                    "Sunucudan Gelen Çözülmüş Mesaj:\n"
                    + data["decrypted_message"]
                    + f"\n\n⏱️ Toplam Süre: {total_time:.6f} saniye"
                ),
                fg="green"
            )

    except Exception as e:
        messagebox.showerror("Bağlantı Hatası", str(e))

def encrypt_file():
    algo = algorithm_combo.get()
    key_text = key_entry.get().encode()

    if algo not in ["AES-128 (kütüphaneli)", "DES (kütüphaneli)"]:
        messagebox.showwarning("Uyarı", "Dosya şifreleme sadece AES veya DES içindir.")
        return

    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    with open(file_path, "rb") as f:
        data = f.read()

    start = time.perf_counter()

    if algo == "AES-128 (kütüphaneli)":
        key = key_text[:16].ljust(16, b'\0')
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted = cipher.encrypt(pad(data, 16))

    elif algo == "DES (kütüphaneli)":
        key = key_text[:8].ljust(8, b'\0')
        cipher = DES.new(key, DES.MODE_ECB)
        encrypted = cipher.encrypt(pad(data, 8))

    elapsed = time.perf_counter() - start

    out_path = file_path + ".enc"
    with open(out_path, "wb") as f:
        f.write(encrypted)

    messagebox.showinfo(
        "Dosya Şifrelendi",
        f"Şifreli dosya:\n{out_path}\n\n⏱ Süre: {elapsed:.6f} saniye"
    )





root = tk.Tk()
root.title("Kriptoloji İstemci")
root.geometry("600x600")

tk.Label(root, text="🔐 Kriptoloji İstemci Uygulaması",
         font=("Arial", 16, "bold")).pack(pady=15)

tk.Label(root, text="Sunucu IP Adresi:").pack()
ip_entry = tk.Entry(root, width=30)
ip_entry.insert(0, "127.0.0.1")
ip_entry.pack()

tk.Label(root, text="Port:").pack()
port_entry = tk.Entry(root, width=10)
port_entry.insert(0, "5000")
port_entry.pack()

tk.Label(root, text="Mesaj:").pack()
message_entry = tk.Entry(root, width=60)
message_entry.pack()

tk.Label(root, text="Anahtar (metin/PEM):").pack()
key_entry = tk.Entry(root, width=60)
key_entry.pack()

tk.Button(root, text="RSA Keypair Üret (client-side)",
          command=generate_rsa_keypair,
          bg="lightblue").pack(pady=5)

tk.Label(root, text="Şifreleme Algoritması:").pack()
algorithm_combo = ttk.Combobox(root, width=45, state="readonly")
algorithm_combo['values'] = [
    "Caesar Cipher",
    "Substitution Cipher",
    "Vigenere Cipher",
    "Playfair Cipher",
    "Rail Fence Cipher",
    "Route Cipher",
    "Columnar Transposition Cipher",
    "Pigpen Cipher",
    "Hill Cipher",
    "AES-128 (kütüphaneli)",
    "DES (kütüphaneli)",
    "RSA (kütüphaneli)",
    "AES-128 (manuel)",
    "DES (manuel)"
]
algorithm_combo.current(0)
algorithm_combo.pack(pady=5)

# --- YENİ EKLENEN BUTONLAR ---
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

encrypt_button = tk.Button(button_frame, text="ŞİFRELE",
                           command=lambda: send_message("Encrypt"),
                           bg="#6fd36f", width=18)
encrypt_button.grid(row=0, column=0, padx=10)

decrypt_button = tk.Button(button_frame, text="DEŞİFRE ET",
                           command=lambda: send_message("Decrypt"),
                           bg="#ff8c8c", width=18)
decrypt_button.grid(row=0, column=1, padx=10)

result_label = tk.Label(root, text="", fg="blue",
                        wraplength=520, justify="left",
                        font=("Consolas", 10))
result_label.pack(pady=15)

tk.Button(
    root,
    text="📁 DOSYA ŞİFRELE (AES/DES)",
    command=encrypt_file,
    bg="#ccccff",
    width=30
).pack(pady=10)

root.mainloop()



