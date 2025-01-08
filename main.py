from modules.gmail_authentification import authenticate_gmail
from modules.fetch_emails import get_unlabeled_emails, save_to_json
from modules.categorize_emails import categorize_emails_to_json 
from modules.apply_label_to_email import categorize_emails_from_json
from modules.delete_emails_from_category import delete_emails_by_category
from modules.delete_emails_from_label import delete_emails_by_label

def main():
    # Étape 1 : Authentification
    service = authenticate_gmail()
    
    # Liste des labels
    labels = ["Newsletter", "Publicité", "Personnel", "Spam", "Notifications", 
                           "Réservations", "Important", "Poubelle"]
    
    # Étape 2 : Récupérer les emails
    print("Fetching emails...")
    emails = get_unlabeled_emails(service, labels, max_results=4)
    save_to_json(emails, file_name="data/emails.json")
    
    # Étape 3 : Labellisation des emails
    print("Categorizing emails...")
    categorize_emails_to_json(input_file="data/emails.json", output_file="data/emails_with_labels.json")
    
    # Étape 4 : label emails into your gmail account with emails ID
    categorize_emails_from_json(input_file="data/emails_with_labels.json")
    
    # Étape 5 : Suppression des emails
    print("Deleting emails from 'Poubelle' label...")
    delete_emails_by_label("Poubelle")
    
if __name__ == "__main__":
    main()
