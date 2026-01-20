from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile, File
from services.market_data import get_stock_summary
from services.analyze_pie import analyze_pie
import pandas as pd

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
def analyze_stock(request: Request, symbol: str = Form(...)):
    try:
        data = get_stock_summary(symbol)
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "data": data}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": str(e)}
        )

@app.post("/pie/analyze")
def analyze_pie_view(
    request: Request,
    pie_name: str = Form(...),
    input_method: str = Form(...),
    symbols: list[str] = Form(default=[]),
    shares: list[int] = Form(default=[]),
    csv_file: UploadFile = File(None),
):

    if input_method == "manual":
        positions = []

        pie = pd.DataFrame({
            "symbols": symbols,
            "shares": shares})
    
    else:
        pie = pd.read_csv(csv_file.filename)
        if "current_price" and "normalized_highest_price_30d_list" in pie.columns:
            pie.columns = ["symbols", "shares", "current_price", "normalized_highest_price_30d_list"]
        else:
            pie.columns = ["symbols", "shares"]
        for idx, symbol in enumerate(pie['symbols']):
            pie["symbols"][idx] = symbol.upper()
    
    pie, pie_data = analyze_pie(pie)
    pie.to_csv(f'{pie_name}.csv', index=False)
    return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": pie_data}
        )

