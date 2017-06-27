from google.appengine.ext import db


class Rainfall(db.Model):
    rainfall_date = db.DateTimeProperty()
    rainfall_till_prev_date = db.FloatProperty(default=0.0)
    rainfall_last_day = db.FloatProperty(default=0.0)
    rainfall_cumulative = db.FloatProperty(default=0.0)
    rainfall_location = db.StringProperty()

    user_name = db.StringProperty()
    user_email = db.StringProperty()
    user_designation = db.StringProperty()
    user_contact = db.StringProperty()
    user_fax = db.StringProperty(default="0260-2641113")

    remarks = db.TextProperty()

    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)
