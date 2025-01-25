from pydantic import BaseModel
from typing import Optional


class CreateCustomerData(BaseModel):
    email: str
    integration: int
    domain: str
    customer_code: str
    id: int
    identified: bool
    identifications: Optional[str] = None
    createdAt: str
    updatedAt: str


class CreateCustomerResponse(BaseModel):
    status: bool
    message: str
    data: CreateCustomerData
