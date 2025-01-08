import json
import requests
import time

def categorize_email(email_content):
    """
    Utilise l'API de Mistral pour catégoriser un email avec logique de retry en cas d'erreur de taux limite.
    """
    prompt = f"Voici le contenu d'un email : '{email_content}'.\n\nCatégories possibles : Newsletter, Publicité, Personnel, Spam, Notifications, Réservations, Important, Poubelle.\n\nRetourne uniquement la catégorie appropriée, sans justification."

    
    # Mistral API endpoint
    mistral_api_url = "https://api.mistral.ai/v1/chat/completions"

    # Payload pour l'API Mistral
    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": "You are an email categorizer."},  # Contexte du modèle
            {"role": "user", "content": prompt}
        ]
    }

    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer [mistral API key]"  # Remplacez par votre clé API
    }
    
    try:
        time.sleep(2)
        # Envoyer la requête à l'API de Mistral
        response = requests.post(mistral_api_url, json=payload, headers=headers)

        # Vérifier la réponse
        if response.status_code == 200:
            result = response.json()
            print("Réponse de l'API Mistral :", result)
            # Extract the category
            category = result['choices'][0]['message']['content'].strip()
            print(f"Category = {category}")
            return category
        else:
            print(f"Erreur : {response.status_code}, {response.text}")
    
    except Exception as e:
        print(f"Erreur lors de la requête à l'API Mistral : {e}")
        

    # Si toutes les tentatives échouent
    print("Toutes les tentatives ont échoué. Email non catégorisé.")
    return "Non catégorisé"


# Fonction pour charger les emails depuis le fichier JSON et ajouter les labels
def categorize_emails_to_json(input_file="emails.json", output_file="emails_with_labels.json"):
    """
    Charge les emails depuis un fichier JSON, catégorise chaque email et sauvegarde les résultats dans un nouveau fichier JSON.
    """
    # Charger les emails existants depuis le fichier JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        emails = json.load(f)

    # Liste des catégories possibles
    categories_possibles = ["Newsletter", "Publicité", "Personnel", "Spam", "Notifications", "Réservations", "Important", "Poubelle"]

    # Catégoriser chaque email
    for email in emails:
        email_content = f"Objet : {email['subject']}, Extrait : {email['snippet'][:200]}"  # Prendre 200 premiers caractères du snippet
        predicted_category = categorize_email(email_content)

        # Ajouter la catégorie à l'email
        if predicted_category in categories_possibles:
            email['labels'] = [predicted_category]
        else:
            email['labels'] = ["Non catégorisé"]

    # Sauvegarder les résultats dans un nouveau fichier JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(emails, f, ensure_ascii=False, indent=4)
    
    print(f"Fichier mis à jour avec les labels : {output_file}")

# Appel de la fonction pour catégoriser les emails
if __name__ == '__main__':
    categorize_emails_to_json()
