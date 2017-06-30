from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/rainfall/add',
                  handler=RainfallHandler,
                  handler_method='add',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/rainfall/fetch_all',
                  handler=RainfallHandler,
                  handler_method='fetch_all',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/rainfall/filter',
                  handler=RainfallHandler,
                  handler_method='filter',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/rainfall/analytics',
                  handler=RainfallHandler,
                  handler_method='analytics',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/rainfall_hourly/add',
                  handler=RainfallHourlyHandler,
                  handler_method='add',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/rainfall_hourly/fetch_all',
                  handler=RainfallHourlyHandler,
                  handler_method='fetch_all',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/rainfall_hourly/filter',
                  handler=RainfallHourlyHandler,
                  handler_method='filter',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/rainfall_hourly/analytics',
                  handler=RainfallHourlyHandler,
                  handler_method='analytics',
                  methods=['GET', 'POST']),

    ('/rainfall/populate_data', PopulateRainfallDataHandler),
    ('/rainfall_hourly/populate_data', PopulateRainfallHourlyDataHandler),
])
