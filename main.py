from threading import Thread, Lock
import logging
import webview
import time
from app import run_server

server_lock = Lock()

logger = logging.getLogger(__name__)

def url_ok(url, port):
    # Use httplib on Python 2
    try:
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection

    try:
        conn = HTTPConnection(url, port)
        conn.request("GET", "/")
        r = conn.getresponse()
        return r.status == 200
    except:
        logger.exception("Server not started")
        return False

if __name__ == '__main__':
    logger.debug("Starting server")
    t = Thread(target=run_server)
    t.daemon = True
    t.start()
    logger.debug("Checking server")

    while not url_ok("127.0.0.1", 1133):
        time.sleep(0.1)

    logger.debug("Server started")
    webview.create_window("Kekcoin Memechain",
                          "http://127.0.0.1:1133",
                          min_size=(640, 480))