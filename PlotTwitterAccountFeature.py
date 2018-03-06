import pickle

with open('data/account_features.pkl', mode='rb') as fhd:
    obj = pickle.load(fhd)


for account in obj:
    print(account)
    for feature in obj[account]:
        print('\t{}: {}'.format(feature, obj[account][feature]))

print(len(obj))
