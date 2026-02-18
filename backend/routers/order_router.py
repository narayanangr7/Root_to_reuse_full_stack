from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.order_models import Order
from schemas.order_schemas import OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    order = Order(
        user_id=data.user_id,
        product_id=data.product_id,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

# Get orders by user
@router.get("/user/{user_id}")
def get_orders(user_id: int, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.user_id == user_id).all()


@router.put("/update/{order_id}")
def update_order_status(
    order_id: int,
    data: OrderUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        return {"error": "Order not found"}

    order.product_states = data.product_states
    db.commit()
    db.refresh(order)

    return order
