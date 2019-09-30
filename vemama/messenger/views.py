import json
import requests
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

VERIFY_TOKEN = "83254341743"
PAGE_ACCESS_TOKEN = "EAAeZC8VVDjr0BANZBWd51sBNRFfXoyi2Oza2ryC0NSKkbga7ByEncIVAfMfrtFM2DKcZALnQViBkoajpO9" \
                    "SAbrCSHeWIZC7tptOYQxKHFOb919UVIjqqQcvWm3F2O9YtWhuWynuu6Og4Iq1BYlsSUFPNbczJqP9LDodLGDuTaAZDZD"


def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())


class MessengerView(generic.View):
    def get(self, request, *args, **kwargs):
        print(self.request.GET)
        return HttpResponse(self.request.GET["hub.challenge"])

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    pprint(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()
