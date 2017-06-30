import csv
import json
import traceback

import webapp2
from google.appengine.ext.webapp import template

from .models import *

import StringIO

class RainfallHandler(webapp2.RequestHandler):
    def add(self):
        user_email = utils.authenticate_user(self, self.request.url, ["eoc.dnh@gmail.com", "dhirenvjti@gmail.com"])
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
        user_email = utils.authenticate_user(self, self.request.url, ["eoc.dnh@gmail.com", "dhirenvjti@gmail.com"])
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

    def filter(self):
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        try:

            start_date = datetime.datetime.strptime(self.request.get("start_date", None), "%Y-%m-%d")
            end_date = datetime.datetime.strptime(self.request.get("end_date", None), "%Y-%m-%d") + datetime.timedelta(days=1)

            query_string = "select * from Rainfall where rainfall_date > datetime({}, {}, {}) and rainfall_date < datetime({}, {}, {})".format(
                start_date.year,
                start_date.month,
                start_date.day,
                end_date.year,
                end_date.month,
                end_date.day,
            )
            response = []
            all_entries = utils.fetch_gql(query_string=query_string)
            for entry in all_entries:
                response.append(Rainfall.get_json_object(entry))

            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def analytics(self):
        if self.request.method == 'GET':
            page = utils.template("analytics.html", "Rainfall/html")
            date_today = datetime.date.today()
            date_7days = date_today - datetime.timedelta(days=7)
            template_values = {
                "default_end_date": date_today.strftime("%Y-%m-%d"),
                "default_start_date": date_7days.strftime("%Y-%m-%d"),
            }
            self.response.out.write(template.render(page, template_values))

class PopulateRainfallDataHandler(webapp2.RequestHandler):
    def get(self):
        user_email = utils.authenticate_user(self, self.request.url, ["eoc.dnh@gmail.com", "dhirenvjti@gmail.com"])
        if not user_email:
            return
        page = utils.template("rainfall_upload.html", "Rainfall/html")
        template_values = {}
        self.response.out.write(template.render(page, template_values))

    def post(self):
        user_email = utils.authenticate_user(self, self.request.url, ["eoc.dnh@gmail.com", "dhirenvjti@gmail.com"])
        if not user_email:
            return
        csv_file_html = self.request.get('csv_file', '')
        csv_file = StringIO.StringIO(csv_file_html)
        csv_reader = csv.reader(csv_file)
        skip_row = 2
        for fields in csv_reader:
            skip_row -= 1
            if skip_row >= 0:
                continue

            rainfall_date = datetime.datetime.strptime(fields[4], '%d/%m/%Y')
            rainfall_till_prev_date = fields[5]
            if rainfall_till_prev_date.lower() in ['', 'nil']:
                rainfall_till_prev_date = 0.0
            else:
                rainfall_till_prev_date = float(rainfall_till_prev_date)

            rainfall_last_day = fields[6]
            if rainfall_last_day.lower() in ['', 'nil']:
                rainfall_last_day = 0.0
            else:
                rainfall_last_day = float(rainfall_last_day)

            rainfall_cumulative = fields[7]
            if rainfall_cumulative.lower() in ['', 'nil']:
                rainfall_cumulative = 0.0
            else:
                rainfall_cumulative = float(rainfall_cumulative)

            rainfall_location = fields[1]
            user_name = fields[9]
            user_email = "eoc.dnh@gmail.com"
            user_designation = fields[10]
            user_contact = fields[11]
            user_fax = fields[12]
            remarks = fields[8]

            Rainfall().add(
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

        self.response.out.write("Upload Successful!")

class RainfallHourlyHandler(webapp2.RequestHandler):
    def add(self):
        user_email = utils.authenticate_user(self, self.request.url, ["eoc.dnh@gmail.com", "dhirenvjti@gmail.com"])
        if not user_email:
            return

        if self.request.method == 'GET':
            page = utils.template("add_hourly.html", "Rainfall/html")
            template_values = {"default_rainfall_date": datetime.datetime.now(utils.TimeZone(+5.5, False, 'IST')).strftime("%Y-%m-%dT%H:%M")}
            self.response.out.write(template.render(page, template_values))

        else:
            self.response.headers['Content-Type'] = "application/json"
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            try:
                rainfall_location = self.request.get("rainfall_location", None)
                rainfall_date = datetime.datetime.strptime(self.request.get("rainfall_date", None), "%Y-%m-%dT%H:%M")
                rainfall_last_hour = float(self.request.get("rainfall_last_hour", None))

                user_name = self.request.get("user_name", None)
                user_designation = self.request.get("user_designation", None)

                response = RainfallHourly().add(
                    rainfall_date=rainfall_date,
                    rainfall_last_hour=rainfall_last_hour,
                    rainfall_location=rainfall_location,
                    user_name=user_name,
                    user_email=user_email,
                    user_designation=user_designation,
                )

                self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
            except Exception as e:
                self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
                logging.error(traceback.format_exc())

    def fetch_all(self):
        user_email = utils.authenticate_user(self, self.request.url, ["eoc.dnh@gmail.com", "dhirenvjti@gmail.com"])
        if not user_email:
            return

        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        try:

            response = RainfallHourly().fetch_all()

            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def filter(self):
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        try:

            start_date = datetime.datetime.strptime(self.request.get("start_date", None), "%Y-%m-%d")
            end_date = datetime.datetime.strptime(self.request.get("end_date", None), "%Y-%m-%d") + datetime.timedelta(days=1)

            query_string = "select * from RainfallHourly where rainfall_date > datetime({}, {}, {}) and rainfall_date < datetime({}, {}, {})".format(
                start_date.year,
                start_date.month,
                start_date.day,
                end_date.year,
                end_date.month,
                end_date.day,
            )
            response = []
            all_entries = utils.fetch_gql(query_string=query_string)
            for entry in all_entries:
                response.append(RainfallHourly.get_json_object(entry))

            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def analytics(self):
        if self.request.method == 'GET':
            page = utils.template("analytics_hourly.html", "Rainfall/html")
            date_today = datetime.date.today()
            date_7days = date_today - datetime.timedelta(days=7)
            template_values = {
                "default_end_date": date_today.strftime("%Y-%m-%d"),
                "default_start_date": date_7days.strftime("%Y-%m-%d"),
            }
            self.response.out.write(template.render(page, template_values))

class PopulateRainfallHourlyDataHandler(webapp2.RequestHandler):
    def get(self):
        user_email = utils.authenticate_user(self, self.request.url, ["eoc.dnh@gmail.com", "dhirenvjti@gmail.com"])
        if not user_email:
            return
        page = utils.template("rainfall_hourly_upload.html", "Rainfall/html")
        template_values = {}
        self.response.out.write(template.render(page, template_values))

    def post(self):
        user_email = utils.authenticate_user(self, self.request.url, ["eoc.dnh@gmail.com", "dhirenvjti@gmail.com"])
        if not user_email:
            return
        csv_file_html = self.request.get('csv_file', '')
        csv_file = StringIO.StringIO(csv_file_html)
        csv_reader = csv.reader(csv_file)
        skip_row = 1
        for fields in csv_reader:
            skip_row -= 1
            if skip_row >= 0:
                continue

            rainfall_date = datetime.datetime.strptime(fields[4]+fields[5], '%d/%m/%Y%H:%M:%S')

            rainfall_last_hour = fields[6]
            if rainfall_last_hour.lower() in ['', 'nil']:
                rainfall_last_hour = 0.0
            else:
                rainfall_last_hour = float(rainfall_last_hour)

            rainfall_location = fields[1]
            user_name = fields[7]
            user_email = "eoc.dnh@gmail.com"
            user_designation = None

            RainfallHourly().add(
                rainfall_date=rainfall_date,
                rainfall_last_hour=rainfall_last_hour,
                rainfall_location=rainfall_location,
                user_name=user_name,
                user_email=user_email,
                user_designation=user_designation,
            )

        self.response.out.write("Upload Successful!")