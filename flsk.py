import re
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>hello world<h1>'  # TODO: add default page

@app.route('/test/', strict_slashes=False)
def test():
    return '<h1>test<h1>'


@app.route('/postjson/<id>/', methods = ['POST'], strict_slashes=False)
def postJsonHandler(id):
    print(request.is_json)
    content = request.get_json()
    for t in content['tunnels']:
        if t['name'] == id:
            #print(t['name'])
            #print(t['public_url'])
            port = re.search(':[0-9]+',t['public_url']).group(0)
            port = re.search('[0-9]+', port).group(0)
            #print(port)
    return port



if __name__ == '__main__':
    app.run(host='0.0.0.0')