import requests
import os
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


def filter_type_meeting(meeting):
    if meeting['type'] == 2:
        return True
    return False


def get_token():
    data = {
        "grant_type": "account_credentials",
        "account_id": account_id,
        "client_secret": client_secret
    }
    response = requests.post(auth_token_url,
                             auth=(client_id, client_secret),
                             data=data)
    if response.status_code != 200:
        return None
    response_data = response.json()
    access_token = response_data["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    return headers


def get_content(data):
    print(data)
    return {
        "id": data["id"],
        "meeting_url": data["join_url"],
        "password": data["password"],
        "meetingTime": data["start_time"],
        "purpose": data["topic"],
        "duration": data["duration"],
        "message": "Success",
        "status": 1
        }


def get_last_meeting():
    headers = get_token()
    resp = requests.get(f"{api_base_url}/users/me/meetings", headers=headers)
    data = resp.json()
    meetings = list(filter(filter_type_meeting, data['meetings']))
    print(meetings)
    if not meetings:
        return []
    last_metting = meetings[-1]
    id = last_metting['id']
    resp = requests.get(f"{api_base_url}/meetings/{id}", headers=headers)
    data = resp.json()
    print(get_content(data))
    return get_content(data)


def create_meeting(topic, duration, start_date, start_time):
    headers = get_token()
    payload = {
        "topic": topic,
        "duration": duration,
        'start_time': f'{start_date}T10:{start_time}',
        "type": 2
    }

    resp = requests.post(f"{api_base_url}/users/me/meetings",
                         headers=headers,
                         json=payload)

    if resp.status_code != 201:
        return None
    response_data = resp.json()

    return get_content(response_data)


def delete_meeting(id):
    headers = get_token()
    requests.delete(f"{api_base_url}/meetings/{id}", headers=headers)
