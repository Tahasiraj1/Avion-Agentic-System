from .db import DB
from models.customer_details import UpdateCustomerDetails

class CustomerDetails(DB):
    def __init__(self):
        super().__init__()
        self.collection = self.db['CustomerDetails']

    def get_customer_details(self, id):
        customer_details = self.collection.find_one(
            {'clerkId': id},
            {'_id': False, 'clerkId': False},
        )
        return customer_details

    def update_customer_details(self, id: str, customer_details: UpdateCustomerDetails):
        # Fetch existing data
        existing_data = self.get_customer_details(id)
        current_details = UpdateCustomerDetails(**existing_data)

        # Compare & build update dict
        update_fields = {
            key: val
            for key, val in customer_details.model_dump(exclude_unset=True).items()
            if val is not None and val != getattr(current_details, key)
        }

        if not update_fields:
            return "No fields changed. Nothing to update."

        try:
            result = self.collection.update_one(
                {"clerkId": id},
                {"$set": update_fields}
            )
            return f"{result.modified_count} customer details updated successfully."
        except Exception as e:
            return f"Error updating customer details: {str(e)}"



if __name__ == "__main__":
    customer_details = CustomerDetails()
    update = customer_details.update_customer_details('user_2s4YFq8ILmoNfr6UeyeYGO0JCjA', UpdateCustomerDetails(country='UK'))
    print(update)