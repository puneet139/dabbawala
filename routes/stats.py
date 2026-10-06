from datetime import datetime, date
from fastapi import APIRouter, Depends, Query, HTTPException
from database import get_session
from models import Order, OrderStatus
from sqlmodel import Session, select, func
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/daily_orders")
def daily_orders(summary_date: date = Query(..., description="Date for which to get the daily order count"),
                 session: Session = Depends(get_session)):
    
    if summary_date is None:
        summary_date = date.today()  # Default to today's date if not provided
    try:
        start_datetime = datetime.combine(summary_date, datetime.min.time())
        end_datetime = datetime.combine(summary_date, datetime.max.time())

        summary  = {}
        total = 0

        for status in OrderStatus:
            count = session.exec(
                select(func.count(Order.id))
                .where(Order.status == status)
                .where(Order.created_at >= start_datetime)
                .where(Order.created_at <= end_datetime)
            ).one()
            summary[str(status)] = count
            total += count

        daily_count = {"total": total, "summary": summary}
        
        return {"date": summary_date, "daily_order_count": daily_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))