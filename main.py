from fastapi import FastAPI
from routers.analytics import analytics_router
from routers.auth import auth_router
from routers.categories import categories_router
from routers.transactions import transaction_router

app = FastAPI()

app.include_router(analytics_router)
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(transaction_router)