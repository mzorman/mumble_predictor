# MUMBLE PREDICTOR
Code adapted from: https://github.com/paladini/py-simple-lyric-generator

Pymarkovchain: https://pypi.org/project/PyMarkovChain/
^ Check dependencies ^

This repository contains a Markov Chain lyric predictor tailored towards mumble rap.
Training data is scraped from the web according to user input

## ----- lyric_predictor.py -----
Uses Settings.txt to generate database if needed and predict lyrics.
Can write line with seed or without - check code to see which is being used.

## ----- Settings.txt -----
db = Set true if you want to scrape lyrics 

db name = If db set False, enter name of db to use in db/ folder

	  If db set True, enter name for new db
	  
number of phrases = # of phrases to predict
