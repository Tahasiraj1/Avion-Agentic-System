from dataclasses import dataclass
import requests
import os
import json

@dataclass
class SanityClient:
    sanity_api_token: str = os.getenv("SANITY_API_TOKEN")
    sanity_api_version: str = os.getenv("SANITY_API_VERSION")
    sanity_dataset: str = os.getenv("SANITY_DATASET")
    sanity_projet_id: str = os.getenv("SANITY_PROJECT_ID")
    sanity_base_url: str = f"https://{sanity_projet_id}.api.sanity.io/v{sanity_api_version}/data/query/{sanity_dataset}"


    def fetch_products(self):
        params = {'query': '*[_type == "product"]'}
        headers = {'Authorization': f'Bearer {self.sanity_api_token}'}

        response = requests.get(self.sanity_base_url, params=params, headers=headers)
        data = response.json()
        return data

    def get_product_by_id(self, product_id):
        params = {'query': f'*[_type == "product" && id == "{product_id}"]'}
        headers = {'Authorization': f'Bearer {self.sanity_api_token}'}

        response = requests.get(self.sanity_base_url, params=params, headers=headers)
        data = response.json()
        return data
    
if __name__ == "__main__":
    sanity_client = SanityClient()
    product1 = sanity_client.get_product_by_id(1)
    variations = product1['result'][0]['variations']
    product_data = json.dumps(product1, indent=4)
    print(product_data)