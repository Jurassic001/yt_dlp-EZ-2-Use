import os
import subprocess
import sys
import time

import keyboard as kb
import pyperclip


class simple_ytdl:
    def __init__(self) -> None:
        self.EXT_DICT: dict[bool, str] = {
            True: "mp4",
            False: "mp3",
        }  # Dictionary of file extensions that correspond to the value of isVideo

        self.ERROR_MSG: dict[type[Exception], str] = {
            subprocess.TimeoutExpired: "Video search timed out.",
            subprocess.CalledProcessError: "Invalid URL or the video cannot be found.",
        }  # Dictionary of error messages that correspond to the exception

        self.clear = lambda: os.system("cls")  # Clear the console
        self.isVideo: bool = True  # Download format: True - mp4, False - mp3

        if sys.platform.startswith("linux"):
            self.paste = lambda: subprocess.check_output("xclip -selection clipboard -o", shell=True).decode().strip()
        else:
            self.paste = pyperclip.paste

    def downloadVideo(self, link: str, vidName: str) -> None:
        """Download the target video

        Args:
            link (str): The URL of the media that you want to download
            vidName (str): The name of the media that you want to download
        """
        # Print the name of the to-be downloaded video and it's destination
        self.clear()
        targ_folder = "Videos" if self.isVideo else "Music"
        print(f"Downloading: {vidName} to your {targ_folder} folder\n")
        # Let the user read the printed line before filling the console with status updates
        time.sleep(1)
        # Start downloading the video
        if self.isVideo:
            subprocess.run(
                [
                    "yt-dlp",
                    "--format",
                    "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
                    "-o",
                    os.path.expanduser("~/Videos/%(title)s.%(ext)s"),
                    link,
                ]
            )
        else:
            subprocess.run(
                [
                    "yt-dlp",
                    "--extract-audio",
                    "--audio-format",
                    "mp3",
                    "--audio-quality",
                    "0",
                    "-o",
                    os.path.expanduser("~/Music/%(title)s.%(ext)s"),
                    link,
                ]
            )
        # Make sure the user sees the successful/failed download status before closing the console.
        print("\nPress Enter to exit the program")
        kb.wait("Enter")
        sys.exit()

    def configDownload(self, link: str) -> None:
        """Here the user can see the video title, choose to download as an mp4 or mp3, and continue or go back

        Args:
            link (str): The URL of the media that you want to download
        """
        self.clear()
        print("Processing the URL...\n")
        try:
            videoName = (subprocess.check_output(["yt-dlp", "-O", "%(title)s", link], text=True, timeout=10)).strip()
        except Exception as e:
            err_msg = self.ERROR_MSG.get(type(e), "An unknown error occurred.")
            print(f"\n{err_msg} Press Enter to try again.")
            kb.wait("enter")
            return
        while True:
            self.clear()
            print(f"Selected video: {videoName}")
            print(f"Downloading as an {self.EXT_DICT[self.isVideo]}")
            print(f"Press M to switch to {self.EXT_DICT[not self.isVideo]}\n")
            print("Press Enter to start the download")
            print("Press Backspace to select another video")
            time.sleep(0.5)
            while True:
                if kb.is_pressed("enter"):
                    self.downloadVideo(link, videoName)
                elif kb.is_pressed("m"):
                    self.isVideo = not self.isVideo
                    break
                elif kb.is_pressed("backspace"):
                    return

    def main(self) -> None:
        while True:
            # Print instructions and wait for user input
            self.clear()
            print("Press Enter once you've copied the URL")
            kb.wait("Enter")
            if sys.platform == "win32":
                url = pyperclip.paste()
            elif sys.platform == "linux":
                pyperclip.set_clipboard("xclip")
            elif sys.platform == "darwin":
                pyperclip.set_clipboard("pbobjc")
            else:  # Unsupported OS
                print("Unsupported OS")
                sys.exit()
            # Look for a valid URL
            if url.startswith("http"):
                self.configDownload(url)
            else:
                # Warn the user if a URL isn't detected and give them the option to abandon/continue the download.
                print("\nValid URL not found. Do you want to continue? (Yes/Y/Enter or No/N/Backspace)")
                time.sleep(0.5)
                while True:
                    if kb.is_pressed("y") or kb.is_pressed("enter"):
                        self.configDownload(url)
                        break
                    elif kb.is_pressed("n") or kb.is_pressed("backspace"):
                        break


if __name__ == "__main__":
    download = simple_ytdl()
    download.main()
