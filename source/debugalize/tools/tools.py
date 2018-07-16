# -*- coding: UTF-8 -*-
'''
Created on May 22, 2014

@author: Rabih Kodeih
'''
import json
import logging
import math
import re
import types
import random

from django.template.context_processors import csrf
from django.db.models import Q
from django.http.response import HttpResponse
from datetime import  datetime
from math import ceil
import string


import pytz
from django.utils import timezone as djangoTZ

log = logging.getLogger(__name__)

def ajax_response(data, allow_cross_domain=False):
    """ Formats json data as a proper ajax response
    """
    response = HttpResponse(json.dumps(data, ensure_ascii=False, default=json_default_fn), content_type='application/json')
    if allow_cross_domain:
        response["Access-Control-Allow-Origin"] = "*"  
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"  
        response["Access-Control-Max-Age"] = "1000"  
        response["Access-Control-Allow-Headers"] = "Origin, X-Titanium-Id, Content-Type, Accept"
    return response

def is_number(value):
    """ checks whether value is a number (ex: float or int)
    """
    try:
        value + 1
        return True
    except TypeError:
        return False

def timeZoneAware(dateStr):
    return pytz.timezone(djangoTZ.get_current_timezone_name()).localize(datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S'))

#===============================================================================
# DB Query Pagination
#===============================================================================

def paginate_query_set(query_set, page_num, items_per_page):
    tmp = []
    tot = len(query_set)
    for item in query_set[page_num*items_per_page: (page_num + 1)*items_per_page]:
        row = {}
        row['type'] = 'data'
        row['model'] = item
        tmp.append(row)
    if page_num*items_per_page + len(tmp) < tot and len(tmp) > 0:
        tmp.append({'type': 'more', 'page_num': page_num + 1})
    elif page_num*items_per_page + len(tmp) == tot and page_num > 0:
        tmp.append({'type': 'more', 'page_num': page_num + 1, 'last_page': True})
    return tmp


#===============================================================================
# Database String Search
#===============================================================================

def _normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 


def get_search_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
        
        @param query_string: space separated tokens
        @param search_field: list of fields or list of tuples(field name, operator_name) in the model object to search. 
            If a list specified then all fields are filtered by <field_name>__icontains
            if a list of tuple, each tuple contains the field in first position and the operator in the second  
        Usage Example:
            entry_query = get_query(query_string, ['title', 'body',])
            Model.objects.filter(entry_query).order_by('-pub_date')
            
            entry_query = get_query(query_string, [('title', 'startswith'), ('id', 'exact')])
    
    '''
    query = None # Query to search for every search term        
    # terms = _normalize_query(query_string) #note: this shouldn't be used as we have exact and startswith queries
    terms = [query_string.strip()]
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            if type(field_name) == tuple:
                q = Q(**{"%s__%s" % field_name: term})
            else:
                q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def toAutoCompleteMap(uid, label, value):
    return {'id': uid, 'label': label, 'value': value}

def isNumber(nbStr):
    """
     @return: returns true if the given param nbStr is a number
    """
    isNum = False
    
    try:
        float(nbStr)
        isNum = True
    except:
        pass
            
    return isNum

def toFloat(nbr):
    '''
     Check if the nubmer is float then it returns it as is. if not then it checks if number and returns it
     if not then it checks if the input is empty then returns zero otherwise will return the input unchanged
    '''
    if isinstance(nbr, float):
        return nbr
    elif isNumber(nbr):
        return float(nbr)
    else:
        return float(str(nbr)) if str(nbr).strip() != '' else float(0);
    
def toInt(nbr):
    '''
     Check if the nubmer is int then it returns it as is. if not then it checks if number and returns it
     if not then it checks if the input is empty then returns zero otherwise will return the input unchanged
    '''
    if isinstance(nbr, int):
        return nbr
    elif isNumber(nbr):
        return int(float(nbr))
    else:
        return int(str(nbr)) if str(nbr).strip() != '' else int(0);
    
def toIntIfNotNone(nbr):
    """
     Tries to parse the input 'nbr' just if not none.
     @return toInt(nbr) if not None
    """
    if nbr != None:
        return toInt(nbr)
    else:
        return None
    
def toBoolean(token):
    """
     returns true if any of the values 'true', 'True', 1
             False otherwise
    """
    token = str(token).lower()
    if token in ['true', 1]:
        return True
    else:
        return False

   
def defaultContextData(request):
    """"
     Inject in a context the default attributes used in most pages. 
     ctx['user'] if authenticated.
     csrf initialization.
     Adds all parameters of GET/POST into the context.
    """
    

    ctx = {}
    
#     if request.user is not None and request.user.is_authenticated():
#         ctx['user'] = request.user
        
    ctx['is_ajax'] =  request.is_ajax()
    
    ctx.update(csrf(request))
    
    if request.GET:
        ctx.update(request.GET)
            
    if request.POST:
        ctx.update(request.POST)
        
    ctx['request'] = request
    
    return ctx;
    
def populateContextForGrid(ctx, rs, rows, page, sidx, sord):
    """
     Fils the necessary data for the grid in order to be used in the XML data of the JQGrid .
     @param rs: the result set returned from the execution of ModelClass.objects.all() or ModelClass.objects.filter()
     @param rows: number of rowas per page
     @param page: page number
     @sidx: sort index
     @sord: sort order "asc" or "desc".
     
     Note: all those parameters: rows, page, sidx, sord are returned from the JQGrid 
    """
    
    rows = int(rows)
    page = int(page)
    
    totalRecords = rs.count()
    
    sortOn = "-" + sidx if sord == "desc" else sidx
    
    rs = rs.order_by(sortOn)[(page - 1) * rows: page * rows]
    
    ctx['grid'] = list(rs)
    ctx['page'] = page
    ctx['totalRecords'] = totalRecords
    ctx['totalPages'] = math.ceil(float(totalRecords) / rows)
    ctx['rows'] = rows

    
    return ctx;

def week_of_month(dt):
    """ Returns the week of the month for the specified date.
    """

    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))


def nullToEmpty(strIn, defaultStr = ""):
    """
     Same as the Apache common StringUtil.defaultString
     if null or empty it returns the defaultStr
    """
    if strIn == None or strIn.strip() == "":
        return defaultStr
    else:
        return strIn

def json_default_fn(obj):
    """
     default function to handle complex types while dumping to JSON. Below is list of handled types. it is used as part of the json.dumps(default=tools.json_default_fn)
         - datetime: if it has isoformat, it calls d.isoformat()
    """
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        obj
        
def parse_date(strDateIn, dFormat, default=None):
    """
     Parse a date using the given format and if it fails it returns null and just log a debug
     @param strDateIn: date string to parse
     @param dFormat: format of the expected date
    """
    rt = default
    try:
        rt = datetime.strptime(strDateIn, dFormat)
    except:
        log.debug("Coudldn't parse date: %s using format: %s", strDateIn, dFormat)
        
    return rt

def verfication_key():
    
    return  "%0.12d" % random.randint(0,999999999999)
    
def generate_string(size):
    
    
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))    
