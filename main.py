from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables
from routes.orders import router as orders_router
from routes.stats import router as stats_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    create_db_and_tables()
    yield
    # Shutdown code (if any)

app = FastAPI(lifespan=lifespan)

app.include_router(orders_router)
app.include_router(stats_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)