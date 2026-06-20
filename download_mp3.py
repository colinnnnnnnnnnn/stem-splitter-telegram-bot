import subprocess


def download_mp3(url: str) -> str:
    result = subprocess.run(
        [
            "yt-dlp",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--print",
            "after_move:filepath",
            "-o",
            "/home/calin/code/stem-splitter-telegram-bot/input/%(title)s.%(ext)s",
            url,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()
