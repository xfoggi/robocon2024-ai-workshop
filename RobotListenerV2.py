import os.path
import tempfile
import json
from robot.api import logger
from openai import OpenAI
from robot.libraries.BuiltIn import BuiltIn
import time

from jira_api import JiraApi

class RobotListenerV2:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, file_name='listen.txt'):
        path = os.path.join("", file_name)
        print('Listener file: %s' % path)
        self.file = open(path, 'w')
        self.client = OpenAI(
            # set api key for ChatGPT from OpenAI API
            api_key="..."
        )
        self.kwd_list = []
        self.jira = JiraApi()
    
    def query_gpt(self, system, message):
        completion = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": message}
            ]
        )
        return completion.choices[0].message.content

    def start_suite(self, name, attrs):
        #self.file.write("%s '%s'\n" % (name, attrs['doc']))
        self.file.write("start_suite" + json.dumps(attrs, indent=4, sort_keys=True) + '\n')
        #logger.warn("start_suite" + json.dumps(attrs, indent=4, sort_keys=True) + '\n')
        

    def start_test(self, name, attrs):
        #tags = ' '.join(attrs['tags'])
        #self.file.write("- %s '%s' [ %s ] :: " % (name, attrs['doc'], tags))
        self.file.write("start_test" + json.dumps(attrs, indent=4, sort_keys=True) + '\n')
        logger.info("start_test" + json.dumps(attrs, indent=4, sort_keys=True) + '\n', html=True)

    def end_test(self, name, attrs):
        self.file.write("end_test" + json.dumps(attrs, indent=4, sort_keys=True) + '\n')
        if attrs['status'] == 'PASS':
            self.file.write('PASS\n')
        else:
            self.file.write('FAIL: %s\n' % attrs['message'])
            #input('FAIL: Press Enter to continue...')
            #result = self.query_gpt(
            #    "Robot Framework test execution, validate the errors and write it in human readable form.",
            #    "Test: " +name+ ", Documentation: " +attrs['doc'] + "keywords: " + json.dumps(self.kwd_list) + ", Error message: " +attrs['message'])
            
            self.create_assistant()
            #self.assistant = self.client.beta.assistants.retrieve("asst_WDLWHmXEIAyWETSsNLL8efaY")

            #from robot.libraries.BuiltIn import BuiltIn
            seleniumlib = BuiltIn().get_library_instance('SeleniumLibrary')
            source = seleniumlib.get_source()

            #browserlib = BuiltIn().get_library_instance('Browser')
            #source = browserlib.get_page_source()
            
            htmlFile = open("failed.html", 'w')
            htmlFile.write(source)

            existing_issue = self.jira.get_issues('project = TOM and reporter = currentUser() and summary ~ "'+attrs['longname'] + '"')
            chat_gpt_message = ""
            if len(existing_issue) > 0:
                chat_gpt_message = "I found an existing issue in Jira. Please check the issue description and check if its the same issue. Write in Jira format for comment. Description" +  existing_issue[0].fields.description
            else:
                chat_gpt_message = "Check the Failed keyword message and find the correct xpath in HTML file. Write the output in JIRA format."

            message = self.create_message(
                chat_gpt_message + 
                "TEST DETAILS: Test: " +name+ ", Documentation: " +attrs['doc'] + "keywords: " + json.dumps(self.kwd_list) + ", Error message: " +attrs['message'],
                "failed.html"
            )

            messages = self.send_message_and_wait(message)            

            result = ""
            if messages is not None:
                for message in reversed(list(messages)):
                    if message.role == 'assistant':
                        print("Answer:")
                        print(message.content[0].text.value)
                        result = message.content[0].text.value + "\n"
                logger.warn(result)
            else:
                result = "Failed to get response from GPT assistant."
                
            if len(existing_issue) == 0:
                issue_dict = {
                    'project': {'key': 'TOM'},
                    'summary': attrs['longname'],
                    'description': result,
                    'issuetype': {'name': 'Bug'}
                }
                self.jira.create_issue(issue_dict)
            else:
                self.jira.add_comment(existing_issue[0].key, result)

        self.kwd_list = []

    def end_suite(self, name, attrs):
         #self.file.write('%s\n%s\n' % (attrs['status'], attrs['message']))
        self.file.write("end_suite" + json.dumps(attrs, indent=4, sort_keys=True) + '\n')

    def start_keyword(self, name, attrs):
        self.file.write("start_keyword" + json.dumps(attrs, indent=4, sort_keys=True) + '\n')
        #self.kwd_list.append(attrs['kwname'] + " args: " + attrs['args'])
    
    def end_keyword(self, name, attrs):
        self.file.write("end_keyword" + json.dumps(attrs, indent=4, sort_keys=True) + '\n')
        self.kwd_list.append(attrs['kwname'] + " args: " + ",".join(attrs['args']) + " status: " + attrs['status'])

    def close(self):
         self.file.close()

    def create_assistant(self):
        self.assistant = self.client.beta.assistants.create(
            name="Xpath expert - David",
            instructions="You are xpath expert and based on provided HTML file, you search for the element and provide the xpath. Use the best practices for writing xpaths, prioritize id, name, class, tag, link text, partial link text, css selector and xpath. Do not write absolute xpaths.",
            tools=[{"type": "retrieval"}],
            model="gpt-4-turbo-preview"
        )
        print(self.assistant.id)

    def create_message(self, message, filePath):
        thread = self.client.beta.threads.create()

        file = self.client.files.create(
            file=open(filePath, "rb"),
            purpose='assistants'
        )

        msg = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message,
            file_ids=[file.id]
        )

        return msg
    
    def send_message_and_wait(self, message):
        run = self.client.beta.threads.runs.create(
            thread_id=message.thread_id,
            assistant_id=self.assistant.id,
            instructions="Please address the user as David the QA."
        )

        run = self.get_run_status(message.thread_id, run.id)
        while run.status != "completed":
            if run.status == "failed":
                return None
            run = self.get_run_status(message.thread_id, run.id)      
            time.sleep(1)
        
        messages = self.client.beta.threads.messages.list(
            thread_id=message.thread_id
        )
        return messages

    def get_run_status(self, thread_id, run_id):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        print(run.status)
        return run