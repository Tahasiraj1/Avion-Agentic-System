from agents import function_tool, RunContextWrapper
from MongoDB.customer_details import CustomerDetails
from models.customer_details import UpdateCustomerDetails
from models.user_context import UserContext


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
        customer_details (UpdateCustomerDetails): The customer details to update.
        user_query (str): The user's query, from which the customer details fields to update will be extracted.

    Returns:
        str: A message indicating the update status.
    """
    try:
        customer = CustomerDetails()
        result = customer.update_customer_details(wrapper.context.userId, customer_details)
        return result
    except Exception as e:
        return f"Error updating customer details: {e}"