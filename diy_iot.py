from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from modules.dashboard import app as dashboard_app
from modules.api import router
from starlette.responses import RedirectResponse
import uvicorn
from modules.db import db
import os
from fast_pony_crud import create_crud_routes

server = FastAPI()
server.include_router(router,prefix="/api",tags=["Device IO"])
create_crud_routes(db,server,"/db",os.environ.get("API_KEY"))

server.mount("/dash", WSGIMiddleware(dashboard_app.server))
@server.get("/",include_in_schema=False)
async def redirect():
    return RedirectResponse(url="/dash/")


if __name__ == "__main__":
    uvicorn.run(server,port=5000,host="0.0.0.0")