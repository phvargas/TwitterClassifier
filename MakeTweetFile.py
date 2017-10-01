import sys
from time import strftime, localtime, time
import os
import re

"""
This Python program
  1. Converts every tweet in a file into a text file. The reading file expect to find a tweed ID and a tweet 
  description. 
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Sat,  Sep 30, 2017 at 16:34:34'
__email__ = 'pvargas@cs.odu.edu'


def cluster(input_file, path):
    """
    :param input_file: complete path of file containing ID and tweet text
    :param path: path of the folder where files are going to be written
    :return:
    """
    with open(input_file, "r", encoding='iso-8859-1') as f:
        counter = 0
        for row in f:
            counter += 1

            regex = re.search("^<(\d+)>(.*)", row)
            print(row.strip())

            if len(regex.groups()) != 2:                             # expecting ID and Tweet description
                print('Something went wrong with tweet: %s' % row)

            else:
                tweet_id = str(regex.group(1)).zfill(5)
                tweet = regex.group(2).strip()
                filename = path + "/" + 'tweet' + tweet_id + ".txt"

                print(filename, tweet.strip())
                output = open(filename, "w")
                output.write(tweet)
                output.close()

    print(counter)
    return


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    if len(sys.argv) < 3:
        print('\nUsage: python3 MakeTweetFile.py <input_filename> <dir_path>')
        sys.exit(-1)

    elif not os.path.isfile(sys.argv[1]):
        print('\nCould not find file: %s' % sys.argv[1])
        print('Usage: python3 MakeTweetFile.py <input_filename> <dir_path>')
        sys.exit(-1)

    elif not os.path.isdir(sys.argv[2]):
        print('\nCould not find folder: %s' % sys.argv[2])
        print('Usage: python3 MakeTweetFile.py <input_filename> <dir_path>')
        sys.exit(-1)

    elif len(os.listdir(sys.argv[2])) != 0:
        print('\nTarget folder << %s >> must be empty.' % sys.argv[2])
        print('Usage: python3 MakeTweetFile.py <input_filename> <dir_path>')
        sys.exit(-1)

    else:
        cluster(sys.argv[1], sys.argv[2])

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)