import jira
import json

class JiraApi:
    def __init__(self):
        self.client = jira.JIRA(
            server='https://robocon2024.atlassian.net',
            # set email and api token
            basic_auth=('email', '...')
        )
    
    def get_projects(self):
        return self.client.projects()
    
    def get_issues(self, query):
        return self.client.search_issues(query)
    
    def create_issue(self, issue_dict):
        return self.client.create_issue(fields=issue_dict)
    
    def add_comment(self, issue, comment):
        return self.client.add_comment(issue, comment)
    

# jira = JiraApi()
# projects = jira.get_projects()
# print(projects)

# jira.add_comment('TOM-1', 'This is a comment from David!')
# #exit()

# issue_dict = {
#     'project': {'key': 'TOM'},
#     'summary': 'New issue from jira-python',
#     'description': 'Look into this one',
#     'issuetype': {'name': 'Story'}, # Epic / Story / Task / Bug
#     'parent': {'key': 'TOM-31'}
# }
# jira.create_issue(issue_dict)

# issues = jira.get_issues('project = TOM and reporter = currentUser()')
# print(issues)
# for issue in issues:
#     print(issue.key)

# # python3 -m venv .venv
# # .venv/bin/pip3 install jira