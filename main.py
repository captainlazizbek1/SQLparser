from fastapi import FastAPI, Request, HTTPException, Form
from sqlalchemy import create_engine, text
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles as StaticFiles
from starlette.templating import Jinja2Templates
from termcolor import colored  #OPTIONAL


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
async def root():
    return {
        "message": "Проект работает корректно"
    }


@app.get('/form')
async def display_form(request: Request):
    template = "form.html"
    context = {"request": request}
    return templates.TemplateResponse(
        template, context
    )


@app.post('/testing', response_class=HTMLResponse)
async def testing(request: Request,
                  username: str = Form(...),
                  password: str = Form(...),
                  host: str = Form(...),
                  port: int = Form(...),
                  db_name: str = Form(...),
                  username2: str = Form(...),
                  password2: str = Form(...),
                  host2: str = Form(...),
                  port2: str = Form(...),
                  db_name2: str = Form(...)):
    try:
        source_db_engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{db_name}", echo=True)
        source_db_engine = source_db_engine.connect()
        source_db_query = text("SELECT * FROM students;")
        source_db_data = source_db_engine.execute(source_db_query).fetchall()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Can not connect to Source database <br> Error: {str(e)}"
        )
    try:
        target_db = create_engine(f"postgresql://{username2}:{password2}@{host2}:{port2}/{db_name2}", echo=True)
        target_db = target_db.connect()
        for row in source_db_data:
            parse_query = text(f"INSERT INTO students(name, last_name, stage) VALUES {row}")
            target_db.execute(parse_query)
        target_db.commit()
        print(colored("Data has been parsed successfully", "green"))
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Can not connect ot Target database <br> Error: {str(e)}"
        )
    template = 'parse.html'
    context = {'request': request, 'data': 75, 'db_name': db_name}
    return templates.TemplateResponse(
        template, context
    )


