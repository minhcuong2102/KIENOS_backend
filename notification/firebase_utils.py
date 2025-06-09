import firebase_admin
from firebase_admin import credentials, messaging
import os
import json
from django.conf import settings
# Lấy đường dẫn tuyệt đối tới file serviceAccountKey.json trong cùng folder
# cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
# if not firebase_admin._apps:
#     firebase_key_str = os.environ.get("FIREBASE_KEY")
#     firebase_key_dict = json.loads(firebase_key_str.replace("\\n", "\n"))
#     cred = credentials.Certificate(firebase_key_dict)
# # Chỉ khởi tạo Firebase một lần
# # if not firebase_admin._apps:
# #     cred = credentials.Certificate(cred_path)
#     firebase_admin.initialize_app(cred)
# if not firebase_admin._apps:
#     # Lấy biến môi trường FIREBASE_KEY và đảm bảo không None
#     # firebase_key_str = os.environ.get("FIREBASE_KEY")
#     # if firebase_key_str:
#     #     # Parse key JSON (chuyển các \\n thành \n cho private_key)
#     #     firebase_key_dict = json.loads(firebase_key_str.replace("\\n", "\n"))
#     #     cred = credentials.Certificate(firebase_key_dict)
#     #     firebase_admin.initialize_app(cred)
#     # else:
#     #     raise ValueError("Biến môi trường FIREBASE_KEY chưa được cấu hình.")
#     firebase_b64 = os.environ.get("FIREBASE_KEY")
#     firebase_key_json = base64.b64decode(firebase_b64).decode("utf-8")
#     firebase_key_dict = json.loads(firebase_key_json)
#     cred = credentials.Certificate(firebase_key_dict)
#     firebase_admin.initialize_app(cred)
if firebase_admin._apps:
        return

    private_key = settings.FIREBASE_KEY.replace("\\n", "\n")
    
    cred_dict = {
        "type": "service_account",
        "project_id": "myappnotifications-45b01",
        "private_key_id": "c9460e58ddaaa8440d9e022e76a7e44fb2ec6bae",
        "private_key": private_key,
        "client_email": "firebase-adminsdk-fbsvc@myappnotifications-45b01.iam.gserviceaccount.com",
        "client_id": "114419167223566519552",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40myappnotifications-45b01.iam.gserviceaccount.com"
    }

    cred = credentials.Certificate(cred_dict)
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
