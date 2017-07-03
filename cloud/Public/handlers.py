import webapp2
from google.appengine.ext.webapp import template

import utils
from FloodLevel.models import FloodLevel
from Rainfall.models import Rainfall
import datetime

class PublicDataDisplayHandler(webapp2.RequestHandler):
    def get(self):
        page = utils.template("dashboard.html", "Public/html")

        rainfall_latest_entry = Rainfall.get_latest_entry()
        floodlevel_latest_entry = FloodLevel.get_latest_entry()
        background_color = "#2d2d2d"
        color = "#ffffff"
        notification_type = ""
        if 250000 <= floodlevel_latest_entry.discharge < 300000:
            background_color = "#ffffff"
            color = "#000000"
            notification_type = "ALERT"
        elif 300000 <= floodlevel_latest_entry.discharge < 350000:
            background_color = "#3b5998"
            notification_type = "READY FOR EVACUATION"
        elif floodlevel_latest_entry.discharge > 350000:
            background_color = "#d34836"
            notification_type = "IMMEDIATE EVACUATION"

        rainfall_date = (rainfall_latest_entry.rainfall_date + datetime.timedelta(days=1)).strftime('%d/%m/%Y 08:%M')

        template_values = {
            "rainfall_date": rainfall_date,
            "rainfall_last_day": rainfall_latest_entry.rainfall_last_day,
            "floodlevel_location": floodlevel_latest_entry.location,
            "floodlevel_last_day": floodlevel_latest_entry.flood_level,
            "floodlevel_key_station": floodlevel_latest_entry.reading_key_station,
            "floodlevel_inflow": floodlevel_latest_entry.inflow,
            "floodlevel_discharge": floodlevel_latest_entry.discharge,
            "floodlevel_date": floodlevel_latest_entry.flood_level_date.strftime('%d/%m/%Y %H:%M'),
            "background_color": background_color,
            "color": color,
            "notification_type": notification_type,
        }
        self.response.out.write(template.render(page, template_values))