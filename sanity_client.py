from dataclasses import dataclass
import requests
import os

@dataclass
class SanityClient:
    sanity_api_token: str = os.getenv("SANITY_API_TOKEN")
    sanity_api_version: str = os.getenv("SANITY_API_VERSION")
    sanity_dataset: str = os.getenv("SANITY_DATASET")
    sanity_project_id: str = os.getenv("SANITY_PROJECT_ID")


    sanity_base_url = f"https://{sanity_project_id}.api.sanity.io/v{sanity_api_version}/data"
    sanity_query_url = f"{sanity_base_url}/query/{sanity_dataset}"
    sanity_mutate_url = f"{sanity_base_url}/mutate/{sanity_dataset}"


    def fetch_products(self):
        params = {'query': '*[_type == "product"]'}
        headers = {'Authorization': f'Bearer {self.sanity_api_token}'}

        response = requests.get(self.sanity_query_url, params=params, headers=headers)
        data = response.json()
        return data

    def get_product_by_id(self, product_id):
        params = {'query': f'*[_type == "product" && id == "{product_id}"]'}
        headers = {'Authorization': f'Bearer {self.sanity_api_token}'}

        response = requests.get(self.sanity_query_url, params=params, headers=headers)
        data = response.json()
        return data
    
    def update_product_quantity(self, product_id, color, size, quantity):
            headers = {'Authorization': f'Bearer {self.sanity_api_token}'}
            product = self.get_product_by_id(product_id)

            if not product['result']:
                return "Product not found."
            
            # Get document _id
            document_id = product['result'][0]['_id']
            variations = product['result'][0]['variations']

            # Find correct variation
            updated_variations = []
            for v in variations:
                if v['color'] == color and v['size'] == size:
                    v['quantity'] += quantity
                updated_variations.append(v)

            # Build correct mutation payload
            patch_payload = {
                "mutations": [
                    {
                        "patch": {
                            "id": document_id,
                            "set": {
                                "variations": updated_variations
                            }
                        }
                    }
                ]
            }

            patch_response = requests.post(self.sanity_mutate_url, headers=headers, json=patch_payload)
            return patch_response.json()