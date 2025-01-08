from modules.fetch_emails import get_unlabeled_emails, save_to_json
from modules.gmail_authentification import authenticate_gmail
from modules.categorize_emails import categorize_emails_to_json
from modules.delete_emails_from_label import delete_emails_by_label
import json
import os
from googleapiclient.discovery import build


def get_existing_labels(service):
    """Retrieve all existing labels in Gmail."""
    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return {label['name']: label['id'] for label in labels}
    except Exception as e:
        print(f"Error fetching existing labels: {e}")
        return {}


def create_label(service, label_name):
    """Create a new label in Gmail."""
    label_object = {
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show',
        'name': label_name
    }
    try:
        label = service.users().labels().create(userId='me', body=label_object).execute()
        return label['id']
    except Exception as e:
        print(f"Error creating label '{label_name}': {e}")
        return None


def apply_label_to_email(service, email_id, label_id):
    """Apply a label to an email."""
    try:
        msg = service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'addLabelIds': [label_id]}
        ).execute()
        print(f"Label {label_id} applied to email {email_id}. Response: {msg}")
    except Exception as e:
        print(f"Failed to apply label '{label_id}' to email {email_id}: {e}")


def categorize_emails_from_json(input_file="emails_with_labels.json"):
    """
    Load emails from the JSON file, categorize them, and apply labels in Gmail.
    """
    # Authenticate Gmail
    service = authenticate_gmail()

    # Load emails and their categories from JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        emails = json.load(f)

    print("Loaded emails from JSON:")
    for email in emails:
        print(email)

    # Fetch existing labels
    category_labels = get_existing_labels(service)
    #print("Existing Labels Mapping:", category_labels)

    # Create missing labels and update the mapping
    for email in emails:
        labels = email.get('labels', [])
        if labels:
            category = labels[0]
            if category not in category_labels:
                category_id = create_label(service, category)
                if category_id:
                    category_labels[category] = category_id
                    print(f"Label '{category}' created with ID: {category_id}")
                else:
                    print(f"Failed to create label '{category}'.")

    print("Final Category Labels Mapping:", category_labels)

    # Apply labels to Gmail emails
    for email in emails:
        email_id = email['id']
        labels = email.get('labels', [])
        if labels:
            label = labels[0]
            label_id = category_labels.get(label)
            if label_id:
                apply_label_to_email(service, email_id, label_id)
            else:
                print(f"Label ID for '{label}' not found. Skipping email {email_id}.")
        else:
            print(f"Email {email_id} has no labels. Skipping.")




if __name__ == '__main__':
    # max numbers of emails to process
    max_results = 2
    # Authentification to your Gmail account with Gmail API
    service = authenticate_gmail()
    # Get emails
    emails = get_unlabeled_emails(service, max_results)
    # Save emails to a JSON file
    save_to_json(emails)
    # label emails with LLM (mistral API)
    categorize_emails_to_json()
    # label emails into your gmail account with emails ID
    categorize_emails_from_json()
    # Delete emails labelled "Poubelle"
    delete_emails_by_label("Poubelle")
