from fastapi import APIRouter
from models.KLine_model import KLineModel

router = APIRouter()
    
@router.get("/api/stock/{number}")
def getStockKLine(number: str):
    try:
        if number == "TAIEX":
            KLine = KLineModel. get_TAIEX_KLine()
        elif number == "TPEX":
            KLine = KLineModel.get_TPEX_KLine()
        else:    
            KLine = KLineModel.get_stock_KLine(number)
        if KLine is None: 
            return {"error": True, "message": "無此股票代碼"}
        return KLine
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}