# Linkedin Dislike Bot
Modified [linkedin API python client](https://github.com/linkedin-developers/linkedin-api-python-client) to permit www requests and handle the resulting authentication *stuff*

# About
LinkedIn Dislike bot. Forward a post you dislike to the dislike bot. The dislike bot will comment on the post saying: "Use this as the dislike button."  

All this projects complexity comes from reversing engineering Linkedin's API.

# Usage
1. Create and activate a python virtual environment
```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

2. Install all dependencies
```bash
pip install -r requirements.txt
```

3. Create .env using the provided .env stub
Remember to rename the file to `.env`!

Acquiring variables: 
* ACCESS_TOKEN: 
* CSRF_TOKEN and LI_AT: Check your LinkedIn cookies for `JSESSIONID`, and `li_at`
* QUERY_ID and MAILBOX_URN: Check query string parameters for request made to `/voyager/api/voyagerMessagingGraphQL/graphql`
    * QUERY_ID has matches ERE pattern: `messengerConversations\..+`
    * MAILBOX_URN matches ERE pattern: `urn:li:fsd_profile:.+`

4. Run the program
```bash
python3.13 main.py
```

