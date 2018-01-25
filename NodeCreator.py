import sys
from time import strftime, localtime, time
import os
import json

"""
This Python program
  1. Reads stored conversations from Twitter Research-Subjects
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  Jan 25, 2018 at 11:30:24'
__email__ = 'pvargas@cs.odu.edu'


def read_conversations(in_filename):
    conv_dict = {}
    screen_dict = {}
    links = []
    nodes = []
    repliers_node = set()

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

    for screen_name in screen_dict:
        for screen_conv in screen_dict[screen_name]['conv']:
            screen_dict[screen_name][screen_conv] = {}

            for record in conv_dict[screen_conv]:
                if record['data-tweet-id'] == screen_conv:
                    screen_dict[screen_name][screen_conv]['tweet-text'] = record['tweet-text']
                    screen_dict[screen_name][screen_conv]['tweet-time'] = record['tweet-time']

                else:
                    if 'responds' in screen_dict[screen_name][screen_conv]:
                        screen_dict[screen_name][screen_conv]['responds'].append(record)
                    else:
                        screen_dict[screen_name][screen_conv]['responds'] = [record]

    for screen_name in screen_dict:
        number_replies = 0
        for conversation in screen_dict[screen_name]:
            conv_replies = 0
            if conversation != 'conv':
                if 'responds' in screen_dict[screen_name][conversation]:
                    conv_replies = len(screen_dict[screen_name][conversation]['responds'])
                    number_replies += conv_replies

                    for edge in screen_dict[screen_name][conversation]['responds']:
                        links.append({"source": edge['data-screen-name'], "target": conversation,
                                      "tweet": edge['tweet-text']})

                        repliers_node.add(edge['data-screen-name'])

                nodes.append({"id": conversation, "tweets": 1, "responses": conv_replies})

                links.append({"source": screen_name, "target": conversation,
                              "tweet": screen_dict[screen_name][conversation]['tweet-text']})

        nodes.append({"id": screen_name, "tweets": len(screen_dict[screen_name]) - 1,
                      "responses": number_replies
                      })

    for link in links:
        print(link)

    for node in nodes:
        print(node)

    print('Number of repliers nodes:', len(repliers_node))
    print('Number of repliers edges:', len(links))

    counter = 0
    for node in repliers_node:
        if node not in nodes:
            counter += 1
            nodes.append({"id": node, "tweets": -1, "responses": 0})
            if counter % 1000 == 0:
                print(node, counter)

    f_out = open('conv_data_json.json', mode='w')
    json.dump(screen_dict, f_out, indent=4)
    f_out.close()

    data_dict = { "nodes": nodes, "links": links }
    f_out = open('force_data.json', mode='w')
    json.dump(data_dict, f_out, indent=4)
    f_out.close()

    return


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    if len(sys.argv) < 2:
        print('\nUsage: python3 ReadConv.py <Input_filename>')
        # /data/harassment/verifiedUserDataset/tweetConvo.dat
        sys.exit(-1)

    if not os.path.isfile(sys.argv[1]):
        print('\nCould not find file: %s' % sys.argv[1])
        print('\nUsage: python3 ReadConv.py <Input_filename>')
        sys.exit(-1)

    read_conversations(sys.argv[1])

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
