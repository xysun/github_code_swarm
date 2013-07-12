'''
Generates code_swarm compatible xml files on GitHub commit history. 
Author: Xiayun Sun
Email: xiayun.sun@gmail.com
July, 2013
'''

import http.client, json, time, sys
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD

BASE_URL = 'api.github.com'

class GitAPIError(Exception):
    '''
    self.value is the GitHub response header
    '''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class GitHub:
    def __init__(self, earliest = '2000-01-01T00:00:00Z'):
        '''
        fname is the output xml file name
        earliest sets the time bound of earliest commits. 
        '''
        self.store = []
        self.earliest = self._convert_to_unix(earliest)
        self.auth_headers = {}
    
    def set_auth(self, token):
        '''
        set the auth token for GitHub
        You can obtain auth token from: https://github.com/settings/applications
            "Personal API Access Tokens"
        This will set the rate limit to 5000 hits/hour
        '''
        self.auth_headers = {"Authorization": "token " + token}
    
    def _convert_to_unix(self, t):
        '''
        convert t (string) returned by GitHub to unix timestamp
        '''
        t_struct = time.strptime(t, '%Y-%m-%dT%H:%M:%SZ')
        return int(1000 * time.mktime(t_struct))
    
    def check_rate_limit(self):
        '''
        check latest rate limit, using octocat
        '''
        url = '/users/octocat/orgs'
        conn = http.client.HTTPSConnection(BASE_URL)
        conn.request("GET", url, headers = self.auth_headers)
        struc = conn.getresponse().getheaders()
        return struc[5][1]
    
    def _api_request(self, handler, url):
        '''
        wrapper function
        '''
        conn = http.client.HTTPSConnection(BASE_URL)
        conn.request('GET', url, headers = self.auth_headers)
        response = conn.getresponse()
        if response.reason == 'OK':
            struc = json.loads(response.read().decode())
            return handler(struc)
            conn.close()
        else:
            conn.close()
            raise GitAPIError(response.getheaders())
    
    def get_repo(self, userID):
        '''
        return [repos], only source repos are included
        '''
        url = '/users/' + userID + '/repos?type=owner'
        return self._api_request(lambda x: [e['name'] for e in x if not e['fork']], url)
    
    def get_commits_history(self, userID, repo):
        '''
        return: [sha]
        '''
        url = '/repos/' + userID + '/' + repo + '/commits'
        handler = lambda struct: [c['sha'] for c in struct]
        return self._api_request(handler, url)


    def get_single_commit(self, userID, repo, sha, realname = ""):
        '''
        return [{date:, author:, filename:}]
        '''
        url = '/repos/' + userID + '/' + repo + '/commits/' + sha

        if realname == "":
            realname = userID

        def handler(struc):
            timestamp = struc['commit']['committer']['date']
            t = self._convert_to_unix(timestamp)
            res = []
            if t > self.earliest:
                res = [{"date":str(t), "author":realname, "filename":'/'+userID+'/'+repo+'/'+e['filename']} for e in struc['files']]
            return res

        return self._api_request(handler, url)

    def all_commits(self, userID, repo, realname = ""):
        '''
        return store + [(author, time, file)]
        '''
        if realname == "":
            realname = userID

        try:
            sha = self.get_commits_history(userID, repo)
            med = [self.get_single_commit(userID, repo, s, realname) for s in sha]
            self.store += [c for e in med for c in e]
        except GitAPIError as err:
            print("Git API Error, headers = ", err)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
            

    def single_user(self, userID, realname = ""):
        '''
        update self.store for [(author, time, file)]
        return remaining rate limits
        '''
        if realname == "":
            realname = userID

        repos = self.get_repo(userID)
        for repo in repos:
            self.all_commits(userID, repo, realname)

        rm_rate = self.check_rate_limit()
        print("remaining rate hits:", rm_rate)
        return int(rm_rate)

    def generate_xml(self, fname = "commits.xml"):
        '''
        takes g.store : [(author, time, filepath)]
        sort by time
        returns xml file compatible for code_swarm
        you can overwrite the output file name here
        '''
        sorted_store = sorted(self.store, key = lambda x: int(x['date']))
        root = ET.Element('file_events')
        for ele in sorted_store:
            ET.SubElement(root, "event", attrib = ele)
        p = MD.parseString(ET.tostring(root, encoding = "unicode"))
        f = open(fname, 'w')
        f.write(p.toprettyxml())
        f.close()
    
