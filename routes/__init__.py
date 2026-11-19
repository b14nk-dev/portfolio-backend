from utils import Router

from .ai import router as ai_router

routes: list[Router] = [Router(router=ai_router, name="ai")]
