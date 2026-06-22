import os
import subprocess
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory

BASE = Path(__file__).resolve().parent
TMP_PARENT = BASE / "data" / "tmp"
INPUT_DIR = BASE / "data" / "input"
TMP_PARENT.mkdir(parents=True, exist_ok=True)
INPUT_DIR.mkdir(parents=True, exist_ok=True)


def download_mp3(url: str) -> tuple[str, str]:
    jobid = uuid.uuid4().hex
    with TemporaryDirectory(dir=TMP_PARENT) as td:
        try:
            res = subprocess.run(
                [
                    "yt-dlp",
                    "--extract-audio",
                    "--audio-format",
                    "mp3",
                    "--print",
                    "after_move:filepath",
                    "-o",
                    os.path.join(td, "%(title)s.%(ext)s"),
                    url,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            downloaded = res.stdout.strip().splitlines()[-1]
            final = Path(INPUT_DIR) / f"{jobid}.mp3"
            os.replace(downloaded, final)
            return str(final), jobid
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"yt-dlp failed: {e.stderr}")
