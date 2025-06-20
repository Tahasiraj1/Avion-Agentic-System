from models import UpdateCustomerDetails, UserContext
from agents import function_tool, RunContextWrapper
from MongoDB import CustomerDetails

@function_tool
async def update_customer_details(
    wrapper: RunContextWrapper[UserContext], 
    customer_details: UpdateCustomerDetails,
    user_query: str
    ) -> str:
    """Updates customer details in MongoDB.
    Only updates fields explicitly provided in the query. Ignores unprovided fields.

    Args:
        wrapper (RunContextWrapper[UserContext]): Context containing userId and timestamp.
        customer_details (UpdateCustomerDetails): Fields to update in customer details, some of which may remain same.
        user_query (str): The user's query, from which the customer details fields to update will be extracted.

    Returns:
        str: A message indicating the update status.
    """
    try:
        customer = CustomerDetails()
        result = await customer.update_customer_details(wrapper.context.userId, customer_details)
        return result
    except Exception as e:
        return f"Error updating customer details: {e}"