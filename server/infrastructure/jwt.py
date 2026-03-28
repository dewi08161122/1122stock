import jwt
import os 
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
SECRET_KEY = os.getenv("JWT_KEY")
ALGORITHM = "HS256"

class JwtModel:
    @staticmethod
    def create_token(user_id):
        payload = {
                    "id": user_id,
                    "exp": datetime.now() + timedelta(days=7)
                }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    @staticmethod
    def verify_token(token: str):
        if not token:
            return {"error": True, "message": "未登入系統，拒絕存取"}
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return {"data":payload}
        except jwt.ExpiredSignatureError:
            return {"error": True, "message": "登入狀態已逾時"}
        except:
            return {"error": True, "message": "登入狀態無效"}