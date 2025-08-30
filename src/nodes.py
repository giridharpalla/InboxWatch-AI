import os
import time

from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.search import GmailSearch

class Nodes():
	"""Node class for handling email operations and workflow control."""
	
	def __init__(self):
		"""Initialize the Nodes class with Gmail toolkit."""
		self.gmail = GmailToolkit()

	def check_email(self, state):
		"""Check for new emails and filter them based on specific criteria.
		
		Args:
			state: Current state containing checked email IDs
			
		Returns:
			Updated state with new emails and updated checked email IDs
		"""
		print("# Checking for new emails")
		
		# Search for emails from the last day
		search = GmailSearch(api_resource=self.gmail.api_resource)
		emails = search('after:newer_than:1d')
		
		# Get list of previously checked email IDs to avoid duplicates
		checked_emails = state['checked_emails_ids'] if state['checked_emails_ids'] else []
		
		# Track thread IDs to avoid processing multiple emails from same conversation
		thread = []
		new_emails = []
		
		# Process each email and apply filtering criteria
		for email in emails:
			# Filter emails based on three conditions:
			# 1. email['id'] not in checked_emails: Skip emails we've already processed
			# 2. email['threadId'] not in thread: to ensure that we are completely looking at the new thread
			# 3. os.environ['MY_EMAIL'] not in email['sender']: Skip emails sent by myself
			if (email['id'] not in checked_emails) and (email['threadId'] not in thread) and ( os.environ['MY_EMAIL'] not in email['sender']):
				# Add thread ID to prevent processing other emails from same conversation
				thread.append(email['threadId'])
				
				# Add filtered email to new emails list
				new_emails.append(
					{
						"id": email['id'],
						"threadId": email['threadId'],
						"snippet": email['snippet'],
						"sender": email["sender"]
					}
				)
		
		# Mark all retrieved emails as checked to avoid reprocessing
		checked_emails.extend([email['id'] for email in emails])
		
		return {
			**state,
			"emails": new_emails,
			"checked_emails_ids": checked_emails
		}

	def wait_next_run(self, state):
		"""Wait for a specified duration before next email check.
		
		Args:
			state: Current state (passed through unchanged)
			
		Returns:
			Unmodified state after waiting period
		"""
		print("## Waiting for 180 seconds")
		# Sleep for 3 minutes before next email check cycle
		time.sleep(180)
		return state

	def new_emails(self, state):
		"""Check if there are new emails and determine next workflow step.
		
		Args:
			state: Current state containing emails list
			
		Returns:
			'end' if no new emails found, 'continue' if new emails exist
		"""
		# Check if any new emails were found in the current check
		if len(state['emails']) == 0:
			print("## No new emails")
			# No new emails found, end the current workflow cycle
			return "end"
		else:
			print("## New emails")
			# New emails found, continue to next step in workflow
			return "continue"

