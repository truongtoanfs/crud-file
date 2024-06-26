from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from model.pydantic import Create_Product, Update_Product, Product, Delete_Module
import json
import uuid

router = APIRouter(prefix="/products", tags=["Products"])


database = {"data": []}


def write_Database():
    with open("database/products.json", "w") as fp:
        json.dump(database, fp)
        print("Database updated and saved.")


def read_Database():
    try:
        with open("database/products.json", "r") as fp:
            global database
            database = json.load(fp)
    except FileNotFoundError:
        write_Database()
        print("Setup Database Success.")


read_Database()


def find_product_id(product_id: str):
    product_index = None
    for index, product in enumerate(database["data"]):
        if product["product_id"] == product_id:
            product_index = index
            break
    if product_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return product_index


@router.get("/", response_model=list[Product])
def get_products(
    limit: Annotated[int | None, Query(description="Default value: all", gt=0)] = None,
    offset: Annotated[int | None, Query(gt=0)] = 1,
    product_name: str | None = None,
):
    products = []
    if product_name is not None:
        for product in database["data"]:
            if product["name"].find(product_name) > -1:
                products.append(product)
    else:
        products = list(database["data"])

    start = 0
    end = 0
    if limit is not None:
        start = (offset - 1) * limit
        end = start + limit
        return products[start:end]
    return products[start:]


@router.get("/{product_id}", response_model=Product)
def get_product_detail(product_id: str):
    product_index = find_product_id(product_id)
    return database["data"][product_index]


@router.post("/", response_model=Product)
def create_product(product: Create_Product):
    product_data = {"product_id": str(uuid.uuid4()), **product.model_dump()}
    database["data"].append(product_data)
    write_Database()
    return product_data


@router.patch("/{product_id}", response_model=Product)
def update_product(product_id: str, product: Update_Product):
    product_index = find_product_id(product_id)
    current_value = database["data"][product_index]
    stored_model = Product(**current_value)
    updated_value = product.model_dump(exclude_unset=True)
    update_model = stored_model.model_copy(update=updated_value)
    database["data"][product_index] = jsonable_encoder(update_model)
    write_Database()
    return database["data"][product_index]


@router.delete("/{product_id}", response_model=Delete_Module)
def delete_product(product_id: str):
    product_index = find_product_id(product_id)
    del database["data"][product_index]
    write_Database()
    return {"status": "Success"}
