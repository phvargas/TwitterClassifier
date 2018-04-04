from Utilities.FilePartition import make_partition, get_partition_range
from Conversation import Conversation
from time import strftime
from collectConversations import genericCommon as extractor
import Utilities.ConvertDataType as conv
import requests
import sys
import os
import json
import gzip

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


def main(**kwarg):
    baseURL = "https://twitter.com/user/status/"
    time_str = strftime("_%Y%m%d.dat")
    local_date = strftime("_%Y%m%d.html.gz")
    root_url = 'https://twitter.com/'

    vmp_accounts = os.listdir(kwarg['path_tweet'])
    for k, account in enumerate(vmp_accounts):
        account = account.split('.')
        vmp_accounts[k] = account[0]

    vmp_accounts = list(set(vmp_accounts))
    vmp_accounts.sort()
    vmp_count = len(vmp_accounts)

    print('\nTotal number of VMPs: {}'.format(vmp_count))

    start = 0
    end = vmp_count

    if 'part' in kwarg:
        print('Partition: {}'.format(kwarg['part']))
        value = kwarg['part'].split('-')
        number_partitions = int(value[1])
        bloc_part = int(value[0])

        blocks = make_partition(vmp_count, number_partitions)
        work_range = get_partition_range(blocks, bloc_part)

        start = work_range[0]
        if len(work_range) == 1:
            end = vmp_count
        else:
            end = work_range[1]

        conversation_file = kwarg['path'] + 'Conversation_' + value[0] + '_' + value[1] + time_str
    else:
        conversation_file = kwarg['path'] + 'Conversation' + time_str

    print('Conversation will be recoreded at: {}'.format(conversation_file))

    print('Capturing conversations from the Twitter VMP account {:,} to {:,} ...'.format(start, end))

    vmp_tweetsID = []
    for counter, handle in enumerate(vmp_accounts):
        if start <= counter < end:
            with gzip.open(kwarg['path_tweet'] + handle + '.twt.gz', mode='rb') as tweetIDFile:
                for records in tweetIDFile.read().decode('utf-8').split("\n"):
                    if records:
                        tweets = json.loads(records)
                        for k, tweet in enumerate(tweets):
                            vmp_tweetsID.append(tweet['id'])

    flag = True
    with open(conversation_file, "w") as outFile:
        for tweetID in vmp_tweetsID:
            print(tweetID)
            if flag:
                url = baseURL + str(tweetID)
                convoDict = extractor.extractTweetsFromTweetURI(tweetConvURI=url)
                outFile.write(json.dumps(convoDict))
                tmp_file = '/tmp/' + str(tweetID) + '.tmp'
                f = open(tmp_file, mode='w')
                f.write('{}\n'.format(json.dumps(convoDict)))
                f.close()
                capture_conv = Conversation(tmp_file)

                handle_files = os.listdir(kwarg['profile_path'])
                for k, handle in enumerate(handle_files):
                    side = handle.split('_')
                    handle_files[k] = side[0]

                handle_files = set(handle_files)

                for handle in capture_conv.all_conversation_elements_set():
                    if handle not in handle_files:
                        profile_url = root_url + handle
                        print('Getting profile for Twitter account: {}'.format(profile_url))
                        r = requests.get(profile_url)

                        if r.status_code == 200:
                            print('\tWriting profile ...')
                            filename = kwarg['profile_path'] + handle + local_date
                            fh = gzip.open(filename, mode='wb')
                            fh.write(r.text.encode())
                            fh.close()
                        elif r.status_code == 302:
                            print('\tAccount was recently suspended ...')
                        elif r.status_code == 404:
                            print('\tAccount was deleted ...')
                        else:
                            print('\tEncountered unanticipated exception. Status:'.format(r.status_code))
                    else:
                        print('Skipping account {}. Already on file...'.format(handle))

                os.remove(tmp_file)
                outFile.write("\n")


if __name__ == '__main__':
    """
    Parameters for the script are:
    :path: path to the file where capture conversations will be stored. The conversations will be uploaded into memory.
           This is a MANDATORY parameter.

    :tweet_path: path of folder where VMPs tweets are stored. This is a MANDATORY parameter.
    
    :profile_pah: path of folder where interacting profiles will be stored. This is a MANDATORY parameter.


    :part: this is an optional parameter. If provided, the list of interacting Twitter accounts will be broken in (n)
           parts. The parameter has the format d1-d2. Where d2 is an integer that represents the number of parts the list
           will be broken into. While d1 is the section that will be inspected.

           Ex: A conversation containing 100 handles could be broken in two pieces. Then, passing the parameter
               part=1-2 indicates that the running instance will work with elements 0-49. Another instance could run
               concurrently (part=2-2) to work elements 50-100.

    running example: python3 getTweetConvos.py part=1-10 path=data/verifiedUserDataset/ 
                     del_path=data/DeletedSuspendedAccounts/ profile_path=data/AccountProfiles/
    """
    if len(sys.argv) < 4:
        print('\nNot enough arguments..', file=sys.stderr)
        print('File where conversations are contained is required ...', file=sys.stderr)
        print('Usage: python3 CollectActive.py path=path-to-conversations path_tweet=path-where-tweets-reside' +
              ' profile_path="path-to-profile-folder>', file=sys.stderr)
        sys.exit(-1)

    params = conv.list2kwarg(sys.argv[1:])

    if 'path' not in params or 'path_tweet' not in params or 'profile_path' not in params:
        print('\npath, profile_path, and path_tweet are MANDATORY parameters', file=sys.stderr)
        print('Usage: python3 getTweetConvos.py path=path-to-conversations path_tweet=path-where-tweets-reside' +
              ' profile_path="path-to-profile-folder>', file=sys.stderr)
        sys.exit(-1)

    if not os.path.isdir(params['path']):
        print('\nCould not find folder where conversation will be stored: {}'.format(params['path']), file=sys.stderr)
        sys.exit(-1)

    if not os.path.isdir(params['path_tweet']):
        print('\nCould not find folder where VMPs tweets reside: {}'.format(params['path_tweet']), file=sys.stderr)
        sys.exit(-1)

    if not os.path.isdir(params['profile_path']):
        print('\nCould not find folder where profiles will be stored: {}'.format(params['profile_path']), file=sys.stderr)
        sys.exit(-1)

    # add / to end of folder path if not given
    if params['path_tweet'][-1] != '/':
        params['path_tweet'] = params['path_tweet'] + '/'

    if params['profile_path'][-1] != '/':
        params['profile_path'] = params['profile_path'] + '/'

    if params['path'][-1] != '/':
        params['path'] = params['path'] + '/'

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

    main(**params)

    sys.exit(1)