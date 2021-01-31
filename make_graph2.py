import glob

subreddits_users = {}
for file in glob.glob('accounts/*'):
    account = file.split('/')[-1]
    for line in open(file):
        line = line.strip()
        if line:
            if line not in subreddits_users:
                subreddits_users['r/'+line] = []
            subreddits_users['r/'+line].append('u/'+account)

for file in glob.glob('subreddits/*'):
    subreddit = file.split('/')[-1]
    if subreddit not in subreddits_users:
        subreddits_users['r/'+subreddit] = []
    for line in open(file):
        line = line.strip()
        if line:
            subreddits_users['r/'+subreddit].append('u/'+line)


subreddits_users = {sub: set(users) for sub, users in subreddits_users.items()}

subreddit2subreddit = {}

import tqdm

for subreddit, users in tqdm.tqdm(list(subreddits_users.items())):
    for subreddit2, users2 in subreddits_users.items():
        if subreddit == subreddit2:
            continue
        count = len(users & users2)
        if count > 4:
            print(subreddit,',',subreddit2, sep='')
