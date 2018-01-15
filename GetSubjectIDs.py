from twitter_apps.Subjects import get_values
from twitter_apps.TwitterFunctions import TwitterObject

all_handles = []
for account in get_values():
    print(account['handle'])
    all_handles.append(account['handle'])

my_api = TwitterObject()

user_ids = my_api.api.lookup_users(screen_names=all_handles[:100])

for user in user_ids:
    print(user.screen_name, user.id)

user_ids = my_api.api.lookup_users(screen_names=all_handles[100:])

print()
print(all_handles[99:105])
print()

for user in user_ids:
    print(user.screen_name, user.id)
