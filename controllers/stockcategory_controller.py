from fastapi import APIRouter, Query
from models.search_model import SearchModel

router = APIRouter()
    
@router.get("/api/stockcategory")
def getstockcategory():
    try:
        stockcategory = SearchModel.get_category()
        if stockcategory is None: 
            return {"error": True, "message": "查無資料"}
        return stockcategory
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}

@router.get("/api/categorystock")
def getcategorystock(category_name: str = Query(None)):
    try:
        if category_name is None:
            return {"error": True, "message": "請提供產業名稱"}
        categorystock = SearchModel.get_categorystock(category_name)
        if categorystock is None: 
            return {"error": True, "message": "此產業別無股票代碼"}
        return categorystock
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}