import json

with open('users_src.json', 'r') as src, open('users.json', 'w') as dest:
    users_src = json.load(src)
    users = {
        person['Branch of Service']: person
        for person in users_src
    }
    json.dump(users, dest, indent=2)
    
