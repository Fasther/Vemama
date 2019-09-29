from django.views import generic
from django.http.response import HttpResponse

VERIFY_TOKEN = "83254341743"


class MessengerView(generic.View):
    def get(self, request, *args, **kwargs):
        print(self.request.GET)
        return HttpResponse(self.request.GET["hub.challenge"])
