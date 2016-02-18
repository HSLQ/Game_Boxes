# -*- coding: utf-8 -*
# Filename: sliceable_deque.py

# from http://stackoverflow.com/questions/10003143/how-to-slice-a-deque
# __author__ = 'Piratf'

import collections
import itertools

class sliceable_deque(collections.deque):
    def __getitem__(self, index):
        try:
            return collections.deque.__getitem__(self, index)
        except TypeError:
            return type(self)(itertools.islice(self, index.start,
                                               index.stop, index.step))