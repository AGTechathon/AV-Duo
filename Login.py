# login.py
import tkinter as tk
from tkinter import messagebox
import os

FILE_PATH = "users.txt"

def verify_user(username, password):
    if not os.path.exists(FILE_PATH):
        return False
    with open(FILE_PATH, "r") as f:
        return any(line.strip() == f"{username},{password}" for line in f)

def login():
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    if not username or not password:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return
    if verify_user(username, password):
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Invalid username or password")

root = tk.Tk()
root.title("Login")
root.geometry("300x200")

tk.Label(root, text="Login", font=("Arial", 16)).pack(pady=10)
tk.Label(root, text="Username").pack()

entry_username = tk.Entry(root)
entry_username.insert(0, "username")  # default username
entry_username.pack()

tk.Label(root, text="Password").pack()
entry_password = tk.Entry(root, show='*')
entry_password.insert(0, "password")  # default password
entry_password.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()
