import hashlib
from threading import Lock

from flask import session, request
from werkzeug.exceptions import Unauthorized, Forbidden


class SessionService:
    __lock = Lock()

    __REQUIRE_SESSION_ID_ENDPOINTS = [
        ('/test-data', 'POST'),
        ('/train-data', 'POST'),
        ('/test-data', 'GET'),
        ('/train-data', 'GET'),
        ('/classification', 'POST'),
        ('/classification-data', 'POST'),
        ('/compare-classification', 'GET'),
        ('/fit-time-plot', 'GET'),
        ('/tokens', 'GET'),
        ('/files', 'DELETE'),
        ('/files', 'GET')
    ]

    __ADMIN_ENDPOINTS = [
        ('/tokens', 'GET'),
        ('/files', 'DELETE'),
        ('/files', 'GET')
    ]

    __ADMIN_TOKENS_HASHES = [
        b'\xb8}\xce\x07j(}.1xn=u\xf1\x13\x11',
        b'\x84K\x84\xd19~\x00\xcd\xf9\xe0a\xae\xda\x80\x8a\x14',
        b'&T\xdcW\x059\xa4@\x84\x88V[c\x04|\x8c'
    ]

    __active_tokens = []

    def process_request(self):
        if not self.__require_session_id():
            return

        if request.args.get('token') is None:
            raise Unauthorized('There is no token is request parameters.')

        if self.__is_admin_endpoint() and not self.__security_check():
            raise Forbidden('You don\'t have enough permissions to perform this operation.')

        session['session_id'] = request.args.get('token')

        self.__lock.acquire()
        if session['session_id'] not in self.__active_tokens:
            self.__active_tokens.append(session['session_id'])
        self.__lock.release()

    def __require_session_id(self):
        return (request.path, request.method) in self.__REQUIRE_SESSION_ID_ENDPOINTS

    def __is_admin_endpoint(self):
        return (request.path, request.method) in self.__ADMIN_ENDPOINTS

    def __security_check(self):
        return hashlib.md5(bytes(request.args.get('token'), 'utf-8')).digest() in self.__ADMIN_TOKENS_HASHES

    def get_session_id(self):
        return request.args.get('token')

    def get_active_tokens(self):
        return self.__active_tokens


session_service = SessionService()
