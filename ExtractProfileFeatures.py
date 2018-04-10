from Conversation import Conversation
from bs4 import BeautifulSoup
from time import strftime
import re
import os
import gzip
import glob

"""
ExtractProfileFeatures.py: given a path where all Twitter accounts profile are stored, the script opens the files in 
                           the folder and inspect their content for further analysis. Some of the features that maybe
                           extracted are the account creation date, number of tweets,  number of followers, etc.
                           The followers and friends for each specific account will be recorded in a different script.
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Mar 28, 2017 at 09:13'
__email__ = 'pvargas@cs.odu.edu'

#profile_path = '/data/harassment/AccountProfile/'
profile_path = 'data/AccountProfile/'
regex = re.compile('.*\.gz$')
local_date = strftime("%Y%m%d")

error_filename = profile_path + 'error_' + local_date + '.log'
feature_filename = profile_path + 'features_' + local_date + '.csv'
month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
         'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

print('\nUploading conversations ...')
#observed = Conversation('/data/harassment/verifiedUserDataset/tweetConvo.dat')
observed = Conversation('data/verifiedUserDataset/Conversation_20180407a.dat')
print('Sorting UserNames interacting in conversations ...')
nosey_handles = sorted(observed.all_conversation_elements_set())
print('Found {:,} unique actors ...'.format(len(nosey_handles)))

print('\nReading Twitter account profile from given path: {}'.format(profile_path))
profile_filenames = os.listdir(profile_path)
profile_filenames = sorted([m.group(0) for l in profile_filenames for m in [regex.search(l)] if m])

print('Found {:,} profiles ...'.format(len(profile_filenames)))

"""
print('\nMatching profiles ...')
profile_dict = {}
profile_count = 0

for save_file in profile_filenames:
    # find where to split filename to obtain handle. Filename format handle_date.html.gz
    idx = save_file.rfind('_')
    handle = save_file[:idx]
    suffix = save_file[idx + 1:idx + 8]

    if handle in nosey_handles:
        profile_count += 1
        if profile_count % 5000 == 0:
            print('{:,} matches ...'.format(profile_count))
        if handle in profile_dict:
            profile_dict[handle].append(suffix)
        else:
            profile_dict[handle] = [suffix]

print('Number of matching profiles: {:,}'.format(len(profile_dict)))
print(nosey_handles[:20])
"""

f_error = open(error_filename, mode='w')
f_feature = open(feature_filename, mode='w')

for counter, filename in enumerate(profile_filenames):

    account = filename[:filename.rfind('_')]
    if account in nosey_handles:
        nosey_handles.remove(account)
        print('Removed {}'.format(account))

        with gzip.open(profile_path + filename, 'rb') as f:
            file_content = f.read()

        idx = filename.rfind('_')
        handle = filename[:idx]
        creation_date = ''
        feature_count = [0, 0, 0, None, None, None]

        soup = BeautifulSoup(file_content, 'html.parser')
        # find joining date
        for html_class in soup.findAll("span", {'class': 'ProfileHeaderCard-joinDateText'}):
            value = html_class.get('title').split(' ')

            if len(value[3]) == 1:
                value[3] = '0' + value[3]
            creation_date = value[5] + month[value[4]] + value[3] + value[0] + value[1]

        if not creation_date:
            f_error.write('{} has no creation date.\n'.format(handle))

        # find number of tweets
        for p_count, html_class in enumerate(soup.findAll("span", {'class': 'ProfileNav-value'})):
            if p_count + 1 > len(feature_count):
                feature_count.append(html_class.get('data-count'))
            else:
                feature_count[p_count] = html_class.get('data-count')

        tweets = feature_count[0]
        followers = feature_count[1]
        likes = feature_count[2]

        if not tweets:
            f_error.write('{} has zero tweets.\n'.format(handle))

        if not followers:
            f_error.write('{} has no followers.\n'.format(handle))

        f_feature.write('{},{},{},{},{}\n'.format(handle, creation_date, tweets, followers, likes))
        print(counter, handle, creation_date, tweets, followers, likes)
    else:
        print('Could not find account: {}'.format(account))

f_error.close()
f_feature.close()
