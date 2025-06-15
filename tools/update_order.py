from MongoDB.order_item import OrderItem
from MongoDB.orders import Order
from agents import function_tool
from sanity_client import SanityClient
from models.update_order import UpdateOrder


@function_tool
async def update_order(params: UpdateOrder) -> str:
    """Updates order in MongoDB using user_id.
    
    Args:
        params (UpdateOrder): Parameters for updating order.
    
    Returns:
        str: A message indicating the order update.
    """
    try:
        items_handler = OrderItem()
        products_handler = SanityClient()
        order_handler = Order()

        order_item = items_handler.get_item_by_order_id(params.order_id)
        if not order_item:
            return "No order found."

        order = order_handler.get_order_by_order_id(params.order_id)
        if not order:
            return "Order not found."

        if order['status'] != 'pending':
            return f"Can't update order. Order status is {order['status']}."

        # Get productId from order item
        product_id = order_item['productId']

        # Fetch product from Sanity
        product_data = products_handler.get_product_by_id(product_id)
        if not product_data:
            return "Product not found."

        variations = product_data['result'][0]['variations']

        # Search matching variation
        matching_variation = None
        for variation in variations:
            if variation['color'] == params.color and variation['size'] == params.size:
                matching_variation = variation
                break

        if not matching_variation:
            return f"No variation found for color '{params.color}' and size '{params.size}'."

        if params.quantity and params.quantity > matching_variation['quantity']:
            return f"Only {matching_variation['quantity']} items available for color '{params.color}' and size '{params.size}'."

        # Perform the actual update
        result = items_handler.update_order(params.order_id, params)
        return result

    except Exception as e:
        return f"Error updating order: {e}"