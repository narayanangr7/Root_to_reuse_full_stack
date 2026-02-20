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
from models.camp_participant_model import CampParticipant

app = FastAPI(title="Root to Reuse API")

# 1. CORS — allow localhost (dev) + any Vercel deployment (production)
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8000",
    # Allow all Vercel domains for this project
    "https://narayanangr7.vercel.app",
]

# Also support a custom domain set via env variable (e.g. https://roottoreuse.com)
custom_origin = os.getenv("FRONTEND_ORIGIN")
if custom_origin:
    allowed_origins.append(custom_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Keep wildcard so the static frontend served by Vercel works seamlessly
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. GLOBAL ERROR DEBUGGER
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"BACKEND CRITICAL ERROR: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "detail": str(exc)},
        headers={"Access-Control-Allow-Origin": "*"}
    )

# 3. DB INIT
Base.metadata.create_all(bind=engine)

# 4. Health-check (Vercel pings this to verify the function is alive)
@app.get("/api")
async def health_check():
    return {"status": "ok", "message": "Root to Reuse API is running"}

# 5. ROUTES
app.include_router(prodect_router)
app.include_router(user_router)
app.include_router(catagory_router)
app.include_router(volunteer_router)
app.include_router(camp_router)
app.include_router(cart_routers)
app.include_router(order_router)
