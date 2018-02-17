import sys
import os
import json
import numpy as np
from time import strftime, localtime, time
from twitter_apps.Subjects import get_values as gv
from collections import Counter

"""
This Python program
  1. Reads stored conversations from Twitter Research-Subjects
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Fri,  Jan 26, 2018 at 20:53:17'
__email__ = 'pvargas@cs.odu.edu'


def read_conversations(in_filename):
    shaker_vector = []
    data_points = set()
    node_dict = {}

    fh = open(in_filename, mode='r')
    nodes_conversation = json.load(fh)
    fh.close()

    all_subjects = gv()

    for subject in all_subjects:
        print(subject)

    max_conversation_size = 0
    conservative_tweets = 0
    liberal_tweets = 0
    male_tweets = 0
    female_tweets = 0

    header = 'Name,Followers,Stance,Sex,Handle,Tweets,Responses,std,Max.responses,Min.respos,Ave.Response,Resp.Freq,' +\
             'deleted,closed,protected,suspended'

    # Find max number of conversation from given sample
    for node in nodes_conversation['nodes']:
        for record in all_subjects:
            if node['id'].lower() == record['handle'].lower():
                if 'responses' in node and 'tweets' in node:
                    if len(node['response-in-conversation']) > max_conversation_size:
                        max_conversation_size = len(node['response-in-conversation'])

    conservative_vector = np.zeros((max_conversation_size,), dtype=int)
    liberal_vector = np.zeros((max_conversation_size,), dtype=int)
    male_vector = np.zeros((max_conversation_size,), dtype=int)
    female_vector = np.zeros((max_conversation_size,), dtype=int)

    for i in range(max_conversation_size):
        header += ",Conv." + str(i)

    print(header)
    for node in nodes_conversation['nodes']:
        for record in all_subjects:
            if node['id'].lower() == record['handle'].lower():
                if 'responses' in node and 'tweets' in node:
                    line = '{},{},{},{},{},{},{},{:.2f},{},{},{:.2f},{}:{},{},{},{},{}'.format(
                        record['name'],
                        record['followers'],
                        record['stance'],
                        record['sex'],
                        record['handle'],
                        node['tweets'],
                        node['responses'],
                        np.std(node['response-in-conversation']),
                        max(node['response-in-conversation']),
                        min(node['response-in-conversation']),
                        np.average(node['response-in-conversation']),
                        Counter(node['response-in-conversation']).most_common()[0][0],
                        Counter(node['response-in-conversation']).most_common()[0][1],
                        node['deleted-count'],
                        node['closed-count'],
                        node['protected-count'],
                        node['suspended-count']
                    )

                    k = len(node['response-in-conversation']) - 1

                    resize_vector = np.insert(sorted(node['response-in-conversation'], reverse=True), k + 1,
                                              np.zeros(max_conversation_size - k - 1))

                    if record['stance'] == 'conservative':
                        conservative_vector += resize_vector
                        conservative_tweets += node['tweets']

                    if record['stance'] == 'liberal':
                        liberal_vector += resize_vector
                        liberal_tweets += node['tweets']

                    if record['sex'] == 'male':
                        male_vector += resize_vector
                        male_tweets += node['tweets']

                    if record['sex'] == 'female':
                        female_vector += resize_vector
                        male_tweets += node['tweets']

                    for i in range(k):
                        line += ',' + str(node['response-in-conversation'][i])

                    line += ',' + str(node['response-in-conversation'][k])
                    for i in range(k + 1, max_conversation_size):
                        line += ','

                    print(line)

                    shaker_vector.append(node['responses'] / node['tweets'])

                    node_dict[node['id']] = {'responses': node['responses'], 'tweets': node['tweets'],
                                             'deleted-accounts': node['deleted-count'],
                                             'closed-accounts': node['closed-count'],
                                             'protected-accounts': node['protected-count'],
                                             'suspended-accounts': node['suspended-count'],
                                             'stance': record['stance'], 'sex': record['sex'],
                                             'response-in-conversation': node['response-in-conversation']}

    # get all conservatives values
    line = '{},{},{},{},{},{},{},{:.2f},{},{},{:.2f},{}:{},{},{},{},{}'.format(
        'All',                          # Name
        '0',                            # Followers
        'conservative',                 # Stance
        'NOTAPPL',                      # Sex
        'all_conservatives',            # Handles
        conservative_tweets,            # Tweets
        sum(conservative_vector),       # Responses
        np.std(conservative_vector),
        max(conservative_vector),
        min(conservative_vector),
        sum(conservative_vector) / conservative_tweets,
        Counter(conservative_vector).most_common()[0][0],
        Counter(conservative_vector).most_common()[0][1],
        '',                             # deleted-accounts
        '',                             # closed-accounts
        '',                             # protected-accounts
        ''                              # suspended-accounts
    )

    for tweet in conservative_vector:
        line += ',' + str(tweet)

    print(line)

    # get all liberal values
    line = '{},{},{},{},{},{},{},{:.2f},{},{},{:.2f},{}:{},{},{},{},{}'.format(
        'All',                          # Name
        '0',                            # Followers
        'liberal',                      # Stance
        'NOTAPPL',                      # Sex
        'all_liberal',                  # Handles
        liberal_tweets,                 # Tweets
        sum(liberal_vector),       # Responses
        np.std(liberal_vector),
        max(liberal_vector),
        min(liberal_vector),
        sum(liberal_vector) / liberal_tweets,
        Counter(liberal_vector).most_common()[0][0],
        Counter(liberal_vector).most_common()[0][1],
        '',                             # deleted-accounts
        '',                             # closed-accounts
        '',                             # protected-accounts
        ''                              # suspended-accounts
    )

    for tweet in liberal_vector:
        line += ',' + str(tweet)
    print(line)

    print(liberal_vector)

    conservative_vector = np.zeros((max_conversation_size,), dtype=int)
    liberal_vector = np.zeros((max_conversation_size,), dtype=int)
    male_vector = np.zeros((max_conversation_size,), dtype=int)
    female_vector = np.zeros((max_conversation_size,), dtype=int)

    conservative_tweets = 0
    liberal_tweets = 0
    male_tweets = 0
    female_tweets = 0

    print('\n\nDeleted tweets\n')
    print(header)
    for node in nodes_conversation['nodes']:
        for record in all_subjects:
            if node['id'].lower() == record['handle'].lower():
                if 'responses' in node and 'tweets' in node:
                    line = '{},{},{},{},{},{},{},{:.2f},{},{},{:.2f},{}:{},{},{},{},{}'.format(
                        record['name'],
                        record['followers'],
                        record['stance'],
                        record['sex'],
                        record['handle'],
                        node['tweets'],
                        node['responses'],
                        np.std(node['response-in-conversation']),
                        max(node['response-in-conversation']),
                        min(node['response-in-conversation']),
                        np.average(node['response-in-conversation']),
                        Counter(node['response-in-conversation']).most_common()[0][0],
                        Counter(node['response-in-conversation']).most_common()[0][1],
                        node['deleted-count'],
                        node['closed-count'],
                        node['protected-count'],
                        node['suspended-count']
                    )

                    k = len(node['suspended-closed']) - 1

                    resize_vector = np.insert(sorted(node['suspended-closed'], reverse=True), k + 1,
                                              np.zeros(max_conversation_size - k - 1))

                    if record['stance'] == 'conservative':
                        conservative_vector += resize_vector
                        conservative_tweets += node['tweets']

                    if record['stance'] == 'liberal':
                        liberal_vector += resize_vector
                        liberal_tweets += node['tweets']

                    if record['sex'] == 'male':
                        male_vector += resize_vector
                        male_tweets += node['tweets']

                    if record['sex'] == 'female':
                        female_vector += resize_vector
                        male_tweets += node['tweets']

                    k = len(node['suspended-closed']) - 1
                    for i in range(k):
                        line += ',' + str(node['suspended-closed'][i])

                    line += ',' + str(node['suspended-closed'][k])
                    for i in range(k + 1, max_conversation_size):
                        line += ','

                    print(line)

    # get all deleted account in conservatives conversations
    line = '{},{},{},{},{},{},{},{:.2f},{},{},{:.2f},{}:{},{},{},{},{}'.format(
        'All',                          # Name
        '0',                            # Followers
        'conservative',                 # Stance
        'NOTAPPL',                      # Sex
        'del_conservatives',            # Handles
        conservative_tweets,            # Tweets
        sum(conservative_vector),       # Responses
        np.std(conservative_vector),
        max(conservative_vector),
        min(conservative_vector),
        sum(conservative_vector) / conservative_tweets,
        Counter(conservative_vector).most_common()[0][0],
        Counter(conservative_vector).most_common()[0][1],
        '',                             # deleted-accounts
        '',                             # closed-accounts
        '',                             # protected-accounts
        ''                              # suspended-accounts
    )

    for tweet in conservative_vector:
        line += ',' + str(tweet)
    print(line)

    # get all deleted account in liberal conversations
    line = '{},{},{},{},{},{},{},{:.2f},{},{},{:.2f},{}:{},{},{},{},{}'.format(
        'All',                          # Name
        '0',                            # Followers
        'liberal',                      # Stance
        'NOTAPPL',                      # Sex
        'del_liberal',                  # Handles
        liberal_tweets,                 # Tweets
        sum(liberal_vector),       # Responses
        np.std(liberal_vector),
        max(liberal_vector),
        min(liberal_vector),
        sum(liberal_vector) / liberal_tweets,
        Counter(liberal_vector).most_common()[0][0],
        Counter(liberal_vector).most_common()[0][1],
        '',                             # deleted-accounts
        '',                             # closed-accounts
        '',                             # protected-accounts
        ''                              # suspended-accounts
    )

    for tweet in liberal_vector:
        line += ',' + str(tweet)
    print(line)

    max_value = max(shaker_vector)

    for shaker in node_dict:
        data_points.add((shaker, node_dict[shaker]['responses'] / node_dict[shaker]['tweets'] / max_value,
                         node_dict[shaker]['sex'], node_dict[shaker]['stance'],
                         node_dict[shaker]['responses'], node_dict[shaker]['tweets'],
                         node_dict[shaker]['deleted-accounts'],
                         node_dict[shaker]['closed-accounts'],
                         node_dict[shaker]['protected-accounts'],
                         node_dict[shaker]['suspended-accounts'],
                         ))

    print('(handle, shaker-ratio, sex, stance, responses, tweets, deleted, closed, protected, suspended)')
    for value in sorted(data_points, key=lambda x: x[1], reverse=True):
        print(value)

    print(sum_by_key(node_dict, 'followers', stance='conservative'))

    return


def sum_by_key(obj, term, **kwargs):
    total = 0

    redux = []

    if not kwargs:
        for subject in obj:
            redux.append(subject)
    else:
        for subject in obj:
            all_keys_correct = False
            for key, value in kwargs.items():
                if key in obj[subject] and obj[subject][key] == value:
                    all_keys_correct = True
                else:
                    all_keys_correct = False
                    break

            if all_keys_correct:
                redux.append(subject)

    print(len(redux), redux)

    for key in redux:
        if term in obj[key] and type(obj[key][term] == int):
            total += obj[key][term]

    return total


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    if len(sys.argv) < 2:
        print('\nUsage: python3 DataGenerator.py <Input_filename>')
        # /data/harassment/verifiedUserDataset/force_data.json
        sys.exit(-1)

    if not os.path.isfile(sys.argv[1]):
        print('\nCould not find file: %s' % sys.argv[1])
        print('\nUsage: python3 DataGenerator.py <Input_filename>')
        sys.exit(-1)

    read_conversations(sys.argv[1])

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
