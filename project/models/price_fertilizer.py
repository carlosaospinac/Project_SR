from pony.orm import Required

from .base import engine


class PriceFertilizer(engine.Entity):
    """docstring for Lot"""
    lab = Required("Lab")
    fertilizer = Required("Fertilizer")
    price = Required(float)
