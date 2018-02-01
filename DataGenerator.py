import sys
import os
import json
from time import strftime, localtime, time
from twitter_apps.Subjects import get_values as gv

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

    for node in nodes_conversation['nodes']:
        for record in all_subjects:
            if node['id'].lower() == record['handle'].lower():
                if 'responses' in node and 'tweets' in node:
                    print(node, node['responses'] / node['tweets'], node['tweets'], node['responses'])
                    shaker_vector.append(node['responses'] / node['tweets'])
                    node_dict[node['id']] = {'responses': node['responses'], 'tweets': node['tweets'],
                                             'deleted-accounts': node['deleted-accounts'],
                                             'closed-accounts': node['closed-accounts'],
                                             'protected-accounts': node['protected-accounts'],
                                             'suspended-accounts': node['suspended-accounts'],
                                             'stance': record['stance'], 'sex': record['sex']}

    max_value = max(shaker_vector)

    for shaker in node_dict:
        print(shaker, node_dict[shaker]['responses'] / node_dict[shaker]['tweets'] / max_value)
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

    print(sum_by_key(node_dict, 'responses', stance='conservative'))

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
