from pony.orm import Required

from base import engine


class Recomendation(engine.Entity):
    """docstring for Lot"""
    date = Required(datetime)
    score = Required(float)
