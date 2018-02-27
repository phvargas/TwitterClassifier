from Conversation import Conversation
from twitter_apps.Subjects import get_values
import plotly.graph_objs as go
import plotly

# plotly.offline.init_notebook_mode(connected=True)

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

for current_handle in get_values():
    del_rows, all_handles = observed.handle_conversation_matrix(current_handle['handle'], my_suspended_deleted_list)
    all_rows = observed.handle_conversations_id(current_handle['handle'])
    print('{} deletion percentage: {}'.format(current_handle['name'], len(del_rows) / len(all_rows)))
