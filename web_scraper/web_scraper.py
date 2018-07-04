from bs4 import BeautifulSoup
from scrape_target import target
import requests


for artist in target:
    print(artist)
    for track in target[artist]:
        print(track)
        url = 'https://azlyrics.com/lyrics/'+artist+'/'+track +'.html'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        read_lyrics = requests.get(url, headers=headers)
        soup = BeautifulSoup(read_lyrics.content, 'html.parser')
        for i in soup.findAll('br'):
            i.extract()
        lyrics = soup.find_all("div", attrs={"class": None, "id": None})
        final = str(str(lyrics).split('\n'))
        print(final)
