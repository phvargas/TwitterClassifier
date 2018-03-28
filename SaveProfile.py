from Conversation import Conversation
from time import strftime
import requests
import gzip


observed = Conversation('/data/harassment/verifiedUserDataset/tweetConvo.dat')

local_date = strftime("_%Y%m%d.html")
root_url = 'https://twitter.com/'
path = "/data/harassment/AccountProfile/"
sus_del_path = '/odu/data/harassment/processed_data/'
interacting_handles = set()
suspended = set()
deleted = set()
interactions = {}

print(len(observed.all_conversation_elements_set()))

for counter, account in enumerate(observed.all_conversation_elements_set()):
    url = root_url + account
    print('Getting profile for Twitter account: {}'.format(url))
    r = requests.get(url)

    if r.status_code == 200:
        print('\tWriting profile ...')
        filename = path + account + local_date
        fh = gzip.open(filename, mode='wb')
        fh.write(r.text)
        fh.close()
    elif r.status_code == 302:
        print('\tAdding account to suspended list.')
        suspended.add(account)
    elif r.status_code == 404:
        print('\tAdding account to deleted list...')
        deleted.add(account)
    else:
        print('\tEncountered unanticipated exception. Status:'.format(r.status_code))

del_path = sus_del_path + 'deleted' + strftime("_%Y%m%d.dat")
with open(del_path) as fh_ds:
    for handle in deleted:
        fh_ds.write('{}\n'.format(handle))

sus_path = sus_del_path + 'suspended' + strftime("_%Y%m%d.dat")
with open(sus_path) as fh_ds:
    for handle in suspended:
        fh_ds.write('{}\n'.format(handle))
