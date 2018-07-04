from bs4 import BeautifulSoup
from scraper_target import target
import requests

# Genius URL format:
# https://genius.com/Playboi-carti-magnolia-lyrics

# Initialize
chorus_only = False
final = ' '
chorus = ' '

# Read in settings
with open('scraper_settings.txt') as f:
    for line in f:
        if 'db_path' in line:
            db_path = str(line.split('=')[1]).strip()
        if 'chorus = True' in line:
            chorus_only = True
f.close()

#-------------------------------------------------------------------------------

# Parse through dictionary and collect all lyrics
for artist in target:
    for track in target[artist]:
        try:
            # Get song page in html from genius
            url = 'https://genius.com/'+artist+'-'+track+'-lyrics'
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            read_lyrics = requests.get(url, headers=headers)
            soup = BeautifulSoup(read_lyrics.text, 'html.parser')

            # Parse out the lyrics
            lyrics = soup.find('div', class_='lyrics').get_text()
            #print(lyrics)

            # Copy only the chorus if specified
            if chorus_only:
                copy = False
                for line in lyrics.split('\n'):
                    if 'Chorus' in line:
                        copy = True
                        #print('true firing')
                    if 'Outro' in line or 'Verse' in line:
                        copy = False
                        #print('false firing')
                    if copy:
                        for word in line.strip('\n').split(' '):
                            #print(word)
                            chorus += word + ' '
                            #print(chorus)

            # fix this
            #final += str(lyrics).split('\n')
            #for line in lyrics:
            #    #print(line)
            #    #print(type(line))
            #    for word in line.strip('\n').split(' '):
            #        final += word + ' '

        except:
            print(url)
            print(track + ' is not correct')

#-------------------------------------------------------------------------------

# Write lyrics to file
f = open(db_path + artist + '.txt', 'a')
f.write(final)
f.close

# Write chorus to file, if specified
if chorus_only:
    f = open(db_path + artist + '_' + 'chorus.txt', 'a')
    f.write(chorus)
    f.close
