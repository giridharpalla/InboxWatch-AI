from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.create_draft import GmailCreateDraft
from langchain_community.tools.gmail.get_thread import GmailGetThread
from langchain_tavily import TavilySearch
from crewai.tools import tool

@tool("Create Draft")
def create_draft(data: str) -> str:
    """
    Useful to create an email draft.
    The input to this tool should be a pipe (|) separated text
    of length 3 (three), representing who to send the email to,
    the subject of the email and the actual message.
    For example, `lorem@ipsum.com|Nice To Meet You|Hey it was great to meet you.`.
    """
    email, subject, message = data.split('|')
    gmail = GmailToolkit()
    draft = GmailCreateDraft(api_resource=gmail.api_resource)
    result = draft({
        'to': [email],
        'subject': subject,
        'message': message
    })
    return f"\nDraft created: {result}\n"

@tool("Get Gmail Thread")
def get_gmail_thread(thread_id: str) -> str:
    """
    Useful to get the content of a Gmail thread by its ID.
    The input should be a thread ID string.
    """
    gmail = GmailToolkit()
    get_thread = GmailGetThread(api_resource=gmail.api_resource)
    result = get_thread({"thread_id": thread_id})
    
    # Extract sender email from the thread for better context
    if isinstance(result, dict) and 'messages' in result:
        for message in result['messages']:
            if 'payload' in message and 'headers' in message['payload']:
                headers = message['payload']['headers']
                from_header = next((h['value'] for h in headers if h['name'] == 'From'), None)
                if from_header:
                    # Extract email from "Name <email@domain.com>" format
                    if '<' in from_header:
                        sender_email = from_header.split('<')[1].split('>')[0]
                        result['sender_email'] = sender_email
                    break
    
    return str(result)

@tool("Search Web")
def search_web(query: str) -> str:
    """
    Useful to search the web for information.
    The input should be a search query string.
    """
    search = TavilySearch()
    result = search.run(query)
    return result


