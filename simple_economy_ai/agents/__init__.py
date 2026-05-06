# -*- coding: utf-8 -*-
"""
Agents Model from the 
Simple Economic Model
"""

import datetime
from EcoSimpy import DiscreteEventAgent
from .agents import EconomicAgent
from .household import Household
from .firm import CGFirm




__title__ = 'simple_economy'
__version__ = '0.0.0'
__license__ = 'GPL-3.0'
__copyright__ = 'Copyright %s Ecos_p Team' % datetime.date.today().year


__all__ = ["Household", "CGFirm"]

