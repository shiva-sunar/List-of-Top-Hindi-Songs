# importing packages
from pytube import YouTube
import os
from pytube import Search
import pandas as pd
os.system('command 2> /dev/null')

def saveSongList():
    tables = []
    for i in range(97, 123):
        url = f"https://bollywoodproduct.in/complete-list-of-bollywood-songs-alphabetically-from-{chr(i)}/"
        table = pd.read_html(url)
        tables.append(table)
    combined = pd.concat([t[0] for t in tables], axis=0)
    combined.reset_index(drop=True, inplace=True)
    combined.to_csv("combined.csv", index=False)


def getYTUrl(searchKeyword):
    s = Search(searchKeyword)
    id = (
        str(s.results[0]).replace("<pytube.__main__.YouTube object: videoId=", "").replace(">", "")
    )  # video id of first video
    return "https://www.youtube.com/watch?v=" + id


def saveYoutubeAudio(yurl, destination="."):
    # url input from user
    yt = YouTube(yurl)
    # extract only audio
    video = yt.streams.filter(only_audio=True).get_audio_only()  # Highest quality audio
    # download the file
    out_file = video.download(output_path=destination)
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"
    os.rename(out_file, new_file)
    # # result of success
    print(yt.title + " has been successfully downloaded.")

saveSongList()

songsDF = pd.read_csv("combined.csv")
for index, row in songsDF.iterrows():
    keyword = f"{row['Song']}, {row['Film']}, {int(row['Year'])}"
    try:
        url = getYTUrl(keyword)
        saveYoutubeAudio(url,"./HindiSongs/")
    except Exception as e:
        print(f"Some Error with Song:{keyword}")

