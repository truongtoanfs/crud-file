from pydantic import BaseModel


class Create_Product(BaseModel):
    name: str
    new_price: int = 0
    old_price: int = 0
    total: int = 0
    sold: int = 0
    description: str | None = None


class Update_Product(Create_Product):
    name: str | None = None


class Product(Create_Product):
    product_id: str


class Delete_Module(BaseModel):
    status: str = "Success"
