# -*- coding: utf-8 -*-
"""Spaces module for the Simple Economy model.

Exposes all Space subclasses so that EcoSimpy's SpaceCreator can locate
them by name via ``importlib.import_module("spaces")``.
"""

from .market import Market, CGMarket, LaborMarket

__all__ = ["Market", "CGMarket", "LaborMarket"]
