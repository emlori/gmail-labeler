# Gmail Email Labeler

A Python script to fetch emails from Gmail and apply labels intelligently using LLM.

- Authenticate securely with Gmail API.
- Fetch emails that have not been labeled yet.
- Automatically label emails using a Local Language Model (LLM).
- Pagination for handling large volumes of emails.

## Prerequisites

Before running the script, ensure you have the following:

1. **Python**: Version 3.7 or later.
2. **Gmail API credentials**:
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the Gmail API for the project.
   - Download the `credentials.json` file and place it in the `config/` directory.

3. **Dependencies**: Install the required Python packages:
   ```bash
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

4. **Token Storage:**
A token.json file will be generated automatically after the first successful authentication.

**Installation**
1. Clone this repository:

```bash
git clone https://github.com/emlori/gmail-labeler.git
cd gmail-labeler
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```
Place your credentials.json in a config/ directory.

3. Place your credentials.json in the config/ directory.

**Usage**
1. Authenticate Gmail API
Run the following command to authenticate:

```bash
python gmail_authentication.py
```
On the first run, a browser window will open asking for Gmail permissions. Once authenticated, a token.json file will be created.

2. Fetch and Label Emails
Run the main script to fetch emails without specific labels:

```bash
python main.py
```
**Customizing Label Exclusions**
Modify the unwanted_labels list in the script to specify the emails that you don't want to label again. Example:

```python
unwanted_labels = ["Newsletter", "Publicité", "Personnel", "Spam", "Notifications", "Réservations", "Important", "Poubelle"]
```

**Output**
The script will fetch emails that lack labels and utilize the LLM to categorize and label them intelligently.

**File Structure**
```bash
gmail-labeler/
├── config/
│   ├── credentials.json  # Google API credentials file
│   ├── token.json        # Generated after authentication
├── main.py                 # Main script for fetching and labeling emails
├── modules/
│   ├── gmail_authentication.py  # Gmail API authentication script
│   ├── apply_label_to_email.py
│   ├── categorize_emails.py
│   ├── delete_emails_from_category.py
│   ├── delete_emails_from_label.py
│   ├── fetch_emails.py
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```

**Contributing**
Contributions are welcome! Feel free to submit a pull request or open an issue.

Fork the repository.
1. Create your feature branch (git checkout -b feature-name).
2. Commit your changes (git commit -m 'Add some feature').
3. Push to the branch (git push origin feature-name).
4. Open a pull request.