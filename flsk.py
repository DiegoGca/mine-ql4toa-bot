
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>hello world<h1>'

@app.route('/test/', strict_slashes=False)
def test():
    return '<h1>test<h1>'


@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
    print (request.is_json)
    content = request.get_json()
    print (content)
    return 'JSON posted'



if __name__ == '__main__':
    app.run(host='0.0.0.0')