import json
import time
import uuid
from threading import Lock

from flask import session
from werkzeug.exceptions import Unauthorized

from Classification_Project.ApplicationConstants import ApplicationConstants
from Classification_Project.ConsoleLogger import console_logger


class SessionService:
    __lock = Lock()
    __session_id_list = []

    __REQUIRE_SESSION_ID_ENDPOINTS = [
        ('/test-data', 'POST'),
        ('/train-data', 'POST'),
        ('/test-data', 'GET'),
        ('/train-data', 'GET'),
        ('/classification', 'POST'),
        ('/classification-data', 'POST')
    ]

    def process_request(self, request):
        if not self.__require_session_id(request):
            return

        session_el = list(filter(lambda el: el.session_id == request.headers.get('session_id'), self.__session_id_list))

        session_el = session_el[0] if len(session_el) > 0 else None

        if session_el is None or self.__is_expired(session_el.creation_time):
            raise Unauthorized('There is invalid session_id in header or session_id expired.')

        session['session_id'] = session_el.session_id

        session_el.creation_time = (int(round(time.time() * 1000)))

    def generate_session_id(self):
        self.__lock.acquire()

        session_id_el = SessionElement(str(uuid.uuid1()), int(round(time.time() * 1000)))

        self.__session_id_list.append(session_id_el)

        self.__lock.release()

        return json.dumps(
            {'session_id': session_id_el.session_id, 'generation_time': session_id_el.creation_time}), 200, \
               {'ContentType': 'application/json'}

    def clear_session_storage(self):
        console_logger.info('Clearing session id storage...')

        self.__session_id_list = filter(lambda el: self.__is_expired(el.creation_time), self.__session_id_list)

        console_logger.info('Clearing session id storage successfully finished.')

    def __is_expired(self, creation_time):
        return (int(round(time.time() * 1000))) - creation_time > ApplicationConstants.get_constant('SESSION_TTL')

    def __require_session_id(self, request):
        return (request.path, request.method) in self.__REQUIRE_SESSION_ID_ENDPOINTS


class SessionElement:
    def __init__(self, session_id, creation_time):
        self.session_id = session_id
        self.creation_time = creation_time


session_service = SessionService()
