import subprocess
from threading import Thread
import pyperclip
import keyboard as kb
import time
import os

clear = lambda: os.system('cls')
dlPhase = 1
isVideo = True

def targFolder():
    if isVideo: return 'Videos'
    else: return 'Music'

def fileExt(formatCode: int):
    """
    Format codes: 0 - terminal format, 1 - display format, 2 - display opposite format
    """
    ext = ['mp4','mp3']
    if isVideo and ext[0] == 'mp3': ext.reverse()
    elif not isVideo and ext[0] == 'mp4': ext.reverse()
    if not formatCode: return '-f ' + ext[0]
    return ext[formatCode - 1]

def processURL():
    for i in range(3):
        processingMsg = "Processing the URL"
        for i in range(3):
            clear()
            processingMsg = processingMsg + "."
            print(processingMsg)
            time.sleep(0.5)

def downloadVideo(link):
    # Print the name of the to-be downloaded video in a more readable format
    print("")
    subprocess.run(['yt-dlp', '-ODownloading: "%(title)s" to your' + targFolder() + 'folder', link])
    print("")
    # Let the user (me) read the printed line before filling the console with status updates
    time.sleep(1)
    # Start downloading the video
    """All of the below commands work, but they all seem to max out at 720p video quality"""
    # subprocess.run(['yt-dlp','--ffmpeg-location','C:/FFmpeg/bin/ffmpeg.exe','-S res:1080','-o~/Videos/%(title)s.%(ext)s', link])

    subprocess.run(['yt-dlp', fileExt(0),'-o~/' + targFolder() + '/%(title)s.%(ext)s', link])

    # subprocess.run(['yt-dlp','-f mp4','-o~/Videos/%(title)s.%(ext)s', link])
    # subprocess.run(['yt-dlp','--ffmpeg-location','C:/FFmpeg/bin/ffmpeg.exe','-x','--audio-format','mp3','-o~/Videos/%(title)s.%(ext)s', link])
    """"""
    # Give the user (again, me) time to process a succesful or failed download
    time.sleep(0.5)

def configDownload(link):
    global isVideo
    dlPhase = 2
    processing.start()
    videoName = subprocess.check_output(['yt-dlp', '-OSelected video: %(title)s', link], text=True, timeout=5)
    processing.join()
    while dlPhase == 2:
        clear()
        print(videoName)
        print("Downloading as an " + fileExt(1))
        print("Press M to switch to " + fileExt(2))
        print("")
        print("Press Enter to start the download")
        print("Press Backspace to select another video")
        time.sleep(0.5)
        while True:
            if kb.is_pressed("enter"): downloadVideo(link)
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
    print("Copy video URL and press Enter to start the download")
    kb.wait("Enter")
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
