from agents import function_tool
from sanity_client import SanityClient

@function_tool
async def get_products():
    """Fetches products from Sanity.io.
    
    Returns:
        list: A list of products.
    """
    sanity_client = SanityClient()
    products = await sanity_client.fetch_products()
    return products