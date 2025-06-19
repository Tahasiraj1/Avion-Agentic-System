from MongoDB import OrderItem, Order
from agents import function_tool
from sanity_client import SanityClient
from models import UpdateOrder
import stripe
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

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

        payment_intent = order['paymentIntentId']

        product_id = order_item['productId']
        old_quantity = order_item['quantity']
        unit_price = order_item['price']

        delta_quantity = params.quantity - old_quantity
        new_price = unit_price * params.quantity
        extra_amount = int(unit_price * delta_quantity * 100)
        
        delta_quantity = params.quantity - old_quantity
        result = await products_handler.adjust_variation_quantity(
            product_id, 
            params.color, 
            params.size, 
            delta_quantity
        )

        if result.get('transactionId'):
            if payment_intent:
                # Ask for payment
                payment = stripe.PaymentIntent.create(
                    amount=extra_amount,
                    currency='usd',
                    payment_method_types=['card'],
                    metadata={
                        "order_id": str(order['_id']),
                        "reason": "quantity increased"
                    }
                )
                await items_handler.update_order(params)
                await order_handler.update_price(params.order_id, new_price)
                return f"Order quantity updated successfully. Payment intitiated."
            else:
                await items_handler.update_order(params)
                await order_handler.update_price(params.order_id, new_price)
                return "Order quantity updated successfully, no stripe payment found."
        
        return "Stock updated failed — but order item not modified."

    except Exception as e:
        return f"Error updating order: {e}"