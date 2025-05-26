import requests
import json


def generate(id,prompt, token):
    url = "https://avapi.arvand-tech.net/api/agents/" +id+ "/generate"
    payload = json.dumps({
        "userPrompt": prompt
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer' + token

    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response
