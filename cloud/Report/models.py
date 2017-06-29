import datetime

import logging

import model
import utils

class FloodDamageReport(object):
    def __init__(self):
        pass

    def add(self, **data):
        flood_report, entry_exists = self.get_datastore_entity(data)
        if entry_exists:
            raise Exception("Flood-damage entry already made for date: {}".format(flood_report.created_at_IST))

        flood_report.put()
        return self.get_json_object(flood_report)

    def get(self, debug=False, **filters):
        query_string = "select * from FloodDamageReport"

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
        return model.FloodDamageReport.all().order('-created_at_IST').get()

    def fetch_all(self):
        all_entries = self.get()

        response = []
        for flood_report in all_entries:
            response.append(self.get_json_object(flood_report))

        return response

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "created_at_IST": datastore_entity.created_at_IST.strftime("%Y-%m-%dT%H:%M:%S"),
            "report_link": datastore_entity.report_link,
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        flood_report_key_name = datetime.datetime.now(utils.TimeZone(+5.5, False, 'IST')).strftime("%Y-%m-%dT%H:%M:%S")
        entry_exists = True
        flood_report = model.FloodDamageReport.get_by_key_name(flood_report_key_name)
        if not flood_report:
            entry_exists = False
            flood_report = model.FloodDamageReport(key_name=flood_report_key_name)

        flood_report.created_at_IST = json_object["created_at_IST"]

        flood_report.report_link = json_object["report_link"]

        return flood_report, entry_exists

class FloodSituationReport(object):
    def __init__(self):
        pass

    def add(self, **data):
        flood_situation_report, entry_exists = self.get_datastore_entity(data)
        if entry_exists:
            raise Exception("Flood-situation entry already made for date: {}".format(flood_situation_report.created_at_IST))

        flood_situation_report.put()
        return self.get_json_object(flood_situation_report)

    def get(self, debug=False, **filters):
        query_string = "select * from FloodSituationReport"

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
        return model.FloodSituationReport.all().order('-created_at_IST').get()

    def fetch_all(self):
        all_entries = self.get()

        response = []
        for flood_situation_report in all_entries:
            response.append(self.get_json_object(flood_situation_report))

        return response

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "created_at_IST": datastore_entity.created_at_IST.strftime("%Y-%m-%dT%H:%M:%S"),
            "report_link": datastore_entity.report_link,
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        flood_situation_report_key_name = datetime.datetime.now(utils.TimeZone(+5.5, False, 'IST')).strftime("%Y-%m-%dT%H:%M:%S")
        entry_exists = True
        flood_situation_report = model.FloodSituationReport.get_by_key_name(flood_situation_report_key_name)
        if not flood_situation_report:
            entry_exists = False
            flood_situation_report = model.FloodSituationReport(key_name=flood_situation_report_key_name)

        flood_situation_report.created_at_IST = json_object["created_at_IST"]

        flood_situation_report.report_link = json_object["report_link"]

        return flood_situation_report, entry_exists