import os

from google.appengine.api import users
from google.appengine.ext import db


def authenticate_user(self, targetURL, email_list=None):
    if 'http://localhost' in self.request.url:
        return 'local-user'

    if not email_list:
        email_list = []
    user = users.get_current_user()
    if user:
        if user.email() in email_list:
            return user.email()
        else:
            self.response.out.write("{user_email} is not authorized.  Please <a href={logout_url}>Logout</a> and re-login.".format(
                user_email=user.email(),
                logout_url=users.create_login_url(targetURL)))
            return False

    else:
        self.response.out.write("Please <a href='{login_url}'>Login...</a>".format(
            login_url=users.create_login_url(targetURL)
        ))
        return False

def fetch_gql(query_string, fetchsize=50):
    q = db.GqlQuery(query_string)
    cursor = None
    results = []
    while True:
        q.with_cursor(cursor)
        intermediate_result = q.fetch(fetchsize)
        if len(intermediate_result) == 0:
            break
        cursor = q.cursor()
        results += intermediate_result

    return results

def template(file_name, directory="templates"):
  return os.path.join(os.path.dirname(__file__), directory, file_name)

def get_formated_am_pm_time(datetime_object):
    am_pm = "AM"
    hour = datetime_object.hour
    min = datetime_object.minute
    if datetime_object.hour == 12:
        am_pm = "PM"
    elif datetime_object.hour > 12:
        am_pm = "PM"
        hour = datetime_object.hour - 12
    elif datetime_object.hour == 0:
        hour = 12

    return '{}:{}{}'.format(hour, min, am_pm)
