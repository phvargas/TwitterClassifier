import os
import re
import sys
from Utilities.LoadFiles import file_list
from Utilities.Sorting import dictionaryByValue

if len(sys.argv) < 2:
    print('\nUsage: python3 CountTerms.py <file_to_inspect>')
    sys.exit(-1)

inspect_file = sys.argv[1]
if not os.path.isfile(inspect_file):
    print('\nCould not find file: ', inspect_file)
    print('Usage: python3 CountTerms.py <file_to_inspect>')
    sys.exit(-1)

counter = 0
bad_terms = file_list('data/terms/derogatory.dat')
term_count = {}
with open(inspect_file, mode='r') as fhs:
    for document in fhs:
        found_derogatory = False
        for term in bad_terms:
            regex = re.compile('\\b%s\\b' % term)
            if regex.search(document.lower()):
                try:
                    term_count[term] += 1

                except KeyError:
                    term_count[term] =1

                found_derogatory = True
                print(term, '-->', document.strip(), counter)
        if found_derogatory:
            counter += 1

print('Number of documents with derogatory terms:', counter)
print()
print('{|\n|Term\n|Freq\n|-')
for term, value in dictionaryByValue(term_count):
    print('|{}\n|{}\n|-'.format(term, value))
print('|}')
