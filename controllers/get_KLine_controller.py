from fastapi import APIRouter
from models.get_KLine_model import KLineModel

router = APIRouter()
    
@router.get("/api/stock/TAIEX")
def getTAIEXKLine():
    try:
        TAIEXKLine = KLineModel.get_TAIEX_KLine()
        if TAIEXKLine is None: 
            return {"error": True, "message": "無此股票代碼"}
        return TAIEXKLine
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}
    
@router.get("/api/stock/TPEX")
def getTPEXKLine():
    try:
        TPEXKLine = KLineModel.get_TPEX_KLine()
        if TPEXKLine is None: 
            return {"error": True, "message": "無此股票代碼"}
        return TPEXKLine
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}
    
@router.get("/api/stock/{number}")
def getStockKLine(number: str):
    try:
        StockKLine = KLineModel.get_stock_KLine(number)
        if StockKLine is None: 
            return {"error": True, "message": "無此股票代碼"}
        return StockKLine
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}