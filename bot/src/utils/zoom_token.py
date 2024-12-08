import base64
import requests
import os
import time
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# replace with your client ID
client_id = os.getenv('CLIENT_ID')

# replace with your account ID
account_id = os.getenv('ACCOUNT_ID')

# replace with your client secret
client_secret = os.getenv('CLIENT_SECRET')

auth_token_url = "https://zoom.us/oauth/token"
api_base_url = "https://api.zoom.us/v2"

cached_token = None
token_expiration = None

def get_token(bot):
    cached_token = bot.cached_token
    token_expiration = bot.token_expiration
    #  Check if the token is cached and not expired
    if cached_token and token_expiration and token_expiration > time.time():
        return {
            'access_token': cached_token,
            'expires_in': token_expiration - time.time(),
            'header_config': {
                'Authorization': f'Bearer {cached_token}',
                'Content-Type': 'application/json'
            },
            'error': None
        }
    try:
        # Create the authorization header
        encoded_auth = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
        headers = {
            'Authorization': f'Basic {encoded_auth}'
        }
        # Prepare the data for the POST request
        data = {
            'grant_type': 'account_credentials',
            'account_id': account_id
        }
        # Make the POST request
        response = requests.post(auth_token_url, data=data, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Parse the JSON response
        result = response.json()
        access_token = result.get('access_token')
        expires_in = result.get('expires_in')

        # Update the cached token and expiration
        cached_token = access_token
        token_expiration = time.time() + expires_in

        header_config = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
        return {
            'access_token': access_token, 
            'expires_in': expires_in,
            'header_config': header_config, 
            'error': None}
    except requests.RequestException as error:
        return {
            'access_token': None, 
            'expires_in': None, 
            'error': str(error)}
