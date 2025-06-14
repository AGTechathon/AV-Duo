import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

# Colors
BG_COLOR = "#e6f0ff"       # Soft blue background
HEADER_COLOR = "#e6f0ff"
BTN_COLOR = "#cce0ff"       # Light blue buttons
TEXT_BG = "#f5faff"         # Pale blue text background
TEXT_COLOR = "#003366"  

current_screen = "voice_to_text"
pause_btn = None
selected_audio_path = ""


def switch_screen(screen):
    global current_screen
    current_screen = screen
    clear_content()
    if screen == "voice_to_text":
        add_text_area_buttons()
    elif screen == "audio_to_text":
        add_audio_to_text()
    elif screen == "meeting":
        add_meeting_placeholder()


def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


def add_text_area_buttons():
    global pause_btn
    text_frame = tk.Frame(content_frame, bg=BG_COLOR, height=150)
    text_frame.pack(padx=10, pady=5, fill="x")

    text_area = tk.Text(text_frame, wrap="word", font=("Arial", 12),
                        bg=TEXT_BG, fg=TEXT_COLOR, height=6)
    text_area.pack(fill="x", expand=False, side="left")

    scrollbar = tk.Scrollbar(text_frame, command=text_area.yview)
    scrollbar.pack(side="right", fill="y")
    text_area.config(yscrollcommand=scrollbar.set)

    bottom_frame = tk.Frame(content_frame, bg=BG_COLOR)
    bottom_frame.pack(fill="x", padx=10, pady=10)

    def toggle_start():
        if start_canvas.itemcget(start_icon, "text") == "▶":
            start_canvas.itemconfig(start_icon, text="■")
            add_pause_button()
        else:
            start_canvas.itemconfig(start_icon, text="▶")
            remove_pause_button()

    def toggle_pause():
        if pause_btn["text"] == "||":
            pause_btn.config(text="▶")
        else:
            pause_btn.config(text="||")

    def add_pause_button():
        global pause_btn
        pause_btn = tk.Button(bottom_frame, text="||", font=("Arial", 16, "bold"),
                              bg=BTN_COLOR, fg=TEXT_COLOR, command=toggle_pause)
        pause_btn.pack(side="left", padx=5)

    def remove_pause_button():
        global pause_btn
        if pause_btn:
            pause_btn.destroy()
            pause_btn = None

    start_canvas = tk.Canvas(bottom_frame, width=50, height=50, bg=BG_COLOR, highlightthickness=0)
    start_canvas.pack(side="left", padx=5)
    start_canvas.create_oval(5, 5, 45, 45, fill=BTN_COLOR, outline=TEXT_COLOR, tags="circle")
    start_icon = start_canvas.create_text(25, 25, text="▶", font=("Arial", 20, "bold"), tags="start")
    start_canvas.tag_bind("circle", "<Button-1>", lambda e: toggle_start())
    start_canvas.tag_bind("start", "<Button-1>", lambda e: toggle_start())

    right_btn_frame = tk.Frame(bottom_frame, bg=BG_COLOR)
    right_btn_frame.pack(side="right")

    tk.Button(right_btn_frame, text="Save", bg=BTN_COLOR, fg=TEXT_COLOR).pack(side="left", padx=5)
    tk.Button(right_btn_frame, text="Edit", bg=BTN_COLOR, fg=TEXT_COLOR).pack(side="left", padx=5)
    tk.Button(right_btn_frame, text="Clear", bg=BTN_COLOR, fg=TEXT_COLOR).pack(side="left", padx=5)


def add_audio_to_text():
    global output_text

    def browse_file():
        nonlocal upload_btn
        global selected_audio_path
        selected_audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.flac")])
        if selected_audio_path:
            upload_btn.config(text="File Selected")

    def convert_audio():
        if selected_audio_path:
            dummy_result = f"Transcribed from audio:\n{selected_audio_path}\n\nLanguage: {output_lang.get()}"
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, dummy_result)
        else:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "Please upload an audio file first.")

    def translate_text():
        current = output_text.get("1.0", tk.END).strip()
        if current:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"Translated text in {output_lang.get()}:\n\n[Translated version of previous text]")
        else:
            output_text.insert(tk.END, "Nothing to translate. Please convert first.")

    tk.Label(content_frame, text="Audio to Text Screen", font=("Arial", 14),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

    input_row = tk.Frame(content_frame, bg=BG_COLOR)
    input_row.pack(pady=10)

    upload_btn = tk.Button(input_row, text="Upload File", command=browse_file,
                           bg=BTN_COLOR, fg=TEXT_COLOR, font=("Arial", 10, "bold"))
    upload_btn.pack(side="left", padx=10)

    output_lang = ttk.Combobox(input_row, values=["English", "Marathi", "Hindi", "Telugu"], width=15)
    output_lang.set("English")
    output_lang.pack(side="left", padx=10)

    convert_btn = tk.Button(content_frame, text="Convert Audio to Text",
                            command=convert_audio, bg=BTN_COLOR, fg=TEXT_COLOR,
                            font=("Arial", 11, "bold"))
    convert_btn.pack(pady=(10, 5))

    translate_btn = tk.Button(content_frame, text="Translate",
                              command=translate_text, bg="#ffddee", fg="#000000",
                              font=("Arial", 11, "bold"))
    translate_btn.pack(pady=(0, 10))

    output_text = tk.Text(content_frame, wrap="word", font=("Arial", 12),
                          bg=TEXT_BG, fg=TEXT_COLOR, height=10)
    output_text.pack(fill="both", expand=False, padx=10, pady=(5, 10))


def add_meeting_placeholder():
    tk.Label(content_frame, text="Meeting Screen", font=("Arial", 14),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)


def open_menu():
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.geometry("200x150+{}+{}".format(hamburger_btn.winfo_rootx(), hamburger_btn.winfo_rooty() + hamburger_btn.winfo_height()))
    popup.configure(bg=BG_COLOR)

    popup_frame = tk.Frame(popup, bg=BG_COLOR, bd=2, relief="raised")
    popup_frame.pack(fill="both", expand=True, padx=2, pady=2)

    close_btn = tk.Button(popup_frame, text="X", bg="red", fg="#000000",
                          font=("Arial", 10, "bold"), command=popup.destroy, bd=0)
    close_btn.pack(anchor="ne", padx=5, pady=5)

    tk.Button(popup_frame, text="Meeting", bg=BTN_COLOR, fg=TEXT_COLOR,
              command=lambda: [popup.destroy(), switch_screen("meeting")]).pack(fill="x", pady=5, padx=10)
    tk.Button(popup_frame, text="Audio to Text", bg=BTN_COLOR, fg=TEXT_COLOR,
              command=lambda: [popup.destroy(), switch_screen("audio_to_text")]).pack(fill="x", pady=5, padx=10)
    tk.Button(popup_frame, text="Voice to Text", bg=BTN_COLOR, fg=TEXT_COLOR,
              command=lambda: [popup.destroy(), switch_screen("voice_to_text")]).pack(fill="x", pady=5, padx=10)


# --- Main App Window ---
root = tk.Tk()
root.title("LiveNoteClass")
root.geometry("1000x600")
root.configure(bg=BG_COLOR)

# --- Top Frame for Logo and Title ---
top_frame = tk.Frame(root, bg=BG_COLOR)
top_frame.pack(pady=(10, 0), fill="x")

center_title_frame = tk.Frame(top_frame, bg=BG_COLOR)
center_title_frame.pack(anchor="center")

logo_img = Image.open("Logo.jpg")
logo_img = logo_img.resize((100, 100))
logo_photo = ImageTk.PhotoImage(logo_img)

logo_label = tk.Label(center_title_frame, image=logo_photo, bg=HEADER_COLOR)
logo_label.pack(side="left", padx=(0, 5))

title_label = tk.Label(center_title_frame, text="LiveNoteClass", font=("Arial", 20, "bold"),
                       bg=HEADER_COLOR, fg=TEXT_COLOR)
title_label.pack(side="left")

# Frame for holding hamburger button pinned top-left
hamburger_frame = tk.Frame(root, bg=BG_COLOR)
hamburger_frame.place(x=10, y=10)

hamburger_btn = tk.Button(hamburger_frame, text="☰", font=("Arial", 16),
                          bg=BTN_COLOR, fg=TEXT_COLOR, command=open_menu)
hamburger_btn.pack()

content_frame = tk.Frame(root, bg=BG_COLOR)
content_frame.pack(fill="both", expand=True)

switch_screen(current_screen)

root.mainloop()
