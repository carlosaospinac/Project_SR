from sanic.response import json
from .base_controller import BaseController


class RecomendationController(BaseController):
    async def get(self, request, arg):
        return json({'Recomendation': 'controller'})
