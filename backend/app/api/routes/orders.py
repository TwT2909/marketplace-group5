from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderOut
from app.core.security import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not data.items:
        raise HTTPException(status_code=400, detail="Заказ должен содержать хотя бы один товар")

    products_to_update = []

    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Товар {item.product_id} не найден")
        if product.owner_id == current_user.id:
            raise HTTPException(status_code=400, detail=f"Нельзя купить собственный товар ({product.name})")
        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточно товара '{product.name}': доступно {product.quantity}, запрошено {item.quantity}",
            )
        products_to_update.append((product, item.quantity))

    order = Order(buyer_id=current_user.id, status="created")
    db.add(order)
    db.flush()

    for product, quantity in products_to_update:
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            price_at_order=product.price,
        )
        db.add(order_item)
        product.quantity -= quantity

    db.commit()
    db.refresh(order)
    return order


@router.get("/my", response_model=list[OrderOut])
def my_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.buyer_id == current_user.id).all()


@router.patch("/{order_id}/complete", response_model=OrderOut)
def complete_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    if order.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к этому заказу")
    if order.status != "created":
        raise HTTPException(status_code=400, detail="Заказ уже завершён")
    order.status = "completed"
    db.commit()
    db.refresh(order)
    return order


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    if order.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к этому заказу")
    return order
