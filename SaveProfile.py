from Conversation import Conversation
from Utilities.FilePartition import get_partition_range, make_partition
import Utilities.ConvertDataType as conv
from time import strftime
import requests
import gzip
import sys
import os

"""
SaveProfile.py: From a captured set of conversations (Verified Media Personalities - VMP) the script extract a
                list of handles that interacted in the conversations. The list is used to get the HTML Twitter page 
                profile, and save it to the path provided as a parameter. As the profiles are retrieve it the profile
                is not found then it place the account username into a delete or suspended file. 
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Fri,  Mar 30, 2018 at 10:38'
__email__ = 'pvargas@cs.odu.edu'


def main(**kwarg):
    print('\nLoading conversations  ...')
    observed = Conversation(params['path'])

    local_date = strftime("_%Y%m%d.html.gz")
    timestamp_file = strftime("_%Y%m%d.dat")

    root_url = 'https://twitter.com/'
    path = params['profile_path']
    sus_del_path = params['del_path']
    interacting_handles = list(observed.all_conversation_elements_set())
    suspended = set()
    deleted = set()

    start = 0
    end = len(interacting_handles)
    print('Number of Twitter accounts interacting in all conversations: {:,}'.format(end))

    if 'part' in kwarg:
        value = kwarg['part'].split('-')
        number_partitions = int(value[1])
        bloc_part = int(value[0])

        blocks = make_partition(end, number_partitions)
        work_range = get_partition_range(blocks, bloc_part)

        start = work_range[0]
        if len(work_range) != 1:
            end = work_range[1]

        timestamp_file = '_' + value[0] + '_' + value[1] + strftime("_%Y%m%d.dat")

    print('Analysing accounts from {:,} to {:,} ...'.format(start, end))

    interacting_handles.sort()
    for counter, account in enumerate(interacting_handles):
        if start <= counter < end:
            url = root_url + account
            print('Getting profile for Twitter account: {}'.format(url))
            r = requests.get(url)

            if r.status_code == 200:
                print('\tWriting profile ...')
                filename = path + account + local_date
                fh = gzip.open(filename, mode='wb')
                fh.write(r.text.encode())
                fh.close()
            elif r.status_code == 302:
                print('\tAdding account to suspended list.')
                suspended.add(account)
            elif r.status_code == 404:
                print('\tAdding account to deleted list...')
                deleted.add(account)
            else:
                print('\tEncountered unanticipated exception. Status:'.format(r.status_code))

    del_path = sus_del_path + 'deleted' + timestamp_file
    with open(del_path) as fh_ds:
        for handle in deleted:
            fh_ds.write('{}\n'.format(handle))
    
    sus_path = sus_del_path + 'suspended' + timestamp_file
    with open(sus_path) as fh_ds:
        for handle in suspended:
            fh_ds.write('{}\n'.format(handle))


if __name__ == '__main__':
    """
    Parameters for the script are:
    :path: path to the file where all capture conversations are stored. The conversations will be uploaded into memory.
           The uploaded object will contain the handles that interacted in the conversations. This is a MANDATORY
           parameter.

    :profile_path: path of folder where profile are stored. This is a MANDATORY parameter.

    :del_path: this parameter is the folder where the discovered deleted and suspended accounts are stored.
                A file containing a list of handles will be save in the folder with the following format:
                deleted_YYMMDD.dat & suspended_YYMMDD.dat - This is a MANDATORY field
                
    :part: this is an optional parameter. If provided, the list of interacting Twitter accounts will be broken in (n)
           parts. The parameter has the format d1-d2. Where d2 is an integer that represents the number of parts the list
           will be broken into. While d1 is the section that will be inspected.

           Ex: A conversation containing 100 handles could be broken in two pieces. Then, passing the parameter
               part=1-2 indicates that the running instance will work with elements 0-49. Another instance could run
               concurrently (part=2-2) to work elements 50-100.

    :rewrite: this is an optional parameter. This is parameter is a boolean variable. Possible values are True or False.
              The default value of this parameter is TRUE. If the values is FALSE and an account profile is already on 
              file script will skip this account, so it will not write or fetch the account profile information.

    running example: python3 SaveProfile.py part=1-10 path=data/verifiedUserDataset/tweetConvo.dat 
                     profile_path=data/AccountProfile/ rewrite=False
    """
    if len(sys.argv) < 3:
        print('\nNot enough arguments..', file=sys.stderr)
        print('Mandatory arguments: path=path-to-conversations, profile_path=path-where-tweets-reside, ' +
              'del_path=path-to-del-sus-folder', file=sys.stderr)
        print('Usage: python3 SaveProfile.py path=path-to-conversations profile_path=path-where-tweets-reside' +
              ' <del_path="path-to-del-sus-folder>', file=sys.stderr)
        sys.exit(-1)

    params = conv.list2kwarg(sys.argv[1:])

    if 'path' not in params or 'profile_path' not in params:
        print('\npath and profile_path are MANDATORY parameters', file=sys.stderr)
        print('Usage: python3 SaveProfile.py path=path-to-conversations profile_path=path-where-tweets-reside' +
              ' del_path="path-to-del-sus-folder', file=sys.stderr)
        sys.exit(-1)

    if not os.path.isfile(params['path']):
        print('\nCould not find file: {}'.format(params['path']), file=sys.stderr)
        sys.exit(-1)

    if not os.path.isdir(params['profile_path']):
        print('\nCould not find folder where profile reside: {}'.format(params['profile_path']), file=sys.stderr)
        sys.exit(-1)

    if not os.path.isdir(params['del_path']):
        print('\nCould not find folder where DELETED/SUSPENDED files reside: {}'.format(params['del_path']),
              file=sys.stderr)
        sys.exit(-1)

    # add / to end of folder path if not given
    if params['profile_path'][-1] != '/':
        params['profile_path'] = params['path_tweet'] + '/'

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

    if 'rewrite' in params:
        if params['rewrite'] not in ['false', 'true', '1', '0']:
            print('\nParameter <rewrite> possible values are: True, False, 0, or 1', file=sys.stderr)
            sys.exit(-1)

    main(**params)

    sys.exit(1)
