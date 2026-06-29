import os
import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SongData:
    jobid: str
    path: Path
    title: str


BASE = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE / "data" / "downloaded"
INCOMING_DIR = BASE / "data" / "incoming"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
INCOMING_DIR.mkdir(parents=True, exist_ok=True)


def download_audio(url: str, jobid: str) -> SongData:
    job_path = DOWNLOAD_DIR / jobid
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
                os.path.join(job_path, "%(title)s.%(ext)s"),
                url,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        res_path = Path(res.stdout.strip().splitlines()[-1])
        song_title = res_path.stem
        return SongData(jobid=jobid, path=res_path, title=song_title)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"yt-dlp failed: {e.stderr}")


