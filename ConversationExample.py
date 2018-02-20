from Conversation import Conversation

from twitter_apps.Subjects import get_values
import math

observed = Conversation('/home/hamar/data/odu/golbeck/verifiedUserDataset/tweetConvo.dat')

my_deleted_list = []
my_suspended_list = []
my_suspended_deleted_list = []
with open('closed_accounts.txt', mode='r') as fs:
    for account in fs:
        my_deleted_list.append(account.strip().lower())
        my_suspended_deleted_list.append(account.strip().lower())

with open('suspended.txt', mode='r') as fs:
    for account in fs:
        my_suspended_list.append(account.strip().lower())
        my_suspended_deleted_list.append(account.strip().lower())

"""
print('length of closed-accounts:', len(my_deleted_list))

print(observed.handle_conversations_id('andylevy'))
print()
print(observed.conversations['andylevy'])
print()
print('Andy total responses:', observed.handle_total_responses('andylevy'))
print(observed.conversation_response_vector('andylevy'))
print('Andy\'s conversation interacting elements list',
      observed.conversation_elements_list('andylevy', '931003955852861441'))
print('Total:', len(observed.conversation_elements_list('andylevy', '931003955852861441')))
print()
print('Andy\'s ALL conversation interacting element set',
      observed.conversation_elements_set('andylevy'))
print('Total:', len(observed.conversation_elements_set('andylevy')))
print()
print(observed.common_elements_list('megynkelly', '894671115808890881', my_deleted_list))


print()
deleted = 0
for idx in observed.handle_conversations_id('megynkelly'):
    deleted_handles = observed.common_elements_list('megynkelly', idx, my_deleted_list)
    print(idx, deleted_handles)
    deleted += len(deleted_handles)

print('deleted handles', deleted)
print()

suspended_deleted = 0
for idx in observed.handle_conversations_id('BillHemmer'):
    deleted_handles = observed.common_elements_list('BillHemmer', idx, my_suspended_deleted_list)
    print(idx, deleted_handles)
    suspended_deleted += len(deleted_handles)

print('deleted handles', suspended_deleted)
print('Responses in Conv:', observed.conversation_response_vector('BillHemmer'))
print('deleted_suspended_vector:', observed.handle_common_element_vector_count('BillHemmer', my_suspended_deleted_list))

print('Max number of conversations:', observed.max_number_conversations)
print('Number of handles in conversation:', len(observed.all_conversation_elements_set()))
"""

subjects_dict = {}
stance_count = {}
counter = 0

for account in get_values():
    subjects_dict[account['handle'].lower()] = {'stance': account['stance']}
    if account['stance'] not in stance_count:
        stance_count[account['stance']] = 1
    else:
        stance_count[account['stance']] += 1

for stance in stance_count:
    print('{}:{}'.format(stance, stance_count[stance]))

for harasser in my_suspended_deleted_list:
    is_valid = False

    account_appearance = []
    stance_type = set()
    intercepts = {}

    for account in observed.conversations:
        presence = sum(observed.handle_common_element_vector_count(account, [harasser]))
        if presence:
            account_appearance.append('{} : {} -> appeared in {} conversations.'.format(account,
                                                                                        subjects_dict[account.lower()],
                                                                                        presence))
            stance_type.add(subjects_dict[account.lower()]['stance'])

            if subjects_dict[account.lower()]['stance'] not in intercepts:
                intercepts[subjects_dict[account.lower()]['stance']] = 1
            else:
                intercepts[subjects_dict[account.lower()]['stance']] += 1

            if len(account_appearance) > 1 and len(stance_type) > 1:
                is_valid = True

    if is_valid:
        counter += 1
        if ('liberal' in intercepts and 'conservative' in intercepts) and \
           (intercepts['conservative'] != intercepts['liberal']):
            print(harasser)
            for row in account_appearance:
                print(row)
            print("-" * 80)
            for tweet in observed.all_handle_tweets(harasser):
                print('{:15} <- {}: {}'.format(tweet['handle'], tweet['data-conversation-id'],
                                               tweet['tweet-text'].replace("\n", " ")))

            po = 0

            if 'conservative' in intercepts and 'liberal' in intercepts:
                po = math.log2((intercepts['conservative'] * stance_count['liberal']) /
                               (intercepts['liberal'] * stance_count['conservative']))
            print('Political Orientation:', po)
            print()

print(counter)
