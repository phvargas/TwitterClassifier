import re
import os
import plotly.graph_objs as go
import plotly

plotly.offline.init_notebook_mode(connected=True)

path = 'data'

dir_list = os.listdir(path)

regex_all = re.compile('^all_interacting_mementos_\d{3}.*')
regex_del = re.compile('^deleted_interacting_mementos_\d{3}.*')

regex_non = re.compile('^non_deleted_interacting_mementos_\d{3}.*')

regex_zero = re.compile(',0')

all_files = [m.group(0) for l in dir_list for m in [regex_all.search(l)] if m]
del_files = [m.group(0) for l in dir_list for m in [regex_del.search(l)] if m]
non_files = [m.group(0) for l in dir_list for m in [regex_non.search(l)] if m]

all_count = []
del_count = []
non_count = []

for read_file in all_files:
    with open(path + '/' + read_file, mode='r') as fs:
        counter = 0
        for size, line in enumerate(fs):
            zero = regex_zero.search(line)
            if zero:
                counter += 1
    all_count.append(size - counter + 1)

for read_file in del_files:
    with open(path + '/' + read_file, mode='r') as fs:
        counter = 0
        for size, line in enumerate(fs):
            zero = regex_zero.search(line)
            if zero:
                counter += 1
    del_count.append(size - counter + 1)

for read_file in non_files:
    with open(path + '/' + read_file, mode='r') as fs:
        counter = 0
        for size, line in enumerate(fs):
            zero = regex_zero.search(line)
            if zero:
                counter += 1
    non_count.append(size - counter + 1)

print(all_files)
print(sorted(all_count))
print(del_files)
print(sorted(del_count))
print(non_files)
print(sorted(non_count))


trace0 = go.Box(
        y=sorted(all_count),
        boxmean=True,
        name='All',
)

trace1 = go.Box(
        y=sorted(non_count),
        boxmean=True,
        name='Active',
)

trace2 = go.Box(
        y=sorted(del_count),
        boxmean=True,
        name='Deleted',
)

layout = go.Layout(
            title='Randomly Selected Twitter Accounts<br>with Mementos Across Web Archives',
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            yaxis=dict(
                title='Number of Twitter Account with Mementos',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            )
        )

data = [trace0, trace1, trace2]

fig = go.Figure(data=data, layout=layout)

#plotly.offline.plot(fig, filename='Plotly/AllArchivedMementos.html', auto_open=True)

"""
                 Twitter Accounts with more than one (1) interaction 
"""

regex_all = re.compile('^all_interacting_mementos_gt1.*')
regex_del = re.compile('^deleted_interacting_mementos_gt1.*')
regex_non = re.compile('^non_deleted_interacting_mementos_gt1.*')

regex_zero = re.compile(',0')

all_files = [m.group(0) for l in dir_list for m in [regex_all.search(l)] if m]
del_files = [m.group(0) for l in dir_list for m in [regex_del.search(l)] if m]
non_files = [m.group(0) for l in dir_list for m in [regex_non.search(l)] if m]

all_count = []
del_count = []
non_count = []

for read_file in all_files:
    with open(path + '/' + read_file, mode='r') as fs:
        counter = 0
        for size, line in enumerate(fs):
            zero = regex_zero.search(line)
            if zero:
                counter += 1
    all_count.append(size - counter + 1)

for read_file in del_files:
    with open(path + '/' + read_file, mode='r') as fs:
        counter = 0
        for size, line in enumerate(fs):
            zero = regex_zero.search(line)
            if zero:
                counter += 1
    del_count.append(size - counter + 1)

for read_file in non_files:
    with open(path + '/' + read_file, mode='r') as fs:
        counter = 0
        for size, line in enumerate(fs):
            zero = regex_zero.search(line)
            if zero:
                counter += 1
    non_count.append(size - counter + 1)

print(all_files)
print(sorted(all_count))
print(del_files)
print(sorted(del_count))
print(non_files)
print(sorted(non_count))

trace0 = go.Box(
        y=sorted(all_count),
        boxmean=True,
        name='All',
)

trace1 = go.Box(
        y=sorted(non_count),
        boxmean=True,
        name='Active',
)

trace2 = go.Box(
        y=sorted(del_count),
        boxmean=True,
        name='Deleted',
)

layout = go.Layout(
            title='Randomly Selected Twitter Accounts<br>with More Than one Observed Account Interaction<br>' +
                  'with Mementos Across All Web Archives',
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            yaxis=dict(
                title='Number of Twitter Account with Mementos',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            )
        )

data = [trace0, trace1, trace2]

fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig, filename='Plotly/AllArchivedMementosGreaterThanOne.html', auto_open=True)

"""
                 Twitter Accounts with one (1) interaction 
"""

regex_all = re.compile('^all_interacting_mementos_eq1.*')
regex_del = re.compile('^deleted_interacting_mementos_eq1.*')
regex_non = re.compile('^non_deleted_interacting_mementos_eq1.*')

regex_zero = re.compile(',0')

all_files = [m.group(0) for l in dir_list for m in [regex_all.search(l)] if m]
del_files = [m.group(0) for l in dir_list for m in [regex_del.search(l)] if m]
non_files = [m.group(0) for l in dir_list for m in [regex_non.search(l)] if m]

all_count = []
del_count = []
non_count = []

for read_file in all_files:
    with open(path + '/' + read_file, mode='r') as fs:
        counter = 0
        for size, line in enumerate(fs):
            zero = regex_zero.search(line)
            if zero:
                counter += 1
    all_count.append(size - counter + 1)

for read_file in del_files:
    with open(path + '/' + read_file, mode='r') as fs:
        counter = 0
        for size, line in enumerate(fs):
            zero = regex_zero.search(line)
            if zero:
                counter += 1
    del_count.append(size - counter + 1)

for read_file in non_files:
    with open(path + '/' + read_file, mode='r') as fs:
        counter = 0
        for size, line in enumerate(fs):
            zero = regex_zero.search(line)
            if zero:
                counter += 1
    non_count.append(size - counter + 1)

print(all_files)
print(sorted(all_count))
print(del_files)
print(sorted(del_count))
print(non_files)
print(sorted(non_count))

trace0 = go.Box(
        y=sorted(all_count),
        boxmean=True,
        name='All',
)

trace1 = go.Box(
        y=sorted(non_count),
        boxmean=True,
        name='Active',
)

trace2 = go.Box(
        y=sorted(del_count),
        boxmean=True,
        name='Deleted',
)

layout = go.Layout(
            title='Randomly Selected Twitter Accounts<br>with One Observed Account Interaction<br>' +
                  'with Mementos Across All Web Archives',
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            yaxis=dict(
                title='Number of Twitter Account with Mementos',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#7f7f7f'
                )
            )
        )

data = [trace0, trace1, trace2]

fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig, filename='Plotly/AllArchivedMementosEqualToOne.html', auto_open=True)
