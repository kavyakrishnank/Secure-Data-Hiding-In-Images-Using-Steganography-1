import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import ttk, messagebox

def int_to_bits(num, bit_length):
    """Convert an integer to a fixed-length list of bits."""
    return [int(b) for b in format(num, f'0{bit_length}b')]

def str_to_bits(s):
    """Convert a string into its 8-bit ASCII representation."""
    bits = []
    for char in s:
        bits.extend([int(b) for b in format(ord(char), '08b')])
    return bits

def embed_data(image, data_bits):
    """Embed binary data into the least significant bit (LSB) of the image."""
    flat = image.flatten()

    if len(data_bits) > len(flat):
        raise ValueError("Data too large to embed in this image!")

    for i in range(len(data_bits)):
        flat[i] = (flat[i] & ~1) | data_bits[i]  # Safely embed bit

    return flat.reshape(image.shape)

def encrypt():
    img_path = "mypic.jpg"

    if not os.path.exists(img_path):
        messagebox.showerror("Error", "Input image 'mypic.jpg' not found!")
        return

    image = cv2.imread(img_path)
    if image is None:
        messagebox.showerror("Error", "Failed to load 'mypic.jpg'. Ensure it's a valid image.")
        return

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB format

    secret_message = secret_message_entry.get().strip()
    passcode = passcode_entry.get().strip()

    if not secret_message or not passcode:
        messagebox.showerror("Error", "Secret message and passcode cannot be empty!")
        return

    # Construct header: Passcode length, passcode, message length, message
    header_bits = []
    header_bits.extend(int_to_bits(len(passcode), 16))  # 16 bits for passcode length
    header_bits.extend(str_to_bits(passcode))           # Passcode in 8-bit ASCII
    header_bits.extend(int_to_bits(len(secret_message), 32))  # 32 bits for message length
    header_bits.extend(str_to_bits(secret_message))     # Secret message in 8-bit ASCII

    try:
        encoded_image = embed_data(image, header_bits)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    output_path = "encrypted.png"
    cv2.imwrite(output_path, cv2.cvtColor(encoded_image, cv2.COLOR_RGB2BGR))  # Preserve color format
    messagebox.showinfo("Success", f"Encryption complete! Saved as '{output_path}'.")

# GUI Setup
root = tk.Tk()
root.title("Steganography - Encrypt")
root.geometry("400x300")
style = ttk.Style(root)
style.theme_use('clam')

frame = ttk.Frame(root, padding="20")
frame.pack(expand=True)

ttk.Label(frame, text="Enter Secret Message:").grid(row=0, column=0, sticky="w", pady=5)
secret_message_entry = ttk.Entry(frame, width=40)
secret_message_entry.grid(row=1, column=0, pady=5)

ttk.Label(frame, text="Enter Passcode:").grid(row=2, column=0, sticky="w", pady=5)
passcode_entry = ttk.Entry(frame, width=40, show="*")
passcode_entry.grid(row=3, column=0, pady=5)

encrypt_button = ttk.Button(frame, text="Encrypt", command=encrypt)
encrypt_button.grid(row=4, column=0, pady=20)

root.mainloop()