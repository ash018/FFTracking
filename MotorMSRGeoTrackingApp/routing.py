from channels.routing import route


# channel_routing = [
#     route('websocket.connect', ws_connect),
#     route('websocket.disconnect', ws_disconnect),
# ]route("websocket.receive", ws_message),
twitter_channel_routing = {
    "some-channel": "MotorMSRGeoTrackingApp.msr_live_tracking_consumer.my_consumer",
    #"http.request": "aianalytics.consumers.http_consumer",
    "websocket.receive": "MotorMSRGeoTrackingApp.msr_live_tracking_consumer.ws_message",
    #"websocket.disconnect": "aianalytics.consumers.ws_disconnect",
}

PharmaFF_channel_routing = {
    "some-channel": "MotorMSRGeoTrackingApp.pharmaff_live_tracking_consumer.my_consumer",
    #"http.request": "aianalytics.consumers.http_consumer",
    "websocket.receive": "MotorMSRGeoTrackingApp.pharmaff_live_tracking_consumer.ws_message",
    #"websocket.disconnect": "aianalytics.consumers.ws_disconnect",
}
#
# facebook_channel_routing = {
#     "some-channel": "aianalytics.facebook_consumers.my_consumer",
#     #"http.request": "aianalytics.consumers.http_consumer",
#     "websocket.receive": "aianalytics.facebook_consumers.ws_message",
#     #"websocket.disconnect": "aianalytics.consumers.ws_disconnect",
# }