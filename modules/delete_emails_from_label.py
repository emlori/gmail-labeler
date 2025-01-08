from modules.gmail_authentification import authenticate_gmail
from googleapiclient.errors import HttpError


def get_emails_by_label(service, label_name):
    """
    Retrieve all emails with a specific label.
    """
    try:
        # Search for messages with the given label
        response = service.users().messages().list(userId='me', labelIds=[label_name]).execute()
        messages = response.get('messages', [])
        print(f"Found {len(messages)} emails with label '{label_name}'.")
        return messages
    except HttpError as error:
        print(f"An error occurred while fetching emails with label '{label_name}': {error}")
        return []


def delete_email(service, email_id):
    """
    Delete an email by ID.
    """
    try:
        service.users().messages().delete(userId='me', id=email_id).execute()
        print(f"Email with ID {email_id} deleted successfully.")
    except HttpError as error:
        print(f"An error occurred while deleting email {email_id}: {error}")


def delete_emails_by_label(label_name):
    """
    Authenticate Gmail, find emails with the given label, and delete them.
    """
    # Authenticate Gmail
    service = authenticate_gmail()

    # Retrieve all Gmail labels to find the label ID
    try:
        labels_response = service.users().labels().list(userId='me').execute()
        labels = {label['name']: label['id'] for label in labels_response.get('labels', [])}

        # Check if the label exists
        label_id = labels.get(label_name)
        if not label_id:
            print(f"Label '{label_name}' not found.")
            return

        # Fetch and delete emails with the given label
        emails = get_emails_by_label(service, label_id)
        for email in emails:
            delete_email(service, email['id'])

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    # Replace "Réseaux sociaux" with the label you want to delete emails from
    delete_emails_by_label("Poubelle")
