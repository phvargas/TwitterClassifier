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


def cluster(input_file, cluster1, cluster2):
    code_file = {'H': cluster1, 'N': cluster2}
    with open(input_file, "r", encoding='iso-8859-1') as f:
        ha_file = open(cluster1, 'w')
        non_ha_file = open(cluster2, 'w')
        ha_except_file = open('ha_exception.dat', 'w')
        counter = 0
        for row in f:
            counter += 1
            if counter > 1:                                         # does not write header
                row = row.strip()                                   # removes EOL character

                try:
                    if isinstance(int(row[0]), int):
                        try:
                            regex = re.search("(.*)(\s{1,}H\s{1,})(.*)", row)
                            print(regex.group(3), "---> Harassment", counter)
                            ha_file.write(regex.group(3) + "\n")
                        except AttributeError as e:
                            try:
                                regex = re.search("(.*)(\s{1,}N\s{1,})(.*)", row)
                                print(regex.group(3), "---> No harassment", counter)
                                non_ha_file.write(regex.group(3) + "\n")
                            except AttributeError as e:
                                print(row)

                except ValueError as e:
                    print(counter - 1, row, "-------------> EXCEPTION")
                    ha_except_file.write(row + "\n")

    # close all file-handles
    ha_except_file.close()
    non_ha_file.close()
    ha_file.close()
    print(counter)
    return

if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    if len(sys.argv) < 4:
        print('Usage: python3 ClassSeparator.py <input_filename> <cluster1_filename> <cluster2_filename>')
        sys.exit(-1)

    elif not os.path.isfile(sys.argv[1]):
        print('Could not find file: %s' % sys.argv[1])
        sys.exit(-1)

    else:
        cluster(sys.argv[1], sys.argv[2], sys.argv[3])

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
