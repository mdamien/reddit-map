import glob, random
import os.path
import requests

subreddits = set()
for file in glob.glob('accounts/*'):
    for line in open(file):
        line = line.strip()
        if line:
            subreddits.add(line)

print('subreddits:', len(subreddits))

accounts = set()
for file in glob.glob('subreddits/*'):
    for line in open(file):
        line = line.strip()
        if line:
            accounts.add(line)

print('accounts:', len(accounts))

if True:
    while True:
        account = random.choice(list(accounts))
        print(account)
        account_file = 'accounts/'+account
        if os.path.exists(account_file):
            print(' - already done')
            continue
        account_subreddits = set()
        with open(account_file, 'w') as file:
            after = None
            while True:
                url = f"https://www.reddit.com/user/{account}/comments/.json"
                if after:
                    url += f'?after={after}'
                print(url)
                data = requests.get(url, headers={'User-agent': 'reddit map'}).json()['data']
                for post in data['children']:
                    post = post['data']
                    if post['subreddit'] not in account_subreddits:
                        account_subreddits.add(post['subreddit'])
                        file.write(post['subreddit']+'\n')
                after = data['after']
                if not after:
                    break

while True:
    subreddit = random.choice(list(subreddits))
    print(subreddit)
    subreddit_file = 'subreddits/'+subreddit
    if os.path.exists(subreddit_file):
        print(' - already done')
        continue
    subreddit_accounts = set()
    with open(subreddit_file, 'w') as file:
        after = None
        while True:
            url = f"https://www.reddit.com/r/{subreddit}/comments/.json"
            if after:
                url += f'?after={after}'
            print(url)
            data = requests.get(url, headers={'User-agent': 'reddit map'}).json()['data']
            for post in data['children']:
                post = post['data']
                if post['author'] not in subreddit_accounts:
                    subreddit_accounts.add(post['author'])
                    file.write(post['author']+'\n')
            after = data['after']
            if not after:
                break