from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from dashboard import app


server = FastAPI()
server.mount("/dash", WSGIMiddleware(app.server))