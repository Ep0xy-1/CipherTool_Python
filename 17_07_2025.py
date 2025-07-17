import tkinter as tk
from tkinter import ttk, simpledialog, colorchooser
import threading
import pygame
import time
import string
 
# Initialize pygame for sound
pygame.init()
pygame.mixer.init()

def play_beep():
    freq = 440
    dur = 100
    sample_rate = 44100
    n_samples = int(sample_rate * dur / 1000)
    buf = (pygame.sndarray.make_sound(
        pygame.surfarray.array2d(
            pygame.Surface((n_samples, 1)).convert()
        )
    ))
    pygame.mixer.Sound.play(buf)

# Cipher Logic
def caesar_cipher(text, shift, decrypt=False):
    result = ''
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            shift_val = -shift if decrypt else shift
            result += chr((ord(char) - offset + shift_val) % 26 + offset)
        else:
            result += char
    return result

def vigenere_cipher(text, key, decrypt=False):
    result = ''
    key = key.lower()
    key_idx = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)]) - 97
            if decrypt:
                shift = -shift
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + shift) % 26 + offset)
            key_idx += 1
        else:
            result += char
    return result

# GUI
class CipherToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caesar / Vigenère Cipher Tool")
        self.root.geometry("700x500")
        self.bg_color = "#282c34"
        self.sound_enabled = True
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg=self.bg_color)

        self.title = tk.Label(self.root, text="Cipher Tool", font=("Arial", 24, "bold"), bg=self.bg_color, fg="white")
        self.title.pack(pady=10)

        self.text_input = tk.Text(self.root, height=5, width=60, font=("Arial", 12))
        self.text_input.pack(pady=5)

        self.method = tk.StringVar(value="Caesar")
        self.key_label = tk.Label(self.root, text="Shift / Key:", bg=self.bg_color, fg="white")
        self.key_label.pack()

        self.key_entry = tk.Entry(self.root, width=20)
        self.key_entry.pack(pady=2)

        method_menu = ttk.Combobox(self.root, textvariable=self.method, values=["Caesar", "Vigenère"], state="readonly")
        method_menu.pack()

        self.decode_btn = tk.Button(self.root, text="Decode", command=self.start_decoding, width=20, bg="#61afef", fg="black")
        self.decode_btn.pack(pady=10)

        self.output = tk.Text(self.root, height=7, width=60, font=("Consolas", 12), bg="#1e1e1e", fg="lime", state="disabled")
        self.output.pack(pady=5)

        self.settings_btn = tk.Button(self.root, text="⚙ Settings", command=self.open_settings, bg="#98c379")
        self.settings_btn.pack(side="bottom", pady=10)

    def start_decoding(self):
        threading.Thread(target=self.live_decode).start()

    def live_decode(self):
        text = self.text_input.get("1.0", tk.END).strip()
        key = self.key_entry.get()
        method = self.method.get()

        self.output.configure(state="normal")
        self.output.delete("1.0", tk.END)

        for i in range(len(text)):
            chunk = text[:i+1]
            if method == "Caesar":
                try:
                    shift = int(key)
                except ValueError:
                    self.output.insert(tk.END, "\n[Invalid Caesar shift]")
                    return
                decoded = caesar_cipher(chunk, shift, decrypt=True)
            else:
                if not key.isalpha():
                    self.output.insert(tk.END, "\n[Key must be letters only]")
                    return
                decoded = vigenere_cipher(chunk, key, decrypt=True)

            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, decoded)
            if self.sound_enabled:
                play_beep()
            self.output.update()
            time.sleep(0.05)

        self.output.configure(state="disabled")

    def open_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Settings")
        settings_win.geometry("300x200")
        settings_win.configure(bg=self.bg_color)

        def change_bg():
            color = colorchooser.askcolor(title="Choose Background Color")[1]
            if color:
                self.bg_color = color
                self.root.configure(bg=color)
                self.title.configure(bg=color)
                self.key_label.configure(bg=color)
                settings_win.configure(bg=color)

        def toggle_sound():
            self.sound_enabled = not self.sound_enabled
            sound_btn.configure(text="Sound: ON" if self.sound_enabled else "Sound: OFF")

        bg_btn = tk.Button(settings_win, text="Change Background", command=change_bg, bg="#e06c75", fg="white")
        bg_btn.pack(pady=10)

        sound_btn = tk.Button(settings_win, text="Sound: ON" if self.sound_enabled else "Sound: OFF", command=toggle_sound, bg="#56b6c2", fg="white")
        sound_btn.pack(pady=10)

        tk.Label(settings_win, text="* Settings apply instantly", bg=self.bg_color, fg="white").pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = CipherToolApp(root)
    root.mainloop()
