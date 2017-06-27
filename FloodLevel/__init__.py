from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/flood_level/add',
                  handler=FloodLevelHandler,
                  handler_method='add',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/flood_level/fetch_all',
                  handler=FloodLevelHandler,
                  handler_method='fetch_all',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/flood_level/sms_notification/daily',
                  handler=SMSNotificationHandler,
                  handler_method='daily',
                  methods=['GET', 'POST']),
])
