from .db import DB
from bson import ObjectId

class OrderItem(DB):
    def __init__(self):
        super().__init__()
        self.collection = self.db['OrderItem']

    def get_items(self, id):
        items = self.collection.find({'clerkId': id})
        return items
    

if __name__ == "__main__":
    order_item = OrderItem()
    order = order_item.get_items('user_2s4YFq8ILmoNfr6UeyeYGO0JCjA')
    for i, doc in enumerate(order):
        print(f'\n{i+1}. Order Item: {doc}\n')