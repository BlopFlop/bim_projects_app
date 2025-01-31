from project.endpoints.bim_model import router as bim_model_router
from project.endpoints.model_section import router as model_section_router
from project.endpoints.project import router as project_router
from project.endpoints.revit_server import router as revit_server_router

__all__ = [
    "bim_model_router",
    "model_section_router",
    "project_router",
    "revit_server_router"
]
