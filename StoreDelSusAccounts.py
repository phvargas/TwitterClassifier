#!/usr/bin/env python3
from Conversation import Conversation
from multiprocessing import Process
from time import strftime
import time
import sys
import os
import requests
import Utilities.ConvertDataType as conv

"""
StoreDelSusAccounts.py: Given a list of Twitter accounts the script determines if the account is suspended or deleted.
                        The determination is based on the RESPONSE CODE obtained by requesting the resource:
                        https://twitter.com/username. The deleted accounts will be placed in a file of the form:
                        <path_deleted_YYMMDD.dat>. Suspended accounts file has the form <path_suspended_YYMMDD.dat>.
                        
                        The script allows to split the list into multiple chunks to increase performance. 
                         
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Mar 29, 2018 at 06:11'
__email__ = 'pvargas@cs.odu.edu'


def main(**kwarg):
    """

    :param kwarg: a dictionary containing the path of the files where the deleted/suspended accounts will be stored.
                  path: is of the file where the capture conversations are stored.
                  sus_del_path: is the folder where the deleted and suspended accountn will be store.
    :return: None
    """
    root_url = 'https://twitter.com/'
    suspended = set()
    deleted = set()
    error = []

    print(kwarg)
    path = kwarg['path']
    sus_del_path = kwarg['del_path']

    print('\nLoading conversations  ...')
    observed = Conversation(path)

    interacting_handles = observed.all_conversation_elements_set()
    number_handles = len(interacting_handles)
    print('Number of Twitter accounts interacting in all conversations: {:,}'.format(number_handles))

    start = 0
    end = number_handles

    time_str = "_%Y%m%d.dat"
    error_str = '_%Y%m%d.log'
    if 'part' in kwarg:
        value = kwarg['part'].split('-')
        number_partitions = int(value[1])
        bloc_part = int(value[0])

        blocks = make_partition(number_handles, number_partitions)
        work_range = get_partition_range(blocks, bloc_part)

        start = work_range[0]
        if len(work_range) == 1:
            end = number_handles
        else:
            end = work_range[1]

        time_str = "_{}_{}_%Y%m%d.dat".format(bloc_part, number_partitions)

    print('Analisyng accounts from {} to {} ...'.format(start, end))

    for counter, account in enumerate(sorted(interacting_handles)):
        url = root_url + account

        if start <= counter < end:
            r = requests.head(url)

            try:
                if r.status_code == 302:
                    print('\t{}. Adding account {} to suspended list ...'.format(counter, account))
                    suspended.add(account)
                elif r.status_code == 404:
                    print('\t{}. Adding account {} to deleted list ...'.format(counter, account))
                    deleted.add(account)
                elif r.status_code == 200:
                    pass
                else:
                    error.append('Account: {}, Error: {}'.format(account, r.status_code))
                    print('\t{}. Encountered unanticipated exception for account {}. Status: {}'.format(counter,
                                                                                                        account,
                                                                                                        r.status_code))
            except:
                local_date = strftime(time_str)

                del_path = sus_del_path + 'deleted' + local_date
                if deleted:
                    with open(del_path, mode='w') as fh_ds:
                        for handle in deleted:
                            fh_ds.write('{}\n'.format(handle))

                sus_path = sus_del_path + 'suspended' + local_date
                if suspended:
                    with open(sus_path, mode='w') as fh_ds:
                        for handle in suspended:
                            fh_ds.write('{}\n'.format(handle))

                if error:
                    error_path = sus_del_path + 'error' + strftime(error_str)
                    with open(error_path, mode='w') as fh_ds:
                        for error_line in error:
                            fh_ds.write('{}\n'.format(error_line))
                exit(-1)

    local_date = strftime(time_str)

    del_path = sus_del_path + 'deleted' + local_date
    if deleted:
        with open(del_path, mode='w') as fh_ds:
            for handle in deleted:
                fh_ds.write('{}\n'.format(handle))

    sus_path = sus_del_path + 'suspended' + local_date
    if suspended:
        with open(sus_path, mode='w') as fh_ds:
            for handle in suspended:
                fh_ds.write('{}\n'.format(handle))

    if error:
        error_path = sus_del_path + 'error' + strftime(error_str)
        with open(error_path, mode='w') as fh_ds:
            for error_line in error:
                fh_ds.write('{}\n'.format(error_line))


def make_partition(size, number_partitions):
    blocks = []
    value = size // number_partitions

    if number_partitions <= 1:
        return [0]

    if value < 1:
        print("Could not make partitions for {} elements. Partitions TOO small".format(number_partitions),
              file=sys.stderr)
        return blocks

    for k in range(number_partitions):
        blocks.append(k * value)

    return blocks


def get_partition_range(part_list, _part):
    start_end = []

    if _part == 0:
        print("First partition MUST be one (1) not {}".format(_part), file=sys.stderr)
        return [0]

    if _part > len(part_list):
        print("The part ({}) CANNOT be greater to the number of fractions".format(_part), file=sys.stderr)
        return [0]

    for k in range(_part - 1, _part + 1):
        start_end.append(part_list[k])

        if k + 1 >= len(part_list):
            return start_end

    return start_end


if __name__ == '__main__':
    """
    Expected parameters for the script are:
    :path: path to the file where all capture conversations are stored. The conversations will be uploaded in memory.
           This object will contain the handles that interacted in the conversations.
           
    :del_path: this parameter is the folder where the discovered deleted and suspended accounts will be stored.
                a file containing a list of handles will be save in the folder with the following format:
                deleted_YYMMDD.dat & suspended_YYMMDD.dat
                
    :part: this is an optional parameter. If provided, the list of interacting Twitter accounts will be broken in n
           parts. The parameter has the format d1-d2. Where d2 is an integer and represents number of parts the list
           will be broken into. Then, d1 is the section that will be inspected.
           
           Ex: A conversation containing 100 handles could be broken in two pieces. Then, passing the parameter
               part=1-2 indicates that the running instance will inspect elements 0-49. Another instance could be ran
               concurrently (part=2-2) to inspect the elements 50-100. 
               
    running example: python3 StoreDelSusAccounts.py part=1-10 path=data/verifiedUserDataset/tweetConvo.dat 
                     del_path=data/DeletedSuspendedAccounts/
    """
    if len(sys.argv) < 3:
        print('\nNot enough arguments..', file=sys.stderr)
        print('Usage: python3 StoreDelSusAccounts.py path="path-to-conversations" del_path="path-to-del-sus-folder"',
              file=sys.stderr)
        sys.exit(-1)

    params = conv.list2kwarg(sys.argv[1:])

    if 'path' not in params or 'del_path' not in params:
        print('\ndel_path and path are required parameters', file=sys.stderr)
        print('Usage: python3 StoreDelSusAccounts.py path="path-to-conversations" del_path="path-to-del-sus-folder"',
              file=sys.stderr)
        sys.exit(-1)

    if not os.path.isfile(params['path']):
        print('\nCould not find file: {}'.format(params['path']), file=sys.stderr)
        sys.exit(-1)

    if not os.path.isdir(params['del_path']):
        print('\nCould not find folder: {}'.format(params['del_path']), file=sys.stderr)
        sys.exit(-1)

    # add / to end of folder path if not given
    if params['del_path'][-1] != '/':
        params['del_path'] = params['del_path'] + '/'
        print(params['del_path'])

    if 'part' in params:
        part = params['part'].split('-')
        if len(part) != 2:
            print('\nParameter <part> MUST have two integers between a dash. Ex: part=1-10', file=sys.stderr)
            sys.exit(-1)

        try:
            value0 = int(part[0])
            value1 = int(part[1])

        except ValueError:
            print('\nParameter <part> MUST have two integers between a dash. Ex: part=1-10', file=sys.stderr)
            sys.exit(-1)

    if 'thread' in params:
        try:
            value = int(params['thread'])

        except ValueError:
            print('\nMulti-Thread parameter must be an INTEGER. Passed value "{}" is not'.format(value), file=sys.stderr)
            sys.exit(-1)

        thread = []
        for part in range(1, int(params['thread']) + 1):
            params['part'] = str(part) + '-' + params['thread']
            thread.append(Process(target=main, kwargs=params))

            time.sleep(2)

            thread[part - 1].start()

        for part in range(int(params['thread'])):
            thread[part].join()

        print('All threads ended ...')
    else:
        main(**params)

    sys.exit(1)
