'''
Example of using github_code_swarm
'''

from github_code_swarm import *

# create a new GitHub object, using default earliet time bound (2000)
g = GitHub()

# setting auth token
# replace the token string by your own
# you can generate your own token at: https://github.com/settings/applications Personal API Access Tokens
g.set_auth('9ddacef67b6723d1ccf00022f791aab2e91c0084')

# check rate limits
g.check_rate_limit()

# get a list of repos for one user
g.get_repo("Drennuz")

# get a list of commit IDs for one repo and save it to variable 'sha'
sha = g.get_commits_history("Drennuz", "regex")

# get a list of {date, author, filename} for one single commit, replace author by real name
# sha is a commit ID that can be obtained from get_commits_history
g.get_single_commit("Drennuz", "regex",sha[0], realname = "Xiayun Sun")

# get all commits history for one REPO and store it in g.store
g.all_commits("Drennuz", "regex", realname = "Xiayun Sun")

# get all commits history for one USER and store it in g.store
g.single_user("Drennuz",realname = "Xiayun Sun")

# generate code_swarm xml file from g.store, overwrite the default output file name
g.generate_xml("commit_Drennuz.xml")

'''
Now you can generate code_swarm videos from the xml file
Detailed instruction about code_swarm can be found here:
https://code.google.com/p/codeswarm/
'''
