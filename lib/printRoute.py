# -*- coding: utf-8 -*
# Filename: printRoute.py

__author__ = 'Piratf'

import inspect

def printRoute(foo):
    def _deco():
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__
        the_method = stack[1][0].f_code.co_name
        print("  I was called by {}.{}()".format(str(the_class), the_method))
        the_class = stack[2][0].f_locals["self"].__class__
        the_method = stack[2][0].f_code.co_name
        print("  I was called by {}.{}()".format(str(the_class), the_method))
        the_class = stack[3][0].f_locals["self"].__class__
        the_method = stack[3][0].f_code.co_name
        print("  I was called by {}.{}()".format(str(the_class), the_method))
        the_class = stack[4][0].f_locals["self"].__class__
        the_method = stack[4][0].f_code.co_name
        print("  I was called by {}.{}()".format(str(the_class), the_method))
        the_class = stack[5][0].f_locals["self"].__class__
        the_method = stack[5][0].f_code.co_name
        print("  I was called by {}.{}()".format(str(the_class), the_method))
        foo()
    return _deco