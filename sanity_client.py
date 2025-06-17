from dataclasses import dataclass
import requests
import os

@dataclass
class SanityClient:
    sanity_api_token: str = os.getenv("SANITY_API_TOKEN")
    sanity_api_version: str = os.getenv("SANITY_API_VERSION")
    sanity_dataset: str = os.getenv("SANITY_DATASET")
    sanity_project_id: str = os.getenv("SANITY_PROJECT_ID")

    @property
    def sanity_base_url(self):
        return f"https://{self.sanity_project_id}.api.sanity.io/v{self.sanity_api_version}/data"

    @property
    def sanity_query_url(self):
        return f"{self.sanity_base_url}/query/{self.sanity_dataset}"

    @property
    def sanity_mutate_url(self):
        return f"{self.sanity_base_url}/mutate/{self.sanity_dataset}"

    @property
    def headers(self):
        return {'Authorization': f'Bearer {self.sanity_api_token}'}
    
    async def _post(self, url, headers, payload):
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    async def _get(self, url, params, headers):
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    async def fetch_products(self):
        params = {'query': '*[_type == "product"]'}
        return await self._get(self.sanity_query_url, params=params, headers=self.headers)

    async def get_product_by_id(self, product_id):
        params = {'query': f'*[_type == "product" && id == "{product_id}"]'}
        return await self._get(self.sanity_query_url, params=params, headers=self.headers)
    
    async def update_product_quantity(self, product_id, color, size, quantity):
        product = await self.get_product_by_id(product_id)

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

        response = await self._post(self.sanity_mutate_url, headers=self.headers, payload=patch_payload)
        return response
    
    async def adjust_variation_quantity(self, product_id, color, size, delta_quantity):
        """
        Adjusts the quantity of a specific variation by delta_quantity (can be positive or negative).
        """
        try:
            product = await self.get_product_by_id(product_id)
            if not product['result']:
                return "Product not found."

            document_id = product['result'][0]['_id']
            variations = product['result'][0]['variations']

            matching_variation = next(
                (v for v in variations if v['color'] == color and v['size'] == size), None
            )
            if not matching_variation:
                return f"Variation with color '{color}' and size '{size}' not found."

            # Adjust quantity safely
            new_quantity = matching_variation['quantity'] + delta_quantity
            if new_quantity < 0:
                return "Quantity cannot go below zero."

            matching_variation['quantity'] = new_quantity

            updated_variations = [matching_variation if v['_key'] == matching_variation['_key'] else v for v in variations]

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

            response = await self._post(self.sanity_mutate_url, headers=self.headers, payload=patch_payload)
            return response

        except Exception as e:
            return f"Error adjusting quantity: {e}"
