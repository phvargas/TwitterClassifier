from Conversation import Conversation
from twitter_apps.Subjects import get_values
from Utilities.Sorting import dictionaryByValue
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

with open('closed_accounts.txt', mode='r') as fs:
    for account in fs:
        my_deleted_list.append(account.strip().lower())
        my_suspended_deleted_list.append(account.strip().lower())

with open('suspended.txt', mode='r') as fs:
    for account in fs:
        my_suspended_list.append(account.strip().lower())
        my_suspended_deleted_list.append(account.strip().lower())

for current_handle in get_values():
    del_rows, all_handles = observed.handle_conversation_matrix(current_handle['handle'], my_suspended_deleted_list)
    all_rows = observed.handle_conversations_id(current_handle['handle'])
    deleted_percent = len(del_rows) / len(all_rows)
    deleted_data[current_handle['handle']] = deleted_percent
    subjects_dict[current_handle['handle']] = current_handle['name']

for key, value in dictionaryByValue(deleted_data):
    print(key, value)

x = list(range(1, len(deleted_data) + 1))
y = [value for key, value in dictionaryByValue(deleted_data)]
text = [subjects_dict[key] for key, value in dictionaryByValue(deleted_data)]

data = [
    go.Scatter(
        x=x,
        y=y,
        text=text,
        mode='markers',
        marker=dict(
            size=10,
            color='rgba(152, 0, 0, .8)'
        )
    )
]

layout = go.Layout(
            title='Deleted Percentage',
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
                title='Percentage',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            )
        )

fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig, filename='Plotly/deletedPercentage.html', auto_open=True)
