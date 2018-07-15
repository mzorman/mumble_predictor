from bs4 import BeautifulSoup
from scraper_target import target
import requests

# Genius URL formats:
# https://genius.com/Playboi-carti-magnolia-lyrics
# https://genius.com/albums/Playboi-carti/Die-lit


#-------------------------------------------------------------------------------
# Parse through dictionary and scrape song urls
def song_list(target):
    songs = []
    # Iterate through albums for artists
    for artist in target:
        for album in target[artist]:
            # Get album page in html from genius
            url = 'https://genius.com/albums/'+artist+'/'+album
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            artist_page = requests.get(url, headers=headers)
            soup = BeautifulSoup(artist_page.text, 'lxml')
            #print(soup)

            # Create list of song urls in album
            for link in soup.find_all(class_="u-display_block"):
                songs.append(link.get('href'))

    #print(songs)
    return songs

#-------------------------------------------------------------------------------
# Scrape lyrics
def scrape(chorus, song_list):
    final = ' '
    db_path = '/Users/marlozorman/Desktop/Work/markov/db/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    for track in song_list:
        # Get song page in html from genius
        url = track
        read_lyrics = requests.get(url, headers=headers)
        soup = BeautifulSoup(read_lyrics.text, 'html.parser')

        # Pull lyrics from soup
        lyrics = soup.find('div', class_='lyrics').get_text()

        # Scrapes only the chorus
        if chorus == True:
            copy = False
            for line in lyrics.split('\n'):
                if 'Chorus' in line:
                    copy = True
                    #print('true firing')
                if 'Outro' in line or 'Verse' in line:
                    copy = False
                    #print('false firing')
                if copy:
                    lyrics += line + '\n'

        # Add song lyrics to db
        final += lyrics + '\n'

    print(final)

    # Write final db to text file
    f = open(db_path + str(input('db name: ')) + '.txt', 'a')
    f.write(final)
    f.close

    return final
