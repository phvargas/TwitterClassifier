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

for idx in observed.handle_conversations_id('megynkelly'):
    print(idx, observed.common_elements_list('megynkelly', idx, my_suspended_deleted_list))
print()

conversation_id = []
handle_set = set()

total = 0
for idx in observed.handle_conversations_id('megynkelly'):
    conversation_row = {idx: observed.common_elements_list('megynkelly', idx, my_suspended_deleted_list),
                        'id': idx,
                        'count': {},
                        'total': 0}
    for handle in conversation_row[idx]:
        conversation_row['total'] += 1
        total += 1

        if handle in conversation_row['count']:
            conversation_row['count'][handle] += 1
        else:
            conversation_row['count'][handle] = 1

        handle_set.add(handle)

    conversation_id.append(conversation_row)
    print(conversation_row)
    print()
print(total)

print(' ' * 20, end='')
for handle in handle_set:
    print(handle, end=' - ')
print()

col_total = np.zeros(len(handle_set), dtype=int)
for row in conversation_id:
    print(row['id'], end=' -')

    k = 0
    for handle in handle_set:
        if handle in row[row['id']]:
            print(' {}'.format(row['count'][handle]), end='  - ')
            col_total[k] += row['count'][handle]
        else:
            print(' 0', end='  - ')

        k += 1

    print(row['total'])
print(col_total)

all_rows, all_keys = observed.handle_conversation_matrix('megynkelly', my_suspended_deleted_list)
z = []
x = list(range(len(all_rows)))
y = list(range(len(handle_set)))

for row in all_rows:
    z_row = []
    key = list(row.keys())[0]
    print(key, end=' -')
    for handle in handle_set:
        if handle in row[key]:
            print(row[key][handle], end=' ')
            z_row.append(row[key][handle])
        else:
            print(' 0 -', end='')
            z_row.append(0)
    print()
    z.append(z_row)

for key in all_keys:
    print(key, all_keys[key])

print(z)
print(x)
print(y)

print('Number of people in conversation:', len(handle_set))
print('Number of conversations:', len(all_rows))
