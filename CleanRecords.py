import sys
import os
import re
from time import strftime, localtime, time

"""
This Python program
  1. Script CheckDuplicate.py must be run first.  After the output file has being inspected 
     and processed, then that file can be used to removed tweets in the corpus that are
     ambiguous.  
     
  2. The code left in the input file will be used to identify records to be removed from the corpus.  
     A new file will be generated without the content of excluded records.
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  Oct 24, 2017 at 11:00:24'
__email__ = 'pvargas@cs.odu.edu'


def remove_records(in_filename, clean_file, out_filename):
    print("Removing records from: %s  ...." % in_filename)

    print("Placing codes of bad records into a set....")
    counter = 0
    codes = set()
    with open(clean_file, mode='r', encoding='iso-8859-1') as bad_file:
        for row in bad_file:
            regex = re.search("^<(\d+)>", row)
            try:
                code = regex.group(1)
                codes.add(int(code))
                counter += 1

            except AttributeError:
                # skip record
                pass
    print("Removing {0} records".format(len(codes)))
    print("Number of lines: {0}".format(counter))

    with open(in_filename, "r", encoding='iso-8859-1') as f_in:
        with open(out_filename, "w", encoding='utf-8') as f_out:
            for row in f_in:
                regex = re.search("^(\d+)(\s+[H|N]\s+)(.*)", row)
                try:
                    bad_code = regex.group(1)
                    print(bad_code)

                    if int(bad_code) in codes:
                        print("Not including: ", row)

                    else:
                        f_out.write('{0}{1}'.format(row.strip(), '\n'))

                except AttributeError:
                    print('error:', row.strip())
                    #f_out.write(row)
    print(codes)
    return


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    if len(sys.argv) < 4:
        print('\nUsage: python3 CleanRecords.py <Input_filename> <bad_code_file> <output_filename>')
        sys.exit(-1)

    if not os.path.isfile(sys.argv[1]):
        print('\nCould not find file: %s', sys.argv[1])
        print('Usage: python3 CleanRecords.py <Input_filename> <bad_code_file> <output_filename>')
        sys.exit(-1)

    if not os.path.isfile(sys.argv[2]):
        print('\nCould not find file: %s', sys.argv[2])
        print('Usage: python3 CleanRecords.py <Input_filename> <bad_code_file> <output_filename>')
        sys.exit(-1)

    remove_records(sys.argv[1], sys.argv[2], sys.argv[3])

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
