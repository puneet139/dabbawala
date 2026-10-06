from fastapi import APIRouter, HttpException, Query, Depends
from database import get_session
from models import OrderStatus, Order, OrderCreate, OrderUpdate, OrderStatusLog
from sqlmodel import Session
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=Order)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    new_order = Order(**order.model_dump())
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

@router.get("/", response_model=list[Order])
def list_orders(status: OrderStatus | None = Query(None, description="Filter by status")
                ,created_date : str | None = Query(None, description="Filter by created date"),
                 skip:int = Query(0, ge=0),
                  limit :int = Query(10, ge=1,le=100),session: Session = Depends(get_session)):
    if status:
        orders = session.exec(Order).filter(Order.status == status).offset(skip).limit(limit).all()
    elif created_date:
        try:
            created_date_obj = datetime.strptime(created_date, "%Y-%m-%d")
            orders = session.exec(Order).filter(Order.created_at >= created_date_obj).offset(skip).limit(limit).all()
        except ValueError:
            raise HttpException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    else:
        orders = session.exec(Order).offset(skip).limit(limit).all()
    return orders
