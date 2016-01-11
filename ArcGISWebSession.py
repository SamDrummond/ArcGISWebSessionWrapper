import json
import requests
from datetime import datetime, timedelta
from requests_ntlm import HttpNtlmAuth


class SessionParameters(object):

    def __init__(self):

        self._domain = None
        self._username = None
        self._password = None
        self._web_adaptor = None
        self._token = None
        self._response = None
        self._arcgis_path = "arcgis"
        self._portal_path = "portal"

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def web_adaptor(self):
        return self._web_adaptor

    @web_adaptor.setter
    def web_adaptor(self, value):
        self._web_adaptor = value

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        self._domain = value

    @property
    def arcgis_path(self):
        return self._arcgis_path

    @arcgis_path.setter
    def arcgis_path(self, value):
        self._arcgis_path = value

    @property
    def portal_path(self):
        return self._portal_path

    @portal_path.setter
    def portal_path(self, value):
        self._portal_path = value


class Session(object):

    def __init__(self, session_parameters):

        if session_parameters is None:
            raise TypeError("session_parameters object cannot be none")

        self._session_parameters = session_parameters

        auth = HttpNtlmAuth(self._session_parameters.domain + '\\' +
                            self._session_parameters.username,
                            self._session_parameters.password)

        session = requests.session()
        session.auth = auth
        self.session_handle = session

    @property
    def session_parameters(self):
        return self._session_parameters

    @property
    def handle(self):

        return self.session_handle


class Token(object):

    def __init__(self, session):

        if session is None:
            raise TypeError("session object cannot be none")

        self._session = session.handle
        session_parameters = session.session_parameters

        self.request_parameters = {
            "username": session_parameters.username,
            "password": session_parameters.password,
            "client": "referer",
            "referer": "https://" + session_parameters.web_adaptor +
                       "/" + session_parameters.arcgis_path + "/admin",
            "f":"json"
        }
        self._token_url = "https://" + session_parameters.web_adaptor + \
                          "/" + session_parameters.portal_path + "/sharing/generateToken"

        self._token = None
        self._expire_date = None

    def aquire(self):

        if not self._is_token_valid():
            self._refresh_token()

        return self._token

    @property
    def expire_date(self):
        return self._expire_date

    def _is_token_valid(self):

        current_date = datetime.now()

        return (self.expire_date is not None) and (current_date < self._expire_date)

    def _refresh_token(self):

        self._expire_date = datetime.now() + timedelta(hours=1)

        response = self._session.post(self._token_url, data=self.request_parameters)

        response_data = response.text
        token_object = json.loads(response_data)
        self._token = token_object['token']