
from flask import Flask, request, jsonify
from fetch import fire

app = Flask(__name__)

@app.route('/createuser', methods=['GET', 'POST'])
def create_user():
	content_type = request.headers.get('Content-Type')
	if content_type == 'application/json':
		content = request.json

		count = fire.call('counter')
		fire.send('counter', count+1)

		uid = content['unique_ID'] = count+1
		_path = f"apigee/{uid}"

		fire.send(_path, content)
		return jsonify(content)


@app.route('/getallusers')
def get_all_users():
	data = fire.call('apigee')
	return jsonify(data)


@app.route('/getuserbyid/<uid>')
def get_user_by_id(uid):
	json_data = fire.call(f'apigee/{uid}')

	if json_data == None:
		return jsonify({
			'error' : {
				'description' : f'Unique ID {uid} not Found in Database.'
			}
		})
	else:
		return jsonify(json_data)

@app.route('/deleteuserbyid/<uid>', methods=['GET', 'POST', 'DELETE'])
def delete_user_by_id(uid):
	_path = f"apigee/{uid}"

	if fire.call(_path) == None:
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
