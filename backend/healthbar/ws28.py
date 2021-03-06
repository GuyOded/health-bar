"""
Healthbar implementation that interfaces with the ws28 led strip
"""
from healthbar.base import HealthBarBase
import board
import neopixel
import math


class WS28HealthBar(HealthBarBase):
    HEALTH_BAR_LENGTH = 60
    DEFAULT_COLOR = (0, 127, 0)

    def __init__(self, *args, **kwargs):
        super.__init__(length=WS28HealthBar.HEALTH_BAR_LENGTH, *args, **kwargs)
        self.__pixels = neopixel.NeoPixel(board.D18, self.HEALTH_BAR_LENGTH)
    
    def draw(self):
        self.__pixels = [WS28HealthBar.DEFAULT_COLOR for i in range(0, math.floor(self.value))]
