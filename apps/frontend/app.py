from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.backend.api.route import router as eco_router

app = FastAPI()

# CORS (IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES
app.include_router(eco_router)