from agents import function_tool, RunContextWrapper
from MongoDB.orders import Order
from MongoDB.order_item import OrderItem
from bson import ObjectId
from rapidfuzz import fuzz
from models.user_context import UserContext

# Threshold based fuzzy match
def is_match(user_input: str, product_name: str, threshold: int = 75) -> bool:
    score = fuzz.ratio(user_input.lower(), product_name.lower())
    return score >= threshold

@function_tool
def cancel_order(ctx: RunContextWrapper[UserContext], product_name: str, user_query: str) -> str:
    """Cancels an order.

    Args:
        name (str): The name of ordered product to cancel.
        user_query (str): The user's query, from which the name will be extracted.
        ctx (RunContextWrapper[UserContext]): The context object containing the user ID, and timestamp.

    Returns:
        str: A message indicating that the order has been cancelled.
    """

    try:
        # Fetch order items and orders for this user
        order_item_handler = OrderItem()
        order_handler = Order()
        
        order_items = order_item_handler.get_items(ctx.context.userId)
        orders_list = order_handler.get_orders(ctx.context.userId)

        # Flatten results
        items = [item for item in order_items]
        orders = [order for order in orders_list]

        # Try to locate matching item
        for item in items:
            if is_match(product_name, item['name']):  # case insensitive
                order_id = item['orderId']
                
                # Find order matching this orderId
                for order in orders:
                    if ObjectId(order['_id']) == ObjectId(order_id):
                        order_handler.cancel_order(order_id)
                        
                        return f"Order '{item['name']}' has been cancelled successfully."

        return f"Order '{item['name']}' not found."
    
    except Exception as e:
        return f"Error cancelling order: {e}"