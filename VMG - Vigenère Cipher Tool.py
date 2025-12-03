# Vigenère Cipher tool made by Voidmother-Glitch
# This tool was made as part of an on-going engagement to facilitate encoded conversations with LLMs.
# The encoding/decoding happens on the local machine, with no data being sent across network or the internet.
# The tool has an input field for plaintext/ciphertext, an encode/decode mode select, and an output field with a copy-to-clipboard button.
# All tested LLMs are able to read and engage with short ciphertext once provided the key, however stateless LLMs seem to have an issue with displaying the decoded text at any length.
# Longer ciphertext appears to break the chain-of-logic and the tested LLMs all resorted to default, pre-System Prompt behavior.
# Ciphertext more than 200 characters in length reliably causes hallucinations or garbled, nonsense responses.
# I was not able to pin down the threshold to cause that more specifcally during testing.
#
#
# Michigan Technical University published an excellent write up of the transformations behind Vigenère Ciphers at the following link:
# https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-Base.html

import tkinter as tk
from tkinter import ttk, messagebox

# Vigenère Cipher Functions (encrypt and decrypt)
# Two separate functions, one to handle encrypting, one to handle decrypting.
# If-else to handle case in text. Checks if each character is upper- or lowercase, then transforms them. Keeps current case.
# Traditional Vigenère ciphers change all letters to uppercase, but in modern networks, case retention is mandatory.


def vigenere_encrypt(plaintext, key):
    result = []
    key = key.upper()
    key_len = len(key)
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % key_len]) - ord('A')
            if char.isupper():
                encrypted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            result.append(encrypted)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

def vigenere_decrypt(ciphertext, key):
    result = []
    key = key.upper()
    key_len = len(key)
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % key_len]) - ord('A')
            if char.isupper():
                decrypted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            result.append(decrypted)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

# GUI App
class VigenereApp:
    def __init__(self, root):
        self.root = root # Root is the base of the window.
        self.root.title("Vigenère Cipher") # Title for the window.
        self.root.geometry("800x600")  # Initial size 800x600.
        self.root.resizable(True, True)  # Allow window to be resized.
        self.root.configure(bg="#1e1e1e") # Sets background color to match Dark Mode theme.

        # Grid weights allow for the UI elements to adjust when the window is resized. These weights allow vertical stretch.
        self.root.grid_rowconfigure(0, weight=0)  # Title
        self.root.grid_rowconfigure(1, weight=0)  # Input label
        self.root.grid_rowconfigure(2, weight=1)  # Input text (expandable)
        self.root.grid_rowconfigure(3, weight=0)  # Key label
        self.root.grid_rowconfigure(4, weight=0)  # Key entry
        self.root.grid_rowconfigure(5, weight=0)  # Radio buttons
        self.root.grid_rowconfigure(6, weight=0)  # Process button
        self.root.grid_rowconfigure(7, weight=0)  # Output label
        self.root.grid_rowconfigure(8, weight=1)  # Output text (expandable)
        self.root.grid_rowconfigure(9, weight=0)  # Copy button
        self.root.grid_rowconfigure(10, weight=0) # Copy result label

        self.root.grid_columnconfigure(0, weight=1)  # This weight, specifically, allows horizontal stretch.

        # Dark Mode because I don't want my eyes stabbed.
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10), padding=5, background='#333333', foreground='white')
        style.map('TButton', background=[('active', '#555555')])
        style.configure('TEntry', fieldbackground='#2d2d2d', foreground='white', insertcolor='white')
        style.configure('TLabel', background='#1e1e1e', foreground='white', font=('Arial', 10))

        # Title - Vigenère Cipher
        title = tk.Label(root, text="Vigenère Cipher", bg="#1e1e1e", fg="white", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, pady=10, sticky="ew", padx=20)

        # Input Text - Put your text in here. Mode select later to determine if this is cipher- or plaintext.
        input_label = tk.Label(root, text="Input Text:", bg="#1e1e1e", fg="white")
        input_label.grid(row=1, column=0, sticky="w", padx=20)
        self.input_text = tk.Text(root, bg="#2d2d2d", fg="white", insertbackground="white", font=("Arial", 10))
        self.input_text.grid(row=2, column=0, sticky="nsew", padx=20, pady=5)

        # Key - Vigenère Cipher uses a key to calculate transformations. Put it here.
        key_label = tk.Label(root, text="Key:", bg="#1e1e1e", fg="white")
        key_label.grid(row=3, column=0, sticky="w", padx=20)
        self.key_entry = ttk.Entry(root, font=("Arial", 10))
        self.key_entry.grid(row=4, column=0, sticky="ew", padx=20, pady=5)

        # Mode Select - Radio buttons to declare if we are encrypting or decrypting.
        self.mode = tk.StringVar(value="encrypt")
        encrypt_rb = tk.Radiobutton(root, text="Encrypt", variable=self.mode, value="encrypt", bg="#1e1e1e", fg="white", selectcolor="#333333", font=("Arial", 10))
        encrypt_rb.grid(row=5, column=0, sticky="w", padx=25)
        decrypt_rb = tk.Radiobutton(root, text="Decrypt", variable=self.mode, value="decrypt", bg="#1e1e1e", fg="white", selectcolor="#333333", font=("Arial", 10))
        decrypt_rb.grid(row=5, column=0, sticky="w", padx=100)

        # Process Button - Makes the magic happen!
        process_btn = ttk.Button(root, text="Process", command=self.process)
        process_btn.grid(row=6, column=0, pady=10, sticky="ew", padx=20)

        # Output - Our results, obvi.
        output_label = tk.Label(root, text="Output:", bg="#1e1e1e", fg="white")
        output_label.grid(row=7, column=0, sticky="w", padx=20)
        self.output_text = tk.Text(root, bg="#2d2d2d", fg="white", state="disabled", font=("Arial", 10))
        self.output_text.grid(row=8, column=0, sticky="nsew", padx=20, pady=5)

        # Copy to Clipboard - Does what it says on the tin.
        copy_btn = ttk.Button(root, text="Copy to Clipboard", command=self.copy_output)
        copy_btn.grid(row=9, column=0, pady=5, sticky="ew", padx=20)

        # Copy Result Label - If copying is successful, a message will appear here for ~2 seconds
        self.copy_result_label = tk.Label(root, text=" ", bg="#1e1e1e", fg="white")
        self.copy_result_label.grid(row=10, column=0, sticky="w", padx=20)


    def process(self):
        text = self.input_text.get("1.0", "end-1c").strip()
        key = self.key_entry.get().strip()
        if not key or not text:
            messagebox.showwarning("Input Error", "Rude! Give me both text AND a key.")
            return
        if not key.isalpha():
            messagebox.showwarning("Key Error", "Only letters, please and thanks!.")
            return

        if self.mode.get() == "encrypt":
            result = vigenere_encrypt(text, key)
        else:
            result = vigenere_decrypt(text, key)

        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.output_text.config(state="disabled")

    def copy_output(self):
        content = self.output_text.get("1.0", "end-1c")
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content) 
            self.copy_result_label.config(text="Copied to clipboard!")
            root.after(2000, lambda: self.copy_result_label.config(text=" "))
        else:
            messagebox.showwarning("Empty", "I am empty.")

# Run App, all python modules need this. root = tk.Tk() to create GUI, app = VigenereApp(root) to run app within the GUI. root.mainloop() to open the window and listen for events in the GUI.
if __name__ == "__main__":
    root = tk.Tk()
    app = VigenereApp(root)
    root.mainloop()