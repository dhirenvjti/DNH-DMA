import csv
import json
import traceback

import webapp2
from google.appengine.ext.webapp import template

from .models import *

import StringIO


class MUHandler(webapp2.RequestHandler):
    def fetch_all(self):

        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        try:
            response = MU().fetch_all()
            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def filter(self):
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        try:
            seat_no_check = self.request.get("seat_no", None)

            query_string = "select * from MU where seat_no = '"+seat_no_check+"'"

            response = []
            all_entries = utils.fetch_gql(query_string=query_string)

            for entry in all_entries:
                response.append(MU.get_json_object(entry))

            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def results(self):
        if self.request.method == 'GET':
            page = utils.template("results.html", "MU/html")
            template_values = {}
            self.response.out.write(template.render(page, template_values))

class PopulateMUResultsHandler(webapp2.RequestHandler):
    def get(self):
        user_email = utils.authenticate_user(self, self.request.url, ["eoc.dnh@gmail.com", "dhirenvjti@gmail.com"])
        if not user_email:
            return
        page = utils.template("mu_populate_results.html", "MU/html")
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

            seat_no = fields[0]
            name = fields[1]
            result = fields[2]
            frem = fields[3]
            res = fields[4]
            exam_no = fields[5]
            exam = fields[6]
            year = fields[7]
            month = fields[8]

            # rainfall_date = datetime.datetime.strptime(fields[4]+fields[5], '%d/%m/%Y%H:%M:%S')
            #
            # rainfall_last_hour = fields[6]
            # if rainfall_last_hour.lower() in ['', 'nil']:
            #     rainfall_last_hour = 0.0
            # else:
            #     rainfall_last_hour = float(rainfall_last_hour)
            #
            # rainfall_location = fields[1]
            # user_name = fields[7]
            # user_email = "eoc.dnh@gmail.com"
            # user_designation = None

            MU().add(
                seat_no=seat_no,
                name=name,
                result=result,
                frem=frem,
                res=res,
                exam_no=exam_no,
                exam=exam,
                year=year,
                month=month,
            )

        self.response.out.write("Upload Successful!")