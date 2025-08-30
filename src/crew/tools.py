from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.create_draft import GmailCreateDraft
from langchain_community.tools.gmail.get_thread import GmailGetThread
from crewai.tools import BaseTool

class CreateDraftTool(BaseTool):
    name: str = "Create Draft"
    description: str = """Useful to create an email draft.
      The input to this tool should be a pipe (|) separated text
      of length 3 (three), representing who to send the email to,
      the subject of the email and the actual message.
      For example, `lorem@ipsum.com|Nice To Meet You|Hey it was great to meet you.`."""

    def _run(self, data: str) -> str:
        email, subject, message = data.split('|')
        gmail = GmailToolkit()
        draft = GmailCreateDraft(api_resource=gmail.api_resource)
        result = draft({
            'to': [email],
            'subject': subject,
            'message': message
        })
        return f"\nDraft created: {result}\n"

class GmailTool(BaseTool):
    name: str = "Get Email Thread"
    description: str = """Useful to get email thread details by thread ID.
    The input should be a thread ID string."""

    def _run(self, thread_id: str) -> str:
        gmail = GmailToolkit()
        get_thread = GmailGetThread(api_resource=gmail.api_resource)
        result = get_thread.run(thread_id)
        return result
