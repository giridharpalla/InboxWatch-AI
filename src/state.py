import datetime
from typing import TypedDict

class EmailsState(TypedDict):
	checked_emails_ids: list[str]
	processed_thread_ids: list[str]  # Track threads that have been processed for drafts
	emails: list[dict]
	action_required_emails: dict