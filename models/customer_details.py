from pydantic import BaseModel
from typing import Optional

class UpdateCustomerDetails(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None
    houseNo: Optional[str] = None
    city: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None