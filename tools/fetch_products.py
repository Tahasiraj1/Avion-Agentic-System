from agents import function_tool
from dotenv import load_dotenv
import requests
import os

load_dotenv()

SANITY_API_TOKEN = os.getenv("SANITY_API_TOKEN")
SANITY_API_VERSION = os.getenv("SANITY_API_VERSION")
SANITY_DATASET = os.getenv("SANITY_DATASET")
SANITY_PROJECT_ID = os.getenv("SANITY_PROJECT_ID")

@function_tool
async def get_products():
    query = '*[_type == "product"]'

    url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/query/{SANITY_DATASET}"
    params = {'query': query}
    headers = {'Authorization': f'Bearer {SANITY_API_TOKEN}'}

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    return data