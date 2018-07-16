'''
Created on Jun 15, 2012

@author: Shadi Moodad
'''
from django.template.defaultfilters import register
from django.contrib.humanize.templatetags.humanize import intcomma, naturaltime,\
    naturalday
import datetime
import pytz
from debugalize.tools import tools


@register.filter
def lookup(value, dictIn, default=''):
    '''
    Lookup a value in dictionary. if not found it returns the value as is
    '''

    if dictIn:
        return dictIn.get(value, default)
    else:
        return default
    
@register.filter
def split(value, separator = ','):
    '''
    Slipt the value using the input separator. Default separator is ','
    '''
    if value:
        return value.split(separator)
    else:
        return value
    
@register.filter
def in_list(value, input_list):
    '''
     Returns true if the value is in the input_list
    '''
    if input_list:
        return value in input_list
    else:
        return False

@register.filter
def writeCommaIfValueExists(value):
    '''
    Write a comma before the value if existed
    '''

    if value is not None and value:
        return ", "+value
    else:
        return "";
    
@register.filter
def currency(value):
    '''
     format a currency
    '''
    nbr = tools.toFloat(value)
    dollars = round(nbr, 2)
    return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])

@register.filter
def naturalDT(dateTime):
    '''
     If the date is less than 8 hours it shows ellapsed hours using naturaltime
     if date is less than a week it shows it using naturaldate
     else format as the given python datetime format string
    '''
    strDate = dateTime
    
    today = datetime.datetime.now(pytz.UTC)
    if(dateTime >= (today - datetime.timedelta(hours=6))):
        strDate = naturaltime(dateTime)
    else: #if(dateTime >= (today - datetime.timedelta(days=3))):
        strDate = "%s %s" % (naturalday(dateTime, "M d, Y "), dateTime.strftime("%H:%M"))
    
    return strDate
    
@register.filter
def to_str(value):
    '''
    Lookup a value in dictionary. if not found it returns the value as is
    '''
    return str(value)

@register.filter
def getValueOf(inLst,index):
    return inLst[index]