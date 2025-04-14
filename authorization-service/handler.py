import base64
import json
import os

def lambda_handler(event, context):
    headers = event.get("headers", {})
    auth_header = headers.get("Authorization")

    if not auth_header:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Authorization header missing"})
        }

    if not auth_header.startswith("Basic "):
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "Invalid authorization type"})
        }

    try:
        token = auth_header.split(" ")[1]
        decoded = base64.b64decode(token).decode("utf-8")  # format: username:password
        username, password = decoded.split(":", 1)

        expected_password = os.environ.get(username)
        if expected_password != password:
            return {
                "statusCode": 403,
                "body": json.dumps({"message": "Access denied"})
            }

        return {
            "isAuthorized": True,
            "context": {
                "user": username
            }
        }

    except Exception as e:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": f"Error: {str(e)}"})
        }
