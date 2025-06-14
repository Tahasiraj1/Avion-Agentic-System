from .db import DB
from dataclasses import asdict
from models.customer_details import UpdateCustomerDetails

class CustomerDetails(DB):
    def __init__(self):
        super().__init__()
        self.collection = self.db['CustomerDetails']

    def get_customer_details(self, id):
        customer_details = self.collection.find({'clerkId': id})
        return customer_details

    def update_customer_details(self, id, customer_details):
        update_fields = {k: v for k, v in customer_details.__dict__.items() if v is not None}
        try:
            result = self.collection.update_one(
                {"clerkId": id},
                {"$set": update_fields}
            )
            if result.matched_count == 0:
                return f"No customer found with clerkId {id}"
            if result.modified_count == 0:
                return "No changes made to customer details."
            return "Customer details updated successfully."
        except Exception as e:
            return f"Error updating customer details: {str(e)}"
