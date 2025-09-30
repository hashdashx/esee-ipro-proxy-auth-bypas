#!/usr/bin/env python3
# cam.py - simple proxy to add preemptive Basic Auth for snapshot.jpg
# Usage: adjust CAMERA_URL and AUTH_HEADER via environment variables or edit below.
from flask import Flask, Response
import requests
import os

# CONFIG — default values (override with env vars if desired)
CAMERA_URL = os.environ.get("CAMERA_URL", "http://192.168.95.123/snapshot.jpg")
AUTH_HEADER = {"Authorization": os.environ.get("AUTH_HEADER", "Basic YWRtaW46YWRtaW4xMjM=")}

app = Flask(__name__)

@app.route("/snapshot.jpg")
def snapshot():
    try:
        r = requests.get(CAMERA_URL, headers=AUTH_HEADER, timeout=6)
        if r.status_code == 200:
            return Response(r.content, mimetype="image/jpeg")
        return f"Camera returned: {r.status_code}", r.status_code
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    # port dan host default
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8081)))
