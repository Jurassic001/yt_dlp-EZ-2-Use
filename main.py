import subprocess
from threading import Thread
import pyperclip
import keyboard as kb
import time
import os

clear = lambda: os.system('cls')
dlPhase = 1
isVideo = True

def targFolder() -> str:
    """ Returns the target folder as a string, based on whether you're downloading a .mp4 or a .mp3 file

    Returns:
        str: _description_
    """
    if isVideo: return 'Videos'
    else: return 'Music'

def fileExt(formatCode: int) -> str:
    """ Returns either the active or inactive download format as a string, based on input.

    Args:
        formatCode (int): Format codes: 0 - display current format, 1 - display opposite format

    Returns:
        str: The download format (mp4 or mp3)
    """
    ext = ['mp4','mp3']
    if isVideo and ext[0] == 'mp3': ext.reverse()
    elif not isVideo and ext[0] == 'mp4': ext.reverse()
    return ext[formatCode]

def processURL() -> None:
    """ Prints a little processing graphic while we fetch the video title
    """
    processingMsg = "Processing the URL"
    print(processingMsg)
    for i in range(2):
        processingMsg = "Processing the URL"
        for i in range(3):
            clear()
            processingMsg = processingMsg + "."
            print(processingMsg)
            time.sleep(0.5)

def downloadVideo(link: str, vidName: str) -> None:
    """ Download the target video

    Args:
        link (str): The URL of the media that you want to download
        vidName (str): The name of the media that you want to download
    """
    # Print the name of the to-be downloaded video and it's destination
    clear()
    print("Downloading: " + vidName + " to your " + targFolder() + " folder")
    print("")
    # Let the user read the printed line before filling the console with status updates
    time.sleep(1)
    # Start downloading the video
    if isVideo:
        output = subprocess.run(['yt-dlp', '-f bv*[vcodec^=avc]+ba[ext=m4a]/b[ext=mp4]/b', '-o~/Videos/%(title)s.%(ext)s', link])
    else:
        output = subprocess.run(['yt-dlp','--ffmpeg-location','C:/FFmpeg/bin/ffmpeg.exe','-x','--audio-format','mp3','-o~/Music/%(title)s.%(ext)s', link])
    # Make sure the user sees the successful/failed download status before closing the console.
    print("")
    print("Press Enter to exit the program")
    kb.wait("Enter")
    exit()

def configDownload(link: str) -> None:
    """ Here the user can see the video title, choose to download as an mp4 or mp3, and continue or go back

    Args:
        link (str): The URL of the media that you want to download
    """
    global isVideo
    dlPhase = 2
    processing.start()
    videoName = (subprocess.check_output(['yt-dlp', '-O"%(title)s"', link], text=True, timeout=5)).strip()
    processing.join()
    while dlPhase == 2:
        clear()
        print("Selected video: " + videoName)
        print("Downloading as an " + fileExt(0))
        print("Press M to switch to " + fileExt(1))
        print("")
        print("Press Enter to start the download")
        print("Press Backspace to select another video")
        time.sleep(0.5)
        while True:
            if kb.is_pressed("enter"):
                downloadVideo(link, videoName)
            elif kb.is_pressed("backspace"):
                dlPhase = 1
                break
            elif kb.is_pressed("m"):
                isVideo = not isVideo
                break

processing = Thread(target=processURL)
while dlPhase == 1:
    # Print instructions and wait for user input
    clear()
    print("Copy video URL and press Enter to start the download or Backspace to close the program")
    time.sleep(0.5)
    while True:
        if kb.is_pressed("Enter"):
            break
        elif kb.is_pressed("Backspace"):
            exit()
        time.sleep(0.05)
    url = pyperclip.paste()
    # Look for a valid URL
    if url.__contains__("http://") or url.__contains__("https://"):
        configDownload(url)
    else:
        # Warn the user if a URL isn't detected and give them the option to abandon/continue the download.
        print("")
        print("Valid URL not found. Do you want to continue? (Y/N)")
        time.sleep(0.5)
        while True:
            if kb.is_pressed("y") or kb.is_pressed("enter"):
                configDownload(url)
            elif kb.is_pressed("n") or kb.is_pressed('backspace'):
                print("Download abandoned")
                time.sleep(1)
                break
