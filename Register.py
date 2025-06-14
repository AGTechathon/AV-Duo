import tkinter as tk
from tkinter import messagebox
import os

# File to store user credentials
USER_DB = "users.txt"

# Save new user to file
def save_user(fullname, username, password):
    with open(USER_DB, "a") as f:
        f.write(f"{fullname},{username},{password}\n")



# Registration inputs
def register():
    fullname = entry_fullname.get().strip()
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not fullname or not username or not password:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    if user_exists(username):
        messagebox.showerror("Error", "Username already exists.")
    else:
        save_user(fullname, username, password)
        messagebox.showinfo("Success", "Registration successful!")
        root.destroy()  # Close window after success (optional)

# --- GUI Setup ---
root = tk.Tk()
root.title("Register")
root.geometry("300x250")
root.resizable(False, False)

tk.Label(root, text="Register", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Full Name").pack()
entry_fullname = tk.Entry(root)
entry_fullname.pack()

tk.Label(root, text="Username").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Register", command=register).pack(pady=10)

root.mainloop()
