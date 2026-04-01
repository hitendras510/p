import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from contextlib import asynccontextmanager
from apps.backend.services.ai_model import choose_best_route
from apps.backend.api.route import router as eco_router
from apps.backend.api.training import router as training_router
from apps.backend.services.training_sceduler import start_training_scheduler
=======

from apps.backend.api.route import router as eco_router
from apps.backend.core.config import settings
from apps.backend.services.ai_model import choose_best_route
from apps.backend.services.training_scheduler import scheduler

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

>>>>>>> 8c3d578ab632eedee7d285f7a1cce0c2f1edc61d

@asynccontextmanager
async def lifespan(_: FastAPI):
    await scheduler.start()
    yield
    await scheduler.stop()


app = FastAPI(title=settings.APP_NAME, version=settings.VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(eco_router, prefix="/api/v1")
app.include_router(training_router, prefix="/api/v1/train")


@app.get("/")
def home():
    return {"message": "EcoNav AI Running 🚀"}


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.APP_NAME, "version": settings.VERSION}


@app.get("/route")
def get_best_route():
    routes = [
        {"path": ["A", "B", "C"], "distance": 5, "traffic": 3},
        {"path": ["A", "D", "C"], "distance": 6, "traffic": 2},
        {"path": ["A", "E", "C"], "distance": 4, "traffic": 6},
    ]

    best, all_routes = choose_best_route(routes)

    return {"best_route": best, "all_routes": all_routes}
