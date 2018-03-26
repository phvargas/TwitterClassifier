import os
import sys
import requests
import random
from time import strftime, localtime, time
# from Utility.Constants import *

"""
Create Archive Timemap file for Screen Name 
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  Mar 22, 2018 at 16:55'
__email__ = 'pvargas@cs.odu.edu'


def fetch_archive_url(handle_list, output):
    """
    :param handle_list is the list of Twitter handles to be fetch from the Web archives
    :param output is the output file containing the number of Twitter handles mementos

    It is for running Memgator in local server mode
    Always run memgator server before it.
    Command:  memgator --contimeout=10s --agent=msiddiqu@cs.odu.edu server
    Memgator Command: http://localhost:1208/timemap/cdxj/url_search
    """

    obj = {}

    fout = open(output, mode='w')

    url_search = "https://twitter.com/"
    url = "http://localhost:1208/timemap/"
    data_format = "cdxj"

    print('\nNumber of username: {}'.format(len(handle_list)))

    for screen_name, freq, now_deleted in handle_list:
        command = url + data_format + "/" + url_search + screen_name

        print('Getting mementos for:', url_search + screen_name)

        try:
            response = requests.get(command)
            response_mementos = response.text
            obj[screen_name] = 0

            if response.status_code == 404:
                pass
            else:
                for line in response_mementos.strip().split('\n')[6:]:
                    value = line.split(' ')
                    timestamp = value[0]
                    uri = value[2].split('"')[1]

                    r = requests.head(uri)
                    print(timestamp, uri, r.status_code)
                    if r.status_code == 200:
                        obj[screen_name] += 1
        except Exception as err:
            print("Fetch Archive Url Error" + str(err))

        fout.write('{},{}\n'.format(screen_name, obj[screen_name]))

        print('Total number of mementos for {} is {}'.format(screen_name, obj[screen_name]))

    fout.close()

    return


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    rand_number = 0

    if len(sys.argv) < 4:
        print('\nUsage: python3 GetMementos.py <input_filename> <output_filename> <random_number_qty>')
        sys.exit(-1)

    if not os.path.isfile(sys.argv[1]):
        print('\nCould not find file: %s' % sys.argv[1])
        print('\nUsage: python3 GetMementos.py <input_filename> <output_filename> <random_number_qty>')
        sys.exit(-1)

    try:
        rand_number = int(sys.argv[3])

    except ValueError:
        print('\nRandom_number_qty MUST be an integer. {} is not'.format(sys.argv[3]))
        print('Usage: python3 GetMementos.py <input_filename> <output_filename> <random_number_qty>')
        sys.exit(-1)

    only_deleted_accounts = False
    only_active_accounts = False

    if len(sys.argv) > 4 and sys.argv[4].lower() == 'd':
        only_deleted_accounts = True
    elif len(sys.argv) > 4 and sys.argv[4].lower() == 'n':
        only_active_accounts = True

    screen_name_holder = []
    screen_name_list = []

    with open(sys.argv[1], mode='r') as fh:
        for record in fh:
            screenname, frequency, was_deleted = record.strip().split(',')
            if was_deleted == 'D':
                was_deleted = True
            else:
                was_deleted = False

            if only_deleted_accounts and was_deleted:
                screen_name_holder.append((screenname, frequency, was_deleted))

            elif only_active_accounts and not was_deleted:
                screen_name_holder.append((screenname, frequency, was_deleted))

            elif len(sys.argv) == 4:
                screen_name_holder.append((screenname, frequency, was_deleted))

    print('Number of accounts to consider: {}'.format(len(screen_name_holder)))

    if rand_number >= len(screen_name_holder):
        print('\nRandom_number_qty must be smaller than input file size: {}'.format(len(screen_name_holder)))
        sys.exit(-1)

    rnd_list = random.sample(range(0, len(screen_name_holder)), rand_number)
    for idx in sorted(rnd_list):
        screen_name_list.append(screen_name_holder[idx])

    fetch_archive_url(screen_name_list, sys.argv[2])

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)

