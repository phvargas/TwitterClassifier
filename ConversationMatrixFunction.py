import numpy as np
from Conversation import Conversation
from twitter_apps.Subjects import get_values
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly

observed = Conversation('/data/harassment/verifiedUserDataset/tweetConvo.dat')

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

for record in get_values(handle='tuckercarlson'):
    print(record)
    current_handle = record
    print(current_handle)

    for idx in observed.handle_conversations_id(current_handle['handle']):
        print(idx, observed.common_elements_list(current_handle['handle'], idx, my_suspended_deleted_list))
    print()

    conversation_id = []
    handle_set = set()

    total = 0
    for idx in observed.handle_conversations_id(current_handle['handle']):
        conversation_row = {idx: observed.common_elements_list(current_handle['handle'], idx, my_suspended_deleted_list),
                            'id': idx,
                            'count': {},
                            'total': 0}
        for handle in conversation_row[idx]:
            conversation_row['total'] += 1
            total += 1

            if handle in conversation_row['count']:
                conversation_row['count'][handle] += 1
            else:
                conversation_row['count'][handle] = 1

            handle_set.add(handle)

        conversation_id.append(conversation_row)
        print(conversation_row)
        print()
    print(total)

    print(' ' * 20, end='')
    for handle in handle_set:
        print(handle, end=' - ')
    print()

    col_total = np.zeros(len(handle_set), dtype=int)
    for row in conversation_id:
        print(row['id'], end=' -')

        k = 0
        for handle in handle_set:
            if handle in row[row['id']]:
                print(' {}'.format(row['count'][handle]), end='  - ')
                col_total[k] += row['count'][handle]
            else:
                print(' 0', end='  - ')

            k += 1

        print(row['total'])
    print(col_total)

    all_rows, all_keys = observed.handle_conversation_matrix(current_handle['handle'], my_suspended_deleted_list)
    z = []
    y = list(range(1, len(all_rows) + 1))
    x = list(range(1, len(handle_set) + 1))

    for row in all_rows:
        z_row = []
        key = list(row.keys())[0]
        print(key, end=' -')
        for handle in handle_set:
            if handle in row[key]:
                print(row[key][handle], end=' ')
                z_row.append(row[key][handle])
            else:
                print(' 0 -', end='')
                z_row.append(0)
        print()
        z.append(z_row)

    for key in all_keys:
        print(key, all_keys[key])

    for key, handle in zip(all_rows, handle_set):
        print(list(key)[0], handle)

    # Display element name and atomic mass on hover
    hover = list(range(len(all_rows)))
    symbol = list(range(len(all_rows)))

    for k, conversation in zip(range(len(all_rows)), all_rows):
        print(conversation)
        hover[k] = ['Handle: ' + handle + '<br>' + 'Conversation: ' +
                    list(conversation)[0] + '<br>Tweets: ' + str(z[k][i]) for i, handle in zip(range(len(handle_set)), handle_set)]
        symbol[k] = [' ' for i in range(len(handle_set))]
        print(len(symbol[k]), symbol[k])
        print(hover[k])

    print('Number of people in conversation:', len(handle_set))
    print('Number of conversations:', len(all_rows))

    if len(handle_set):
        print(current_handle['name'])
        trace = go.Heatmap(z=z,
                           x=x,
                           y=y, colorscale="Viridis")

        layout = go.Layout(
            title=current_handle['name'],
            xaxis=dict(
                title='Conversation Handles',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Conversation IDX',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )

        # Invert Matrices
        # hover = hover[::-1]

        print(len(z), len(symbol))

        data = [trace]
        fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=symbol, text=hover, hoverinfo='text',
                                          colorscale="Viridis", showscale=True)

        fig.layout.title = 'Deleted Accounts in ' + current_handle['name'] + ' Conversations'
        fig.layout.xaxis = dict(title='Conversation Handles',
                                titlefont=dict(
                                    family='Courier New, monospace',
                                    size=18,
                                    color='#7f7f7f'
                                ))

        fig.layout.yaxis = dict(title='Conversation IDX',
                                titlefont=dict(
                                    family='Courier New, monospace',
                                    size=18,
                                    color='#7f7f7f'
                                ))

        plotly.offline.plot(fig, filename='Plotly/' + current_handle['handle'] + '.html', auto_open=False)
