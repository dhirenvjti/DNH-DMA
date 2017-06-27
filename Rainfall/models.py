import datetime

import model


class Rainfall(object):
    def __init__(self):
        pass

    def add(self, **data):
        rainfall_entry, entry_exists = self.get_datastore_entity(data)
        if entry_exists:
            raise Exception("Rainfall entry already made for date: {}".format(rainfall_entry.rainfall_date))

        rainfall_entry.put()
        return self.get_json_object(rainfall_entry)

    def fetch_all(self):
        pass

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

        rainfall_entry.remarks = json_object["remarks"]

        return rainfall_entry, entry_exists