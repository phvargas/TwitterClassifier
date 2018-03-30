import plotly.graph_objs as go
import numpy as np
import plotly
from twitter_apps.Subjects import get_values
from Conversation import Conversation

plotly.offline.init_notebook_mode(connected=True)

del_path = '/odu/data/harassment/DeletedSuspendedAccounts/deleted_20180329.dat'
sus_path = '/odu/data/harassment/DeletedSuspendedAccounts/suspended_20180329.dat'
path = 'data/verifiedUserDataset/tweetConvo.dat'

print('\nLoading conversations  ...')
observed = Conversation(path)

interacting_handles = list(observed.all_conversation_elements_set())
interacting_handles.sort()
number_handles = len(interacting_handles)
print('Number of Twitter accounts interacting in all conversations: {:,}'.format(number_handles))

del_accounts = []
sus_accounts = []

with open(del_path, mode='r') as fh:
    for account in fh:
        del_accounts.append(account.strip())
del_accounts.sort()

with open(sus_path, mode='r') as fh:
    for account in fh:
        sus_accounts.append(account.strip())
sus_accounts.sort()

x_del = []
x_sus = []
for counter, account in enumerate(interacting_handles, 1):
    if account in del_accounts:
        x_del.append(counter)

    if account in sus_accounts:
        x_sus.append(counter)


trace0 = go.Scatter(
        x=x_del,
        y=[1] * len(x_del),
        name='Deleted',
        mode='markers',
        marker=dict(
            size=3,
            color='rgb(49, 163, 84)'
        )
)

trace1 = go.Scatter(
        x=x_sus,
        y=[1] * len(x_sus),
        name='Suspended',
        mode='markers',
        marker=dict(
            size=3,
            color='rgb(255, 163, 84)'
        )
)

layout = dict(
            title='Deleted and Suspended Twitter Accounts Through Time',
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            xaxis=dict(
                title='Twitter Accounts',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Time Elapsed in Weeks',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            )
        )

data = [trace0, trace1]

fig = dict(data=data, layout=layout)

plotly.offline.plot(fig, filename='Plotly/DeletionThroughTime.html', auto_open=True)