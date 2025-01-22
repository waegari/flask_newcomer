from flask import Flask, request, jsonify, send_from_directory
from db_conn import user, password, dsn
from db import DB, Task, Request
from flask_cors import CORS
import oracledb
import os

oracledb.init_oracle_client()

app = Flask(__name__)
CORS(app)
@app.route('/employees', methods=['POST'])
def create_employee():
    try:
        data = request.json
        if not data or not all(key in data for key in ("id", "name", "email", "role")):
            return jsonify({"error": "Missing required fields: id, name, email, role."}), 400
        
        req = Request(body=data)
        db_instance = DB(Task.CREATE, req)
        result = db_instance.execute()

        if result['success']:
            return jsonify({"message": "Employee created successfully."}), 201
        else:
            return jsonify({"error": result['error']}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        req = Request(params=request.args.to_dict())  # Get query parameters if any
        db_instance = DB(Task.READ, req)
        result = db_instance.execute()

        if result['success']:
            return jsonify(result['data']), 200
        else:
            return jsonify({"error": result['error']}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    try:
        req = Request(params={"id": id})
        db_instance = DB(Task.READ, req)
        result = db_instance.execute()

        if result['success'] and result['data']:
            return jsonify(result['data'][0]), 200
        else:
            return jsonify({"error": "Employee not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/employees/<int:id>', methods=['PATCH'])
def update_employee(id):
    try:
        params = request.args.to_dict()
        params['id'] = id
        data = request.json
        if not data:
            return jsonify({"error": "No fields provided to update."}), 400
        
        req = Request(data, params)

        db_instance = DB(Task.UPDATE, req)
        result = db_instance.execute()

        if result['success']:
            return "", 204
        else:
            return jsonify({"error": result['error']}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        params = request.args.to_dict()
        params['id'] = id
        req = Request(params=params)
        db_instance = DB(Task.DELETE, req)
        result = db_instance.execute()

        if result['success']:
            return "", 204
        else:
            return jsonify({"error": result['error']}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def serve_mainpage():
    try:
        return send_from_directory(os.path.join(os.getcwd(), 'mainpage'), 'index.html')
    except Exception as e:
        return jsonify({"error": "Main page not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
