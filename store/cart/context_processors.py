"""
context_processors is a list of dotted Python paths to callables
that are used to populate the context when a template is rendered with a request. 
These callables take a request object as their argument and return a dict of items
to be merged into the context.
"""

from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}