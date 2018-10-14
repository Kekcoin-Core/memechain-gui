#/usr/bin/env python
# -*- coding: utf-8 -*-
import flask

# Debug
# Set this to 'False' in a production environment.
debug = False

# Initialize Flask App
app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1 # disable caching

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

# Index route: renders the landing/home page from templates.
@app.route("/")
def index():
    return flask.render_template("index.html", isform=False)

def run_server():
    app.run(host='127.0.0.1', port=1133, debug=debug, use_reloader=False, threaded=True)

# Run app
if __name__ == '__main__':
    run_server()