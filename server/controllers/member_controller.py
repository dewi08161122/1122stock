from fastapi import APIRouter, Body, Cookie, Response
from models.member_model import MemberModel
from infrastructure.jwt import JwtModel
import os

ENV = os.getenv("ENV", "development")

router = APIRouter()

@router.post("/api/user")
def sign(body: dict=Body(...)):
    email=body["email"]
    password=body["password"]
    try:
        member = MemberModel.get_member_by_email(email)
        if member is not None:
            return{"error":True,"message":"此信箱已被註冊"}
        success = MemberModel.increase_member(email, password)
        return{"ok":success}
            
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}

@router.get("/api/user/auth")
def check(token: str = Cookie(None)):
    if token is None:
        return {"error": True, "message": "未登入系統"}
    try:
        payload = JwtModel.verify_token(token)
        if "error" in payload:
            return payload
        return {"ok":True, "data":payload["data"]}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器出現未知問題"}
    
@router.put("/api/user/auth")
def login(response: Response, body: dict=Body(...)):
    email=body["email"]
    password=body["password"]
    try:
        member = MemberModel.get_member_by_email(email)
        if member==None:
            return{"error":True,"message":"信箱輸入錯誤"}
        elif member["password"]!=password:
            return{"error":True,"message":"密碼輸入錯誤"}
        else:
            token=JwtModel.create_token(member["id"])
            max_age_seconds = 7 * 24 * 60 * 60
            response.set_cookie(
                key="token", 
                value=token, 
                httponly=True, 
                samesite="lax", 
                secure=True if ENV == "production" else False,
                max_age=max_age_seconds
            )
            return{"ok": True}
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}
@router.delete("/api/user/auth")
def logout(response: Response):
    response.delete_cookie(key="token")
    return {"ok": True}