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

    webapp2.Route(template='/flood_level/sms_notification/alert',
                  handler=SMSNotificationHandler,
                  handler_method='alert',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/flood_level/filter',
                  handler=FloodLevelHandler,
                  handler_method='filter',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/flood_level/analytics',
                  handler=FloodLevelHandler,
                  handler_method='analytics',
                  methods=['GET', 'POST']),

    ('/flood_level/populate_data', PopulateFloodLevelDataHandler),
])
