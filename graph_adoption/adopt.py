import json
import datetime
import random as r


class User:
    def __init__(self, name):
        self.name = name
        self.libs = {}
        self.repos = {}

    def implicit_view(self, repo_libs, repo, time):
        for lib in repo_libs:
            self.libs[lib] = time
        self.repos[repo] = time

    def use_lib(self, lib, repo_libs, time):
        self.libs[lib] = time

    def last_interaction(self, repo):
        if repo not in self.repos:
            return -1
        return self.repos[repo]


class Repo:
    def __init__(self, name):
        self.name = name
        self.libs = {}

    def use_lib(self, lib, time):
        self.libs[lib] = time

    def last_interaction(self, lib):
        return self.libs[lib]


users = {}
repos = {}


def process_commit(c):
    # resolve implicit pulls
    repo = c['repo']
    time = int(c['time'])
    if c['user'] == '':
        print(c)
        user = 0
    else:
        user = int(c['user'])

    added_libs = c['add_libs']
    deleted_libs = c['del_libs']

    # change deleted_libs so that "moved libs" i.e., libs that are added and deleted in the same commit
    # are not considered
    added_and_deleted = set(added_libs).intersection(set(deleted_libs))
    deleted_libs = [item for item in deleted_libs if item not in added_and_deleted]
    added_libs = [item for item in added_libs if item not in added_and_deleted]

    if repo not in repos:
        repos[repo] = Repo(repo)
    repo = repos[repo]

    if user not in users:
        users[user] = User(user)
    user = users[user]

    # updated_libs are those libraries that were implicitly viewed by the user via a pull (immediately) before a commit
    updated_libs = [lib for lib in repo.libs if repo.last_interaction(lib) > user.last_interaction(repo)]

    # If an added lib is in updated_lib but not in the user's quiver, then it must be an adoption.
    for lib in added_libs:
        if lib in updated_libs and lib not in user.libs:
            if r.random() > .9:
                print(user.name, 'adopts', lib, 'at:', datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))

    user.implicit_view(updated_libs, repo, time)

    # resolve updates
    for added_lib in added_libs:
        user.use_lib(added_lib, updated_libs, time)
        repo.use_lib(added_lib, time)


def stream(f):
    obj_str = ''
    # f.read(1) # eat first [
    f.seek(2531350053) # 2531350054 offset to start at 2015
    while True:
        c = f.read(1)
        if not c:
            print('EOF')
            break
        if c == '\n':
            continue
        if c == '\'':
            c = '"'
        obj_str = obj_str + c
        if c == '}':
            obj_str = obj_str.replace('u"', '"')
            yield json.loads(obj_str)
            obj_str = ''
            c = f.read(1) # eat comma


if __name__ == "__main__":
    f = open('../data/all_commits_SUB_sorted.json')
    commits = stream(f)
    for x in commits:
        process_commit(x)
    f.close()
