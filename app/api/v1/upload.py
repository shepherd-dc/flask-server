import os
import uuid

from flask import request, current_app, send_from_directory
from werkzeug.utils import secure_filename

from app.libs.error_code import NotFound, FileSizeLimit, DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.restful_json import restful_json
from app.validators.forms import UploadForm

api = Redprint('upload')


@api.route('/image', methods=['POST'])
def upload_image():
    # form = UploadForm().validate_for_api()
    # f = form.photo.data

    file = request.files['file']

    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        filename = random_filename(file.filename)
        image_path = current_app.config['UPLOAD_IMAGE_FOLDER']

        if not os.path.exists(image_path):
            os.makedirs(image_path)

        file.save(os.path.join(image_path, filename))

        data = {
            'filename': filename,
            'url': '/v1/upload/image'
        }

        return restful_json(data), 201


@api.route('/image/<filename>', methods=['GET', 'DELETE'])
def uploaded_image(filename):
    image_path = current_app.config['UPLOAD_IMAGE_FOLDER']

    if not os.path.exists(os.path.join(image_path, filename)):
        return NotFound()

    if request.method == 'GET':
        return send_from_directory(current_app.config['UPLOAD_IMAGE_FOLDER'],
                               filename)

    if request.method == 'DELETE':
        os.remove(os.path.join(image_path, filename))
        return DeleteSuccess()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename