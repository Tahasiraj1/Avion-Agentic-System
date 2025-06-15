from .db import DB
from models.update_order import UpdateOrder
from bson import ObjectId

class OrderItem(DB):
    def __init__(self):
        super().__init__()
        self.collection = self.db['OrderItem']

    def get_items(self, id):
        items = self.collection.find({'clerkId': id})
        return items
    
    def update_order(self, orderId, updated_order: UpdateOrder):
        update_fields = {}

        if updated_order.quantity is not None:
            update_fields['quantity'] = updated_order.quantity
        if updated_order.size is not None:
            update_fields['size'] = updated_order.size
        if updated_order.color is not None:
            update_fields['color'] = updated_order.color

        if not update_fields:
            return "Nothing to update."

        self.collection.update_one({'orderId': ObjectId(orderId)}, {'$set': update_fields})
        return f"Order updated successfully."
    
    def get_item_by_order_id(self, order_id):
        item = self.collection.find_one({'orderId': ObjectId(order_id)})
        return item

if __name__ == "__main__":
    order_item = OrderItem()
    order = order_item.get_items('user_2s4YFq8ILmoNfr6UeyeYGO0JCjA')
    for i, doc in enumerate(order):
        print(f'\n{i+1}. Order Item: {doc}\n')