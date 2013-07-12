### Introduction
`github_code_swarm` is a small script to get GitHub commit history and generate [code_swarm](https://code.google.com/p/codeswarm/) compatible xml files.

The script is in Python 3.

### To start 
The main logic is implemented in the `GitHub` class in `github_code_swarm.py` file. `example.py` contains the complete interface and sample function calls.

To start, initialize a `GitHub` object:

```python
from github_code_swarm import *
g = GitHub()
```

You can also pass in an optional `earliest` parameter to set the time bound for earliest commits. For example:

```python
g = GitHub(earliest = '2010-01-01T00:00:00Z')
```

It is set to the year of 2000 by default.

### Interface

Below functions are available on the created object (refer to `example.py` for example calls):

- - -

```python
g.set_auth(auth_token)
```

Sets GitHub's authorization token on the object. It will raise the rate limit to 5000 hits/hour. You can obtain your own token [here](https://github.com/settings/applications) under "Personal API Access Tokens".

- - - 

```python
g.check_rate_limit()
```

Returns the remaining rate limits available.

- - - 

```python
g.get_repo(github_ID)
```

Returns a list of source repos from the user. Forked repos are excluded.

- - -

```python
sha = g.get_commits_history(github_ID, repo_name)
```

Returns a list of commit IDs and save it to variable `sha` for the specified repo. (`sha` is GitHub's name for commit ID in the response header) 

- - -

```python
g.get_single_commit(github_ID, repo, commit_ID, realname = "")
```

Returns a list of dictionary `{date, author, filename}` for a single commit. `commit_ID` can be obtained by previous calls to `get_commits_history`, optional realname can be passed to replace the `author` field in the generated xml file. It is set to github_ID by default.

- - -

```python
g.all_commits(github_ID, repo_name, realname = "")
```

Updates `g.store` with the complete commit history for the specified repo. `g.store` holds the commit history and is used to generate the final xml file later.

- - -

```python
g.single_user(github_ID, realname = "")
```

Updates `g.store` with the complete commit history for the specified user. Returns the remaining rate limit as a reminder. 

- - -

```python
g.generate_xml(file_name = "commits.xml")
```

Generates the `code_swarm` compatible xml file. You can replace the default file name.

Now you can use `code_swarm` to generate videos based on this xml file. 
