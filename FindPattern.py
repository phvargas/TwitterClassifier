from Conversation import Conversation
from twitter_apps.Subjects import get_values
import plotly.graph_objs as go
import plotly

plotly.offline.init_notebook_mode(connected=True)
observed = Conversation('/home/hamar/data/odu/golbeck/verifiedUserDataset/tweetConvo.dat')

my_deleted_list = []
my_suspended_list = []
my_suspended_deleted_list = []
subjects_dict = {}
stance_count = {}
deleted_data = {}
deleted_amount = {}
interacting_handles = set()
interactions = {}

with open('closed_accounts.txt', mode='r') as fs:
    for account in fs:
        my_deleted_list.append(account.strip().lower())
        my_suspended_deleted_list.append(account.strip().lower())

with open('suspended.txt', mode='r') as fs:
    for account in fs:
        my_suspended_list.append(account.strip().lower())
        my_suspended_deleted_list.append(account.strip().lower())

for current_handle in get_values():
    all_rows, all_handles = observed.handle_conversation_matrix(current_handle['handle'],
                                                                observed.conversation_elements_set(
                                                                    current_handle['handle']))
    for handle in all_handles:
        if handle.lower() in interactions:
            interactions[handle.lower()].append({current_handle['handle']: all_handles[handle]})
        else:
            interactions[handle.lower()] = [{current_handle['handle']: all_handles[handle]}]

    for handle in all_handles:
        interacting_handles.add(handle.lower())

summary = [(len(interactions[handle]), handle) for handle in interactions]


"""
for handle in interactions:
    summary.append(len(interactions[handle]))
"""
print(sorted(summary, reverse=True)[:100])

deleted_interaction = []

x_deleted = []
y_deleted = []
text_deleted = []

x_non_deleted = []
y_non_deleted = []
text_non_deleted = []

y_deleted_tweets = []
text_deleted_tweets = []

counter = 0

for count, handle in sorted(summary, reverse=True):
    counter += 1
    if handle in my_suspended_deleted_list:
        tweet_count = 0
        for tweet in interactions[handle]:
            account, value = list(tweet.items())[0]
            tweet_count += value

        #print('Username: {}, Number appearing: {}, Total Tweets: {}'.format(handle, count, tweet_count))
        deleted_interaction.append((count, tweet_count, handle))

        x_deleted.append(counter)
        y_deleted.append(count)
        text_deleted.append(handle)

    else:
        x_non_deleted.append(counter)
        y_non_deleted.append(count)
        text_non_deleted.append(handle)

print('Number of interacting handles', len(interacting_handles))
print(deleted_interaction[:50])

with open('data/interacting_handles.dat', mode='w') as fout:
    for handle in interacting_handles:
        fout.write('{}\n'.format(handle))

fout.close()

trace = go.Scatter(
        x=x_non_deleted,
        y=y_non_deleted,
        name='Non-deleted',
        text=text_non_deleted,
        mode='markers',
        marker=dict(
            size=6,
            color='rgb(49, 163, 84)'
        )
)

trace0 = go.Scatter(
        x=x_deleted,
        y=y_deleted,
        name='Deleted',
        text=text_deleted,
        mode='markers',
        marker=dict(
            size=6,
            color='rgb(255, 163, 84)'
        )
)
"""
layout = go.Layout(
            title='Twitter Accounts in Conversations<br>with Research Twitter Accounts',
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            xaxis=dict(
                title='Interacting Accounts',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Number of Account Interaction',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            )
        )


data = [trace, trace0]

fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig, filename='Plotly/AccountInteraction.html', auto_open=True)


x_deleted = list(range(1, len(x_deleted) + 1))

trace0 = go.Scatter(
        x=x_deleted,
        y=y_deleted,
        name='Deleted',
        text=text_deleted,
        mode='markers',
        marker=dict(
            size=10,
            color='rgb(227,26,28)'
        )
)

layout = go.Layout(
            title='Deleted/Suspended Twitter Accounts in Conversations<br>with Research Twitter Accounts',
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            xaxis=dict(
                title='Interacting Accounts',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Number of Account Interaction',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            )
        )

data = [trace0]

fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig, filename='Plotly/DeletedAccountInteraction.html', auto_open=True)
"""

x_deleted = list(range(1, len(x_deleted) + 1))

y_deleted = []
text_deleted = []

y_deleted_tweets = []

deleted_interaction.sort(key=lambda l: (l[1], l[0], l[2]), reverse=True)

for count, deleted_tweets, handle in deleted_interaction:
    y_deleted_tweets.append(deleted_tweets)
    y_deleted.append(count)
    text_deleted.append(handle)

trace0 = go.Scatter(
        x=x_deleted,
        y=y_deleted_tweets,
        name='Tweet Count',
        text=text_deleted,
        mode='markers',
        marker=dict(
            size=10,
            color='rgb(227,26,28)'
        )
)

trace1 = go.Scatter(
        x=x_deleted,
        y=y_deleted,
        name='Interaction Count',
        text=text_deleted,
        mode='markers',
        marker=dict(
            size=10,
            color='rgb(100,26,28)'
        )
)

layout = go.Layout(
            title='Deleted/Suspended Twitter Accounts in Conversations<br>with Research Twitter Accounts',
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            xaxis=dict(
                title='Interacting Accounts',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Tweet Count',
                type='log',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            )
        )

data = [trace0]

fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig, filename='Plotly/DeletedTweetsAndAccountInteraction.html', auto_open=True)
