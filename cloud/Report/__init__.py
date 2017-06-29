from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/report/flood_damage/generate',
                  handler=FloodDamageHandler,
                  handler_method='generate',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/report/flood_damage/download',
                  handler=FloodDamageHandler,
                  handler_method='download',
                  methods=['GET', 'POST']),
])