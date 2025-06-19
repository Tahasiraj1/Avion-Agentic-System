from agents import function_tool, RunContextWrapper
from MongoDB import Order
from models import UserContext
from typing import List

@function_tool
async def fetch_orders(wrapper: RunContextWrapper[UserContext]) -> List[str]:
    """Fetches customer orders from MongoDB using user_id.
    
    Args:
        wrapper (RunContextWrapper[UserContext]): Context containing userId and timestamp.

    Returns:
        list: A list of orders.
    """
    try:
        orders_list = []

        get_orders = Order()

        orders = await get_orders.get_orders(wrapper.context.userId)
        for ord in orders:
            orders_list.append(ord)
        
        if not orders_list:
            return "No orders found."
        return orders_list
    except Exception as e:
        return f"Error fetching orders: {e}"
