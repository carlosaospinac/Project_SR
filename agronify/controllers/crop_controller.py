from datetime import datetime
from uuid import uuid4

from pony.orm import db_session, select, exists
from sanic.response import json

from .base_controller import BaseController
from models import Crop, Land


class CropController(BaseController):
    async def post(self, request):
        user = request['session'].get('user')
        if not user:
            return self.response_status(401)
        req_land = request.args.get('land')
        req = request.form
        try:
            with db_session:
                if not exists(
                    x for x in Land if x.id == req_land and x.user.id == user
                ):
                    return self.response_status(401)
                Crop(
                    **self.not_null_data(
                        id=uuid4().hex,
                        name=req.get('name'),
                        lot_name=req.get('lot_name'),
                        lot_size=req.get('lot_size'),
                        land=Land[req_land],
                    )
                )
        except Exception as e:
            self.response_status(500)
        return self.response_status(201)

    async def get(self, request, id):
        user = request['session'].get('user')
        if not user:
            return self.response_status(401)
        with db_session:
            if id == 'all':
                req_land = request.args.get('land')
                return self.response_status(
                    200, Crop.select(lambda x: x.land.id == req_land)
                )
            if not Crop.exists(id=id):
                return self.response_status(404)
            return self.response_status(
                200, Crop[id]
            )

    async def patch(self, request, id):
        user = request['session'].get('user')
        if not user:
            return self.response_status(401)
        with db_session:
            if not Crop.exists(id=id):
                return self.response_status(404)
            if Crop[id].land.user.id != user:
                return self.response_status(401)
            req = request.form
            try:
                Crop.get_for_update(id=id)
                changes = self.not_null_data(
                    **dict(
                        (k, v)
                        for k, v in dict(
                            modified=datetime.now(),
                            name=req.get('name'),
                            lot_name=req.get('lot_name'),
                            lot_size=req.get('lot_size'),
                        ).items()
                        if v
                    )
                )
                Crop[id].set(**changes)
                return self.response_status(200, changes)
            except Exception as e:
                return self.response_status(202)

    async def delete(self, request, id):
        user = request['session'].get('user')
        if not user:
            return self.response_status(401)
        with db_session:
            if not Crop.exists(id=id):
                return self.response_status(404)
            if Crop[id].land.id != land:
                return self.response_status(401)
            try:
                Crop.get_for_update(id=id)
                Crop[id].delete()
            except Exception as e:
                self.response_status(500)
            else:
                return self.response_status(200)
