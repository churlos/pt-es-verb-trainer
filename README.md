# pt-es-verb-trainer
A customizable Portuguese verb trainer, designed mainly for Spanish speakers. Aims to offer flexible practice modes and, eventually, adaptive behaviour based on user performance.
This project consists of a verb conjugation trainer for learning Portuguese. The simpler version will store no statistics on performance and will not be
adaptive, although the final goal is to experiment and, hopefully, achieve a good learning model (better than pure space repetition as I have used it so far). Some customization will be available at both versions.
It will come along with some lists based of learning objectives, and with some translations from the Spanish - Portuguese part as example. Each users 
should provide their own personal translations, since this is somewhat subjective or dependant on regional uses of verbs.

## General info.
### Project structure (so far...)
root/
│
├── preprocessing/        # Preprocessing scripts
├── src/                  # Main project code (not yet available)
├── json/                 # Initial dataset (ignored by Git)
├── json_01/              # Intermediate dataset (ignored by Git)
├── verbs/                # Final dataset
├── README.md             # This file
├── LICENSE               # GPLv3 license
└── .gitignore            # Ignored files and folders

### Execution

Scripts must be executed at the directory they are located.

### Requirements

- Python 3.x  

### License

This project is licensed under **GNU GPLv3**.  
See the `LICENSE` file for details.

#### About datasets

Original verbs dataset was taken from https://github.com/ian-hamlin/verb-data, and it is originally sourced from wikipedia. Hence, my dataset in verbs/ continues the same license that the original set had, updated to version 4.0: https://creativecommons.org/licenses/by-sa/4.0/

## Pipeline
- having the initial dataset from verb-data
- preprocessing/preprocessing01.py
- preprocessing/preprocessing02.py

## Collaborations

Open to suggestions, corrections (please, if u find anything let me know) and working together in this project or related ones (resources for learning Portuguese).
  






