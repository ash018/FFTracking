from channels import Group
from channels.handler import AsgiHandler, AsgiRequest
from django.http import HttpResponse
from django.utils.timezone import now
from json import dumps
from .models import *


def http_consumer(message):
    response = HttpResponse(
        "It is now {} and you've requested {} with {} as request parameters.".format(
            now(),
            message.content['path'],
            dumps(message.content['get'])
        )
    )
    message.reply_channel.send(response.channel_encode())


def ws_message(message):
    pharmaff_initial_locations = GetInitialPharmaFFPosition()
    data = ""
    for ff in pharmaff_initial_locations:
        data += str(ff['ID']) + '|' + str(ff['UserId']) + '|' + str(ff['Level1Name']) + '|' + str(ff['Latitude'])+ '|' + str(ff['Longitude']) + '|' + str(ff['MaxUpdateTime'])
        data += '||'
    message.reply_channel.send({
        "text": data
    })

def ws_connect(message):
    # Group('users').add(message.reply_channel)
    print('Test1' + message)


def ws_disconnect(message):
    # Group('users').discard(message.reply_channel)
    print('Test2' + message)
    message.discard(message.reply_channel)


def my_consumer(message):
    print(('yesss' + message.handle))
    # response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    django_request = AsgiRequest(message)
    # Run view
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)

        # message.reply_channel.send({"accept": True})
        # message.reply_channel.send({
        #     "text": message.content['text'],
        # })


        # django_response = view(django_request)

        # response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
        # #Encode that response into message format (ASGI)
        # for chunk in AsgiHandler.encode_response(response):
        #     message.reply_channel.send(chunk)


        # Encode the response into message format
        # for chunk in AsgiHandler.encode_response(django_response):
        # for chunk in AsgiHandler.encode_response(django_request):
        #     message.reply_channel.send(chunk)
        # message.reply_channel.send('111')

