from channels import include

channel_routing = [
    include("MotorMSRGeoTrackingApp.routing.twitter_channel_routing", path=r"^/MotorMSRGeoTrackingApp/twittermining"),
    include("MotorMSRGeoTrackingApp.routing.PharmaFF_channel_routing", path=r"^/MotorMSRGeoTrackingApp/pharmaff_routing"),
    #include("MotorMSRGeoTrackingApp.routing.facebook_channel_routing", path=r"^/MotorMSRGeoTrackingApp/facebookmining"),
]
