import logging
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from contextlib import asynccontextmanager

from config.settings import settings
from services.sensor_service import SensorService
from api import routes

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instance
sensor_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global sensor_service
    
    # Startup
    logger.info("Starting Smart Agriculture System...")
    sensor_service = SensorService()
    sensor_service.start_logging_loop()
    routes.init_routes(sensor_service)
    logger.info("System ready!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    sensor_service.stop()
    logger.info("Shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="Smart Agriculture System",
    description="IoT-based agricultural monitoring and control system",
    version="2.0.0",
    lifespan=lifespan
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include API routes
app.include_router(routes.router)

# Serve dashboard
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render main dashboard"""
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )