from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/public/data_display',
                  handler=PublicDataDisplayHandler,
                  handler_method='get',
                  methods=['GET', 'POST']),

])
