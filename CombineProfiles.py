import os
import shutil


def retrieve_account(filename):
    return filename[:filename.rfind('_')]


data_folder = ['data/AccountProfile/', 'data/OtherProfiles/']
account_profiles = os.listdir(data_folder[0])
account_other_profiles = os.listdir(data_folder[1])
profile = {}

for account in account_profiles:
    handle = retrieve_account(account)
    if handle in profile:
        profile[handle].append(account + '-0')
        profile[handle].sort(reverse=True)
    else:
        profile[handle] = [account + '-0']

for account in account_other_profiles:
    handle = retrieve_account(account)
    if handle in profile:
        profile[handle].append(account + '-1')
        profile[handle].sort(reverse=True)
    else:
        profile[handle] = [account + '-1']

count = 0
for account in profile:
    remove_tag = profile[account][0].split('-')
    location = data_folder[int(remove_tag[1])]
    filename = location + remove_tag[0]
    print('Copying {} ...'.format(filename))
    shutil.copy2(filename, 'data/AllProfiles/')
