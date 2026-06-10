import customtkinter as ctk

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Window
app = ctk.CTk()
app.title("MediaTranscoder")
app.geometry("800x500")

# Title
title = ctk.CTkLabel(
    app,
    text="MediaTranscoder",
    font=("Arial", 28, "bold")
)
title.pack(pady=30)

# Description
subtitle = ctk.CTkLabel(
    app,
    text="Convert MOV files to MP4 effortlessly"
)
subtitle.pack(pady=10)

# Button
select_button = ctk.CTkButton(
    app,
    text="Select MOV File"
)
select_button.pack(pady=20)

app.mainloop()