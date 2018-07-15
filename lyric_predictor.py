import requests
import sys
import os
import shutil
import datetime
import hashlib
import scraper
from scraper_target import target
from pymarkovchain import MarkovChain

# Read settings
gen_db = False
chorus = False

with open('Settings.txt') as f:
    for line in f:
        if 'db = True' in line:
            gen_db = True
            if str(input('chorus only? ')) == 'y':
                chorus = True
        if 'db name' in line:
            db_name = str(line.split('=')[1]).strip()
        if 'number of phrases' in line:
            number_of_phrases = int(line.split('=')[1])
f.close()

#-------------------------------------------------------------------------------
# Create run folder
folder = os.path.join(os.getcwd(), ('runs/' + db_name + '_' + datetime.datetime.now().strftime('%d_%H-%M-%S'))) + '/'
os.makedirs(folder)

# Copy settings and target files to folder
shutil.copy2('Settings.txt', folder + 'Settings.txt')
shutil.copy2('scraper_target.py', folder + 'scraper_target.py')

#-------------------------------------------------------------------------------
# Generate lyric string
lyrics = ''

if gen_db:
    song_list = scraper.song_list(target)
    lyrics = scraper.scrape(chorus, song_list)

    # Clean up lyrics
    lyrics = lyrics.replace('(', '').replace(')', '')
    lyrics = lyrics.replace('"', '')
    lyrics = lyrics.lower()
    #print(lyrics)

# Import lyrics
#else:
#    with open(db_path, 'r') as inputfile:
#        for line in inputfile:
#            lyrics += line + '\n'

# Create model instance
mc = MarkovChain('db/' + db_name)

# Generate db
mc.generateDatabase(lyrics)
mc.dumpdb()

#-------------------------------------------------------------------------------
# Write lyrics
f = open(folder + db_name + '.txt', 'w')

for i in range(0, int(number_of_phrases)):
    seed = str(input('seed: '))
    f.write(mc.generateStringWithSeed(seed) + '\n')
	#f.write(mc.generateString() + '\n')

f.close
