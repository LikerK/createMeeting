import requests

api_base_url = "https://api.zoom.us/v2"

# def get_content(data):
#     return {
#         "id": data["id"],
#         "meeting_url": data["join_url"],
#         "password": data["password"],
#         "meetingTime": data["start_time"],
#         "purpose": data["topic"],
#         "duration": data["duration"],
#         "message": "Success",
#         "status": 1
#         }


def get_data_meeting(id, header):
    resp = requests.get(f'{api_base_url}/meetings/{id}', headers=header)
    data = resp.json()
    return data


def create_meeting(topic, duration, start_date, start_time, header):
    payload = {
        "topic": topic,
        "duration": duration,
        'start_time': f'{start_date}T10:{start_time}',
        "type": 2
    }

    resp = requests.post(f"{api_base_url}/users/me/meetings",
                         headers=header,
                         json=payload)

    if resp.status_code != 201:
        print(resp)
        return None
    return resp.json()


# def delete_meeting(id):
#     requests.delete(f"{api_base_url}/meetings/{id}", headers=headers)
