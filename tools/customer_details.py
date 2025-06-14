from agents import function_tool, RunContextWrapper
from dataclasses import dataclass
from MongoDB.customer_details import CustomerDetails

@dataclass
class UserContext:
    timestamp: str
    userId: str = None

@function_tool
async def fetch_customer_details(wrapper: RunContextWrapper[UserContext]) -> str:
    """Fetches customer details from MongoDB using user_id.
    
    Args:
        wrapper (RunContextWrapper[UserContext]): Context containing userId and timestamp.

    Returns:
        str: A message indicating the customer details.
    """
    try:
        get_customer_details = CustomerDetails()
        customer_details = get_customer_details.get_customer_details(wrapper.context.userId)
        if not customer_details:
            return "No customer details found."
        return f"Customer Details: {customer_details[0]}"
    except Exception as e:
        return f"Error fetching customer details: {e}"
