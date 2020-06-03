import json

from flask import Flask, send_file, request

from Classification_Project.ApplicationConstants import ApplicationConstants
from Classification_Project.ClassificationRequestDtoMapper import ClassificationRequestDtoMapper
from Classification_Project.ClassificationService import ClassificationService
from Classification_Project.FileUtils import FileUtils
from Classification_Project.Scheduler import Scheduler
from Classification_Project.SessionService import session_service

app = Flask(__name__)
app.secret_key = ApplicationConstants.get_constant('APP_SECRET_KEY')
host = ApplicationConstants.get_constant('CLIENT_HOST')

mapper = ClassificationRequestDtoMapper()
classification_service = ClassificationService()
file_utils = FileUtils()
scheduler = Scheduler()

scheduler.schedule_clearing_tmp_folder()


@app.route('/', methods=['GET'])
def home_page():
    return json.dumps({'result': 'Hello world from PythonClassification!'}), 200, {'ContentType': 'application/json'}


@app.route('/test-data', methods=['POST'])
def upload_test_data():
    if request.files['file'].content_type == 'application/zip':
        file_utils.save_session_based_image_data(request.files['file'], 'test_data.zip', 'test_data.json')
    else:
        file_utils.save_session_based_file(request.files['file'], 'test_data.txt')

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/train-data', methods=['POST'])
def upload_train_data():
    if request.files['file'].content_type == 'application/zip':
        file_utils.save_session_based_image_data(request.files['file'], 'train_data.zip', 'train_data.json')
    else:
        file_utils.save_session_based_file(request.files['file'], 'train_data.txt')

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/test-data', methods=['GET'])
def is_test_data_for_session():
    return json.dumps({'file_exists': file_utils.is_file_for_session('test_data')}), \
           200, {'ContentType': 'application/json'}


@app.route('/train-data', methods=['GET'])
def is_train_data_for_session():
    return json.dumps({'file_exists': file_utils.is_file_for_session('train_data')}), \
           200, {'ContentType': 'application/json'}


@app.route('/classification/methods', methods=['GET'])
def get_all_classification_methods():
    return classification_service.get_available_methods()


@app.route('/classification', methods=['POST'])
def classify_and_get_info():
    request_params = mapper.map(request.get_json())

    return classification_service.classify_and_get_info(request_params).serialize


@app.route('/compare-classification', methods=['GET'])
def classify_with_all_methods():
    return classification_service.map_to_default_response_dto(classification_service.compare_classification()).serialize


@app.route('/classification-data', methods=['GET'])
def classify_and_get_data():
    return send_file(classification_service.get_classification_result_archive(request.args['method_name']),
                     attachment_filename='classification_results.zip', as_attachment=True)


@app.route('/fit-time-plot', methods=['GET'])
def get_fit_time_plot():
    return send_file(classification_service.build_fit_time_plot(), attachment_filename='fit-time-plot.png')


@app.route('/test-accuracy-plot', methods=['GET'])
def get_test_accuracy_plot():
    return send_file(classification_service.build_test_accuracy_plot(), attachment_filename='test-accuracy-plot.png')


@app.route('/tokens', methods=['GET'])
def get_active_tokens():
    return json.dumps(session_service.get_active_tokens())


@app.route('/files', methods=['DELETE'])
def delete_user_files():
    file_utils.delete_user_files(request.args['pattern'])

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/files', methods=['GET'])
def get_user_files_names():
    return json.dumps(file_utils.get_user_files_names(request.args['pattern']))


@app.before_request
def process_request():
    session_service.process_request()


@app.after_request
def set_cross_origin(response):
    response.headers['Access-Control-Allow-Origin'] = host
    response.headers['Access-Control-Allow-Headers'] = host
    response.headers['Access-Control-Allow-Methods'] = host

    return response


if __name__ == '__main__':
    app.run()
