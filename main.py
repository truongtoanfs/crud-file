from fastapi import FastAPI
import routers.products as products

app = FastAPI()

app.include_router(products.router)
