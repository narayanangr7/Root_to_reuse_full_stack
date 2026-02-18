from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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

# 1. CORE CORS SETTINGS (Broad for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. GLOBAL ERROR DEBUGGER
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"BACKEND CRITICAL ERROR: {exc}")
    # Force CORS headers even on crash
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "detail": str(exc)},
        headers={"Access-Control-Allow-Origin": "*"}
    )

# 3. DB INIT
Base.metadata.create_all(bind=engine)

# 4. ROUTES
app.include_router(prodect_router)
app.include_router(user_router)
app.include_router(catagory_router)
app.include_router(volunteer_router)
app.include_router(camp_router)
app.include_router(cart_routers)
app.include_router(order_router)
