from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/mu/mu_results',
                  handler=MUHandler,
                  handler_method='results',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/mu/mu_filter',
                  handler=MUHandler,
                  handler_method='filter',
                  methods=['GET', 'POST']),

    ('/mu/mu_populate_results', PopulateMUResultsHandler),
])
