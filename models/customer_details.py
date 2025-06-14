from pydantic import BaseModel

class UpdateCustomerDetails(BaseModel):
    firstName: str | None = None
    lastName: str | None = None
    email: str | None = None
    phoneNumber: str | None = None
    houseNo: str | None = None
    city: str | None = None
    postalCode: str | None = None
    country: str | None = None