from src.graph import WorkFlow

app = WorkFlow().app
initial_state = {
    "checked_emails_ids": [],
    "emails": [],
    "action_required_emails": {}
}
app.invoke(initial_state)