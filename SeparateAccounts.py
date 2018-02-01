import re
import requests
from requests.auth import HTTPBasicAuth

"""
This Python program
  1. From a list of given Twitter accounts finds which are accounts are deleted, protected, or suspended
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Fri,  Jan 31, 2018 at 15:41:23'
__email__ = 'pvargas@cs.odu.edu'


deleted_accounts = []
protected = []
suspended = []
no_existence = []
open_account = []

url = 'https://twitter.com/'
user = 'FemalePHV'
pwd = 'h@r@$$ment'

regex_suspended = re.compile('<h1>Account suspended</h1>')
regex_protected = re.compile("This account's Tweets are protected.")

with open('deleted_accounts.txt', mode='r') as fh_deleted:
    for account in fh_deleted:
        deleted_accounts.append(account.strip())


requests.get(url, auth=HTTPBasicAuth(user, pwd))

counter = 0
for account in deleted_accounts:
    counter += 1

    r = requests.get(url + account)

    print(counter, account, '-->', r.status_code, '-->', r.reason, end=' ')
    if r.status_code == 404:
        no_existence.append(account)

    elif r.status_code == 200:
        if regex_suspended.findall(r.content.decode('utf-8')):
            print('--> Suspended ...', end=' ')
            suspended.append(account)

        elif regex_protected.findall(r.content.decode('utf-8')):
            print('--> Protected', end=' ')
            protected.append(account)

        else:
            print('--> Open account', end=' ')
            open_account.append(account)
    print()

print('suspended --> ', suspended)
print('no_existence --> ', no_existence)
print('protected --> ', protected)
print('Open-Acct -->', open_account)
