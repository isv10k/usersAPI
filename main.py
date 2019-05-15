import pickle

from flask import Flask, jsonify, request, make_response, abort
import os.path

app = Flask(__name__)

DB_PATH = 'db.pickle'


def get_data(is_it_post=None):
    """Returns data from file"""
    data = []
    # If file with data exists
    if os.path.isfile(DB_PATH):
        # If file with data not empty
        if os.path.getsize(DB_PATH) > 0:
            with open(DB_PATH, 'rb') as db_in:
                # Load data from file
                data = pickle.load(db_in)
        elif not is_it_post:
            abort(404)
    elif not is_it_post:
        abort(404)
    return data


def post_to_db(user=None, users=None):
    """Load incoming data to file"""
    data = get_data(is_it_post=True)

    if user:
        # If data was loaded, get id from last element
        if data:
            user['id'] = data[-1]['id'] + 1
        else:
            user['id'] = 1
        data.append(user)
        with open(DB_PATH, 'wb+') as db_out:
            pickle.dump(data, db_out)
    if users:
        if data:
            start_id = data[-1]['id'] + 1
        else:
            start_id = 1
        for entry in users:
            entry['id'] = start_id
            data.append(entry)
            start_id += 1
        with open(DB_PATH, 'wb+') as db_out:
            pickle.dump(data, db_out)


def del_from_db(user_id=None):
    """Method DELETE realization"""
    data = get_data()

    if user_id:
        for entry in data:
            if entry['id'] == user_id:
                data.remove(entry)
                # If data still have elements
                if data:
                    with open(DB_PATH, 'wb+') as db_out:
                        pickle.dump(data, db_out)
                else:
                    open(DB_PATH, 'wb+')
                return
        # If id was not found
        abort(404)
    else:
        open(DB_PATH, 'wb+')


def patch_data(new_data, user_id=None):
    """Chage entries in data fail"""
    data = get_data()

    if user_id:
        for entry in data:
            if entry['id'] == user_id:
                # Set new or existing data
                entry['name'] = new_data.get('name', entry['name'])
                entry['age'] = new_data.get('age', entry['age'])
                with open(DB_PATH, 'wb+') as db_out:
                    pickle.dump(data, db_out)
                return
        # If id was not found
        abort(404)
    else:
        for entry in data:
            entry['name'] = new_data.get('name', entry['name'])
            entry['age'] = new_data.get('age', entry['age'])
        with open(DB_PATH, 'wb+') as db_out:
            pickle.dump(data, db_out)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'message': error.description}), 400)


@app.route('/')
def index():
    return 'Simple user management api. Available commands GET, POST, PATCH, DELETE'


@app.route('/users/', methods=['GET'])
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id=None):
    data = None
    try:
        db_in = open(DB_PATH, 'rb')
    except FileNotFoundError as e:
        abort(404)
    else:
        if os.path.getsize(DB_PATH) > 0:
            data = pickle.load(db_in)
        else:
            abort(404)
        db_in.close()
    if user_id:
        for user in data:
            if user['id'] == user_id:
                return jsonify({'user': user})
        return abort(404)
    else:
        return jsonify({'users': data})


@app.route('/users/', methods=['POST'])
def create_user():

    data = request.json
    # If posted one user
    if isinstance(data, dict):
        if 'name' not in data or 'age' not in data:
            abort(400, f'Incorrect data at {data}')
        user_to_db = {
            'name': data['name'],
            'age': data['age']
        }
        post_to_db(user=user_to_db)
        return jsonify({'user': user_to_db}), 201
    # If posted list of users
    else:
        users_to_db = []
        for user in data:
            if 'name' not in user or 'age' not in user:
                abort(400, f'Incorrect data at {user}')
                continue
            user_to_db = {
                'name': user['name'],
                'age': user['age']
            }
            users_to_db.append(user_to_db)
        post_to_db(users=users_to_db)
        return jsonify({'users': users_to_db}), 201


@app.route('/users/', methods=['DELETE'])
@app.route('/users/<int:user_to_del_id>', methods=['DELETE'])
def delete_user(user_to_del_id=None):
    if user_to_del_id:
        del_from_db(user_id=user_to_del_id)
    else:
        del_from_db()
    return jsonify({'result': True}), 200


@app.route('/users/', methods=['PATCH'])
@app.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id=None):

    if not request.json:
        abort(400)

    if 'name' in request.json or 'age' in request.json:

        if user_id:
            patch_data(request.json, user_id=user_id)
        else:
            patch_data(request.json)

        return jsonify({'result': True}), 200
    else:
        abort(400)


if __name__ == '__main__':
    app.run(debug=True)
