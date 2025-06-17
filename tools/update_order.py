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

        order_item = await items_handler.get_item_by_order_id(params.order_id)
        if not order_item:
            return "No order found."

        order = await order_handler.get_order_by_order_id(params.order_id)
        if not order:
            return "Order not found."

        if order['status'] != 'pending':
            return f"Can't update order. Order status is {order['status']}."

        # Get productId and quantity from order item
        product_id = order_item['productId']
        old_quantity = order_item['quantity']
        
        delta_quantity = params.quantity - old_quantity
        result = await products_handler.adjust_variation_quantity(product_id, params.color, params.size, delta_quantity)

        if result.get('transactionId'):
            # Perform the actual update
            await items_handler.update_order(params.order_id, params)
            return "Order quantity updated successfully."
        
        return "Stock updated failed — but order item not modified."

    except Exception as e:
        return f"Error updating order: {e}"