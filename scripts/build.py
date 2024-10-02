import argparse
import os
import shutil
import subprocess

WORKING_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)))


def build(clean: bool, simple: bool) -> None:
    """Builds the project using pyinstaller"""
    if clean:
        shutil.rmtree(os.path.join(WORKING_DIR, "pyinstaller"), ignore_errors=True)

    if simple:
        executable_name = "simple_ytdl"
    else:
        executable_name = f"simple_ytdl.{subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], text=True).strip()}"

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
            executable_name,
            "main.py",
        ],
        cwd=WORKING_DIR,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--clean",
        "-c",
        action="store_true",
        default=True,
        help="Remove the previous build files",
    )
    parser.add_argument(
        "--simple",
        "-s",
        action="store_true",
        default=False,
        help="Build the executable with a simple name, instead of the git hash",
    )

    args = parser.parse_args()
    build(args.clean, args.simple)
