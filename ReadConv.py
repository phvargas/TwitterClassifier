import sys
from time import strftime, localtime, time
import os
import json

"""
This Python program
  1. Reads stored conversations from Twitter Research-Subjects
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  Jan 23, 2018 at 21:01:14'
__email__ = 'pvargas@cs.odu.edu'


def read_conversations(in_filename):
    with open(in_filename, "r", encoding='iso-8859-1') as fs:
        for record in fs:
            conv = json.loads(record.strip())
            for idx in conv:
                print('{}: {}'.format(idx, conv[idx]))
                for key in conv[idx]:
                    print('\t{}: {}'.format(key, conv[idx][key]))
                    if key == 'data-conversation-id' and conv[idx][key] == idx:
                        print('\t\tConversation originator: {}'.format(conv[idx]['data-screen-name']))
            print()
    return


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    if len(sys.argv) < 2:
        print('\nUsage: python3 ReadConv.py <Input_filename>')
        sys.exit(-1)

    if not os.path.isfile(sys.argv[1]):
        print('\nCould not find file: %s' % sys.argv[1])
        print('\nUsage: python3 ReadConv.py <Input_filename>')
        sys.exit(-1)

    read_conversations(sys.argv[1])

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
