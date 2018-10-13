#/usr/bin/env python
# -*- coding: utf-8 -*-
import flask

# Debug
# Set this to 'False' in a production environment.
debug = True

# Initialize Flask App
app = flask.Flask(__name__)

# Index route: renders the landing/home page from templates.
@app.route("/")
def index():
    return flask.render_template("index.html", isform=False)

# Run app
if __name__ == '__main__':
    if debug:
        app.run(host='127.0.0.1', port=1133, debug=True)
    else:
        app.run()