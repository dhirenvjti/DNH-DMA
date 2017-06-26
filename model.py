from google.appengine.ext import db


class Rainfall(db.Model):
    rainfall_date = db.DateTimeProperty()
    rainfall_till_date = db.FloatProperty(default=0.0)
    rainfall_today = db.FloatProperty(default=0.0)
    rainfall_cumulative = db.FloatProperty(default=0.0)
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)
