import customtkinter as ctk
from tkinter import filedialog
import threading

from converter import convert_mov_to_mp4
from video_info import get_video_info

# -----------------------------
# App Config
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -----------------------------
# Main Window
# -----------------------------
app = ctk.CTk()
app.title("MediaTranscoder")
app.geometry("950x750")

selected_files = []
output_folder = ""

# -----------------------------
# Select Files
# -----------------------------
def choose_file():

    global selected_files

    selected_files = filedialog.askopenfilenames(
        title="Select MOV Files",
        filetypes=[("MOV Files", "*.mov")]
    )

    if selected_files:

        file_label.configure(
            text=f"{len(selected_files)} file(s) selected"
        )

        try:

            info = get_video_info(
                selected_files[0]
            )

            video_info_label.configure(
                text=
                f"📁 File Size: {info['size']} MB\n"
                f"⏱ Duration: {info['duration']} sec\n"
                f"📺 Resolution: {info['width']} x {info['height']}\n"
                f"🎬 FPS: {info['fps']}\n"
                f"🎥 Codec: {info['codec']}"
            )

        except Exception as e:

            video_info_label.configure(
                text=f"Unable to read video info\n{e}"
            )

        status_label.configure(
            text="✅ Files Selected"
        )


# -----------------------------
# Output Folder
# -----------------------------
def choose_output_folder():

    global output_folder

    output_folder = filedialog.askdirectory(
        title="Choose Output Folder"
    )

    if output_folder:

        output_label.configure(
            text=output_folder
        )


# -----------------------------
# Conversion Worker
# -----------------------------
def conversion_worker():

    try:

        total_files = len(selected_files)

        for index, file in enumerate(selected_files):

            app.after(
                0,
                lambda i=index, t=total_files:
                status_label.configure(
                    text=f"🔄 Converting File {i+1} of {t}"
                )
            )

            def update_progress(percent):

                overall_progress = (
                    (index + percent / 100)
                    / total_files
                ) * 100

                app.after(
                    0,
                    lambda p=overall_progress:
                    progress_bar.set(
                        p / 100
                    )
                )

                app.after(
                    0,
                    lambda p=overall_progress:
                    progress_label.configure(
                        text=f"{int(p)}%"
                    )
                )

            convert_mov_to_mp4(
                file,
                output_folder,
                update_progress
            )

        app.after(
            0,
            lambda:
            progress_bar.set(1)
        )

        app.after(
            0,
            lambda:
            progress_label.configure(
                text="100%"
            )
        )

        app.after(
            0,
            lambda:
            status_label.configure(
                text=f"✅ Successfully Converted {total_files} File(s)"
            )
        )

        app.after(
            0,
            lambda:
            convert_btn.configure(
                state="normal"
            )
        )

    except Exception as e:

        app.after(
            0,
            lambda:
            status_label.configure(
                text=f"❌ Error\n{e}"
            )
        )

        app.after(
            0,
            lambda:
            convert_btn.configure(
                state="normal"
            )
        )


# -----------------------------
# Convert
# -----------------------------
def convert_video():

    if not selected_files:

        status_label.configure(
            text="⚠ Select MOV files first"
        )

        return

    if not output_folder:

        status_label.configure(
            text="⚠ Select output folder first"
        )

        return

    progress_bar.set(0)

    progress_label.configure(
        text="0%"
    )

    convert_btn.configure(
        state="disabled"
    )

    threading.Thread(
        target=conversion_worker,
        daemon=True
    ).start()


# -----------------------------
# UI
# -----------------------------
title = ctk.CTkLabel(
    app,
    text="MediaTranscoder",
    font=("Arial", 36, "bold")
)
title.pack(pady=(30, 15))

subtitle = ctk.CTkLabel(
    app,
    text="Universal MOV → MP4 Converter",
    font=("Arial", 16)
)
subtitle.pack(pady=(0, 20))

select_btn = ctk.CTkButton(
    app,
    text="Select MOV Files",
    width=300,
    height=45,
    command=choose_file
)
select_btn.pack(pady=10)

output_btn = ctk.CTkButton(
    app,
    text="Select Output Folder",
    width=300,
    height=45,
    command=choose_output_folder
)
output_btn.pack(pady=10)

convert_btn = ctk.CTkButton(
    app,
    text="Convert All To MP4",
    width=300,
    height=45,
    command=convert_video
)
convert_btn.pack(pady=10)

progress_bar = ctk.CTkProgressBar(
    app,
    width=500
)
progress_bar.pack(pady=(20, 10))
progress_bar.set(0)

progress_label = ctk.CTkLabel(
    app,
    text="0%"
)
progress_label.pack()

file_label = ctk.CTkLabel(
    app,
    text="No MOV files selected",
    wraplength=850
)
file_label.pack(pady=(20, 10))

output_label = ctk.CTkLabel(
    app,
    text="No output folder selected",
    wraplength=850
)
output_label.pack(pady=(10, 10))

video_info_label = ctk.CTkLabel(
    app,
    text="Video information will appear here",
    justify="left"
)
video_info_label.pack(pady=(15, 15))

status_label = ctk.CTkLabel(
    app,
    text="Waiting..."
)
status_label.pack(pady=20)

app.mainloop()