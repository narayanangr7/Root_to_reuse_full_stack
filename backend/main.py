from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from db.database import Base, engine
from routers.user_router import router as user_router
from routers.prodect_router import router as prodect_router
from routers.category_routers import router as catagory_router
from routers.volunteer_router import router as volunteer_router
from routers.camp_router import router as camp_router
from routers.cart_routers import router as cart_routers
from routers.order_router import router as order_router

# Initialize FastAPI with the /api root path for production routing
app = FastAPI(title="Root to Reuse API", root_path="/api")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"BACKEND CRITICAL ERROR: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "detail": str(exc)},
        headers={"Access-Control-Allow-Origin": "*"}
    )

# Database Initialization
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database initialization skipped or failed: {e}")

# Health-check Endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Root to Reuse API is running"}

# Include Routers
app.include_router(prodect_router)
app.include_router(user_router)
app.include_router(catagory_router)
app.include_router(volunteer_router)
app.include_router(camp_router)
app.include_router(cart_routers)
app.include_router(order_router)
