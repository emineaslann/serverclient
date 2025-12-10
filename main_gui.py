import customtkinter as ctk
from tkinter import messagebox
from client import send_request  # Client fonksiyonunu kullanıyoruz

# Tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

ALGO_MAP = {
    "Caesar Cipher (Kaydırma)": "Caesar Cipher",
    "Vigenere Cipher": "Vigenere Cipher",
    "SHA-256": "SHA-256",
    "MD5": "MD5"
}

class CryptoGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Şifreleme Arayüzü")
        self.geometry("600x450")

        # Algoritma seçimi
        self.algo_label = ctk.CTkLabel(self, text="Algoritma:")
        self.algo_label.pack(pady=5)

        self.algo_box = ctk.CTkComboBox(self, values=list(ALGO_MAP.keys()))
        self.algo_box.pack(pady=5)

        # Mesaj alanı
        self.msg_label = ctk.CTkLabel(self, text="Metin:")
        self.msg_label.pack(pady=5)

        self.msg_entry = ctk.CTkEntry(self, width=400)
        self.msg_entry.pack(pady=5)

        # Anahtar alanı
        self.key_label = ctk.CTkLabel(self, text="Anahtar (gerekliyse):")
        self.key_label.pack(pady=5)

        self.key_entry = ctk.CTkEntry(self, width=400)
        self.key_entry.pack(pady=5)

        # İşlem butonları
        self.encrypt_button = ctk.CTkButton(self, text="Şifrele", command=self.encrypt_text)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = ctk.CTkButton(self, text="Çöz", command=self.decrypt_text)
        self.decrypt_button.pack(pady=10)

        # Sonuç alanı
        self.output_label = ctk.CTkLabel(self, text="Sonuç:")
        self.output_label.pack(pady=5)

        self.output_box = ctk.CTkTextbox(self, width=450, height=100)
        self.output_box.pack(pady=5)

    def send(self, mode):
        algo = ALGO_MAP[self.algo_box.get()]
        msg = self.msg_entry.get()
        key = self.key_entry.get()

        if not msg:
            messagebox.showerror("Hata", "Lütfen metin girin!")
            return

        # İstek gönder
        response = send_request(algo, msg, key, mode)

        if response is None:
            messagebox.showerror("Sunucu Hatası", "Sunucuya bağlanılamadı!")
            return

        if "result" in response:
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", response["result"])
        else:
            messagebox.showerror("Hata", response.get("error", "Bilinmeyen hata"))

    def encrypt_text(self):
        self.send("encrypt")

    def decrypt_text(self):
        self.send("decrypt")


if __name__ == "__main__":
    app = CryptoGUI()
    app.mainloop()
