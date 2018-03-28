from Conversation import Conversation
from time import strftime
import requests


local_date = strftime("_%Y%m%d.dat")
root_url = 'https://twitter.com/'
path = "/data/harassment/AccountProfile/"
sus_del_path = '/odu/data/harassment/processed_data/'
suspended = set()
deleted = set()

print('\nLoading conversations  ...')
observed = Conversation('/data/harassment/verifiedUserDataset/tweetConvo.dat')

interacting_handles = observed.all_conversation_elements_set()
print('Number of Twitter accounts interacting in all conversations: {:,}'.format(len(interacting_handles)))

for counter, account in enumerate(sorted(interacting_handles)):
    url = root_url + account
    r = requests.head(url)

    if r.status_code == 302:
        print('\t{}. Adding account {} to suspended list ...'.format(counter, account))
        suspended.add(account)
    elif r.status_code == 404:
        print('\t{}. Adding account {} to deleted list ...'.format(counter, account))
        deleted.add(account)
    elif r.status_code == 200:
        pass
    else:
        print('\t{}. Encountered unanticipated exception for account {}. Status:'.format(counter, account.status_code))

del_path = sus_del_path + 'deleted' + local_date
with open(del_path) as fh_ds:
    for handle in deleted:
        fh_ds.write('{}\n'.format(handle))

sus_path = sus_del_path + 'suspended' + local_date
with open(sus_path) as fh_ds:
    for handle in suspended:
        fh_ds.write('{}\n'.format(handle))
