import datetime

import logging

import model
import utils

class MU(object):
    def __init__(self):
        pass

    def add(self, **data):
        result_entry, entry_exists = self.get_datastore_entity(data)
        result_entry.put()
        return self.get_json_object(result_entry)

    def get(self, debug=False, **filters):
        query_string = "select * from MU"

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

    def fetch_all(self):
        all_entries = self.get()

        response = []
        for result_entry in all_entries:
            response.append(self.get_json_object(result_entry))

        return response

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "seat_no": datastore_entity.seat_no,
            "name": datastore_entity.name,
            "result": datastore_entity.result,
            "frem": datastore_entity.frem,
            "res": datastore_entity.res,
            "exam_no": datastore_entity.exam_no,
            "exam": datastore_entity.exam,
            "year": datastore_entity.year,
            "month": datastore_entity.month,
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        result_key_name = json_object["seat_no"]
        entry_exists = True
        result_entry = model.MU.get_by_key_name(result_key_name)
        if not result_entry:
            entry_exists = False
            result_entry = model.MU(key_name=result_key_name)

        result_entry.seat_no = json_object["seat_no"]
        result_entry.name = json_object["name"]
        result_entry.result = json_object["result"]
        result_entry.frem = json_object["frem"]
        result_entry.res = json_object["res"]

        result_entry.exam_no = json_object["exam_no"]
        result_entry.exam = json_object["exam"]
        result_entry.year = json_object["year"]
        result_entry.month = json_object["month"]

        return result_entry, entry_exists