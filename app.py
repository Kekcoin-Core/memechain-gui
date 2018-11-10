#/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import os, requests

from utils import MemeTimeline, Pagination

# Debug
# Set this to 'False' in a production environment.
debug = False

# Initialize Flask App
app = flask.Flask(__name__)

# Config
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1 # disable caching
app.config['UPLOAD_FOLDER'] = './'
ALLOWED_EXT = ["jpg", "png", "gif"]

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route("/")
@app.route('/<int:page>')
def index(page=1):
    p = Pagination(per_page=5, current_page=page)

    timeline = MemeTimeline.find_paginated(p)
    return flask.render_template('index.html', timeline=timeline, pagination=p, isForm=False)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = flask.request.files['image']
    fpath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    ext = file.filename.split('.')[-1]

    if ext in ALLOWED_EXT:
        # TODO: Sightengine check

        if ext == 'jpg':
            ext = 'jpeg'
        headers = {'Content-Type' : 'image/%s' % ext.lower()}

        req = requests.post("http://95.179.132.93:1337/api/addmeme", data=file.read(), stream=True, headers=headers)
        json_response = req.json()

        try:
            if json_response['success'] == True:
                return flask.redirect('/upload-success')

        except KeyError as e:
            return flask.abort(400)
    
    else:
        return flask.abort(400)

@app.route('/upload-success')
def upload_success():
	return flask.render_template('upload-success.html')

@app.route('/settings')
def settings():
	return flask.render_template('settings.html')

def run_server():
    app.run(host='127.0.0.1', port=1133, debug=debug, use_reloader=False, threaded=True)

# Run app
if __name__ == '__main__':
    run_server()