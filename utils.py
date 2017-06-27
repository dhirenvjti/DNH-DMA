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