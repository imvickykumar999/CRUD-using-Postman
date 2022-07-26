
from flask import Flask, request, jsonify
from fetch import fire
import json

app = Flask(__name__)

@app.route('/createuser', methods=['POST'])
def create_user():
	content_type = request.headers.get('Content-Type')
	
	if content_type == 'text/plain':
		content = request.get_data().decode('ascii')
	
	elif content_type == 'application/json':
		content = request.json

	count = fire.call('counter')
	uid = count+1
	fire.send('counter', uid)

	content = fire.decodeit(json.dumps(content))
	content = json.loads(content)
	content['unique_ID'] = uid
	
	_path = f"apigee/{uid}"
	fire.send(_path, content)

	content = fire.encodeit(json.dumps(content))
	return content, 201


# @app.route('/updateuserbyid/<uid>', methods=['PUT'])
def update_user_by_id(uid):
	content_type = request.headers.get('Content-Type')
	
	if content_type == 'text/plain':
		content = request.get_data().decode('ascii')
	
	elif content_type == 'application/json':
		content = request.json

	jsondata = fire.call(f'apigee/{uid}')
	print(jsondata)
	jsondata['fname'] = content['fname']
	jsondata['lname'] = content['lname']
	jsondata['age']   = content['age']
	
	_path = f"apigee/{uid}"
	fire.send(_path, jsondata)
	
	content = fire.encodeit(json.dumps(jsondata))
	return content, 201


@app.route('/getallusers')
def get_all_users():
	content = fire.call('apigee')
	content = fire.encodeit(json.dumps(content))
	return content, 200


@app.route('/getuserbyid/<uid>')
def get_user_by_id(uid):
	content = fire.call(f'apigee/{uid}')

	if content == None:
		return jsonify({
			'error' : {
				'description' : f'Unique ID {uid} not Found in Database.'
			}
		})
	else:
		content = fire.encodeit(json.dumps(content))
		return content, 200


@app.route('/deleteuserbyid/<uid>', methods=['DELETE'])
def delete_user_by_id(uid):
	_path = f"apigee/{uid}"

	if fire.call(_path) == None:
		fire.send('counter', 1000)
		return jsonify({
			'message' : {
				'description' : f'Unique ID {uid} not fount in Database.'
			}
		})

	else:
		fire.send(_path, {})
		return jsonify({
				'message' : {
					'description' : f'Unique ID {uid} has been deleted from Database.'
				}
			})


if __name__ == '__main__':
	app.run(debug = True)
