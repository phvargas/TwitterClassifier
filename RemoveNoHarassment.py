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


def cluster(in_file, out_file):
    with open(in_file, "r", encoding='iso-8859-1') as f:
        inventory = {'e': 0, 'h': 0, 'n': 0, 'o': 0}
        ha_except_file = open('ha_exception.dat', 'w')
        ha_out_file = open(out_file, "w")
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

                            tweet = regex.group(3).strip()

                            ha_out_file.write(regex.group(1).strip() + "\t" + "H" + "\t" + tweet + "\n")

                        except AttributeError:
                            try:
                                # writes non-harassment tweets with CODE type 'N' into non-harassment file
                                regex = re.search("^(\d+)(\s+N\s+)(.*)", row)
                                print(regex.group(3), "---> No harassment", counter)

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
    ha_out_file.close()

    print(counter)
    return


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    if len(sys.argv) < 3:
        print('Usage: python3 RemoveNoHarassment.py <input_filename> <dataset_folder>')
        sys.exit(-1)

    elif not os.path.isfile(sys.argv[1]):
        print('Could not find file: %s' % sys.argv[1])
        sys.exit(-1)

    # assign input/output file value
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # cluster dataset
    cluster(input_file, output_file)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
