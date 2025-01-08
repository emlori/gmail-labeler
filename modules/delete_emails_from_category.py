from modules.gmail_authentification import authenticate_gmail
from googleapiclient.errors import HttpError


def delete_emails_by_category(category):
    """Delete all emails from a specific category."""
    try:
        service = authenticate_gmail()
        # Modify query to include 'in:anywhere' for archived emails
        query = f"category:{category} in:anywhere"
        response = service.users().messages().list(userId='me', q=query).execute()

        # Process all emails across pages
        while 'messages' in response:
            for message in response['messages']:
                try:
                    # Delete the email
                    service.users().messages().delete(userId='me', id=message['id']).execute()
                    print(f"Email with ID {message['id']} deleted.")
                except HttpError as error:
                    print(f"Failed to delete email with ID {message['id']}. Error: {error}")
            
            # If there are more pages of emails, get the next page
            if 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
            else:
                break  # No more pages, exit the loop
        else:
            print(f"No emails found in category: {category}")
    except HttpError as error:
        print(f"Failed to list emails in category {category}. Error: {error}")


if __name__ == "__main__":
    # Delete emails from "Réseaux sociaux" category
    delete_emails_by_category(category="social")
