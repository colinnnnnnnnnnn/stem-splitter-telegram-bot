import subprocess

url = "https://www.youtube.com/watch?v=aonTwBM1AZM"
subprocess.run(
    [
        "yt-dlp",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "-o",
        "/home/calin/code/stem-splitter-telegram-bot/input/%(title)s.%(ext)s",
        url,
    ]
)
