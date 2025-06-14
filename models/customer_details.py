from dataclasses import dataclass
from typing import Optional, TypedDict

@dataclass
class UpdateCustomerDetails(TypedDict):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    phoneNumber: Optional[str]
    houseNo: Optional[str]
    city: Optional[str]
    postalCode: Optional[str]
    country: Optional[str]