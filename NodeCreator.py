import sys
import os
import json
import twitter
from time import strftime, localtime, time
from twitter_apps.Keys import provide_keys
from twitter_apps.GetTweets import retrieve_tweets

"""
This Python program
  1. Reads stored conversations from Twitter Research-Subjects
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Tue,  Jan 25, 2018 at 11:30:24'
__email__ = 'pvargas@cs.odu.edu'


def read_conversations(in_filename):
    screen_dict = {}
    links = []
    nodes = []
    repliers_node = set()

    deleted_accounts = []
    closed_accounts = []
    suspended_accounts = []
    protected_accounts = []

    # upload deleted accounts
    with open('deleted_accounts.txt', mode='r') as fs_deleted:
        for account in fs_deleted:
            deleted_accounts.append(account.strip().lower())

    # upload closed accounts
    with open('closed_accounts.txt', mode='r') as fs_closed:
        for account in fs_closed:
            closed_accounts.append(account.strip().lower())

    # upload suspended accounts
    with open('suspended.txt', mode='r') as fs_suspended:
        for account in fs_suspended:
            suspended_accounts.append(account.strip().lower())

    # upload protected accounts
    with open('protected.txt', mode='r') as fs_protected:
        for account in fs_protected:
            protected_accounts.append(account.strip().lower())

    # load conversations
    with open(in_filename, "r", encoding='iso-8859-1') as fs:
        for record in fs:
            conv = json.loads(record.strip())
            conv_dict = {'responds': []}

            deleted_count = 0
            protected_count = 0
            suspended_count = 0
            closed_count = 0

            # gets the Twitter Conversation-ID from the thread
            if conv:
                conv_idx = next(iter(conv.values()))['data-conversation-id']
                conv_dict['data-conversation-id'] = conv_idx

            for idx in conv:
                print('{}: {}'.format(idx, conv[idx]))

                is_original_tweet = False

                for key in conv[idx]:
                    print('\t{}: {}'.format(key, conv[idx][key]))

                    # check if conversation-id is the root
                    if key == 'data-conversation-id' and conv[idx][key] == idx:
                        is_original_tweet = True
                        break

                if is_original_tweet:
                    conv_dict['data-screen-name'] = conv[idx]['data-screen-name']
                    conv_dict['tweet-time'] = conv[idx]['tweet-time']
                    conv_dict['tweet-text'] = conv[idx]['tweet-text']
                else:
                    if conv[idx]['data-screen-name'].lower() in deleted_accounts:
                        deleted_count += 1

                    if conv[idx]['data-screen-name'].lower() in protected_accounts:
                        protected_count += 1

                    if conv[idx]['data-screen-name'].lower() in closed_accounts:
                        closed_count += 1

                    if conv[idx]['data-screen-name'].lower() in suspended_accounts:
                        suspended_count += 1

                    conv_dict['responds'].append({'data-tweet-id': conv[idx]['data-tweet-id'],
                                                  'data-screen-name': conv[idx]['data-screen-name'],
                                                  'tweet-time': conv[idx]['tweet-time'],
                                                  'tweet-text': conv[idx]['tweet-text']
                                                  })

            if conv:
                if conv_dict['data-screen-name'] not in screen_dict:
                    screen_dict[conv_dict['data-screen-name']] = {conv_dict['data-conversation-id']: {
                        'tweet-time': conv_dict['tweet-time'],
                        'tweet-text': conv_dict['tweet-text'],
                        'responds': conv_dict['responds'],
                        'deleted-accounts': deleted_count,
                        'suspended-accounts': suspended_count,
                        'protected-accounts': protected_count,
                        'closed-accounts': closed_count
                    }}
                else:
                    screen_dict[conv_dict['data-screen-name']][conv_dict['data-conversation-id']] = {
                        'tweet-time': conv_dict['tweet-time'],
                        'tweet-text': conv_dict['tweet-text'],
                        'responds': conv_dict['responds'],
                        'deleted-accounts': deleted_count,
                        'suspended-accounts': suspended_count,
                        'protected-accounts': protected_count,
                        'closed-accounts': closed_count
                    }

    # add nodes
    nodes.append({"id": "0", "tweets": 0,
                  "responses": 0
                  })
    for screen_name in screen_dict:
        number_replies = 0

        deleted_count = 0
        protected_count = 0
        suspended_count = 0
        closed_count = 0

        for conversation in screen_dict[screen_name]:
            conv_replies = 0

            if 'responds' in screen_dict[screen_name][conversation]:
                conv_replies = len(screen_dict[screen_name][conversation]['responds'])
                number_replies += conv_replies
                deleted_count += screen_dict[screen_name][conversation]['deleted-accounts']
                suspended_count += screen_dict[screen_name][conversation]['suspended-accounts']
                protected_count += screen_dict[screen_name][conversation]['protected-accounts']
                closed_count += screen_dict[screen_name][conversation]['closed-accounts']

                for edge in screen_dict[screen_name][conversation]['responds']:
                    # links.append({"source": edge['data-screen-name'], "target": conversation,
                    #               "tweet": edge['tweet-text']})

                    repliers_node.add(edge['data-screen-name'])

            # conversations nodes
            nodes.append({"id": conversation, "tweets": 1, "responses": conv_replies})

            links.append({"source": screen_name, "target": conversation,
                          "tweet": screen_dict[screen_name][conversation]['tweet-text']})

        # nodes of research group conversations
        nodes.append({"id": screen_name, "tweets": len(screen_dict[screen_name]),
                      "responses": number_replies, 'deleted-accounts': deleted_count,
                      'closed-accounts': closed_count, 'protected-accounts': protected_count,
                      'suspended-accounts': suspended_count
                      })

        links.append({"source": "0", "target": screen_name,
                      "tweet": ""})

    for link in links:
        print(link)

    for node in nodes:
        print(node)

    print('Number of repliers nodes:', len(repliers_node))
    print('Number of repliers edges:', len(links))

    """    
    # find which nodes were deleted
    key = provide_keys('males')
    deleted_accounts = []
    api = twitter.Api(consumer_key=key['consumer_key'],
                      consumer_secret=key['consumer_secret'],
                      access_token_key=key['access_token_key'],
                      access_token_secret=key['access_token_secret'])

    for node in repliers_node:
        print(node)
        if not retrieve_tweets(api, node, count=1):
            print(node, 'was deleted...')
            deleted_accounts.append(node)
    
    with open('deleted_accounts.txt', mode='w') as fs_deleted:
        for node in deleted_accounts:
            fs_deleted.write('{}\n'.format(node))

    """

    # nodes of Twitter handles interacting with research group conversations
    """
    counter = 0
    for node in repliers_node:
        if node not in nodes:
            counter += 1
            nodes.append({"id": node, "tweets": -1, "responses": 0})
            if counter % 1000 == 0:
                print(node, counter)
    """

    f_out = open('conv_data_json.json', mode='w')
    json.dump(screen_dict, f_out, indent=4)
    f_out.close()

    data_dict = {"nodes": nodes, "links": links}
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
