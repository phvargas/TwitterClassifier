import numpy as np
from Conversation import Conversation
from twitter_apps.Subjects import get_values
import plotly.graph_objs as go
import plotly

# plotly.offline.init_notebook_mode(connected=True)

observed = Conversation('data/verifiedUserDataset/Conversation_20180407a.dat')

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

print(observed.handle_text_conversation_replies('iamsambee', '885869337063686144', 'camarogirl91'))
print(len(observed.conversation_elements_set('fredbarnes')))

density_dict = {}

total_number_tweets = 0
total_number_handles = 0
total_number_conversations = 0
total_number_handles_in_conversation = 0
total_appearance_across_conversation = 0

for current_handle in get_values('fredbarnes'):
    print(current_handle)
    conversation_id = []

    if is_tweet_density:
        all_rows, all_handles = observed.handle_conversation_matrix(current_handle['handle'],
                                                                    observed.conversation_elements_set(current_handle['handle']))
    else:
        all_rows, all_handles = observed.handle_conversation_matrix(current_handle['handle'], my_suspended_deleted_list)

    z = []
    # y = ['C' + str(k) for k in (range(1, len(all_rows) + 1))]
    y = [k for k in (range(1, len(all_rows) + 1))]
    # x = ['H'+str(k) for k in (range(1, len(all_handles) + 1))]
    x = [k for k in (range(1, len(all_handles) + 1))]

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

    area = len(all_handles) * len(all_rows)
    try:
        density = sum([all_handles[k] for k in all_handles]) / area * 100

    except ZeroDivisionError:
        density = 0

    print([sum(z[k]) for k in range(len(z))])
    print([all_handles[k] for k in all_handles])
    print('Area:', area)
    print('Density: {:.2f}%'.format(density))

    if max_density < density:
        max_density = density
        handle_max_density = current_handle['name']

    density_dict[current_handle['handle']] = density

    max_single_tweet = 0
    max_tweets_in_conversation = 0
    max_handles_in_conversation = 0
    account_number_tweets = 0
    handles_in_conversations = 0
    single_tweet_set = set()
    k_max = {}

    for k, conversation in zip(range(len(all_rows)), all_rows):
        single_tweet_set = single_tweet_set.union(set(z[k]))

        if max_tweets_in_conversation < sum(z[k]):
            max_tweets_in_conversation = sum(z[k])
            k_max['tweet-in-conversation-id'] = list(conversation)[0]
            k_max['tweets-in-conversation-count'] = max_tweets_in_conversation

        if max_handles_in_conversation < np.count_nonzero(z[k]):
            max_handles_in_conversation = np.count_nonzero(z[k])
            k_max['handles-in-conversation-id'] = list(conversation)[0]
            k_max['handles-in-conversation-count'] = max_handles_in_conversation

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

    for max_value in max_3_single_tweets:
        k_max[max_value] = set()

    for max_value in max_3_single_tweets:
        for k in range(len(z)):
            for i in range(len(z[k])):
                if z[k][i] == max_value:
                    k_max[max_value].add(list(all_handles)[i])

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

        if max_appearance_across_conversations < np.count_nonzero(z_t[k]):
            max_appearance_across_conversations = np.count_nonzero(z_t[k])
            k_max['appearance-across-conversation-handles'] = set([list(all_handles)[k]])
        elif max_appearance_across_conversations == np.count_nonzero(z_t[k]):
            k_max['appearance-across-conversation-handles'].add(list(all_handles)[k])

        appearance_across_conversations += np.count_nonzero(z_t[k])
    total_appearance_across_conversation += appearance_across_conversations

    print(k_max)
    print('Handle-Tweets Across Conv: {}, '.format(max_tweets_across_conversations) +
          'Handle\'s Appearance Across Conversation: {}'.format(max_appearance_across_conversations))
    print('Ave. Appearance Across Conversations: {:.2f}'.format(appearance_across_conversations / number_handles))
    print('List of max number of tweets:', max_3_single_tweets)

    feature_matrix = []
    idx = len(max_3_single_tweets)

    # insert global tweets-average into feature matrix
    feature_matrix.insert(0, [1.36] * idx)

    # add averages extra-features to matrix
    feature_matrix[0].append(1.18)
    feature_matrix[0].append(1.36)
    feature_matrix[0].append(47.88)
    feature_matrix[0].append(41.76)

    # insert local tweets-average into feature matrix
    local_tweet_handle = account_number_tweets / number_handles
    feature_matrix.insert(1, [local_tweet_handle] * idx)

    # add averages extra-features to matrix
    feature_matrix[1].append(appearance_across_conversations / number_handles)
    feature_matrix[1].append(account_number_tweets / number_handles)
    feature_matrix[1].append(account_number_tweets / number_conversations)
    feature_matrix[1].append(handles_in_conversations / number_conversations)

    # insert max_3 number of tweets
    feature_matrix.insert(2, max_3_single_tweets)

    # add extra-features to matrix
    feature_matrix[2].append(max_appearance_across_conversations)
    feature_matrix[2].append(max_tweets_across_conversations)
    feature_matrix[2].append(max_tweets_in_conversation)
    feature_matrix[2].append(max_handles_in_conversation)

    # Display handle and conversationID on hover
    hover = [[], [], []]

    global_tweet = 1.36
    global_appearance = 1.18
    global_tweets_in_conversation = 47.88
    global_handles_in_conversations = 41.76

    for k in range(idx):
        hover[0].append('Global ave number<br>Tweets per handle<br>' + str(global_tweet))
        hover[1].append('Local ave number<br>Tweets per handle<br>{:.2f}'.format(local_tweet_handle))

    for k in range(idx):
        comment = ''
        if k == 0:
            comment = 'Highest number <br>of tweets<br>per handle<br>'
        elif k == 1:
            comment = '2nd highest number <br>of tweets<br>per handle<br>'
        else:
            comment = '3rd highest number <br>of tweets<br>per handle<br>'

        hover[2].append(comment + '{}'.format(max_3_single_tweets[k]))

    hover[0].append('Global Ave<br>Handle appeared across<br>Conversations: ' + str(global_appearance))
    hover[0].append('Global ave number<br>Tweets across conversations<br>' + str(global_tweet))
    hover[0].append('Global ave Number<br>Tweet in conversations<br>' + str(global_tweets_in_conversation))
    hover[0].append('Global ave Number<br>Handles in conversations<br>' + str(global_handles_in_conversations))

    hover[1].append('Local Ave<br>Handle appeared across<br>Conversations: {:.2f}'.format(
                                                                    appearance_across_conversations / number_handles))
    hover[1].append('Local ave number<br>Tweet across conversations<br>{:.2f}'.format(local_tweet_handle))
    hover[1].append('Local ave Number<br>Tweet in conversations<br>{:.2f}'.format(account_number_tweets /
                                                                                  number_conversations))
    hover[1].append('Local ave Number<br>Handles in conversations<br>{:.2f}'.format(handles_in_conversations /
                                                                                    number_conversations))

    hover[2].append('Max number of<br>Handles appearing across<br>Conversations: {}'.format(
                                                                                    max_appearance_across_conversations))
    hover[2].append('Max number of<br>Tweets across conversations<br>{}'.format(max_tweets_across_conversations))
    hover[2].append('Max number of<br>Tweet in conversations<br>{}'.format(max_tweets_in_conversation))
    hover[2].append('Max number of<br>Handles in conversations<br>{}'.format(max_handles_in_conversation))

    if is_tweet_density:
        title = 'Extracted Features<br>' + current_handle['name'] + ' Conversations'
        # colorscale = 'Picnic'
        colorscale = [
            [0, 'rgb(199,233,192)'],
            [0.001, 'rgb(199,233,192)'],

            [0.001, 'rgb(161,217,155)'],
            [0.01, 'rgb(161,217,155)'],

            [0.01, 'rgb(255,255,178)'],
            [0.1, 'rgb(255,255,178)'],

            # Let values between 10-20% of the min and max of z
            # have color rgb(20, 20, 20)
            [0.1, 'rgb(254,217,118)'],
            [0.2, 'rgb(254,217,118'],

            # Values between 20-30% of the min and max of z
            # have color rgb(40, 40, 40)
            [0.2, 'rgb(254,178,76)'],
            [0.4, 'rgb(254,178,76)'],

            [0.4, 'rgb(253,141,60)'],
            [0.5, 'rgb(253,141,60)'],

            [0.5, 'rgb(252,78,42)'],
            [0.7, 'rgb(252,78,42)'],

            [0.7, 'rgb(227,26,28)'],
            [0.9, 'rgb(227,26,28)'],

            [0.9, 'rgb(177,0,38)'],
            [1.0, 'rgb(177,0,38)'],
        ]
    else:
        title = 'Extracted Features in' + current_handle['name'] + ' Deletion Tweets'
        colorscale = 'Viridis'

    print(feature_matrix)

    if len(all_handles):
        layout = go.Layout(
            autosize=False,
            width=500,
            height=350,
            title=title,
            font=dict(family='Courier New, monospace', size=14, color='#7f7f7f'),
            xaxis=dict(
                title='Feature',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=14,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Locality',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=14,
                    color='#7f7f7f'
                )
            )
        )

        data = [
            go.Heatmap(
                z=feature_matrix,
                x=[k for k in range(len(feature_matrix[0]))],
                y=['l1', 'l2', 'l3'],
                colorscale=colorscale,
                text=hover,
                hoverinfo='text'
            )
        ]

        fig = go.Figure(data=data, layout=layout)

        if is_tweet_density:
            plotly.offline.plot(fig, filename='Plotly/' + current_handle['handle'] + 'feature-mtx.html', auto_open=True)
        else:
            plotly.offline.plot(fig, filename='Plotly/' + current_handle['handle'] + 'feature-deleted-mtx.html',
                                auto_open=True)

    print('Max density of all conversations: {:.2f}'.format(max_density))
    print('Account with max density:', handle_max_density)
    print('Tweet density vector:', density_dict)


print()
print('Total Ave. Handle\'s Tweets: {:.2f}'.format(total_number_tweets / total_number_handles))
print('Total Ave. Tweets in Conversations: {:.2f}'.format(total_number_tweets / total_number_conversations))
print('Total Ave. Number of Handle in Conversations: {:.2f}'.format(total_number_handles_in_conversation /
                                                                    total_number_conversations))
print('Total Ave. Number of Handle Across Conversations: {:.2f}'.format(total_appearance_across_conversation /
                                                                        total_number_handles))
