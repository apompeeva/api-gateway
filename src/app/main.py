from fastapi import FastAPI

from app.endpoints.auth_endpoints import auth_router
from app.endpoints.transaction_endpoints import transaction_router

app = FastAPI()

app.include_router(auth_router, tags=['auth'])
app.include_router(transaction_router, tags=['trasaction'])
