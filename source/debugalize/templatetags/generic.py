'''
Created on Jun 4, 2014

@author: Shadi Moodad
'''

from django.template.defaultfilters import register
import logging

log = logging.getLogger(__name__)

@register.filter
def mul(value, coef):
    '''
    Multiply the value via the coef.
    Usage {{your_value|mul:100}}
    '''
    return value*coef;

@register.filter
def sub(value, coef):
    '''
    Substract a coef from value
    Usage {{your_value|sub:5}}
    '''
    return value-coef;

@register.filter
def negate(value):
    '''
    Returns the negative of a value
    Usage {{your_value|negate}}
    '''
    return -value;

@register.filter
def split(value, delim='\\n'):
    """
     Split the value string using the given delimiter and return a list.
     If error happened, it returns it as a single item list
    """
    rt = None
    try:
        rt = str(value).split(delim)
        log.debug("str:%s, split:%s", value, rt)
    except:
        log.warning("Issue with django.filter split. Value: %s, delim: %s", value, delim)
        rt = [value]
        
    return rt