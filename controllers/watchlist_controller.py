from fastapi import APIRouter, Body, Cookie
from models.function_model import FunctionModel
from infrastructure.jwt import JwtModel
from datetime import timedelta, date

router = APIRouter()

@router.post("/api/watchlist")
def increase(body: dict=Body(...),token: str = Cookie(None)):
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        user_id = payload["data"].get("id")
        number = body["number"]
        success = FunctionModel.increase_observe(user_id, number)
        return{"ok":success}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}
    
@router.delete("/api/watchlist")
def delete(body: dict=Body(...),token: str = Cookie(None)):
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        user_id = payload["data"].get("id")
        number = body["number"]
        success = FunctionModel.delete_observe(user_id, number)
        return{"ok":success}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}

@router.get("/api/watchlist")
def check(token: str = Cookie(None)):
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        user_id = payload["data"].get("id")
        trade_date = date.today()
        data = FunctionModel.get_observe(user_id, trade_date)
        retry_limit = 10
        while not data and retry_limit > 0:
            trade_date -= timedelta(days=1)
            retry_limit -= 1
            if trade_date.weekday() >= 5:
                continue
            data = FunctionModel.get_observe(user_id, trade_date)
        return {"ok": True, "data": data}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}