from fastapi import APIRouter, Body, Cookie
from models.function_model import FunctionModel
from infrastructure.jwt import JwtModel

router = APIRouter()

@router.post("/api/holdlist", summary="新增個人持股", tags=["Member Function"])
def increase_hold(body: dict=Body(...),token: str = Cookie(None)):
    if not token:
        return {"error": True, "message": "未登入或憑證已過期"}
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        user_id = int(payload["data"].get("id"))
        number = str(body["number"])
        hold_volume = int(body["hold_volume"])
        hold_price = float(body["hold_price"])
        trade_date = body["trade_date"].replace('/', '-')
        success = FunctionModel.increase_hold(user_id, number, hold_volume, hold_price, trade_date)
        return{"ok":success}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}

@router.put("/api/holdlist", summary="修改單一個股持股紀錄", tags=["Member Function"])
def update_hold(body: dict=Body(...),token: str = Cookie(None)):
    if not token:
        return {"error": True, "message": "未登入或憑證已過期"}
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        user_id = int(payload["data"].get("id"))
        id = int(body["id"])
        hold_volume = int(body["hold_volume"])
        hold_price = float(body["hold_price"])
        trade_date = body["trade_date"].replace('/', '-')
        if hold_volume == 0:
            success = FunctionModel.delete_hold_by_id(user_id, id)
            return{"ok":success}
        success = FunctionModel.put_hold(id, user_id, hold_volume, hold_price, trade_date)
        return{"ok":success}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}   
     
@router.delete("/api/holdlist/stock/{number}", summary="刪除單一個股所有持股紀錄", tags=["Member Function"])
def delete_stock_all(number: str, token: str = Cookie(None)):
    if not token:
        return {"error": True, "message": "未登入或憑證已過期"}
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        user_id = int(payload["data"].get("id"))
        success = FunctionModel.delete_hold_by_number(user_id, number)
        return{"ok":success}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}

@router.delete("/api/holdlist/single/{id}", summary="刪除單一個股的一筆紀錄", tags=["Member Function"])
def delete_single_record(id: int, token: str = Cookie(None)):
    if not token:
        return {"error": True, "message": "未登入或憑證已過期"}
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        user_id = int(payload["data"].get("id"))
        success = FunctionModel.delete_hold_by_id(user_id, id)
        return{"ok":success}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}

@router.get("/api/holdlist", summary="取得會員持股紀錄", tags=["Member Function"])
def get_holdlist(token: str = Cookie(None)):
    if not token:
        return {"error": True, "message": "未登入或憑證已過期"}
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        user_id = int(payload["data"].get("id"))
        data = FunctionModel.get_hold(user_id)
        return {"ok": True, "data": data}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}
    
@router.get("/api/holdlist/stock/{number}", summary="取得單一個股所有持股紀錄", tags=["Member Function"])
def get_holdlist_stock(number: str, token: str = Cookie(None)):
    if not token:
        return {"error": True, "message": "未登入或憑證已過期"}
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        user_id = int(payload["data"].get("id"))
        data = FunctionModel.get_hold_by_number(user_id, number)
        return {"ok": True, "data": data}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}