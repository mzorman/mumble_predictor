# MUMBLE PREDICTOR
Code adapted from: https://github.com/paladini/py-simple-lyric-generator
Pymarkovchain: https://pypi.org/project/PyMarkovChain/

This repository contains a Markov Chain lyric predictor tailored towards mumble rap
Training data is scraped from the web according to user input

## ----- predictor.py -----
Uses Settings.txt to generate database if needed and predict lyrics

## ----- Settings.txt -----
generate_database = (True, unless you want to reuse old db)
db_name = (name of old db if previous if False)
add_path = db/ + (name of text file with additional data)
number_of_phrases = (lines to predict)
artists = (Enter artists to include in db - seperate with commas)

