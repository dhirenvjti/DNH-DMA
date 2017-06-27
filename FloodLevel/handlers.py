import json
import traceback

import webapp2
from google.appengine.ext.webapp import template

from .models import *


class FloodLevelHandler(webapp2.RequestHandler):
    def add(self):
        user_email = utils.authenticate_user(self, self.request.url, ["dhirenvjti@gmail.com"])
        if not user_email:
            return

        if self.request.method == 'GET':
            page = utils.template("add.html", "FloodLevel/html")
            template_values = {"default_flood_level_date": datetime.datetime.now(TimeZone(+5.5, False, 'IST')).strftime("%Y-%m-%dT%H:%M")}
            self.response.out.write(template.render(page, template_values))

        else:
            self.response.headers['Content-Type'] = "application/json"
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            try:
                flood_level_date = datetime.datetime.strptime(self.request.get("flood_level_date", None), "%Y-%m-%dT%H:%M")
                flood_level = float(self.request.get("flood_level", None))
                discharge = float(self.request.get("discharge", None))
                inflow = float(self.request.get("inflow", None))
                location = self.request.get("location", None)
                user_name = self.request.get("user_name", None)
                user_designation = self.request.get("user_designation", None)
                reading_key_station = float(self.request.get("reading_key_station", None))

                high_tide_from = self.request.get("high_tide_from", None)
                if high_tide_from:
                    high_tide_from = datetime.datetime.strptime(high_tide_from, "%Y-%m-%dT%H:%M")

                low_tide_from = self.request.get("low_tide_from", None)
                if low_tide_from:
                    low_tide_from = datetime.datetime.strptime(low_tide_from, "%Y-%m-%dT%H:%M")

                low_tide_to = self.request.get("low_tide_to", None)
                if low_tide_to:
                    low_tide_to = datetime.datetime.strptime(low_tide_to, "%Y-%m-%dT%H:%M")

                high_tide_to =self.request.get("high_tide_to", None)
                if high_tide_to:
                    high_tide_to = datetime.datetime.strptime(high_tide_to, "%Y-%m-%dT%H:%M")

                response = FloodLevel().add(
                    flood_level_date=flood_level_date,
                    flood_level=flood_level,
                    discharge=discharge,
                    inflow=inflow,
                    location=location,
                    user_name=user_name,
                    user_designation=user_designation,
                    reading_key_station=reading_key_station,
                    high_tide_from=high_tide_from,
                    low_tide_from=low_tide_from,
                    low_tide_to=low_tide_to,
                    high_tide_to=high_tide_to,
                    user_email=user_email,
                )

                self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
            except Exception as e:
                self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
                logging.error(traceback.format_exc())

    def fetch_all(self):
        user_email = utils.authenticate_user(self, self.request.url, ["dhirenvjti@gmail.com"])
        if not user_email:
            return

        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        try:

            response = FloodLevel().fetch_all()

            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())