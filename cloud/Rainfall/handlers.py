import json
import traceback

import webapp2
from google.appengine.ext.webapp import template

from .models import *


class RainfallHandler(webapp2.RequestHandler):
    def add(self):
        user_email = utils.authenticate_user(self, self.request.url, ["dhirenvjti@gmail.com"])
        if not user_email:
            return

        if self.request.method == 'GET':
            page = utils.template("add.html", "Rainfall/html")
            template_values = {"default_rainfall_date": datetime.datetime.today().strftime("%Y-%m-%d")}
            self.response.out.write(template.render(page, template_values))

        else:
            self.response.headers['Content-Type'] = "application/json"
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            try:
                rainfall_date = datetime.datetime.strptime(self.request.get("rainfall_date", None), "%Y-%m-%d")
                rainfall_till_prev_date = float(self.request.get("rainfall_till_prev_date", None))
                rainfall_last_day = float(self.request.get("rainfall_last_day", None))
                rainfall_cumulative = rainfall_till_prev_date + rainfall_last_day
                rainfall_location = self.request.get("rainfall_location", None)
                user_name = self.request.get("user_name", None)
                user_designation = self.request.get("user_designation", None)
                user_contact = self.request.get("user_contact", None)
                user_fax = self.request.get("user_fax", "0260-2641113")
                remarks = self.request.get("remarks", None)

                response = Rainfall().add(
                    rainfall_date=rainfall_date,
                    rainfall_till_prev_date=rainfall_till_prev_date,
                    rainfall_last_day=rainfall_last_day,
                    rainfall_cumulative=rainfall_cumulative,
                    rainfall_location=rainfall_location,
                    user_name=user_name,
                    user_email=user_email,
                    user_designation=user_designation,
                    user_contact=user_contact,
                    user_fax=user_fax,
                    remarks=remarks,
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

            response = Rainfall().fetch_all()

            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())