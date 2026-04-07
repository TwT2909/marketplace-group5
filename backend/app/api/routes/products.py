import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.product import Product
from app.schemas.product import ProductOut, ProductUpdate
from app.core.security import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

MEDIA_DIR = "media/products"


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/my", response_model=list[ProductOut])
def my_products(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.owner_id == current_user.id).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    name: str = Form(...),
    description: str | None = Form(None),
    price: float = Form(...),
    quantity: int = Form(...),
    image: UploadFile | None = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if price <= 0:
        raise HTTPException(status_code=400, detail="Цена должна быть больше 0")
    if quantity < 0:
        raise HTTPException(status_code=400, detail="Количество не может быть отрицательным")

    image_url = None
    if image:
        ext = os.path.splitext(image.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        path = os.path.join(MEDIA_DIR, filename)
        with open(path, "wb") as f:
            f.write(await image.read())
        image_url = f"/{path}"

    product = Product(
        owner_id=current_user.id,
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        image_url=image_url,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    data: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к этому товару")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к этому товару")

    db.delete(product)
    db.commit()
