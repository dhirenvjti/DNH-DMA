from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/report/flood_damage',
                  handler=ReportHandler,
                  handler_method='flood_damage',
                  methods=['GET', 'POST']),
])