import base64
import json
import os

def lambda_handler(event, context):
    headers = event.get("headers", {})
    auth_header = headers.get("Authorization") or headers.get("authorization")

    if not auth_header:
        return {
            "isAuthorized": False,
            "context": {}
        }

    if not auth_header.startswith("Basic "):
        return {
            "isAuthorized": False,
            "context": {}
        }

    try:
        token = auth_header.split(" ")[1]
        decoded = base64.b64decode(token).decode("utf-8")  # format: username:password
        username, password = decoded.split(":", 1)

        expected_password = os.environ.get(username)
        if expected_password == password:
            return {
                "isAuthorized": True,
                "context": {
                    "user": username
                }
            }
        else:
            return {
                "isAuthorized": False,
                "context": {}
            }

    except Exception as e:
        return {
            "isAuthorized": False,
            "context": {}
        }
