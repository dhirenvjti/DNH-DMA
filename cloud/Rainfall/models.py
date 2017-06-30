import datetime

import logging

import model
import utils

from google.appengine.api import memcache

class Rainfall(object):
    def __init__(self):
        pass

    def add(self, **data):
        rainfall_entry, entry_exists = self.get_datastore_entity(data)

        rainfall_entry.put()
        memcache.delete("rainfall_latest_entry")
        return self.get_json_object(rainfall_entry)

    def get(self, debug=False, **filters):
        query_string = "select * from Rainfall"

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
        entry = memcache.get("rainfall_latest_entry")
        if not entry:
            entry = model.Rainfall.all().order('-rainfall_date').get()
            memcache.set("rainfall_latest_entry", entry)
        return entry

    def fetch_all(self):
        all_entries = self.get()

        response = []
        for rainfall_entry in all_entries:
            response.append(self.get_json_object(rainfall_entry))

        return response

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "rainfall_date": datastore_entity.rainfall_date.strftime("%Y-%m-%d"),
            "rainfall_till_prev_date": datastore_entity.rainfall_till_prev_date,
            "rainfall_last_day": datastore_entity.rainfall_last_day,
            "rainfall_cumulative": datastore_entity.rainfall_cumulative,
            "rainfall_location": datastore_entity.rainfall_location,
            "user_name": datastore_entity.user_name,
            "user_designation": datastore_entity.user_designation,
            "user_contact": datastore_entity.user_contact,
            "user_fax": datastore_entity.user_fax,
            "user_email": datastore_entity.user_email,
            "remarks": datastore_entity.remarks,
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        rainfall_entry_key_name = datetime.datetime.strftime(json_object["rainfall_date"], "%Y-%m-%d")
        entry_exists = True
        rainfall_entry = model.Rainfall.get_by_key_name(rainfall_entry_key_name)
        if not rainfall_entry:
            entry_exists = False
            rainfall_entry = model.Rainfall(key_name=rainfall_entry_key_name)

        rainfall_entry.rainfall_date = json_object["rainfall_date"]
        rainfall_entry.rainfall_till_prev_date = json_object["rainfall_till_prev_date"]
        rainfall_entry.rainfall_last_day = json_object["rainfall_last_day"]
        rainfall_entry.rainfall_cumulative = json_object["rainfall_cumulative"]
        rainfall_entry.rainfall_location = json_object["rainfall_location"]

        rainfall_entry.user_name = json_object["user_name"]
        rainfall_entry.user_designation = json_object["user_designation"]
        rainfall_entry.user_contact = json_object["user_contact"]
        rainfall_entry.user_fax = json_object["user_fax"]
        rainfall_entry.user_email = json_object["user_email"]

        rainfall_entry.remarks = json_object["remarks"]

        return rainfall_entry, entry_exists

class RainfallHourly(object):
    def __init__(self):
        pass

    def add(self, **data):
        rainfall_hourly_entry, entry_exists = self.get_datastore_entity(data)

        rainfall_hourly_entry.put()
        memcache.delete("rainfall_hourly_latest_entry")
        return self.get_json_object(rainfall_hourly_entry)

    def get(self, debug=False, **filters):
        query_string = "select * from RainfallHourly"

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
        entry = memcache.get("rainfall_hourly_latest_entry")
        if not entry:
            entry = model.RainfallHourly.all().order('-rainfall_date').get()
            memcache.set("rainfall_hourly_latest_entry", entry)
        return entry

    def fetch_all(self):
        all_entries = self.get()

        response = []
        for rainfall_hourly_entry in all_entries:
            response.append(self.get_json_object(rainfall_hourly_entry))

        return response

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "rainfall_date": datastore_entity.rainfall_date.strftime("%Y-%m-%dT%H:%M"),
            "rainfall_last_hour": datastore_entity.rainfall_last_hour,
            "rainfall_location": datastore_entity.rainfall_location,
            "user_name": datastore_entity.user_name,
            "user_designation": datastore_entity.user_designation,
            "user_email": datastore_entity.user_email
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        rainfall_hourly_entry_key_name = datetime.datetime.strftime(json_object["rainfall_date"], "%Y-%m-%dT%H:%M") + json_object["rainfall_location"]
        entry_exists = True
        rainfall_hourly_entry = model.RainfallHourly.get_by_key_name(rainfall_hourly_entry_key_name)
        if not rainfall_hourly_entry:
            entry_exists = False
            rainfall_hourly_entry = model.RainfallHourly(key_name=rainfall_hourly_entry_key_name)

        rainfall_hourly_entry.rainfall_date = json_object["rainfall_date"]
        rainfall_hourly_entry.rainfall_last_hour = json_object["rainfall_last_hour"]
        rainfall_hourly_entry.rainfall_location = json_object["rainfall_location"]

        rainfall_hourly_entry.user_name = json_object["user_name"]
        rainfall_hourly_entry.user_designation = json_object["user_designation"]
        rainfall_hourly_entry.user_email = json_object["user_email"]

        return rainfall_hourly_entry, entry_exists