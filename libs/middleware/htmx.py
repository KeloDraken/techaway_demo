from django.http import HttpRequest, QueryDict
from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequest):

    htmx: HtmxDetails

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.htmx = HtmxDetails(self)
        self.DELETE = QueryDict(mutable=True)
        self.PUT = QueryDict(mutable=True)
