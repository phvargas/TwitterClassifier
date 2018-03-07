import pickle
import plotly.graph_objs as go
import numpy as np
import plotly
from twitter_apps.Subjects import get_values

plotly.offline.init_notebook_mode(connected=True)

with open('data/account_features.pkl', mode='rb') as fhd:
    obj = pickle.load(fhd)

x = list(range(1, len(obj) + 1))
y = []
text = []
values = []

for account in obj:
    subject = get_values(handle=account)[0]

    print(subject['name'])
    print('User-name: {}, Number of appearances across conversations: {}, Ave. appearances across conversations: {}'.
          format(account, obj[account]['appearance-across-conversation-count'],
                 obj[account]['ave-handle-appearance-across-conversation']))

    values.append((obj[account]['appearance-across-conversation-count'], subject['name']))

    #for feature in obj[account]:
    #    print('\t{}: {}'.format(feature, obj[account]['ave-handle-appearance-across-conversation']))

print(len(obj))

for y_value, name in sorted(values, reverse=True):
    y.append(y_value)
    text.append(name)

global_average = np.average(y)


trace = go.Scatter(
        x=x,
        y=sorted(y, reverse=True),
        name='Max Count',
        text=text,
        mode='markers',
        marker=dict(
            size=10,
            color='rgb(49, 163, 84)'
        )
)

trace0 = go.Scatter(
        x=[min(x), max(x)],
        y=[global_average, global_average],
        name='Global Average',
        text=['Global Average'],
        mode='line',
        marker=dict(
            size=10,
            color='rgb(255, 163, 84)'
        )
)

layout = dict(
            title='User-name Count Across Conversation<br>Features of Observed Twitter Accounts',
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            xaxis=dict(
                title='Name of Twitter Accounts',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='User-name Count Across Conversations',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            )
        )

data = [trace, trace0]

fig = dict(data=data, layout=layout)

plotly.offline.plot(fig, filename='Plotly/UserNameCountFeature.html', auto_open=True)