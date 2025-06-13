from .db import DB
from bson import ObjectId

class Order(DB):
    def __init__(self):
        super().__init__()
        self.collection = self.db['Order']

    def get_orders(self, id):
        orders = self.collection.find({'clerkId': id})
        return orders
    
    def cancel_order(self, id):
        self.collection.update_one({'_id': ObjectId(id)}, {'$set': {'status': 'cancelled'}})
        return f"Order cancelled successfully."