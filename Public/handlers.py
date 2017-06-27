import webapp2
from google.appengine.ext.webapp import template

import utils
from FloodLevel.models import FloodLevel
from Rainfall.models import Rainfall


class PublicDataDisplayHandler(webapp2.RequestHandler):
    def get(self):
        page = utils.template("dashboard.html", "Public/html")

        rainfall_latest_entry = Rainfall.get_latest_entry()
        floodlevel_latest_entry = FloodLevel.get_latest_entry()
        template_values = {
            "rainfall_date": rainfall_latest_entry.rainfall_date.strftime('%Y-%m-%d %H:%M'),
            "rainfall_last_day": rainfall_latest_entry.rainfall_last_day,
            "floodlevel_location": floodlevel_latest_entry.location,
            "floodlevel_last_day": floodlevel_latest_entry.flood_level,
            "floodlevel_key_station": floodlevel_latest_entry.reading_key_station,
            "floodlevel_inflow": floodlevel_latest_entry.inflow,
            "floodlevel_discharge": floodlevel_latest_entry.discharge,
            "floodlevel_date": floodlevel_latest_entry.flood_level_date.strftime('%Y-%m-%d %H:%M'),
        }
        self.response.out.write(template.render(page, template_values))