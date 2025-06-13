from dataclasses import dataclass
from typing import Optional

@dataclass
class UpdateCustomerDetails:
    firstName: Optional[str] = ''
    lastName: Optional[str] = ''
    email: Optional[str] = ''
    phoneNumber: Optional[str] = ''
    houseNo: Optional[str] = ''
    city: Optional[str] = ''
    postalCode: Optional[str] = ''
    country: Optional[str] = ''