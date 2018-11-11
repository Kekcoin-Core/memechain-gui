#/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import os, requests

from sightengine.client import SightengineClient

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
    p = Pagination(per_page=4, current_page=page)

    timeline = MemeTimeline.find_paginated(p)
    return flask.render_template('index.html', timeline=timeline, pagination=p, isForm=False)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = flask.request.files['image']
    fpath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    ext = file.filename.split('.')[-1]

    file_read = file.read()

    if ext in ALLOWED_EXT:
        sightclient = SightengineClient("1347331372", "BhoFasNuF3zAGp8XSRXi")

        sight_output = sightclient.check('nudity').set_bytes(file_read)

        if sight_output['nudity']['safe'] > 0.5:
            if ext == 'jpg':
                ext = 'jpeg'
            headers = {'Content-Type' : 'image/%s' % ext.lower()}

            req = requests.post("http://95.179.132.93:1337/api/addmeme", data=file_read, stream=True, headers=headers)
            json_response = req.json()

            try:
                if json_response['success'] == True:
                    return flask.render_template('upload-success.html')

            except KeyError as e:
                error_msg = json_response['description']
                return flask.render_template('upload-failed.html', error_msg = error_msg)

        else:
            error_msg = "Meme image has not passed profanity filter. Please do not upload offensive materials."
            return flask.render_template('upload-failed.html', error_msg = error_msg) 
    
    else:
        error_msg = "Meme file extension not supported."
        return flask.render_template('upload-failed.html', error_msg = error_msg)

@app.route('/settings')
def settings():
	return flask.render_template('settings.html')

def run_server():
    app.run(host='127.0.0.1', port=1133, debug=debug, use_reloader=debug, threaded=True)

# Run app
if __name__ == '__main__':
    run_server()