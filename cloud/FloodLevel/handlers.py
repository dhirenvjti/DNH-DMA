import json
import traceback

import webapp2
from google.appengine.ext.webapp import template

from .models import *
import StringIO
import csv


class FloodLevelHandler(webapp2.RequestHandler):
    def add(self):
        user_email = utils.authenticate_user(self, self.request.url, ["eoc.dnh@gmail.com", "dhirenvjti@gmail.com"])
        if not user_email:
            return

        if self.request.method == 'GET':
            page = utils.template("add.html", "FloodLevel/html")
            template_values = {"default_flood_level_date": datetime.datetime.now(utils.TimeZone(+5.5, False, 'IST')).strftime("%Y-%m-%dT%H:%M")}
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
        user_email = utils.authenticate_user(self, self.request.url, ["eoc.dnh@gmail.com", "dhirenvjti@gmail.com"])
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

class SMSNotificationHandler(webapp2.RequestHandler):
    def alert(self):
        debug = self.request.get("debug", "0")
        floodlevel_latest_entry = FloodLevel.get_latest_entry()
        if floodlevel_latest_entry.flood_level > 79.86 or floodlevel_latest_entry.reading_key_station > 29 or floodlevel_latest_entry.discharge > 250000:
            group_ids = [12124] if debug == "1" else [12124]  # [12337, 12338] for production
            floodlevel_latest_entry = FloodLevel.get_latest_entry()

            message = "ALERT: ATHAL {athallevel}m (Danger at 30.00m), Dam {madhubandam}m (Danger at 82.40m), Inflow " \
                      "{inflow} cusec, Outflow {outflow} cusec (Evacuation at 300000) {time} {date} -DNHDMA".format(
                athallevel=floodlevel_latest_entry.reading_key_station,
                madhubandam=floodlevel_latest_entry.flood_level,
                inflow=int(floodlevel_latest_entry.inflow),
                outflow=int(floodlevel_latest_entry.discharge),
                time=utils.get_formated_am_pm_time(datetime.datetime.now(utils.TimeZone(+5.5, False, 'IST'))),
                date=datetime.datetime.today().strftime("%d/%m/%y")
            )
            sms_notification = SMSNotification()
            for group_id in group_ids:
                sms_notification.send_group_sms(
                    user="dnhdm2017",
                    password="123456",
                    senderid="DNHDMC",
                    channel="Trans",
                    DCS=0,
                    flashsms=0,
                    number=917874148005,
                    text=message,
                    groupid=group_id,
                    route=15
                )

    def daily(self):
        debug = self.request.get("debug", "0")
        group_id = 12124 if debug=="1" else 12124 # 12339 for production
        floodlevel_latest_entry = FloodLevel.get_latest_entry()

        message = "UPDATE: ATHAL {athallevel}m (Danger at 30.00m), Dam {madhubandam}m (Danger at 82.40m), Inflow " \
                  "{inflow} cusec, Outflow {outflow} cusec (Evacuation at 300000) {time} {date} -DNHDMA".format(
            athallevel=floodlevel_latest_entry.reading_key_station,
            madhubandam=floodlevel_latest_entry.flood_level,
            inflow=int(floodlevel_latest_entry.inflow),
            outflow=int(floodlevel_latest_entry.discharge),
            time="06:30PM",
            date=datetime.datetime.today().strftime("%d/%m/%y")
        )
        sms_notification = SMSNotification()
        sms_notification.send_group_sms(
            user="dnhdm2017",
            password="123456",
            senderid="DNHDMC",
            channel="Trans",
            DCS=0,
            flashsms=0,
            number=917874148005,
            text=message,
            groupid=group_id,
            route=15
        )

class PopulateFloodLevelDataHandler(webapp2.RequestHandler):
    @staticmethod
    def format_float(input_string):
        if input_string.lower() in ['', 'nil']:
            return 0.0
        else:
            return float(input_string)

    def get(self):
        user_email = utils.authenticate_user(self, self.request.url, ["eoc.dnh@gmail.com", "dhirenvjti@gmail.com"])
        if not user_email:
            return
        page = utils.template("flood_level_upload.html", "FloodLevel/html")
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

            flood_level_date = datetime.datetime.strptime(fields[2]+fields[3], '%d/%m/%Y%H:%M:%S')
            flood_level = self.format_float(fields[5])
            discharge = self.format_float(fields[6])
            inflow = self.format_float(fields[7])
            location = fields[4]
            user_name = fields[13].replace("\n","")
            user_designation = None
            reading_key_station = self.format_float(fields[8])
            high_tide_from = None
            low_tide_from = None
            low_tide_to = None
            high_tide_to = None
            user_email = "eoc.dnh@gmail.com"

            if not model.FloodLevel.get_by_key_name(datetime.datetime.strftime(flood_level_date, "%Y-%m-%dT%H:%M")):
                FloodLevel().add(
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

        self.response.out.write("Upload Successful!")