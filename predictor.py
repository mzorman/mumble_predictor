import requests
import sys
import os
import shutil
import datetime
import hashlib
from pymarkovchain import MarkovChain

# Lyrics source
API_URI = "http://lyrics.wikia.com/api.php?action=lyrics&fmt=realjson"

# Initialize
generate_database = False
base_db = False
add_path = False

# Read settings
with open('Settings.txt') as f:
    for line in f:
        if 'generate_database = True' in line:
            generate_database = True
        if 'generate_base = True' in line:
            base_db = True
        if 'db_name' in line:
            db_name = str(line.split('=')[1]).strip()
        if 'add_path' in line:
            path = str(line.split('=')[1]).strip()
        if 'number_of_phrases' in line:
            number_of_phrases = int(line.split('=')[1])
        if 'artists' in line:
            artists = str(line.split('=')[1]).split(', ')
f.close()

# Create run folder
folder = os.path.join(os.getcwd(), ('runs/' + db_name + '_' + datetime.datetime.now().strftime('%d_%H-%M-%S'))) + '/'
os.makedirs(folder)

# Copy settings file to folder
shutil.copy2('Settings.txt', folder + 'Settings.txt')

#-------------------------------------------------------------------------------

# Create model instance
mc = MarkovChain('db/' + db_name)

# Generate db of lyrics
if generate_database:
    # Giant string with all lyrics
    lyrics = ''

    # Iterate through artits to create db
    if base_db:
        for rapper in artists:
            params = {
                'artist': rapper
            }
            artist = requests.get(API_URI, params=params).json()
            for album in artist['albums']:
                for song in album['songs']:
                    params = {
                        'artist': rapper,
                        'song': song
                    }
                    print("Parsing \"{}\" from Wikia.".format(song))
                    response = requests.get(API_URI, params=params).json()["lyrics"]
                    lyrics += response.replace('[...]', '') + ' '

    # Add music not on lyrics.wikia from text file
    if add_path:
        with open(add_path, 'r') as inputfile:
            for line in inputfile:
                for word in line.strip('\n').split(' '):
                    lyrics += str(word) + ' '

    # Clean up database
    lyrics = lyrics.replace('(', '').replace(')', '')
    lyrics = lyrics.replace('"', '')
    lyrics = lyrics.lower()

    # Generating the database
    mc.generateDatabase(lyrics)
    mc.dumpdb()

#-------------------------------------------------------------------------------


# Predicting lyrics
f = open(folder + db_name + '.txt', 'w')

for i in range(0, int(number_of_phrases)):
	f.write(mc.generateString() + '\n')

f.close
