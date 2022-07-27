
from flask import Flask, request, jsonify
from fetch import fire
import json

app = Flask(__name__)

@app.route('/createuser', methods=['POST'])
def create_user():
	content_type = request.headers.get('Content-Type')
	count = fire.call('counter')
	uid = count+1
	fire.send('counter', uid)
	_path = f"apigee/{uid}"

	if content_type == 'text/plain':
		content = request.get_data().decode('ascii')
		content = fire.decodeit(content)
		content = json.loads(content)
		content['unique_ID'] = uid
		
		fire.send(_path, content)
		content = json.dumps(content)
		content = fire.encodeit(content)
		return content, 201

	elif content_type == 'application/json':
		content = request.json
		
		content['unique_ID'] = uid
		fire.send(_path, content)
		return content, 201
		

@app.route('/updateuserbyid/<uid>', methods=['PUT'])
def update_user_by_id(uid):
	content_type = request.headers.get('Content-Type')
	_path = f"apigee/{uid}"
	jsondata = fire.call(_path)

	if jsondata == None:
		return jsonify({
			'error' : {
				'description' : f'Unique ID {uid} not Found in Database.'
			}
		})

	elif content_type == 'text/plain':
		content = request.get_data().decode('ascii')
		content = fire.decodeit(content)
		content = json.loads(content)

		try:
			jsondata['fname'] = content['fname']
		except:
			pass

		try:
			jsondata['lname'] = content['lname']
		except:
			pass

		try:
			jsondata['age']   = content['age']
		except:
			pass
		
		fire.send(_path, jsondata)
		content = json.dumps(jsondata)
		content = fire.encodeit(content)
		return content, 201
		
	elif content_type == 'application/json':
		content = request.json

		try:
			jsondata['fname'] = content['fname']
		except:
			pass

		try:
			jsondata['lname'] = content['lname']
		except:
			pass

		try:
			jsondata['age']   = content['age']
		except:
			pass

		fire.send(_path, jsondata)
		return jsondata, 201

	else:
		return jsonify({
			'error' : {
				'description' : f'content_type = {content_type} is not Supported.'
			}
		})


@app.route('/getallusers')
def get_all_users():
	content = fire.call('apigee')
	content = json.dumps(content)
	content = fire.encodeit(content)
	return content, 200


@app.route('/getuserbyid/<uid>')
def get_user_by_id(uid):
	_path = f'apigee/{uid}'
	content = fire.call(_path)

	if content == None:
		return jsonify({
			'error' : {
				'description' : f'Unique ID {uid} not Found in Database.'
			}
		})

	else:
		content = json.dumps(content)
		content = fire.encodeit(content)
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
