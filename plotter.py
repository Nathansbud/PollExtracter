from parser import polls, Poll
from textwrap import wrap
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import defaultdict

for poll in polls:
    fig, ax = plt.subplots()

    responses = [pr for pr in polls[poll].responses if pr['response'] is not None]
    users = {}
    for r in responses:
        r['response'] = r['response'].replace("â\x80\x99", "'").replace("â\x80\x9c", '"').replace("â\x80\x9d", '"')

        if not r['actor'] in users:
            users[r['actor']] = {
                'votes':[]
            }
        if r['type'] == Poll.Action.VOTED:
            users[r['actor']]['votes'].append(r['response'])
        elif r['type'] == Poll.Action.REMOVED:
            users[r['actor']]['votes'].remove(r['response'])
        elif r['type'] == Poll.Action.CHANGED:
            if users[r['actor']]['votes']: users[r['actor']]['votes'].pop(0)
            users[r['actor']]['votes'].append(r['response'])

    votes = []
    for u in users:
        votes += users[u]['votes']

    frequency = defaultdict(int)
    for r in votes:
        frequency[r] += 1

    y_pos = np.arange(len(frequency.keys()))

    title = ax.set_title("\n".join(wrap(polls[poll].name, 60)))
    plt.bar(y_pos, frequency.values())
    plt.xticks(y_pos, frequency.keys())
    loc, labels = plt.xticks()
    plt.setp(labels, rotation=45)
    plt.yticks(np.arange(0, 10))
    fig.tight_layout()
    plt.show()
    fig.savefig(f'{os.path.join(os.path.dirname(__file__), "graphs", poll)}.png')

if __name__ == '__main__':
    pass

