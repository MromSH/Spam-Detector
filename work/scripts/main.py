from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from ..library.model import reteach_model, load_model
from ..library.database_manipulation import add_message
import pickle
import os

app = FastAPI()

df_path = Path(__file__).parent.parent / "Data" / "SMSSpamCollection"
model_path = Path(__file__).parent.parent / 'library' / 'spam_model.pkl'
vectorizer_path = Path(__file__).parent.parent / 'library' / 'vectorizer.pkl'
text_report_path = Path(__file__).parent.parent / "Output" / "text_report.txt"
graphic_report_path = Path(__file__).parent.parent / "Graphics" / "graphic.png"
model_report_path = Path(__file__).parent.parent / "Output" / "model_report.txt"

paths_dict = {"graphic_report": graphic_report_path, 
            "model_report": model_report_path, 
            "text_report": text_report_path}

model, vectorizer = load_model(model_path, vectorizer_path)

app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent.parent/ "work" / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent.parent.parent/ "work" / "templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    text: str = Form(None)
):
    if not text or not text.strip():
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": "Введите текст для проверки", "input_text": ""}
        )
    
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)[0]
    result = "Спам" if prediction == 1 else "Не спам"
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result, "input_text": text}
    )

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

@app.get("/addinfo", response_class=HTMLResponse)
async def addinfo_page(request: Request):
    return templates.TemplateResponse("addinfo.html", {"request": request, "selected_choice": None})

@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    return templates.TemplateResponse("reports.html", {"request": request})

@app.post("/reporting", response_model=None)
async def reporting(
    request: Request
):
    form_data = await request.form()
    report_type = form_data.getlist("report_type")

    if len(report_type) == 0:
        return templates.TemplateResponse(
            "reports.html",
            {"request": request, "result": "Отчеты не выбраны"}
        )
    if len(report_type) == 1:
        file_path = paths_dict[report_type[0]]
        filename = os.path.basename(file_path) 

        return FileResponse(file_path, media_type="application/octet-stream",
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"}
        )
    
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, "w") as zip_file:
        for report in report_type:
            file_path = paths_dict[report]
            filename = os.path.basename(file_path)
            with open(file_path, 'rb') as file_to_zip:
                zip_file.writestr(filename, file_to_zip.read())
    zip_buffer.seek(0)

    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=reports.zip",
            "Content-Length": str(zip_buffer.getbuffer().nbytes)
        }
    )


@app.post("/newinfo", response_class=HTMLResponse)
async def newinfo(
    request: Request,
    text: str = Form(None),
    choice: str = Form(None)
):
    if not text or not text.strip():
        return templates.TemplateResponse(
            "addinfo.html",
            {"request": request, "result": "Введите текст для проверки"}
        )
    if not choice or not choice.strip():
        return templates.TemplateResponse(
            "addinfo.html",
            {"request": request, "result": "Выберите маркер (спам/не спам)", "input_text": text}
        )
    add_message(text, choice, df_path)
    return templates.TemplateResponse(
        "addinfo.html",
        {"request": request, "result": "Запись успешно добавлена", "input_text": "", "selected_choice": None}
    )

@app.post("/reteach", response_class=HTMLResponse)
async def reteach(
    request: Request
):
    reteach_model()
    return templates.TemplateResponse(
        "addinfo.html",
        {"request": request, "result": "Модель переобучена"}
    )