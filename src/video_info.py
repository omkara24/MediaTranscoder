import subprocess
import json
import os


def get_video_info(file_path):

    command = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    data = json.loads(result.stdout)

    video_stream = None

    for stream in data["streams"]:
        if stream["codec_type"] == "video":
            video_stream = stream
            break

    file_size_mb = (
        int(data["format"]["size"])
        / (1024 * 1024)
    )

    duration = float(
        data["format"]["duration"]
    )

    width = video_stream.get("width", "Unknown")
    height = video_stream.get("height", "Unknown")

    codec = video_stream.get(
        "codec_name",
        "Unknown"
    ).upper()

    fps_raw = video_stream.get(
        "r_frame_rate",
        "0/1"
    )

    num, den = fps_raw.split("/")

    fps = round(
        float(num) / float(den),
        2
    )

    return {
        "size": round(file_size_mb, 2),
        "duration": round(duration, 2),
        "width": width,
        "height": height,
        "codec": codec,
        "fps": fps
    }