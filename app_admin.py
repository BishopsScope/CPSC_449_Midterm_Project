# Import required libraries
from flask import Flask, request, abort, jsonify
import pymysql
from flask_cors import CORS
import datetime
import os
from flask_restful import Api
import jwt
from functools import wraps
from werkzeug.utils import secure_filename

# Create a Flask instance
app = Flask(__name__)
API = Api(app)

# Configiure the file upload
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.pdf'] 
app.config['UPLOAD_PATH'] = 'uploads'

# Create a list of items for public access
public = [
    {"id": 1, "name": "Item 1", "description": "Public 1 test."},
    {"id": 2, "name": "Item 2", "description": "Public 2 test."},
    {"id": 3, "name": "Item 3", "description": "Public 3 test."}
]

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Set the secret key
app.secret_key = 'happykey'

# To connect MySQL database
conn = pymysql.connect(
        host='127.0.0.1',
        user='root', 
        password = "toortoor",
        db='449_db',
        )

cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

# Define a token_required decorator for routes requiring authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Error handling for HTTP 400, 401, 404
@app.errorhandler(400)
def unauthorized_access(e):
	return jsonify(error=str(e)), 400

@app.errorhandler(401)
def unauthorized_access(e):
	return jsonify(error=str(e)), 401

@app.errorhandler(404)
def unauthorized_access(e):
	return jsonify(error=str(e)), 404

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cur.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
		conn.commit()
		account = cur.fetchone()
		if account:
			# Generate JWT token
			token = jwt.encode({'username': account['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, app.config['SECRET_KEY'], algorithm="HS256")
			return jsonify({'token': token})
		else:
			msg = 'Incorrect username / password !'

	return jsonify({'Invalid Password': msg})

# Route for file upload
@app.route('/file', methods=['POST'])
@token_required
def upload_files(current_user):
	uploaded_file = request.files['file']
	filename = secure_filename(uploaded_file.filename) 
	if filename != '':
		file_ext = os.path.splitext(filename)[1]
		if file_ext not in app.config['UPLOAD_EXTENSIONS']:
			abort(400) 
		uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
	return jsonify({'message': 'File successfully uploaded'})

# Route for public items
@app.route('/public', methods=['GET'])
def get_public_items():
    return jsonify(public)

# Route to display username based on token access
@app.route("/display")
@token_required
def display(current_user):
	return jsonify(current_user)


if __name__ == "__main__":
	app.run(host ="127.0.0.1")


