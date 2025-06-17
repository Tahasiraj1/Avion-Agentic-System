from agents import function_tool
from MongoDB.orders import Order
from MongoDB.order_item import OrderItem
from sanity_client import SanityClient

@function_tool
async def cancel_order(order_id: str) -> str:
    """Cancels an order.

    Args:
        order_id: The ID of the order to cancel.

    Returns:
        str: A message indicating that the order has been cancelled.
    """
    try:
        item_handler = OrderItem()
        order_handler = Order()
        products_handler = SanityClient()

        order_data = order_handler.get_order_by_order_id(order_id)
        if not order_data:
            return "Order not found."

        if order_data['status'] == 'pending':
            item_data = item_handler.get_item_by_order_id(order_id)
            name = item_data['name'] if item_data else "Unknown Product"

            try:
                await products_handler.update_product_quantity(item_data['productId'], item_data['color'], item_data['size'], item_data['quantity'])
                order_handler.cancel_order(order_id)
                return f"Order '{name}' has been cancelled successfully."
            except Exception as e:
                return f"Error cancelling order: {e}"
        else:
            return f"Order cannot be cancelled. Current status is '{order_data['status']}'."
    
    except Exception as e:
        return f"Error cancelling order: {e}"
