from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.cart_models import Cart
from schemas.cart_schemas import CartCreate, CartUpdate

router = APIRouter(prefix="/cart", tags=["Cart"])
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/add")
def add_to_cart(data: CartCreate, db: Session = Depends(get_db)):
    # Check if product already exists for this user
    existing_item = db.query(Cart).filter(
        Cart.user_id == data.user_id,
        Cart.product_id == data.product_id
    ).first()

    if existing_item:
        existing_item.quantity += data.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    cart = Cart(
        user_id=data.user_id,
        product_id=data.product_id,
        quantity=data.quantity
    )
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart
@router.get("/user/{user_id}")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    results = []
    for item in cart_items:
        results.append({
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "name": item.product.name,
            "price": item.product.price,
            "image": item.product.image,
            "description": item.product.description
        })
    return results
@router.put("/{cart_id}")
def update_cart(cart_id: int, data: CartUpdate, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if data.quantity <= 0:
        db.delete(cart)
        db.commit()
        return {"message": "Item removed from cart"}

    cart.quantity = data.quantity
    db.commit()
    db.refresh(cart)
    return cart
@router.delete("/{cart_id}")
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(cart)
    db.commit()
    return {"message": "Cart item deleted"}

@router.delete("/user/{user_id}")
def delete_cart_by_user(user_id: int, db: Session = Depends(get_db)):
    carts = db.query(Cart).filter(Cart.user_id == user_id).all()

    if not carts:
        raise HTTPException(status_code=404, detail="No cart items found for this user")

    for cart in carts:
        db.delete(cart)

    db.commit()
    return {"message": f"All cart items deleted for user_id {user_id}"}
