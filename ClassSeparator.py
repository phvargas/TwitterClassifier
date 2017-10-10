import sys
from time import strftime, localtime, time
import os
import re

"""
This Python program
  1. Separate Harassment collection into two separate cluster files:
     Harassment and non-harassment.
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Sat,  Sep 23, 2017 at 21:24:16'
__email__ = 'pvargas@cs.odu.edu'


def cluster(in_file, cat_dict):
    with open(in_file, "r", encoding='iso-8859-1') as f:
        inventory = {'e': 0, 'h': 0, 'n': 0, 'o': 0}
        ha_except_file = open('ha_exception.dat', 'w')
        counter = 0
        for row in f:
            counter += 1
            if counter > 1:                                         # does not write header
                row = row.strip()                                   # removes EOL character
                row = row.replace('"', '')

                try:
                    """
                    If ID in harassment corpus is numeric, then makes classification based on CODE type [H|N].
                    Otherwise, it creates an entry in the exception harassment file
                    """
                    if isinstance(int(row[0]), int):
                        try:
                            # writes harassment tweets with CODE type 'H' into harassment file
                            regex = re.search("^(\d+)(\s+H\s+)(.*)", row)
                            print(regex.group(1).strip(), regex.group(3), "---> Harassment", counter)
                            inventory['h'] += 1

                            filename = cat_dict['h'] + 'tweet' + str(regex.group(1)).zfill(5) + ".txt"
                            tweet = regex.group(3).strip()

                            create_tweet_file(filename, tweet)

                        except AttributeError:
                            try:
                                # writes non-harassment tweets with CODE type 'N' into non-harassment file
                                regex = re.search("^(\d+)(\s+N\s+)(.*)", row)
                                print(regex.group(3), "---> No harassment", counter)
                                inventory['n'] += 1

                                filename = cat_dict['n'] + 'tweet' + str(regex.group(1)).zfill(5) + ".txt"
                                tweet = regex.group(3).strip()

                                create_tweet_file(filename, tweet)

                            except AttributeError:
                                print(row, "not classified, no exception")
                                ha_except_file.write(row + "\n")
                                inventory['o'] += 1

                except ValueError:
                    # writes exception tweets data into exception file
                    print(row, "-------------> EXCEPTION")
                    inventory['e'] += 1
                    ha_except_file.write(row + "\n")

    # print classification inventory
    for key in inventory:
        print('key: %c; quantity: %d' % (key, inventory[key]))

    # close all file-handles
    ha_except_file.close()

    print(counter)
    return


def create_tweet_file(filename, tweet):
    fhs = open(filename, "w")
    fhs.write(tweet)
    fhs.close()
    return


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    """
                  :parameter dataset_folder has a file structure as shown below. The required value for this parameter
                  is the path to the top level of sub-folders where category documents reside.
                  Ex: python3 harassment_corpus.dat /dataset/raw_tweets.
                  Sub-folders where tweets documents will be created must be empty. 
    / dataset
    └── raw_tweets
        ├── harassment
        └── no_harassment
    """

    if len(sys.argv) < 3:
        print('Usage: python3 ClassSeparator.py <input_filename> <dataset_folder>')
        sys.exit(-1)

    elif not os.path.isfile(sys.argv[1]):
        print('Could not find file: %s' % sys.argv[1])
        sys.exit(-1)

    elif not os.path.isdir(sys.argv[2]):
        print('\nCould not find folder: %s' % sys.argv[2])
        print('Usage: python3 ClassSeparator.py <input_filename> <dataset_folder>')
        sys.exit(-1)

    # assign input file value
    input_file = sys.argv[1]

    # assign path value
    if sys.argv[2][-1] != '/':
        path = sys.argv[2] + "/"
    else:
        path = sys.argv[2]

    # verify if dataset folder is empty
    cat_folders = []
    for folder in os.listdir(path):
        cat_folders.append(folder)
        if not os.path.isdir(path + folder):
            print("Only folder must be present in dataset path .... %s is not a folder" % (path+folder))
            print('Usage: python3 ClassSeparator.py <input_filename> <dataset_folder>')
            sys.exit(-1)

    cat_dict = {}
    for folder in cat_folders:
        if len(os.listdir(path + folder)):
            print("Dataset sub-folder MUST be empty.")
            print('Usage: python3 ClassSeparator.py <input_filename> <dataset_folder>')
            sys.exit(-1)

        elif folder[0] in cat_dict:
            print("Category folders must not start with same letter")
            print('Usage: python3 ClassSeparator.py <input_filename> <dataset_folder>')
            sys.exit(-1)
        else:
            cat_dict[folder[0]] = path + folder + "/"

    # cluster dataset
    cluster(input_file, cat_dict)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
