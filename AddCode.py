import sys
from time import strftime, localtime, time
import os

"""
This Python program
  1. Inspect data set used for Twitter Harassment
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Fri,  Sep 22, 2017 at 18:28:30'
__email__ = 'pvargas@cs.odu.edu'


def add_code(in_filename, out_filename, counter):
    print("Adding code to: %s" % in_filename)

    with open(in_filename, "r", encoding='iso-8859-1') as f_in:
        with open(out_filename, "w", encoding='iso-8859-1') as f_out:
            f_out.write("ID\tCode\tTweet")
            for line in f_in:
                counter += 1
                print("%d\t%s" % (counter, line))
                f_out.write("%d\t%s" % (counter, line))

    return


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    if len(sys.argv) < 4:
        print('\nUsage: python3 AddCode.py <Input_filename> <output_filename> <start_code>')
        sys.exit(-1)

    if not os.path.isfile(sys.argv[1]):
        print('\nCould not find file: %s', sys.argv[1])
        print('Usage: python3 AddCode.py <Input_filename> <output_filename> <start_code>')
        sys.exit(-1)

    try:
        add_code(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    except ValueError:
        print('\nStart_code value ==>  %s must be an integer value' % sys.argv[3])
        print('Usage: python3 AddCode.py <Input_filename> <output_filename> <start_code>')
        sys.exit(-1)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
