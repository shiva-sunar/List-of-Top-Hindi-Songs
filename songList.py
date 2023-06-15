# importing packages
from pytube import YouTube
import os
from pytube import Search
import pandas as pd
os.system('command 2> /dev/null')

def saveSongListHindi():
    tables = []
    for i in range(97, 123):
        url = f"https://bollywoodproduct.in/complete-list-of-bollywood-songs-alphabetically-from-{chr(i)}/"
        table = pd.read_html(url)
        tables.append(table)
    combined = pd.concat([t[0] for t in tables], axis=0)
    combined.reset_index(drop=True, inplace=True)
    combined.to_csv("combined.csv", index=False)

def saveSongListBillBoard():
    tables=[]
    for year in range(1959,2024):
        url = f'https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number_ones_of_{str(year)}'
        dfs = pd.read_html(url, header=0)
        dfs = [df for df in dfs if 'Song' in df.columns]
        dfs=[df.drop_duplicates(subset=["Song"]) for df in dfs]
        for df in dfs:
            rename_dict = {col: 'Artist' for col in df.columns if 'artist' in col.lower()}
            df = df.rename(columns=rename_dict)
            tables.append(df)
    combined = pd.concat([t[["Song","Artist"]] for t in tables], axis=0)
    combined.reset_index(drop=True, inplace=True)
    combined.to_csv("billboardCombined.csv", index=False)

    
def getYTUrl(searchKeyword):
    s = Search(searchKeyword)
    id = (
        str(s.results[0]).replace("<pytube.__main__.YouTube object: videoId=", "").replace(">", "")
    )  # video id of first video
    return "https://www.youtube.com/watch?v=" + id


def saveYoutubeAudio(yurl, songDir):
    # url input from user
    yt = YouTube(yurl)
    # extract only audio
    video = yt.streams.filter(only_audio=True).get_audio_only()  # Highest quality audio
    # download the file
    out_file = video.download(output_path=songDir)
    # # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"
    os.rename(out_file, new_file)
    # # result of success
    print(yt.title + " has been successfully downloaded.")

# saveSongListBillBoard()
# saveSongListHindi()

import pandas as pd

# songsDF = pd.read_csv("combined.csv")
# songDir="./HindiSongs/"

songsDF = pd.read_csv("billboardCombined.csv")
songDir="./Billboard/"

songsDF.dropna(how='all', inplace=True)
for index, row in songsDF.iterrows():
    # keyword = f"{row['Song']}, {row['Film']}, {int(row['Year'])}"
    # fileName=f"{row['Song']} ({row['Film']} {int(row['Year'])}).mp3"
 
    keyword = f"{row['Song']}, ({row['Artist']})"
    # fileName=f"{row['Song']}-({row['Artist']}).mp3"
    try:
        url = getYTUrl(keyword)
        saveYoutubeAudio(yurl= url,songDir=songDir)
    except Exception as e:
        print(f"Some Error with Song:{keyword}")
        os.system(f"echo {keyword} >> error.txt")

