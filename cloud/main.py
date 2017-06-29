import webapp2
from google.appengine.ext.webapp import template

import utils


class MainHandler(webapp2.RequestHandler):
    def get(self):
        page = utils.template("index.html", "templates")
        self.response.out.write(template.render(page, {}))

class AdminHandler(webapp2.RequestHandler):
    def get(self):
        user_email = utils.authenticate_user(self, self.request.url, ["dhirenvjti@gmail.com"])
        if not user_email:
            return

        page = utils.template("admin.html", "templates")
        self.response.out.write(template.render(page, {}))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/administrator', AdminHandler),
])