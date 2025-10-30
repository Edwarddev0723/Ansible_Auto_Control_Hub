from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth, 
    inventory, 
    playbooks, 
    deployments, 
    settings, 
    ai_assistant
)

api_router = APIRouter()

# (模組 1)
api_router.include_router(auth.router, prefix="/auth", tags=["1. Auth & Users"])
# (模組 2)
api_router.include_router(inventory.router, prefix="/inventory", tags=["2. Inventory (Hosts)"])
# (模組 3)
api_router.include_router(playbooks.router, prefix="/playbooks", tags=["3. Playbooks"])
# (模組 4 & 5)
api_router.include_router(deployments.router, prefix="/deployments", tags=["4. Deployments & History"])
# (模組 6)
api_router.include_router(settings.router, prefix="/settings", tags=["6. System Settings"])
# (模組 7)
api_router.include_router(ai_assistant.router, prefix="/ai", tags=["7. AI Assistant"])