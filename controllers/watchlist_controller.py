from fastapi import APIRouter, Body, Cookie
from models.function_model import FunctionModel
from infrastructure.jwt import JwtModel

router = APIRouter()

@router.post("/api/watchlist")
def increase_stock(body: dict=Body(...),token: str = Cookie(None)):
    if not token:
        return {"error": True, "message": "未登入或憑證已過期"}
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        user_id = int(payload["data"].get("id"))
        number = str(body["number"])
        success = FunctionModel.increase_observe(user_id, number)
        return{"ok":success}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}
    
@router.delete("/api/watchlist/{number}")
def delete_stock(number: str, token: str = Cookie(None)):
    if not token:
        return {"error": True, "message": "未登入或憑證已過期"}
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        user_id = int(payload["data"].get("id"))
        success = FunctionModel.delete_observe(user_id, number)
        return{"ok":success}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}

@router.get("/api/watchlist")
def get_watchlist(token: str = Cookie(None)):
    if not token:
        return {"error": True, "message": "未登入或憑證已過期"}
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        user_id = int(payload["data"].get("id"))
        data = FunctionModel.get_observe(user_id)
        return {"ok": True, "data": data}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}