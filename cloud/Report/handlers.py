import datetime
import logging
import traceback
import json
import re
import StringIO

import webapp2
from google.appengine.ext.webapp import template
import cloudstorage as gcs

import utils
from docx import Document
from .models import *

class FloodDamageHandler(webapp2.RequestHandler):
    def generate(self):
        user_email = utils.authenticate_user(self, self.request.url, ["dhirenvjti@gmail.com"])
        if not user_email:
            return

        if self.request.method == 'GET':
            page = utils.template("flood_damage.html", "Report/html")
            template_values = {}
            self.response.out.write(template.render(page, template_values))

        else:
            self.response.headers['Content-Type'] = "application/json"
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            try:
                date_of_sending = datetime.datetime.strptime(self.request.get("date_of_sending", None), "%Y-%m-%d")
                date_of_reporting = datetime.datetime.strptime(self.request.get("date_of_reporting", None), "%Y-%m-%d")
                replace_info = {
                    "date_of_sending": date_of_sending.strftime("%d/%m/%Y"),
                    "date_of_reporting": date_of_reporting.strftime("%d/%m/%Y"),
                    "general_trend_of_rainfall_last_24": self.request.get("general_trend_of_rainfall_last_24", None),
                    "cumulative_total_rainfall": self.request.get("cumulative_total_rainfall", None),
                    "river_name_levels_observed": self.request.get("river_name_levels_observed", None),
                    "name_engineering_works": self.request.get("name_engineering_works", None),
                    "communication_disruption_details": self.request.get("communication_disruption_details", None),
                    "relief_measures_taken": self.request.get("relief_measures_taken", None),
                    "comments_press_news": self.request.get("comments_press_news", None),
                    "enclosed_map": self.request.get("enclosed_map", None),
                    "flood_damaged_stats_attached": self.request.get("flood_damaged_stats_attached", None),
                    "sr_no": self.request.get("sr_no", None),
                    "state": self.request.get("state", "Dadra Nagar Haveli"),
                    "area_affected": self.request.get("area_affected", None),
                    "population_affected": self.request.get("population_affected", None),
                    "damage_to_crops": self.request.get("damage_to_crops", None),
                    "damage_to_houses": self.request.get("damage_to_houses", None),
                    "cattles_lost": self.request.get("cattles_lost", None),
                    "human_lives_lost": self.request.get("human_lives_lost", None),
                    "damage_to_public_utilities": self.request.get("damage_to_public_utilities", None),
                    "total_damage": self.request.get("total_damage", None),
                    "user_name": self.request.get("user_name", None),
                    "user_designation": self.request.get("user_designation", None),
                    "user_contact": self.request.get("user_contact", None),
                    "user_fax": self.request.get("user_fax", None),
                }

                document = Document(utils.template('Report-InformationrelatedtoFlood.docx', 'templates'))
                for phrase, replacement in replace_info.iteritems():
                    utils.docx_replace_regex(document, re.compile(phrase), replacement)

                target_stream = StringIO.StringIO()
                document.save(target_stream)

                created_at_IST = datetime.datetime.now(utils.TimeZone(+5.5, False, 'IST'))
                key = 'Report - Information related to Flood Stamp:{}'.format(created_at_IST.strftime("%Y-%m-%dT%H:%M"))
                write_retry_params = gcs.RetryParams(backoff_factor=1.1)
                filename = '/dnh-dma.appspot.com/%s.docx' % key
                gcs_file = gcs.open(filename, 'w', content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', options={'x-goog-acl': 'public-read'},
                                    retry_params=write_retry_params)
                gcs_file.write(target_stream.getvalue())
                gcs_file.close()
                html_link = "https://storage.googleapis.com" + filename
                FloodDamageReport().add(
                    created_at_IST=created_at_IST,
                    report_link = html_link
                )
                self.response.out.write(json.dumps({'success': True, 'error': None, 'response': html_link}))
            except Exception as e:
                self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
                logging.error(traceback.format_exc())

    def download(self):
        flood_report = FloodDamageReport.get_latest_entry()
        self.redirect(str(flood_report.report_link))