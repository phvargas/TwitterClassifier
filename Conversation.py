import os
import json


class Conversation:
    def __init__(self, conversation_filename):
        self.conversations = {}

        if os.path.isfile(conversation_filename):
            self.load_conversations(conversation_filename)

        self.max_number_conversations = max([len(self.handle_conversations_id(x))
                                             for x in self.conversations])

    def load_conversations(self, filename):
        with open(filename, "r", encoding='iso-8859-1') as fs:
            for record in fs:
                if record.strip() != '{}':
                    loaded_conversation = json.loads(record.strip())
                    conversation_block = {'interactions': []}

                    # gets the Twitter Conversation-ID from the thread
                    if loaded_conversation:
                        conversation_idx = next(iter(loaded_conversation.values()))['data-conversation-id']
                        conversation_block['data-conversation-id'] = conversation_idx

                    # separate root from response conversations
                    for _idx in loaded_conversation:
                        # print('{}: {}'.format(_idx, loaded_conversation[_idx]))

                        is_original_tweet = False   # flag to find root conversation

                        for key in loaded_conversation[_idx]:
                            # print('\t{}: {}'.format(key, loaded_conversation[_idx][key]))

                            # check if conversation-id is the root
                            if key == 'data-conversation-id' and loaded_conversation[_idx][key] == _idx:
                                is_original_tweet = True
                                break

                        if is_original_tweet:
                            conversation_block['data-screen-name'] = loaded_conversation[_idx]['data-screen-name']
                            conversation_block['tweet-time'] = loaded_conversation[_idx]['tweet-time']
                            conversation_block['tweet-text'] = loaded_conversation[_idx]['tweet-text']
                        else:
                            conversation_block['interactions'].append({
                                'data-tweet-id': loaded_conversation[_idx]['data-tweet-id'],
                                'data-screen-name': loaded_conversation[_idx]['data-screen-name'],
                                'tweet-time': loaded_conversation[_idx]['tweet-time'],
                                'tweet-text': loaded_conversation[_idx]['tweet-text']
                            })

                    if conversation_block['data-screen-name'] in self.conversations:
                        self.conversations[conversation_block['data-screen-name']][conversation_idx] = {
                            'tweet-time': conversation_block['tweet-time'],
                            'tweet-text': conversation_block['tweet-text'],
                            'interactions': conversation_block['interactions']
                        }
                    else:
                        self.conversations[conversation_block['data-screen-name']] = {
                            conversation_idx: {
                                'tweet-time': conversation_block['tweet-time'],
                                'tweet-text': conversation_block['tweet-text'],
                                'interactions': conversation_block['interactions']
                            }
                        }
        return

    def handle_conversations_id(self, handle):
        """
        finds accounts interacting in an observed conversation for a given Twitter handle. Some accounts may be
        interacting more than once in the conversation

        :param handle: Twitter handle of observed accounts
        :return: a vector containing tweets data-conversation-id from all conversations observed by a given
                 Twitter handle.
                 Ex: ['891800580842246145', '891809774769254404', '924629283447955462', '914822313799045120']
        """
        return [x for x in self.conversations[handle]]

    def handle_total_responses(self, handle):
        """
        Provides the sum of all responses to all observed tweets made by a given Twitter handle

        :param handle: Twitter handle of an observed account
        :return: number of tweeted responses. Ex: 24
        """
        return sum(self.conversation_response_vector(handle))

    def conversation_response_vector(self, handle):
        """
        Provides the sum of all responses per conversation initiated by an observed Twitter handle

        :param handle: Twitter handle of an observed account
        :return: list of number of responses. Ex: [10, 20, 0, 11, 99]
        """
        return [len(self.conversations[handle][x]['interactions']) for x in self.conversations[handle]]

    def conversation_elements_list(self, handle, conversation_id):
        """
        finds accounts interacting in an observed conversation for a given Twitter handle. Some accounts may be
        interacting more than once in the conversation

        :param handle: Twitter handle of observed accounts
        :param conversation_id: Twitter conversation-id number
        :return: a vector containing deleted tweet handles in a conversation. Ex: [Handle1, Handle2, Handle1]
        """
        if conversation_id not in self.conversations[handle]:
            return []

        return [x['data-screen-name'] for x in self.conversations[handle][conversation_id]['interactions']]

    def common_elements_list(self, handle, conversation_id, _list):
        """
        finds ONLY deleted accounts interacting in an observed conversation for a given Twitter handle

        :param handle: Twitter handle of observed accounts
        :param conversation_id: Twitter conversation-id number
        :param _list: elements comparing with a specific conversation for a given Twitter handle
        :return: a vector containing handles in the passed list and the conversation. Ex: [Handle1, Handle2, Handle1]
        """
        _common_elements = []
        accounts = self.conversation_elements_list(handle, conversation_id)

        for _account in accounts:
            if _account.lower() in _list:
                _common_elements.append(_account)

        return _common_elements

    def handle_common_element_vector_count(self, handle, _list):
        """
        creates a vector that given a list L any element L(i) appearing in a conversation a the observed Twitter handle
        adds the number of occurrences L(i) is present in the conversation.

        :param handle: Twitter handle of observed accounts
        :param _list: elements comparing with a specific conversation for a given Twitter handle
        :return: a vector containing number of deleted tweets per conversation. Ex: [3, 1, 0, 33, 0]
        """
        _occurrence_vector = []

        for _idx in self.handle_conversations_id(handle):
            accounts = self.conversation_elements_list(handle, _idx)
            _occurrence_elements = []

            for _account in accounts:
                if _account.lower() in _list:
                    _occurrence_elements.append(_account)
            _occurrence_vector.append(len(_occurrence_elements))

        return _occurrence_vector

    def conversation_elements_set(self, handle):
        """
        Provide a set of all handles responding to tweets made by ONE SPECIFIC observed Twitter account

        :return: set of Twitter handles. Ex: {'Handle1, Handle2, ..., HandleN}
        """
        _conversation_handles = set()

        for _conversation in self.conversations[handle]:
            if self.conversations[handle][_conversation]['interactions']:
                for _account in self.conversations[handle][_conversation]['interactions']:
                    _conversation_handles.add(_account['data-screen-name'].lower())

        return _conversation_handles

    def all_conversation_elements_set(self):
        """
        Provide a set of all handles responding to tweets made by ALL observed Twitter accounts

        :return: set of Twitter handles. Ex: {'Handle1, Handle2, ..., HandleN}
        """
        _conversation_handles = set()

        for _handle in self.conversations:
            for _conversation in self.conversations[_handle]:
                if self.conversations[_handle][_conversation]['interactions']:
                    for _account in self.conversations[_handle][_conversation]['interactions']:
                        _conversation_handles.add(_account['data-screen-name'].lower())

        return _conversation_handles

    def all_handle_tweets(self, handle):
        """
        Given a Twitter handle returns all conversation for which the handle interacted with

        :param handle: Twitter handle
        return: object containing conversation data
        """

        _conversation_list = []

        for _handle in self.conversations:
            for _conversation in self.conversations[_handle]:
                if self.conversations[_handle][_conversation]['interactions']:
                    for _account in self.conversations[_handle][_conversation]['interactions']:
                        if _account['data-screen-name'].lower() == handle:
                            _conversation_list.append({
                                'handle': _handle,
                                'data-conversation-id': _conversation,
                                'tweet-time': _account['tweet-time'],
                                'tweet-text': _account['tweet-text'],
                            })

        return _conversation_list


from twitter_apps.Subjects import get_values
import math

observed = Conversation('/data/harassment/verifiedUserDataset/tweetConvo.dat')

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
