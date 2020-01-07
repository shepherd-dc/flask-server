from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerException

app = create_app()

CORS(app, resources={r"/v1/*": {"origins": "*"}})


@app.errorhandler(Exception)
def framework_error(e):
    """
    falsk == 1.0
    APIException
    HTTPException
    Exception
    DEBUG
    """
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        if not app.config['DEBUG']:
            return ServerException()
        else:
            raise e


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051, threaded=True)
