import logging
from typing import Optional

import requests
from paystackapi.customer import Customer

from libs.paystack.api_responses import CreateCustomerResponse
from libs.paystack.exceptions import CustomerCreationException
from libs.paystack.models import OrganisationCustomer


def add_new_customer(
    customer: OrganisationCustomer,
) -> tuple[
    Optional[CreateCustomerResponse],
    Optional[Exception],
]:
    res = Customer.create(
        first_name=customer.name,
        email=customer.email,
    )
    if res.status_code != requests.codes.ok:
        logging.debug(res.json())
        logging.error(f"Failed to create customer. Status code: {res.status_code}.")
        return None, CustomerCreationException("Failed to create customer.")
    return CreateCustomerResponse(**res.json()), None
