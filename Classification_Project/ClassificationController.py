import json
import uuid

from flask import Flask, send_file, request, session

from classification_project.ApplicationConstants import ApplicationConstants
from classification_project.ClassificationRequestDtoMapper import ClassificationRequestDtoMapper
from classification_project.ClassificationService import ClassificationService
from classification_project.FileUtils import FileUtils
from classification_project.Scheduler import Scheduler

app = Flask(__name__)
app.secret_key = ApplicationConstants.APP_SECRET_KEY.value
host = ApplicationConstants.LOCAL_CLIENT_HOST.value

mapper = ClassificationRequestDtoMapper()
classification_service = ClassificationService()
file_utils = FileUtils()
scheduler = Scheduler()

scheduler.schedule_clearing_tmp_folder()


@app.route('/test-data', methods=['POST'])
def upload_test_data():
    file_utils.save_session_based_txt_file(request.files['file'], 'test_data')

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/train-data', methods=['POST'])
def upload_train_data():
    file_utils.save_session_based_txt_file(request.files['file'], 'train_data')

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/test-data', methods=['GET'])
def is_test_data_for_session():
    return json.dumps({'file_exists': file_utils.is_file_for_session('test_data')}), \
           200, {'ContentType': 'application/json'}


@app.route('/train-data', methods=['GET'])
def is_train_data_for_session():
    return json.dumps({'file_exists': file_utils.is_file_for_session('train_data')}), \
           200, {'ContentType': 'application/json'}


@app.route('/classification', methods=['POST'])
def classify_and_get_info():
    request_params = mapper.map(request.get_json())

    return classification_service.classify_and_get_info(request_params).serialize


@app.route('/classification-data', methods=['POST'])
def classify_and_get_data():
    return send_file(classification_service.classify_and_get_data(),
                     attachment_filename='classification_results.zip', as_attachment=True)


@app.before_request
def set_session_id():
    if 'session_id' not in session:
        session['session_id'] = uuid.uuid1()


@app.after_request
def set_cross_origin(response):
    response.headers['Access-Control-Allow-Origin'] = host
    response.headers['Access-Control-Allow-Headers'] = host
    response.headers['Access-Control-Allow-Methods'] = host

    return response


if __name__ == '__main__':
    app.run()
