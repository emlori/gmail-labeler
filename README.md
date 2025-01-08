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

***Installation***
1. Clone this repository:

```bash
git clone https://github.com/yourusername/gmail-email-labeler.git
cd gmail-email-labeler
```
2. Install dependencies:

```bash
pip install -r requirements.txt
Place your credentials.json in the config/ directory.
```

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
Modify the unwanted_labels list in the script to specify the labels you want to exclude. Example:

```python
unwanted_labels = ["Newsletter", "Publicité", "Personnel", "Spam", "Notifications", "Réservations", "Important", "Poubelle"]
```

**Output**
The script will fetch emails that lack labels and utilize the LLM to categorize and label them intelligently.

**File Structure**
gmail-email-sorter/
├── config/
│   ├── credentials.json  # Google API credentials file
│   ├── token.json        # Generated after authentication
├── main.py                 # Main script for fetching and labeling emails
├── modules/
│   ├── gmail_authentication.py  # Gmail API authentication script
│   ├── apply_label_to_email
categorize_emails
│   ├── delete_emails_from_category
│   ├── delete_emails_from_label
│   ├── fetch_emails
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation

**Limitations**
* Requires manual setup of Google Cloud Project and Gmail API credentials.
Gmail API rate limits may apply for high-volume requests.
* The LLM's accuracy depends on the quality of the model used.

**Contributing**
Contributions are welcome! Feel free to submit a pull request or open an issue.

Fork the repository.
1. Create your feature branch (git checkout -b feature-name).
2. Commit your changes (git commit -m 'Add some feature').
3. Push to the branch (git push origin feature-name).
4. Open a pull request.