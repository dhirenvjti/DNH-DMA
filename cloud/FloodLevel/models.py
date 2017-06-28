import datetime

import logging
import urllib

from google.appengine.api import urlfetch

import model
import utils


class FloodLevel(object):
    def __init__(self):
        pass

    def add(self, **data):
        flood_level_entry, entry_exists = self.get_datastore_entity(data)
        if entry_exists:
            raise Exception("Flood level entry already made for date: {}".format(flood_level_entry.flood_level_date))

        flood_level_entry.put()
        return self.get_json_object(flood_level_entry)

    def get(self, debug=False, **filters):
        query_string = "select * from FloodLevel"

        filters = {key: val for key, val in filters.iteritems() if val != None}

        i = 0
        for field in filters:
            if i == 0:
                query_string += " where "

            if i < len(filters) - 1:
                query_string += "%s='%s' and " % (field, filters[field])
            else:
                query_string += "%s='%s'" % (field, filters[field])
            i += 1

        response = utils.fetch_gql(query_string)
        if debug:
            logging.error("Query String: %s\n\n Response Length: %s" % (query_string, len(response)))

        return response

    @staticmethod
    def get_latest_entry():
        return model.FloodLevel.all().order('-flood_level_date').get()

    def fetch_all(self):
        all_entries = self.get()

        response = []
        for flood_level_entry in all_entries:
            response.append(self.get_json_object(flood_level_entry))

        return response

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "flood_level_date": datastore_entity.flood_level_date.strftime("%Y-%m-%dT%H:%M"),
            "flood_level": datastore_entity.flood_level,
            "discharge": datastore_entity.discharge,
            "inflow": datastore_entity.inflow,
            "location": datastore_entity.location,
            "user_name": datastore_entity.user_name,
            "user_designation": datastore_entity.user_designation,
            "reading_key_station": datastore_entity.reading_key_station,
            "high_tide_from": datastore_entity.high_tide_from.strftime("%Y-%m-%dT%H:%M") if datastore_entity.high_tide_from else None,
            "user_email": datastore_entity.user_email,
            "high_tide_to": datastore_entity.high_tide_to.strftime("%Y-%m-%dT%H:%M") if datastore_entity.high_tide_to else None,
            "low_tide_from": datastore_entity.low_tide_from.strftime("%Y-%m-%dT%H:%M") if datastore_entity.low_tide_from else None,
            "low_tide_to": datastore_entity.low_tide_to.strftime("%Y-%m-%dT%H:%M") if datastore_entity.low_tide_to else None,

        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        flood_level_entry_key_name = datetime.datetime.strftime(json_object["flood_level_date"], "%Y-%m-%dT%H:%M")
        entry_exists = True
        flood_level_entry = model.FloodLevel.get_by_key_name(flood_level_entry_key_name)
        if not flood_level_entry:
            entry_exists = False
            flood_level_entry = model.FloodLevel(key_name=flood_level_entry_key_name)

        flood_level_entry.flood_level_date = json_object["flood_level_date"]
        flood_level_entry.flood_level = json_object["flood_level"]
        flood_level_entry.discharge = json_object["discharge"]
        flood_level_entry.inflow = json_object["inflow"]
        flood_level_entry.location = json_object["location"]
        flood_level_entry.reading_key_station = json_object["reading_key_station"]
        flood_level_entry.high_tide_from = json_object["high_tide_from"]
        flood_level_entry.high_tide_to = json_object["high_tide_to"]
        flood_level_entry.low_tide_from = json_object["low_tide_from"]
        flood_level_entry.low_tide_to = json_object["low_tide_to"]
        flood_level_entry.user_name = json_object["user_name"]
        flood_level_entry.user_designation = json_object["user_designation"]
        flood_level_entry.user_email = json_object["user_email"]

        return flood_level_entry, entry_exists

class SMSNotification(object):
    def __init__(self):
        self.base_url = "http://dnd.saakshisoftware.com/api/mt/SendSMS?"

    def send_group_sms(self, **payload):
        logging.info(payload)
        result = urlfetch.fetch(
            url=self.base_url + urllib.urlencode(payload),
            method=urlfetch.GET,
            deadline=50
        )