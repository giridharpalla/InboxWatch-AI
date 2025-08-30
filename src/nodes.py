import os
import time

from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.search import GmailSearch

class Nodes():
	def __init__(self):
		self.gmail = GmailToolkit()

	def check_email(self, state):
		print("# Checking for new emails")
		search = GmailSearch(api_resource=self.gmail.api_resource)
		
		# Try multiple search strategies to ensure we get emails
		try:
			# First try: emails from last day
			emails = search.invoke('newer_than:1d')
			print(f"Found {len(emails)} emails with 'newer_than:1d' search")
		except Exception as e:
			print(f"Error with 'newer_than:1d' search: {e}")
			try:
				# Fallback: search for emails in inbox
				emails = search.invoke('in:inbox')
				print(f"Found {len(emails)} emails with 'in:inbox' search")
			except Exception as e2:
				print(f"Error with 'in:inbox' search: {e2}")
				# Last resort: get any emails
				emails = search.invoke('')
				print(f"Found {len(emails)} emails with empty search")
		
		checked_emails = state.get('checked_emails_ids', [])
		processed_threads = state.get('processed_thread_ids', [])
		thread = []
		new_emails = []
		
		print(f"My email from env: {os.environ.get('MY_EMAIL', 'NOT_SET')}")
		print(f"Already checked emails: {len(checked_emails)}")
		print(f"Already processed threads: {len(processed_threads)}")
		
		for email in emails:
			# Extract email address from sender (handle format "Name <email@domain.com>")
			sender_email = email['sender']
			if '<' in sender_email:
				# Extract email from "Name <email@domain.com>" format
				sender_email = sender_email.split('<')[1].split('>')[0]
			
			print(f"Processing email from: {sender_email}")
			print(f"Thread ID: {email['threadId']}")
			
			# Skip if: already checked, thread already processed, or email is from user
			if (email['id'] not in checked_emails) and (email['threadId'] not in thread) and (email['threadId'] not in processed_threads) and (sender_email != os.environ.get('MY_EMAIL', '')):
				thread.append(email['threadId'])
				new_emails.append(
					{
						"id": email['id'],
						"threadId": email['threadId'],
						"snippet": email['snippet'],
						"sender": email['sender'],
						"sender_email": sender_email  # Add clean email address
					}
				)
				print(f"Added email from {sender_email} to new_emails")
			else:
				print(f"Skipped email from {sender_email} (already processed or from self)")
		checked_emails.extend([email['id'] for email in emails])
		return {
			**state,
			"emails": new_emails,
			"checked_emails_ids": checked_emails,
			"processed_thread_ids": processed_threads  # Maintain the processed threads list
		}

	def wait_next_run(self, state):
		print("## Waiting for 180 seconds")
		time.sleep(30)
		return state

	def new_emails(self, state):
		if len(state.get('emails', [])) == 0:
			print("## No new emails")
			return "end"
		else:
			print("## New emails")
			return "continue"
