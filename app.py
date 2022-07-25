
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
	if(request.method == 'GET'):

		from fetch import fire
		path = 'apigee'
		json_data = fire.call(path)
		return jsonify(json_data)

if __name__ == '__main__':
	app.run(debug = True)
