from agents import function_tool
from MongoDB.orders import Order
from MongoDB.order_item import OrderItem
from sanity_client import SanityClient
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

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

        order_data = await order_handler.get_order_by_order_id(order_id)
        if not order_data:
            return "Order not found."
        
        payment_intent = order_data.get('paymentIntentId')

        if order_data['status'] == 'pending':
            item_data = await item_handler.get_item_by_order_id(order_id)
            name = item_data['name'] if item_data else "Unknown Product"

            try:
                await products_handler.update_product_quantity(item_data['productId'], item_data['color'], item_data['size'], item_data['quantity'])
                await order_handler.cancel_order(order_id)

                if payment_intent:
                    refund = stripe.Refund.create(payment_intent=payment_intent, reason='requested_by_customer')
                    return f"Order '{name}' has been cancelled successfully. Refund intitiated: {refund.id}"
                else:
                    return f"Order '{name}' has been cancelled successfully."
            except Exception as e:
                return f"Error cancelling order: {e}"
        else:
            return f"Order cannot be cancelled. Current status is '{order_data['status']}'."
    
    except Exception as e:
        return f"Error cancelling order: {e}"
