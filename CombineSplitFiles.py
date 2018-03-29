import re
import os
import sys

"""
CombineSplitFiles.py: Combines all splits file of the form filedescription_{9,}_{9,}_YYMMDD.ext into a single file of
                      the form FileDescription_YYMMDD.ext 
                      Script takes for argument the path where all split files are located.
                       
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Mar 29, 2018 at 05:51'
__email__ = 'pvargas@cs.odu.edu'


def main(folder_path):
    """
    :param folder_path: Location where the files are separated
    :return: None
    """

    regex_split = re.compile('(\w+)_\d+_\d+_(\d+)(\..*)')
    regex_single = re.compile('([a-zA-Z]*)_(\d+)(\..*)')

    file_list = os.listdir(folder_path)
    delete_files = []
    combine_dict = {}

    print(file_list)
    for filename in file_list:
        result = regex_single.match(filename)
        if result:
            single_name = result.group(1) + '_' + result.group(2) + result.group(3)
            print('File: {} is single. Value:'.format(filename, single_name))
            print('\n\n\n')

            if single_name not in combine_dict:
                combine_dict[single_name] = []

            with open(folder_path + filename, mode='r') as fh:
                for handle in fh:
                    combine_dict[single_name].append(handle.strip())

        else:
            result = regex_split.match(filename)
            if result:
                combine_name = result.group(1) + '_' + result.group(2) + result.group(3)
                delete_files.append(filename)
                print('File: {} is combined. It will be merged to: {}'.format(filename, combine_name))

                if combine_name not in combine_dict:
                    combine_dict[combine_name] = []

                with open(folder_path + filename, mode='r') as fh:
                    for handle in fh:
                        combine_dict[combine_name].append(handle.strip())

    for filename in combine_dict:
        combine_dict[filename].sort()
        print(filename, len(combine_dict[filename]), combine_dict[filename])

        with open(folder_path + filename, mode='w') as fh:
            for handle in combine_dict[filename]:
                fh.write('{}\n'.format(handle))

    print('\nFiles to delete:')
    for filename in sorted(delete_files):
        print('Deleting file: {} ...'.format(filename))
        os.remove(folder_path + filename)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('\nFolder path is required ...', file=sys.stderr)
        print('Usage: python3 CombineSplitFiles.py <path-where-split-files-located>', file=sys.stderr)
        sys.exit(-1)

    path = sys.argv[1]
    if not os.path.isdir(path):
        print('\nCouldn\'t find Folder {} ...'.format(path), file=sys.stderr)
        print('Usage: python3 CombineSplitFiles.py <path-where-split-files-located>', file=sys.stderr)
        sys.exit(-1)

    if path[-1] != '/':
        path = path + '/'

    main(path)

    sys.exit(0)
