#!/usr/bin/env python


class TiendaMobilError(Exception):
    """Base class for Tienda Mobil errors"""

    @property
    def message(self):
        '''Returns the first argument used to construct this error.'''
        return self.args[0]



