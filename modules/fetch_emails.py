import json
from modules.gmail_authentification import authenticate_gmail


def get_unlabeled_emails(service, unwanted_labels, max_results=2000):
    """
    Récupère les emails qui ne contiennent aucun des labels indésirables.

    Args:
        service: Objet de service Gmail authentifié.
        unwanted_labels: Liste des labels à exclure (e.g., ['Newsletter', 'Spam']).
        max_results: Nombre maximum d'emails à récupérer.

    Returns:
        Liste de dictionnaires contenant l'ID, le sujet, le snippet et un indicateur sur la présence de labels indésirables.
    """
    emails = []
    next_page_token = None

    while len(emails) < max_results:
        try:
            # Récupérer les messages avec pagination
            response = service.users().messages().list(
                userId='me',
                maxResults=min(100, max_results - len(emails)),
                pageToken=next_page_token
            ).execute()

            messages = response.get('messages', [])
            if not messages:
                break

            # Parcourir les messages
            for message in messages:
                email_id = message['id']

                # Récupérer les détails du message
                msg = service.users().messages().get(userId='me', id=email_id).execute()

                # Vérifier les labels associés
                labels = msg.get('labelIds', [])
                has_unwanted_label = any(label in labels for label in unwanted_labels)

                # Si le mail ne contient aucun label indésirable
                if not has_unwanted_label:
                    payload = msg.get('payload', {})
                    headers = payload.get('headers', [])
                    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
                    snippet = msg.get('snippet', 'No Snippet')

                    emails.append({
                        'id': email_id,
                        'subject': subject,
                        'snippet': snippet,
                        'labels': labels  # Ajout des labels existants pour référence
                    })

            # Gérer la pagination
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        except Exception as e:
            print(f"Erreur lors de la récupération des emails : {e}")
            break

    return emails


def save_to_json(data, file_name="emails.json"):
    """
    Saves data to a JSON file.
    
    Args:
        data: Data to be saved.
        file_name: Name of the JSON file.
    """
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"Data saved to {file_name}")
    
    

if __name__ == '__main__':
    max_results = 10
    service = authenticate_gmail()
    emails = get_unlabeled_emails(service, max_results)
    
    print(f"Nombre d'e-mails récupérés : {len(emails)}")
    
    # Save emails to a JSON file
    save_to_json(emails)

    # Optional: Print emails for verification
    for email in emails:
        subject = email['subject']
        snippet = email['snippet'][:100]
        print(f"ID : {email['id']}")
        print(f"Objet : {subject}")
        print(f"Contenu : {snippet}\n")
