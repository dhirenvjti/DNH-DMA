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

class RainfallHourly(db.Model):
    rainfall_date = db.DateTimeProperty()
    rainfall_last_hour = db.FloatProperty(default=0.0)
    rainfall_location = db.StringProperty()
    user_name = db.StringProperty()
    user_email = db.StringProperty()
    user_designation = db.StringProperty()

class FloodLevel(db.Model):
    flood_level_date = db.DateTimeProperty()
    flood_level = db.FloatProperty(default=0.0)
    discharge = db.FloatProperty(default=0.0)
    inflow = db.FloatProperty(default=0.0)
    location = db.StringProperty()
    reading_key_station = db.FloatProperty(default=0.0)
    high_tide_from = db.DateTimeProperty()
    high_tide_to = db.DateTimeProperty()
    low_tide_from = db.DateTimeProperty()
    low_tide_to = db.DateTimeProperty()

    user_name = db.StringProperty()
    user_email = db.StringProperty()
    user_designation = db.StringProperty()

    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)

class FloodDamageReport(db.Model):
    created_at_IST = db.DateTimeProperty()
    report_link = db.TextProperty()

class FloodSituationReport(db.Model):
    created_at_IST = db.DateTimeProperty()
    report_link = db.TextProperty()

class NDMAReport(db.Model):
    created_at_IST = db.DateTimeProperty()
    report_link = db.TextProperty()

class MiscellaneousStats(db.Model):
    athal_level_alert = db.StringProperty()
    info = db.FloatProperty(default=0.0)

class MU(db.Model):
    seat_no = db.StringProperty()
    name = db.StringProperty()
    result = db.StringProperty()
    frem = db.StringProperty()
    res = db.StringProperty()
    exam_no = db.StringProperty()
    exam = db.StringProperty()
    year = db.StringProperty()
    month = db.StringProperty()