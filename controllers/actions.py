from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import json

app = Blueprint('actions', __name__)

@app.route("/list", methods=['POST'])
def list():
    params = request.json
    print(params)
    # user_token = create_access_token(identity=params['username'])
    res = '{ "columns": ['
    res += '{ "dataField": "id", "text": "", "sort": true, "filter": "textFilter()", "headerStyle": { "minWidth": "50px", "maxWidth": "50px" } }'
    res += ']'
    res += ',"datas": ['
    res += '{ "id": 1, "name": "Item name 1", "price3": 1001 }'
    res += ']'
    res += '}'

    print(res)
    print(json.dumps(res))
    return jsonify(res)
