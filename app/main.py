from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.router import api_router

app = FastAPI()
app.mount('/static', StaticFiles(directory='app/static'), 'static')
templates = Jinja2Templates(directory='app/templates')

app.include_router(api_router)


@app.get('/')
async def main_page(request: Request):
    return templates.TemplateResponse(
        name='index.html',
        context={'request': request}
    )
