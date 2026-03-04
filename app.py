from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
app=FastAPI()

from controllers.today_market_controller import router as todaymarket_router
from controllers.KLine_controller import router as KLine_router
from controllers.stockcategory_controller import router as stockcategory_router
from controllers.member_controller import router as member_router

app.include_router(KLine_router)
app.include_router(todaymarket_router)
app.include_router(stockcategory_router)
app.include_router(member_router)

@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/todaymarket", include_in_schema=False)
async def stockindex(request: Request):
	return FileResponse("./static/todaymarket.html", media_type="text/html")
@app.get("/stockcategory", include_in_schema=False)
async def stockcategory(request: Request):
	return FileResponse("./static/stockcategory.html", media_type="text/html")
@app.get("/hotstock", include_in_schema=False)
async def hotstock(request: Request):
	return FileResponse("./static/hotstock.html", media_type="text/html")
@app.get("/watchlist", include_in_schema=False)
async def watchlist(request: Request):
	return FileResponse("./static/watchlist.html", media_type="text/html")
@app.get("/selfstock", include_in_schema=False)
async def selfstock(request: Request):
	return FileResponse("./static/selfstock.html", media_type="text/html")
@app.get("/stock/{number}", include_in_schema=False)
async def stock(request: Request, number: str):
	return FileResponse("./static/stock.html", media_type="text/html")

app.mount("/css", StaticFiles(directory="public/css"), name="css")
app.mount("/js", StaticFiles(directory="public/javascript"), name="js")
app.mount("/img", StaticFiles(directory="public/image"), name="img")
app.mount("/", StaticFiles(directory="static", html=True))