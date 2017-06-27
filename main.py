import webapp2
from google.appengine.ext.webapp import template

import utils


class MainHandler(webapp2.RequestHandler):
    def get(self):
        page = utils.template("index.html", "templates")
        self.response.out.write(template.render(page, {}))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
])