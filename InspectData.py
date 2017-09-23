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


def inspect_file(filename, action="head", lines=-1):
    print("inspected file: %s" % filename)

    if lines == -1:    # printing all the lines
        with open(filename, "r", encoding='iso-8859-1') as f:
            for line in f:
                print(line.strip())

    elif action == "head":
        counter = 0
        with open(filename, "r", encoding='iso-8859-1') as f:
            for line in f:
                counter += 1
                print(line.strip())
                if counter > lines:
                    break
    else:
        counter = 0
        stack = [None] * lines
        header = ""
        with open(filename, "r", encoding='iso-8859-1') as f:
            for line in f:
                counter += 1
                if counter == 1:
                    header = line.strip()
                else:
                    stack = stack[1:]
                    stack.append(line.strip())

        print(header)
        for n in range(lines):
            print(stack[n])
    return

if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    if len(sys.argv) < 2:
        print('Usage: python3 InspectData.py <filename>')
        sys.exit(-1)

    elif len(sys.argv) == 2:
        if not os.path.isfile(sys.argv[1]):
            print('Could not find file: %s', sys.argv[1])
            sys.exit(-1)

        else:
            inspect_file(sys.argv[1])

    elif len(sys.argv) == 3:
        if not os.path.isfile(sys.argv[2]):
            print('Could not find file: %s' % sys.argv[2])
            print("Usage: python3 InspectData.py [head|tail] <filename>")
            sys.exit(-1)

        elif sys.argv[1].lower() != "head" and sys.argv[1].lower() != "tail":
            print("Usage: python3 InspectData.py [head|tail] <filename>")
            sys.exit(-1)

        else:
            inspect_file(sys.argv[2], sys.argv[1])
    else:
        if not os.path.isfile(sys.argv[3]):
            print('Could not find file: %s' % sys.argv[2])
            print("Usage: python3 InspectData.py [head|tail] <filename>")
            sys.exit(-1)

        elif sys.argv[1].lower() != "head" and sys.argv[1].lower() != "tail":
            print("Usage: python3 InspectData.py [head|tail] <filename>")
            sys.exit(-1)

        else:
            inspect_file(sys.argv[3], sys.argv[1], int(sys.argv[2]))

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
