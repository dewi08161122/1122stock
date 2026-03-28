from fastapi import APIRouter
from models.today_market_model import dayModel
from infrastructure.connection import get_connection

router = APIRouter()

@router.get("/api/todaymarket")
def gettodaymarket():
    try:
        with get_connection() as con:
            with con.cursor(dictionary=True) as cursor:
                TAIEX_information = dayModel.get_TAIEX_information_today(cursor)
                TPEX_information = dayModel.get_TPEX_information_today(cursor)
                TAIEX_market = dayModel.get_market_today(cursor,TAIEX_information["time"],"上市")
                TPEX_market = dayModel.get_market_today(cursor,TPEX_information["time"],"上櫃")
                data={"TAIEX_information":TAIEX_information,"TPEX_information":TPEX_information,"TAIEX_market":TAIEX_market,"TPEX_market":TPEX_market}
                return data
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}