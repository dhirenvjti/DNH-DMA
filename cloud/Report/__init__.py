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

    webapp2.Route(template='/report/flood_damage/all_reports',
                  handler=FloodDamageHandler,
                  handler_method='all_reports',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/report/flood_situation/generate',
                  handler=FloodSituationHandler,
                  handler_method='generate',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/report/flood_situation/download',
                  handler=FloodSituationHandler,
                  handler_method='download',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/report/flood_situation/all_reports',
                  handler=FloodSituationHandler,
                  handler_method='all_reports',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/report/ndma/generate',
                  handler=NDMAHandler,
                  handler_method='generate',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/report/ndma/download',
                  handler=NDMAHandler,
                  handler_method='download',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/report/ndma/all_reports',
                  handler=NDMAHandler,
                  handler_method='all_reports',
                  methods=['GET', 'POST']),




])