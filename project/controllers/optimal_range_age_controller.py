from sanic.response import json
from .base_controller import BaseController


class OptimalRangeAgeController(BaseController):
    async def get(self, request, arg):
        return json({'OptimalRangeAge': 'controller'})
