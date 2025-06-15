import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from PIL import Image, ImageTk
import os
import speech_recognition as sr

USER_DB = "users.txt"

# --------- DB Utilities ---------
def save_user(fullname, username, password):
    with open(USER_DB, "a") as f:
        f.write(f"{fullname},{username},{password}\n")

def user_exists(username):
    with open(USER_DB, "r") as f:
        for line in f:
            if line.strip().split(",")[1] == username:
                return True
    return False

def verify_user(username, password):
    with open(USER_DB, "r") as f:
        for line in f:
            user = line.strip().split(",")
            if len(user) == 3 and user[1] == username and user[2] == password:
                return True
    return False

# --------- Main App Launcher ---------
def launch_main_app():
    login_root.destroy()

    app = tk.Tk()
    app.title("LiveNoteClass - Voice to Text")
    app.geometry("900x700")
    app.config(bg="pink")

    top_frame = tk.Frame(app, bg="pink")
    top_frame.pack(fill=tk.X)
    tk.Label(top_frame, text="LiveNoteClass", font=("Arial", 20, "bold"), bg="pink", fg="#003366").pack(pady=10)

    content = tk.Frame(app, bg="pink")
    content.pack(fill=tk.BOTH, expand=True)

    language_from = tk.StringVar(value="English")
    language_to = tk.StringVar(value="English")

    lang_frame = tk.Frame(content, bg="pink")
    lang_frame.pack(pady=5)
    ttk.Label(lang_frame, text="Speaker Language:").pack(side=tk.LEFT)
    ttk.Combobox(lang_frame, textvariable=language_from, values=["English", "Hindi", "Spanish"]).pack(side=tk.LEFT)
    ttk.Label(lang_frame, text="Translate To:").pack(side=tk.LEFT)
    ttk.Combobox(lang_frame, textvariable=language_to, values=["English", "Hindi", "Spanish"]).pack(side=tk.LEFT)

    text_box = scrolledtext.ScrolledText(content, height=12, wrap=tk.WORD)
    text_box.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    option_frame = tk.Frame(content, bg="pink")
    option_frame.pack(anchor=tk.SE, pady=5, padx=10)
    tk.Button(option_frame, text="save docs", command=lambda: save_doc(text_box), fg="red").pack(side=tk.LEFT, padx=3)
    tk.Button(option_frame, text="clear", command=lambda: text_box.delete("1.0", tk.END), fg="red").pack(side=tk.LEFT, padx=3)
    tk.Button(option_frame, text="edit", command=lambda: text_box.config(state=tk.NORMAL), fg="red").pack(side=tk.LEFT, padx=3)

    bottom_frame = tk.Frame(content, bg="pink")
    bottom_frame.pack(pady=10)

    global pause_btn
    pause_btn = None
    recording = False
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    def start_recording():
        nonlocal recording
        recording = True
        text_box.delete(1.0, tk.END)
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                while recording:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    try:
                        text = recognizer.recognize_google(audio)
                        text_box.insert(tk.END, text + " ")
                        text_box.see(tk.END)
                        app.update()
                    except sr.UnknownValueError:
                        continue
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_recording():
        nonlocal recording
        recording = False

    def toggle_start():
        if start_canvas.itemcget(start_icon, "text") == "▶":
            start_canvas.itemconfig(start_icon, text="■")
            add_pause_button()
            start_recording()
        else:
            start_canvas.itemconfig(start_icon, text="▶")
            remove_pause_button()
            stop_recording()

    def toggle_pause():
        if pause_btn["text"] == "||":
            pause_btn.config(text="▶")
        else:
            pause_btn.config(text="||")

    def add_pause_button():
        global pause_btn
        pause_btn = tk.Button(bottom_frame, text="||", font=("Arial", 16, "bold"), bg="white", fg="black", command=toggle_pause)
        pause_btn.pack(side="left", padx=5)

    def remove_pause_button():
        global pause_btn
        if pause_btn:
            pause_btn.destroy()
            pause_btn = None

    def save_doc(text_widget):
        text = text_widget.get(1.0, tk.END).strip()
        if text:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_path:
                with open(file_path, "w") as f:
                    f.write(text)
                messagebox.showinfo("Saved", "Text saved successfully.")

    start_canvas = tk.Canvas(bottom_frame, width=50, height=50, bg="pink", highlightthickness=0)
    start_canvas.pack(side="left", padx=5)
    start_canvas.create_oval(5, 5, 45, 45, fill="white", outline="black", tags="circle")
    start_icon = start_canvas.create_text(25, 25, text="▶", font=("Arial", 20, "bold"), tags="start")
    start_canvas.tag_bind("circle", "<Button-1>", lambda e: toggle_start())
    start_canvas.tag_bind("start", "<Button-1>", lambda e: toggle_start())

    right_btn_frame = tk.Frame(bottom_frame, bg="pink")
    right_btn_frame.pack(side="right")
    tk.Button(right_btn_frame, text="Save", command=lambda: save_doc(text_box), bg="white", fg="black").pack(side="left", padx=5)
    tk.Button(right_btn_frame, text="Edit", command=lambda: text_box.config(state=tk.NORMAL), bg="white", fg="black").pack(side="left", padx=5)
    tk.Button(right_btn_frame, text="Clear", command=lambda: text_box.delete("1.0", tk.END), bg="white", fg="black").pack(side="left", padx=5)

    app.mainloop()

# --------- Registration Window ---------
def open_registration():
    reg = tk.Toplevel(login_root)
    reg.title("Register")
    reg.geometry("300x300")
    reg.config(bg="pink")

    tk.Label(reg, text="Full Name:", bg="pink").pack(pady=5)
    fullname_entry = tk.Entry(reg)
    fullname_entry.pack(pady=5)

    tk.Label(reg, text="Username:", bg="pink").pack(pady=5)
    username_entry = tk.Entry(reg)
    username_entry.pack(pady=5)

    tk.Label(reg, text="Password:", bg="pink").pack(pady=5)
    password_entry = tk.Entry(reg, show="*")
    password_entry.pack(pady=5)

    def register():
        fn, un, pw = fullname_entry.get(), username_entry.get(), password_entry.get()
        if not fn or not un or not pw:
            messagebox.showerror("Error", "All fields are required")
            return
        if user_exists(un):
            messagebox.showerror("Error", "Username already exists")
        else:
            save_user(fn, un, pw)
            messagebox.showinfo("Success", "Account created! Please log in.")
            reg.destroy()

    tk.Button(reg, text="Register", command=register, bg="white", fg="red").pack(pady=20)

# --------- Login Window ---------
login_root = tk.Tk()
login_root.title("Login - LiveNoteClass")
login_root.geometry("350x300")
login_root.config(bg="pink")

logo = tk.Label(login_root, text="LiveNoteClass", font=("Arial", 18, "bold"), bg="pink", fg="#003366")
logo.pack(pady=10)

tk.Label(login_root, text="Username:", bg="pink").pack()
username_entry = tk.Entry(login_root)
username_entry.pack(pady=5)

tk.Label(login_root, text="Password:", bg="pink").pack()
password_entry = tk.Entry(login_root, show="*")
password_entry.pack(pady=5)

def login():
    un = username_entry.get()
    pw = password_entry.get()
    if verify_user(un, pw):
        messagebox.showinfo("Success", "Login successful!")
        launch_main_app()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

tk.Button(login_root, text="Login", command=login, bg="white", fg="red").pack(pady=10)
tk.Label(login_root, text="Don't have an account?", bg="pink").pack()
tk.Button(login_root, text="Register here", command=open_registration, bg="white", fg="blue").pack()

login_root.mainloop()
