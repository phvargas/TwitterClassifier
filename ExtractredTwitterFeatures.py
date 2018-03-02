import numpy as np
from Conversation import Conversation
from twitter_apps.Subjects import get_values
import plotly.graph_objs as go
import plotly

# plotly.offline.init_notebook_mode(connected=True)

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

print(observed.handle_text_conversation_replies('iamsambee', '885869337063686144', 'camarogirl91'))
print(len(observed.conversation_elements_set('tuckercarlson')))

density_dict = {}

total_number_tweets = 0
total_number_handles = 0
total_number_conversations = 0
total_number_appearance_conversation = 0
total_appearance_across_conversation = 0

for current_handle in get_values(handle='iamsambee'):
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

    # Display handle and conversationID on hover
    hover = list(range(len(all_rows) + 1))
    symbol = list(range(len(all_rows) + 1))

    max_single_tweet = 0
    max_conversation_tweet = 0
    max_appearance_number = 0
    account_number_tweets = 0
    appearance_in_conversations = 0
    k_max = {}

    for k, conversation in zip(range(len(all_rows)), all_rows):
        hover[k] = ['Handle: ' + handle + '<br>' + 'Appeared: ' + str(appearance[handle]) +
                    ' in ' + str(len(all_rows)) + ' conversations' +
                    '<br>Conversation: ' + list(conversation)[0] + '<br>Tweets: ' + str(z[k][i]) + ' of ' +
                    str(sum(z[k])) for i, handle in zip(range(len(all_handles)), all_handles)]

        symbol[k] = [' ' for i in range(len(all_handles))]

        if max_single_tweet < max(z[k]):
            max_single_tweet = max(z[k])
            k_max['single-tweet'] = list(all_handles)[k]

        if max_conversation_tweet < sum(z[k]):
            max_conversation_tweet = sum(z[k])
            k_max['conversation-tweet'] = list(conversation)[0]

        if max_appearance_number < np.count_nonzero(z[k]):
            max_appearance_number = np.count_nonzero(z[k])
            k_max['conversation-appearance'] = list(conversation)[0]

        account_number_tweets += sum(z[k])
        appearance_in_conversations += np.count_nonzero(z[k])

        print(max(z[k]), sum(z[k]), np.count_nonzero(z[k]))

    total_number_tweets += account_number_tweets
    total_number_appearance_conversation += appearance_in_conversations

    number_handles = len(all_handles)
    total_number_handles += number_handles

    number_conversations = len(all_rows)
    total_number_conversations += number_conversations

    print('Number of people in conversation:', number_handles)
    print('Number of conversations:', number_conversations)
    print('Hndl_Tweets_Conv: {}, Tweets-in-Conv: {}, Number Handle in Convers: {}'.format(max_single_tweet,
                                                                                          max_conversation_tweet,
                                                                                          max_appearance_number))
    print('Ave Handl Tweets Conv: {:.2f}, Ave Tweets in Conv: {:.2f}'.format(account_number_tweets / number_handles,
                                                                             account_number_tweets / number_conversations))
    print('Ave Number Handles in Conv: {:.2f}'.format(appearance_in_conversations / number_conversations))

    print(k_max)

    z_t = np.transpose(z)

    tweets_across_conversations = 0
    max_tweets_across_conversations = 0
    appearance_across_conversations = 0
    max_appearance_across_conversations = 0

    for k in range(len(z_t)):
        if max_tweets_across_conversations < sum(z_t[k]):
            max_tweets_across_conversations = sum(z_t[k])

        if max_appearance_across_conversations < np.count_nonzero(z_t[k]):
            max_appearance_across_conversations = np.count_nonzero(z_t[k])

        appearance_across_conversations += np.count_nonzero(z_t[k])
    total_appearance_across_conversation += appearance_across_conversations

    print('Handle-Tweets Across Conv: {}, '.format(max_tweets_across_conversations) +
          'Handle\'s Appearance Across Conversation: {}'.format(max_appearance_across_conversations))
    print('Ave. Appearance Across Conversations: {:.2f}'.format(appearance_across_conversations / number_handles))

    """

    if is_tweet_density:
        title = 'Tweets Accounts in ' + current_handle['name'] + ' Conversations<br>Tweet Density: '
        # colorscale = 'Picnic'
        colorscale = [[0.0, 'rgb(255,255,255)'], [0.1111111111111111, 'rgb(166,189,219)'],
                      [0.222222222, 'rgb(43,140,190)'], [0.3333333333, 'rgb(252,146,114)'],
                      [1, 'rgb(255,0,0)']]
    else:
        title = 'Deleted Accounts in ' + current_handle['name'] + ' Conversations<br>Deletion Density: '
        colorscale = 'Viridis'

    if len(all_handles):
        layout = go.Layout(
            title=title +
            '{:.2f}%'.format(density),
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            xaxis=dict(
                title='Handles',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Conversation IDX',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            )
        )

        data = [
            go.Heatmap(
                z=z,
                x=x,
                y=y,
                colorscale=colorscale,
                text=hover,
                hoverinfo='text'
            )
        ]

        fig = go.Figure(data=data, layout=layout)

        if is_tweet_density:
            plotly.offline.plot(fig, filename='Plotly/' + current_handle['handle'] + 'tweet-mtx.html', auto_open=True)
        else:
            plotly.offline.plot(fig, filename='Plotly/' + current_handle['handle'] + 'deleted-mtx.html', auto_open=True)

    print('Max density of all conversations: {:.2f}'.format(max_density))
    print('Account with max density:', handle_max_density)
    print('Tweet density vector:', density_dict)
    """

print()
print('Total Ave. Handle\'s Tweets in Single Conversation: {:.2f}'.format(total_number_tweets / total_number_handles))
print('Total Ave. Tweets in Conversations: {:.2f}'.format(total_number_tweets / total_number_conversations))
print('Total Ave. Number of Handle in Conversations: {:.2f}'.format(total_number_appearance_conversation /
                                                                    total_number_conversations))
print('Total Ave. Number of Handle Across Conversations: {:.2f}'.format(total_appearance_across_conversation /
                                                                        total_number_handles))
