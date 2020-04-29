from threading import Lock

from flask import session, request
from werkzeug.exceptions import Unauthorized


class SessionService:
    __lock = Lock()

    __REQUIRE_SESSION_ID_ENDPOINTS = [
        ('/test-data', 'POST'),
        ('/train-data', 'POST'),
        ('/test-data', 'GET'),
        ('/train-data', 'GET'),
        ('/classification', 'POST'),
        ('/classification-data', 'POST')
    ]

    def process_request(self):
        if not self.__require_session_id(request):
            return

        if request.args.get('token') is None:
            raise Unauthorized('There is no token is request parameters.')

        session['session_id'] = request.args.get('token')

    def __require_session_id(self, request):
        return (request.path, request.access_control_request_method) in self.__REQUIRE_SESSION_ID_ENDPOINTS

    def get_session_id(self):
        return request.args.get('token')


session_service = SessionService()
