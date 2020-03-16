#!/usr/bin/env python3
'''
Base health bar class.

Implements a base for a health bar logic.
'''
import threading

from abc import ABCMeta, abstractmethod
from time import sleep
from typing import Union

class HealthBarBase(metaclass=ABCMeta):
    '''
    Base class for health bar implementations.
    '''
    def __init__(self, length: int, max_value: Union[int, float] = 100, *, start_at: Union[int, float] = None,
                 interval: float = 0.1):
        self.__length = length
        self.__max_value = max_value
        if start_at is None:
            self.__value = max_value
        else:
            self.value = start_at
        self.__thread = None
        self.__interval = interval
        self.__run = False

    @property
    def length(self):
        '''
        The amount of segments in the bar.
        For example: the amount of LEDs or the amount of characters.
        '''
        return self.__length

    @property
    def max_value(self):
        '''
        The value that represents a full bar.
        '''
        return self.__max_value

    @property
    def value(self):
        '''
        The current value for the health bar.
        '''
        return self.__value

    @value.setter
    def value(self, value):
        '''
        Set the value while keeping the value in range [0, max_value].
        '''
        self.__value = max(0, min(value, self.max_value))

    def set_value(self, value):
        '''
        Sets the value for the current health bar.
        This is the preferred method as it can be overridden by implementing classes.
        Uses the self.value property.
        '''
        self.value = value

    @property
    def interval(self):
        '''
        The refresh interval of the health bar's thread.
        '''
        return self.__interval

    def is_alive(self):
        '''
        Check if the drawing thread is alive.
        '''
        return self.__thread is not None and self.__thread.is_alive()

    def start(self):
        '''
        Starts the thread. If it is already running, does nothing.
        '''
        if self.is_alive():
            return
        self.__run = True
        self.__thread = threading.Thread(target=self.__loop)
        self.__thread.start()

    def stop(self):
        '''
        Stops the thread.
        '''
        if self.is_alive():
            self.__run = False
            self.__thread.join()

    def in_drawing_thread(self):
        '''
        Checks if the current thread is the drawing thread.
        This is meant for implementing healthbars to be able to check whether the draw method
        is called in the drawing thread or called manually.
        '''
        return threading.current_thread() is self.__thread

    @abstractmethod
    def draw(self):
        '''
        Visually display the health bar.
        '''
        raise NotImplementedError

    def __loop(self):
        '''
        Run the loop for the drawing thread.
        '''
        while self.__run:
            self.draw()
            sleep(self.interval)
