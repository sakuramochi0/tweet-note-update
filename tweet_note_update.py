#!/usr/bin/env python3
import sys
import json
import yaml
import requests
from twython import Twython

tweeted_file = 'tweeted.yaml'
user_names = ['staffwhy']

# prepare twitter object
with open('.credentials') as f:
    api_key, api_secret, token, token_secret = f.read().strip().split()

t = Twython(api_key, api_secret, token, token_secret)

# load already tweeted note ids
with open(tweeted_file) as f:
    tweeted = yaml.load(f)

# get user data
for user_name in user_names:
    # initiate tweeted
    if user_name not in tweeted:
        tweeted[user_name] = []
    
    # get notes data
    r = requests.get('https://note.mu/api/v1/notes?note_intro_only=true&urlname=' + user_name)
    notes = json.loads(r.text)['data']['notes']

    for note in notes:
        # if duplicate
        if note['key'] in tweeted[user_name]:
            break
        
        if note['name']:
            note_name = note['name']
        else:
            note_name = '"{}"'.format(note['body'].split()[0])
        text = '｜'.join([note_name, note['user']['nickname'], 'note（ノート）'])
        tweet_text = '{text}- https://note.mu/{user_urlname}/n/{key}'.format(text=text, user_urlname=note['user']['urlname'], key=note['key'])
        print(note['key'])
        print(tweet_text)
        res = t.update_status(status=tweet_text)
        if res:
            tweeted[user_name].append(note['key'])
            with open(tweeted_file, 'w') as f:
                yaml.dump(tweeted, f, allow_unicode=True, default_flow_style=False)
