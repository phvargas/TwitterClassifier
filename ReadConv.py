import sys
from time import strftime, localtime, time
import os
import json

"""
This Python program
  1. Reads stored conversations from Twitter Research-Subjects
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  Jan 23, 2018 at 21:01:14'
__email__ = 'pvargas@cs.odu.edu'


def read_conversations(in_filename):
    conv_dict = {}
    screen_dict = {}

    with open(in_filename, "r", encoding='iso-8859-1') as fs:
        for record in fs:
            conv = json.loads(record.strip())
            print(conv)
            if conv:
                conv_idx = next(iter(conv.values()))['data-conversation-id']
                conv_dict[conv_idx] = []
            for idx in conv:
                print('{}: {}'.format(idx, conv[idx]))
                conv_dict[conv_idx].append({'data-tweet-id': conv[idx]['data-tweet-id'],
                                            'data-screen-name': conv[idx]['data-screen-name'],
                                            'tweet-time': conv[idx]['tweet-time'],
                                            'tweet-text': conv[idx]['tweet-text']
                                            })

                for key in conv[idx]:
                    print('\t{}: {}'.format(key, conv[idx][key]))
                    if key == 'data-conversation-id' and conv[idx][key] == idx:
                        print('\t\tConversation originator: {}'.format(conv[idx]['data-screen-name']))

                        # add screen_name to conversation initiated by research group member
                        if conv[idx]['data-screen-name'] in screen_dict:
                            screen_dict[conv[idx]['data-screen-name']]['conv'].append(conv_idx)
                        else:
                            screen_dict[conv[idx]['data-screen-name']] = {}
                            screen_dict[conv[idx]['data-screen-name']]['conv'] = [conv_idx]
            print()

    print(len(conv_dict))
    print(screen_dict)

    for screen_name in screen_dict:
        for screen_conv in screen_dict[screen_name]['conv']:
            # print(screen_conv)
            screen_dict[screen_name][screen_conv] = {}
            for record in conv_dict[screen_conv]:
                if record['data-tweet-id'] == screen_conv:
                    # print(record, 'is main text')
                    screen_dict[screen_name][screen_conv]['tweet-text'] = record['tweet-text']
                    screen_dict[screen_name][screen_conv]['tweet-time'] = record['tweet-time']

                else:
                    if 'responds' in screen_dict[screen_name][screen_conv]:
                        screen_dict[screen_name][screen_conv]['responds'].append(record)
                    else:
                        screen_dict[screen_name][screen_conv]['responds'] = [record]

    for screen_name in screen_dict:
        print('{}: '.format(screen_name))
        for conversation in screen_dict[screen_name]:
            if conversation != 'conv':
                print(screen_name, conversation)

                print('\t{}: '.format(conversation))

                print('\t\ttweet-descrip: {}'.format(screen_dict[screen_name][conversation]['tweet-text']))
                print('\t\ttweet-time: {}'.format(screen_dict[screen_name][conversation]['tweet-time']))

                print('\t\t:[')
                if 'responds' in screen_dict[screen_name][conversation]:
                    for tweet in screen_dict[screen_name][conversation]['responds']:
                        print('\t\t\tdata-tweet-id: {}'.format(tweet['data-tweet-id']))
                        print('\t\t\ttweet-text: {}'.format(tweet['tweet-text']))
                        print('\t\t\ttweet-time: {}'.format(tweet['tweet-time']))
                        print('\t\t\tdata-screen-name: {}'.format(tweet['data-screen-name']))
                        print()

    f_out = open('conv_data_json.json', mode='w')
    json.dump(screen_dict, f_out, indent=4)
    f_out.close()

    return


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    if len(sys.argv) < 2:
        print('\nUsage: python3 ReadConv.py <Input_filename>')
        sys.exit(-1)

    if not os.path.isfile(sys.argv[1]):
        print('\nCould not find file: %s' % sys.argv[1])
        print('\nUsage: python3 ReadConv.py <Input_filename>')
        sys.exit(-1)

    read_conversations(sys.argv[1])

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
