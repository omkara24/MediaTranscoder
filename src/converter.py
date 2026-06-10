import subprocess
import os


def get_video_duration(input_file):
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        input_file
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return float(result.stdout.strip())


def convert_mov_to_mp4(
    input_file,
    output_folder,
    progress_callback=None
):

    file_name = os.path.splitext(
        os.path.basename(input_file)
    )[0]

    output_file = os.path.join(
        output_folder,
        f"{file_name}_converted.mp4"
    )

    total_duration = get_video_duration(input_file)

    command = [
        "ffmpeg",
        "-i",
        input_file,

        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-crf",
        "28",

        "-pix_fmt",
        "yuv420p",

        "-c:a",
        "aac",
        "-b:a",
        "128k",

        "-movflags",
        "+faststart",

        "-progress",
        "pipe:1",

        "-nostats",

        "-y",
        output_file
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:

        if "out_time_ms=" in line:

            try:

                out_time_ms = int(
                    line.strip().split("=")[1]
                )

                current_time = out_time_ms / 1000000

                percent = min(
                    int(
                        (current_time / total_duration)
                        * 100
                    ),
                    100
                )

                if progress_callback:
                    progress_callback(percent)

            except:
                pass

    process.wait()

    if process.returncode != 0:
        raise Exception("Conversion failed")

    return output_file