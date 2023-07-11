from fastapi import FastAPI

from src.api.endpoints import router as api_router
from src.main.views import router as shop_router
from src.settings import static, media

app = FastAPI(title='Project')

app.include_router(router=api_router)
app.include_router(router=shop_router)

app.mount(path='/static', app=static, name='static')
app.mount(path='/media', app=media, name='media')