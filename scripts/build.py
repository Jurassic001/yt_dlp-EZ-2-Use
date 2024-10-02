import os
import subprocess

WORKING_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)))


def build() -> None:
    """Builds the project using pyinstaller"""
    subprocess.run(
        [
            "pyinstaller",
            "--onefile",
            "--add-binary",
            f"{WORKING_DIR}/bin/yt-dlp.exe;bin",
            "--add-binary",
            f"{WORKING_DIR}/bin/ffmpeg.exe;bin",
            "--distpath",
            "./pyinstaller/dist",
            "--workpath",
            "./pyinstaller/build",
            "--specpath",
            "./pyinstaller",
            "--name",
            f"simple_ytdl.{subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], text=True).strip()}",
            "main.py",
        ],
        cwd=WORKING_DIR,
    )


if __name__ == "__main__":
    build()
