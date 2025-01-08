import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Constantes
CONFIG_FOLDER = 'config'
CREDENTIALS_FILE = os.path.join(CONFIG_FOLDER, 'credentials.json')
TOKEN_FILE = os.path.join(CONFIG_FOLDER, 'token.json')
SCOPES = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels',
]


def load_credentials():
    """
    Charge les informations d'authentification depuis un fichier JSON ou initie une nouvelle authentification.

    Returns:
        Credentials: Les informations d'authentification valides.
    """
    creds = None
    # Vérifie si le token existe déjà
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Rafraîchit ou génère de nouvelles informations d'authentification si nécessaires
    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    raise FileNotFoundError(f"Fichier '{CREDENTIALS_FILE}' introuvable.")
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            # Assure que le dossier config existe avant de sauvegarder le token
            os.makedirs(CONFIG_FOLDER, exist_ok=True)
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'authentification : {e}")
    return creds


def authenticate_gmail():
    """
    Authentifie l'utilisateur auprès de l'API Gmail et retourne un service Gmail.

    Returns:
        Resource: Objet de service Gmail authentifié.
    """
    try:
        creds = load_credentials()
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        raise RuntimeError(f"Erreur lors de la création du service Gmail : {error}")


if __name__ == '__main__':
    try:
        gmail_service = authenticate_gmail()
        print("Authentification réussie ! Le service Gmail est prêt à être utilisé.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
