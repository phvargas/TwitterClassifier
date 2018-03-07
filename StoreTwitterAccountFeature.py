import numpy as np
import pickle
from Conversation import Conversation
from twitter_apps.Subjects import get_values

observed = Conversation('/home/hamar/data/odu/golbeck/verifiedUserDataset/tweetConvo.dat')

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

max_density = 0
handle_max_density = ''
is_tweet_density = True
appearance = {}

total_number_tweets = 0
total_number_handles = 0
total_number_conversations = 0
total_number_handles_in_conversation = 0
total_appearance_across_conversation = 0
k_max = {}

for current_handle in get_values():
    print(current_handle)
    conversation_id = []

    if is_tweet_density:
        all_rows, all_handles = observed.handle_conversation_matrix(current_handle['handle'],
                                                                    observed.conversation_elements_set(current_handle['handle']))
    else:
        all_rows, all_handles = observed.handle_conversation_matrix(current_handle['handle'], my_suspended_deleted_list)

    z = []

    print(' ' * 20, end='')
    for handle in all_handles:
        print(handle, end=' - ')
    print()

    # fill the matrix
    for row in all_rows:
        z_row = []
        key = list(row.keys())[0]
        print(key, end=' -')
        for handle in all_handles:
            if handle in row[key]:
                if handle in appearance:
                    appearance[handle] += 1
                else:
                    appearance[handle] = 1

                print(' {}'.format(row[key][handle]), end='  - ')
                z_row.append(row[key][handle])
            else:
                print(' 0', end='  - ')
                z_row.append(0)
        print()

        z.append(z_row)

    print([sum(z[k]) for k in range(len(z))])
    print([all_handles[k] for k in all_handles])

    max_single_tweet = 0
    max_tweets_in_conversation = 0
    max_handles_in_conversation = 0
    account_number_tweets = 0
    handles_in_conversations = 0
    single_tweet_set = set()
    k_max[current_handle['handle']] = {}

    for k, conversation in zip(range(len(all_rows)), all_rows):
        single_tweet_set = single_tweet_set.union(set(z[k]))

        if max_tweets_in_conversation < sum(z[k]):
            max_tweets_in_conversation = sum(z[k])
            k_max[current_handle['handle']]['tweet-in-conversation-id'] = list(conversation)[0]
            k_max[current_handle['handle']]['tweets-in-conversation-count'] = max_tweets_in_conversation

        if max_handles_in_conversation < np.count_nonzero(z[k]):
            max_handles_in_conversation = np.count_nonzero(z[k])
            k_max[current_handle['handle']]['handles-in-conversation-id'] = list(conversation)[0]
            k_max[current_handle['handle']]['handles-in-conversation-count'] = max_handles_in_conversation

        account_number_tweets += sum(z[k])
        handles_in_conversations += np.count_nonzero(z[k])

        print(max(z[k]), sum(z[k]), np.count_nonzero(z[k]))

    total_number_tweets += account_number_tweets
    total_number_handles_in_conversation += handles_in_conversations

    number_handles = len(all_handles)
    total_number_handles += number_handles

    number_conversations = len(all_rows)
    total_number_conversations += number_conversations

    max_3_single_tweets = sorted(list(single_tweet_set), reverse=True)[:3]

    # remove 0 and 1 values if they exist
    try:
        max_3_single_tweets.remove(0)
        max_3_single_tweets.remove(1)

    except ValueError:
        pass

    k_max[current_handle['handle']]['max-values'] = {}
    for max_value in max_3_single_tweets:
        k_max[current_handle['handle']]['max-values'][max_value] = set()

    for max_value in max_3_single_tweets:
        for k in range(len(z)):
            for i in range(len(z[k])):
                if z[k][i] == max_value:
                    k_max[current_handle['handle']]['max-values'][max_value].add(list(all_handles)[i])

    k_max[current_handle['handle']]['handle-count'] = number_handles
    k_max[current_handle['handle']]['conversation-count'] = number_conversations
    k_max[current_handle['handle']]['ave-number-tweets'] = account_number_tweets / number_handles
    k_max[current_handle['handle']]['ave-conversation-tweets'] = account_number_tweets / number_conversations
    k_max[current_handle['handle']]['ave-conversation-handle'] = handles_in_conversations / number_conversations

    print('Number of people in conversation:', number_handles)
    print('Number of conversations:', number_conversations)
    print('Hndl max 3 # Tweets in_Conv: {}, Tweets-in-Conv: {}, Number Handle in Convers: {}'.
          format(max_3_single_tweets, max_tweets_in_conversation, max_handles_in_conversation))

    print('Ave Handl Tweets Conv: {:.2f}, Ave Tweets in Conv: {:.2f}'.format(account_number_tweets / number_handles,
                                                                             account_number_tweets / number_conversations))
    print('Ave Number Handles in Conv: {:.2f}'.format(handles_in_conversations / number_conversations))

    z_t = np.transpose(z)

    max_tweets_across_conversations = 0
    appearance_across_conversations = 0
    max_appearance_across_conversations = 0

    for k in range(len(z_t)):
        if max_tweets_across_conversations < sum(z_t[k]):
            max_tweets_across_conversations = sum(z_t[k])
            k_max[current_handle['handle']]['tweets-across-conversation-count'] = max_tweets_across_conversations
            k_max[current_handle['handle']]['tweets-across-conversation-handles'] = set([list(all_handles)[k]])
        elif max_tweets_across_conversations == sum(z_t[k]):
            k_max[current_handle['handle']]['tweets-across-conversation-handles'].add(list(all_handles)[k])

        if max_appearance_across_conversations < np.count_nonzero(z_t[k]):
            max_appearance_across_conversations = np.count_nonzero(z_t[k])
            k_max[current_handle['handle']]['appearance-across-conversation-count'] = max_appearance_across_conversations
            k_max[current_handle['handle']]['appearance-across-conversation-handles'] = set([list(all_handles)[k]])

        elif max_appearance_across_conversations == np.count_nonzero(z_t[k]):
            k_max[current_handle['handle']]['appearance-across-conversation-handles'].add(list(all_handles)[k])

        appearance_across_conversations += np.count_nonzero(z_t[k])
    total_appearance_across_conversation += appearance_across_conversations

    k_max[current_handle['handle']]['ave-handle-appearance-across-conversation'] = appearance_across_conversations / number_handles

    print('Handle-Tweets Across Conv: {}, '.format(max_tweets_across_conversations) +
          'Handle\'s Appearance Across Conversation: {}'.format(max_appearance_across_conversations))
    print('Ave. Appearance Across Conversations: {:.2f}'.format(appearance_across_conversations / number_handles))
    print('List of max number of tweets:', max_3_single_tweets)

print(k_max)

with open('data/account_features.pkl', mode='wb') as fhd:
    pickle.dump(k_max, fhd)
