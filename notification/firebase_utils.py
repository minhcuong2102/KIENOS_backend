import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

# Lấy đường dẫn tuyệt đối tới file serviceAccountKey.json trong cùng folder
# cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
if not firebase_admin._apps:
    firebase_key_str = os.environ.get("FIREBASE_KEY")
    firebase_key_dict = json.loads(firebase_key_str.replace("\\n", "\n"))
    cred = credentials.Certificate(firebase_key_dict)
# Chỉ khởi tạo Firebase một lần
# if not firebase_admin._apps:
#     cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

def send_push_notification(device_token, title, body, data=None):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=device_token,
        data=data or {}
    )
    response = messaging.send(message)
    print(response)
    return response
