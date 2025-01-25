from pydantic import BaseModel


class OrganisationCustomer(BaseModel):
    name: str
    email: str
