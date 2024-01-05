import subprocess
import pyperclip
import keyboard as kb
import time

def downloadVideo(link):
    # Print the name of the to-be downloaded video in a more readable format
    print("")
    subprocess.run(['yt-dlp', '-ODownloading: "%(title)s" to your Videos folder', link])
    print("")
    # Let the user (me) read the printed line before filling the console with status updates
    time.sleep(1)
    # Start downloading the video
    """All of the below commands work, but they all seem to max out at 720p video quality"""
    subprocess.run(['yt-dlp','--ffmpeg-location','C:/FFmpeg/bin/ffmpeg.exe','-S res:1080','-o~/Videos/%(title)s.%(ext)s', link])
    #subprocess.run(['yt-dlp','-f mp4','-o~/Videos/%(title)s.%(ext)s', link])
    #subprocess.run(['yt-dlp','--ffmpeg-location','C:/FFmpeg/bin/ffmpeg.exe','-x','--audio-format','mp3','-o~/Videos/%(title)s.%(ext)s', link])
    """"""
    # Give the user (again, me) time to process a succesful or failed download
    time.sleep(0.5)

# Loop to check the clipboard's content and start the download
while True:
    # Capture the current content on the clipboard
    url = pyperclip.paste()
    # If the content on the clipboard looks like a URL then start downloading
    if url.__contains__("http://") or url.__contains__("https://"):
        downloadVideo(url)
        # Once the download is finished break out of the loop
        break
    # If the content of the clipboard doesn't look like a URL then wait a little bit and check again. 
    time.sleep(1)
    # Make sure to tell the user (me) what's happening.
    print("Cannot identify valid URL. Checking again...")
