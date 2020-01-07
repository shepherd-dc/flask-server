from flask import jsonify


def restful_json(data, error_code=0, msg='ok'):
    data_json={
        "error_code": error_code,
        "msg": msg,
        "data": data
    }
    return jsonify(data_json)