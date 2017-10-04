import sys
from time import strftime, localtime, time
import os, re

"""
This Python program
  1. Strip specific content of Harassment Dataset 
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  Oct 03, 2017 at 11:19:50'
__email__ = 'pvargas@cs.odu.edu'


def strip_data(action, in_file, out_file):
    print("Stripping file: %s" % in_file)

    counter = 0
    if action == "handle":
        with open(in_file, "r", encoding='iso-8859-1') as f_in:
            with open(out_file, "w") as f_out:
                for line in f_in:
                    regex = re.findall("(@.*?)\s", line + " ")
                    line = line.strip()
                    for value in regex:
                        print('Replacing:', value, line)
                        line = line.replace(value, '')

                    counter += 1
                    f_out.write(line.strip() + '\n')

    print('Number of line: ', counter)

    return


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    if len(sys.argv) != 4:
        print('Usage: python3 StripData.py <Tco|handle> <input_filename> <output_filename')
        sys.exit(-1)

    elif sys.argv[1].lower() != "tco" and sys.argv[1].lower() != "handle":
        print('\nOption MUST be Tco or handle')
        print('Usage: python3 StripData.py <Tco|handle> <input_filename> <output_filename>')
        sys.exit(-1)

    elif not os.path.isfile(sys.argv[2]):
        print('Could not find input file: %s' % sys.argv[2])
        print('Usage: python3 StripData.py <Tco|handle> <input_filename> <output_filename>')
        sys.exit(-1)

    strip_data(sys.argv[1].lower(), sys.argv[2], sys.argv[3])

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
