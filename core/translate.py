import requests
import os
from dotenv import load_dotenv

load_dotenv()
IAM_TOKEN = os.environ.get('IAM_TOKEN')
RESOURCE_MANAGER_API = \
        "https://resource-manager.api.cloud.yandex.net/resource-manager/v1"
TRANSLATE_API = "https://translate.api.cloud.yandex.net/translate/v2/translate"


def get_cloud():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    responce = requests.get(f"{RESOURCE_MANAGER_API}/clouds", headers=headers)

    return responce.json()["clouds"][0]["id"]


def get_folder(cloud_id=None):
    if cloud_id is None:
        cloud_id = get_cloud()

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }
    params = {
        'cloudId': cloud_id
    }

    responce = requests.get(
        f"{RESOURCE_MANAGER_API}/folders",
        headers=headers,
        params=params
    )

    return responce.json()["folders"][0]["id"]


def translate(texts, target_language='ru', folder_id=None):
    if folder_id is None:
        folder_id = get_folder()

    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    response = requests.post(
        TRANSLATE_API,
        json=body,
        headers=headers
    )

    return [t['text'] for t in response.json()['translations']]
