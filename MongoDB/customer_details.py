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
    
    @staticmethod
    def sanitize_update_fields(customer_details: UpdateCustomerDetails):
        """Sanitizes update fields by removing invalid or empty values."""
        invalid_values = {"", None, "unknown", "null", "not provided", "N/A", "test"}

        update_fields = {
            key: value
            for key, value in customer_details.__dict__.items()
            if value not in invalid_values
        }

        return update_fields
    
    @staticmethod
    def to_update_dict(self):
        """Returns a dictionary of only explicitly provided fields."""
        # Convert dataclass to dict, excluding empty strings
        fields = asdict(self)
        return {key: value for key, value in fields.items() if value}

    def update_customer_details(self, id, customer_details):
        update_fields = self.to_update_dict(customer_details)
        sanitized_fields = self.sanitize_update_fields(update_fields)
        if not sanitized_fields:
            return "No valid fields provided to update."

        if not update_fields:
            return f"No fields to update."
        
        try:
            result = self.collection.update_one(
                {"clerkId": id},
                {"$set": sanitized_fields}
            )
            if result.matched_count == 0:
                return f"No customer found with clerkId {id}"
            if result.modified_count == 0:
                return "No changes made to customer details."
            return "Customer details updated successfully."
        except Exception as e:
            return f"Error updating customer details: {str(e)}"
