import numpy as np
from Conversation import Conversation
from twitter_apps.Subjects import get_values

observed = Conversation('/data/harassment/verifiedUserDataset/tweetConvo.dat')

my_deleted_list = []
my_suspended_list = []
my_suspended_deleted_list = []
subjects_dict = {}
stance_count = {}

with open('closed_accounts.txt', mode='r') as fs:
    for account in fs:
        my_deleted_list.append(account.strip().lower())
        my_suspended_deleted_list.append(account.strip().lower())

with open('suspended.txt', mode='r') as fs:
    for account in fs:
        my_suspended_list.append(account.strip().lower())
        my_suspended_deleted_list.append(account.strip().lower())


# get political stance for all Twitter observed accounts
for account in get_values():
    subjects_dict[account['handle'].lower()] = {'stance': account['stance']}
    if account['stance'] not in stance_count:
        stance_count[account['stance']] = 1
    else:
        stance_count[account['stance']] += 1

conversation_id = []
handle_set = set()

for idx in observed.handle_conversations_id('megynkelly'):
    conversation_row = {idx: observed.common_elements_list('megynkelly', idx, my_deleted_list), 'count': {}}
    for handle in conversation_row[idx]:
        if handle in conversation_row['count']:
            conversation_row['count'][handle] += 1
        else:
            conversation_row['count'][handle] = 1

        handle_set.add(handle)
    conversation_id.append(conversation_row)

print(' ' * 20, end='')
for handle in handle_set:
    print(handle, end=' - ')

for row in conversation_id:
    print(row)

    """
    for handle in handle_set:
        if handle in row['count']:
            print(row['count'][handle], end=' -')
        else:
            print(' - 0 ')
    """
