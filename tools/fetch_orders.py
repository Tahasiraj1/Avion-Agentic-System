from agents import function_tool, RunContextWrapper
from dataclasses import dataclass
from MongoDB.orders import Order
from models.user_context import UserContext

@function_tool
async def fetch_orders(wrapper: RunContextWrapper[UserContext]) -> str:
    """Fetches customer orders from MongoDB using user_id."""
    try:
        orders_list = []

        get_orders = Order()

        orders = get_orders.get_orders(wrapper.context.userId)
        for ord in orders:
            orders_list.append(ord)
        
        if not orders_list:
            return "No orders found."
        return f"Orders: {orders_list}\n"
    except Exception as e:
        return f"Error fetching orders.: {e}"
