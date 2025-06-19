from .db import DB
from models import UpdateOrder
from bson import ObjectId

class OrderItem(DB):
    def __init__(self):
        super().__init__()
        self.collection = self.db['OrderItem']

    async def get_items(self, id):
        items = self.collection.find({'clerkId': id})
        return items
    
    async def update_order(self, updated_order: UpdateOrder):
        update_fields = {}

        if updated_order.quantity is not None:
            update_fields['quantity'] = updated_order.quantity
        if updated_order.size is not None:
            update_fields['size'] = updated_order.size
        if updated_order.color is not None:
            update_fields['color'] = updated_order.color

        if not update_fields:
            return "Nothing to update."

        self.collection.update_one(
            {'orderId': ObjectId(updated_order.order_id)},
            {'$set': update_fields}
        )
    
    async def get_item_by_order_id(self, order_id):
        item = self.collection.find_one({'orderId': ObjectId(order_id)})
        return item
    

if __name__ == "__main__":
    import asyncio
    order_handler = OrderItem()
    item = asyncio.run(order_handler.update_order(UpdateOrder(order_id="6851f24ff60f1ff9c0c2dd81", quantity=2, color="Red", size="S")))
    it = asyncio.run(order_handler.get_item_by_order_id("6851f24ff60f1ff9c0c2dd81"))
    print(item)
    print(it)

    