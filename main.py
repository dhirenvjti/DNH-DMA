import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello DNH-DMA User!')


app = webapp2.WSGIApplication([
    ('/', MainHandler)
])