import json

with open('../data/all_import_commits_SUB.json') as f:
    data = json.load(f)
ordered_commits = sorted(data, key=lambda k: k['time'])
with open('../data/all_import_commits_SUB_sorted.json', 'w') as f:
    f.write(str(ordered_commits))
