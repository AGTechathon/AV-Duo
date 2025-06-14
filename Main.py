import tkinter as tk
from tkinter import ttk

# Colors
BG_COLOR = "#ffffff"        
HEADER_COLOR = "#ffffff"    
BTN_COLOR = "#f0f0f0"       
TEXT_BG = "#ffffff"        
TEXT_COLOR = "#000000"      

# Main App Window
root = tk.Tk()
root.title("LiveNoteClass")
root.geometry("1000x600")
root.configure(bg=BG_COLOR)

# --- App Title ---
title_label = tk.Label(root, text="LiveNoteClass", font=("Arial", 16, "bold"),
                       bg=HEADER_COLOR, fg=TEXT_COLOR, padx=10, pady=5)
title_label.pack(pady=(10, 0))

# --- Language Selection ---
lang_frame = tk.Frame(root, bg=BG_COLOR)
lang_frame.pack(fill="x", padx=10, pady=10)

tk.Label(lang_frame, text="Speaker Language:", bg=BG_COLOR, fg=TEXT_COLOR).pack(side="left")
speaker_lang = ttk.Combobox(lang_frame, values=["English", "Marathi", "Hindi", "Telugu"], width=15)
speaker_lang.set("English")
speaker_lang.pack(side="left", padx=5)

tk.Label(lang_frame, text="Translate To:", bg=BG_COLOR, fg=TEXT_COLOR).pack(side="left")
translate_to = ttk.Combobox(lang_frame, values=["English", "Marathi", "Hindi", "Telugu"], width=15)
translate_to.set("English")
translate_to.pack(side="left", padx=5)

# --- Text Area ---
text_frame = tk.Frame(root, bg=BG_COLOR)
text_frame.pack(padx=10, pady=5, fill="both", expand=True)

text_area = tk.Text(text_frame, wrap="word", font=("Arial", 12),bg=TEXT_BG, fg=TEXT_COLOR)
text_area.pack(fill="both", expand=True, side="left")

scrollbar = tk.Scrollbar(text_frame, command=text_area.yview)
scrollbar.pack(side="right", fill="y")
text_area.config(yscrollcommand=scrollbar.set)

# --- Bottom Buttons ---
bottom_frame = tk.Frame(root, bg=BG_COLOR)
bottom_frame.pack(fill="x", padx=10, pady=10)

# Start/Stop Buttons
center_btn_frame = tk.Frame(bottom_frame, bg=BG_COLOR)
center_btn_frame.pack(side="bottom")

start_btn = tk.Button(center_btn_frame, text="Start", bg=BTN_COLOR, fg=TEXT_COLOR, padx=10)
start_btn.pack(side="left", padx=10)

stop_btn = tk.Button(center_btn_frame, text="Stop", bg=BTN_COLOR, fg=TEXT_COLOR, padx=10)
stop_btn.pack(side="left", padx=10)

# Right Controls: Save, Clear, Edit
right_btn_frame = tk.Frame(bottom_frame, bg=BG_COLOR)
right_btn_frame.pack(side="right")

tk.Button(right_btn_frame, text="save docs", bg=BTN_COLOR, fg=TEXT_COLOR).pack(side="left", padx=5)
tk.Button(right_btn_frame, text="clear", bg=BTN_COLOR, fg=TEXT_COLOR).pack(side="left", padx=5)
tk.Button(right_btn_frame, text="edit", bg=BTN_COLOR, fg=TEXT_COLOR).pack(side="left", padx=5)

root.mainloop()
