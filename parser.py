import json
from string import punctuation
from enum import Enum, auto
import re
import os.path

folder = os.path.join(os.path.dirname(__file__), "data")
file_objects = []

for f in os.listdir(folder):
    if not f == '.gitkeep' and not f == '.DS_Store':
        with open(os.path.join(os.path.dirname(__file__), "data", f)) as jf:
            file_objects.append(json.load(jf))

created_string = "created a poll: "

voted_for  = 'voted for "'
removed_for = 'removed vote for "'
changed_for = 'changed vote to "'
in_the_poll = '" in the poll: '

behavior_strings = [voted_for, removed_for, changed_for]

class Poll:
    class Action(Enum):
        CREATED = auto()
        VOTED = auto()
        CHANGED = auto()
        REMOVED = auto()

    def __init__(self, name, creator, timestamp):
        self.name = name
        self.responses = []
        self.creator = creator
        self.timestamp = timestamp

polls = {}

matched_messages = []

for m in file_objects[0]['messages']:
    if 'content' in m:
        if (any(n in m['content'] for n in behavior_strings) and in_the_poll in m['content']) or created_string in m['content']:
            matched_messages.append(m)

for m in matched_messages.__reversed__():
    actor = m['sender_name']
    if created_string in m['content']:
        poll_name = m['content'][m['content'].find(created_string) + len(created_string):].rstrip(punctuation)
        if not poll_name in polls:
            polls[poll_name] = Poll(poll_name, m['sender_name'], m['timestamp_ms'])
            polls[poll_name].responses.append({
                'response':None,
                'actor':actor,
                'type':Poll.Action.CREATED
            })
    else:
        poll_name = m['content'][m['content'].find(in_the_poll) + len(in_the_poll):].rstrip(punctuation)
        if changed_for in m['content']:
            match_obj = (re.search(f'{changed_for}(.*?){in_the_poll}', m['content']))
            if poll_name in polls:
                polls[poll_name].responses.append({
                    'response':m['content'][match_obj.start() + len(changed_for):match_obj.end() - len(in_the_poll)],
                    'actor':actor,
                    'type':Poll.Action.CHANGED
                })
        elif voted_for in m['content']:
            match_obj = (re.search(f'{voted_for}(.*?){in_the_poll}', m['content']))
            if poll_name in polls:
                polls[poll_name].responses.append({
                    'response': m['content'][match_obj.start() + len(voted_for):match_obj.end() - len(in_the_poll)],
                    'actor': actor,
                    'type': Poll.Action.VOTED
                })
        elif removed_for in m['content']:
            match_obj = (re.search(f'{removed_for}(.*?){in_the_poll}', m['content']))
            if poll_name in polls:
                polls[poll_name].responses.append({
                    'response': m['content'][match_obj.start() + len(removed_for):match_obj.end() - len(in_the_poll)],
                    'actor': actor,
                    'type': Poll.Action.REMOVED
                })

if __name__ == '__main__':
    pass
