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
deleted_amount = {}
text0 = []
x0 = []
y0 = []
text1 = []
x1 = []
y1 = []
text2 = []
x2 = []
y2 = []
text3 = []
x3 = []
y3 = []
text4 = []
x4 = []
y4 = []
text5 = []
x5 = []
y5 = []

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

    deleted_amount[current_handle['handle']] = 0
    for row in del_rows:
        for handle in row[list(row)[0]]:
            deleted_amount[current_handle['handle']] += row[list(row)[0]][handle]

    deleted_percent = len(del_rows) / len(all_rows)
    deleted_data[current_handle['handle']] = deleted_percent
    subjects_dict[current_handle['handle']] = current_handle['name']

    print(deleted_amount[current_handle['handle']])

for key, value in dictionaryByValue(deleted_data):
    print(key, value)

x = list(range(1, len(deleted_data) + 1))
y = [value for key, value in dictionaryByValue(deleted_data)]

text = [subjects_dict[key] + '<br>Deleted:' + str(deleted_amount[key]) for key, value in dictionaryByValue(deleted_data)]

for k, (key, value) in zip(range(1, len(deleted_data) + 1), dictionaryByValue(deleted_data)):
    check = int(deleted_amount[key])
    if check <= 25:
        x0.append(k)
        y0.append(value)
        text0.append(subjects_dict[key] + '<br>Deleted:' + str(deleted_amount[key]))

    elif check <= 50:
        x1.append(k)
        y1.append(value)
        text1.append(subjects_dict[key] + '<br>Deleted:' + str(deleted_amount[key]))

    elif check <= 75:
        x2.append(k)
        y2.append(value)
        text2.append(subjects_dict[key] + '<br>Deleted:' + str(deleted_amount[key]))

    elif check <= 125:
        x3.append(k)
        y3.append(value)
        text3.append(subjects_dict[key] + '<br>Deleted:' + str(deleted_amount[key]))

    elif check <= 175:
        x4.append(k)
        y4.append(value)
        text4.append(subjects_dict[key] + '<br>Deleted:' + str(deleted_amount[key]))
    else:
        x5.append(k)
        y5.append(value)
        text5.append(subjects_dict[key] + '<br>Deleted:' + str(deleted_amount[key]))

print(len(x0), len(x1), len(x2), len(x3), len(x4), len(x5))

trace0 = go.Scatter(
        x=x0,
        y=y0,
        name='0 - 25',
        text=text0,
        mode='markers',
        marker=dict(
            size=10,
            color='rgb(49, 163, 84)'
        )
    )

trace1 = go.Scatter(
        x=x1,
        y=y1,
        name='26 - 50',
        text=text1,
        mode='markers',
        marker=dict(
            size=10,
            color='rgb(254, 217, 118)'
        )
    )

trace2 = go.Scatter(
            x=x2,
            y=y2,
            name='51 - 75',
            text=text2,
            mode='markers',
            marker=dict(
                size=10,
                color='rgb(254, 178, 76)'
            )
        )

trace3 = go.Scatter(
        x=x3,
        y=y3,
        name='76 - 125',
        text=text3,
        mode='markers',
        marker=dict(
            size=10,
            color='rgb(253, 141, 60)'
        )
    )

trace4 = go.Scatter(
        x=x4,
        y=y4,
        name='126 - 175',
        text=text4,
        mode='markers',
        marker=dict(
            size=10,
            color='rgb(240, 59, 32)'
        )
    )

trace5 = go.Scatter(
        x=x5,
        y=y5,
        name=' > 175',
        text=text5,
        mode='markers',
        marker=dict(
            size=10,
            color='rgb(189, 0, 38)'
        )
    )

layout = dict(
            title='Percentage of Conversations<br>with Deleted Tweets',
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

data = [trace0, trace1, trace2, trace3, trace4, trace5]

fig = dict(data=data, layout=layout)

plotly.offline.plot(fig, filename='Plotly/deletedPercentage.html', auto_open=True)
