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
* CSRF_TOKEN and LI_AT: Check your LinkedIn cookies for `JSESSIONID`, and `li_at`
* ACCESS_TOKEN: (Optional. Used only for calling get_user_info)
1. Create or use an existing developer application from the LinkedIn Developer Portal
2. Request access to the Sign In With LinkedIn API product. This is a self-serve product that will be provisioned immediately to your application.
3. Generate a 3-legged access token using the Developer Portal token generator tool, selecting the r_liteprofile scope.

4. Run the program
```bash
python3.13 main.py
```

# Debugging
## Redirected more than 30 times exception
Your LI_AT variable has expired

## CSRF error
Get the new CSRF_TOKEN