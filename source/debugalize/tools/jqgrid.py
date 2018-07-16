'''
Created on Dec 13, 2014

@author: Shadi Moodad
List of tools for JQGrid
'''
from django.forms.models import model_to_dict
from django.db.models.query import Q

import types
import logging

log = logging.getLogger(__name__)

def get_search_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. 
        That combination aims to search keywords within a model by testing the given search fields.
        All fields are in the form of an OR query
        
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
    terms = query_string.split(" ").strip()
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            if type(field_name) == types.TupleType:
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



def build_search_for_model(ModelObject, paramsDict):
    ''' Returns a QuerySet filter for the given model. Fields to be filtered are the one used from paramsDic (e.g. request.GET or request.POST) and it makes sure those fields exists in the model
        
        @param ModelObject: Object model reference. should inherit django.db.models.base.models.Model
        @param paramsDic: dictionary of key/value where key is a field in the ModelObject and value is it's filter value. Note that if not present it is ignored
    
    '''
    query = None # Query to search for every search term        
    model_fields = [f.name for f in ModelObject._meta.get_fields()]
     
    for k,v in paramsDict.items():
        if k in model_fields:
            q = Q(**{"%s__icontains" % k: v})
            if query is None:
                query = q
            else:
                query = query & q
                
    return query


def get_jqgrid_data_json(request, ModelObj, baseFilter = None, methodType='POST', annotate_qset_fn=None, dict_annotation=None):
    """
    Returns the list of objects as JSON based on the request.
    @param request: http request
    @param ModelObj: Object model reference. should inherit django.db.models.base.models.Model
    @param baseFilter:  django.db.models.query.QuerySet. A query set to filter the query of that model before doing the jqgrid filters
    @param methodType: POST or GET based on the configuration in the JQGrid. default is post
    @param annotate_qset_fn: if not none, it will pass the query set as parameter before returning the results. This function should return query set.
    @param dict_annotation: dict_annotation(dict, object) where dict is the model_to_dict(object) and object is a record from query set. 
                            Used to enrich the dictionary and workaround the model_to_dict that doesn't export readonly fields or annotations.
                            Should return dictionary
    
    @return: result as json containing rows, page, records, total
    """
    
    params = request.POST if methodType == 'POST' else request.GET
    
    sidx = params['sidx']
    rows = int(params['rows'])
    is_search = False if params['_search'] == u'false' else True
    sord = params['sord']
    page = int(params['page']) - 1
    
    qset = ModelObj.objects
    
    if baseFilter:
        qset = qset.filter(baseFilter)
    
    if is_search:
#         model_fields = [f.name for f in ModelObj._meta.get_fields()]
#         keys = []
#         values = []
#         for k,v in params.iteritems():
#             if k in model_fields:
#                 keys.append(k)
#                 values.append(v)
        
        qFilter = build_search_for_model(ModelObj, params)
        if qFilter:
            qset = qset.filter(qFilter)
                
    
    recs = qset.count()
    total = recs / rows + 1
    
    qset = qset.order_by('%s%s' % ('-' if sord == u'desc' else '', sidx) )
    
    if annotate_qset_fn:
        qset = annotate_qset_fn(qset)
        
    log.debug("Query to jqgrid: %s", qset.query)
    
    qset = qset[page*rows: (page + 1)*rows]
    
    if dict_annotation:
        data = [dict_annotation(model_to_dict(o), o) for o in qset]
    else:
        data = [model_to_dict(o) for o in qset]
    
    result = {'rows': data,
              'page': page + 1,
              'records': recs,
              'total': total}
    
    return result

def get_jqgrid_subdata_json(request, ModelObj, baseFilter = None, methodType='POST'):
    """
        Returns the list of objects as JSON based on the request for use with subgrid. Subgrid doens't have search and sorting
        @param request: http request
        @param ModelObj: Object model reference. should inherit django.db.models.base.models.Model
        @param baseFilter:  django.db.models.query.QuerySet. A query set to filter the query of that model before doing the jqgrid filters
        @param methodType: POST or GET based on the configuration in the JQGrid. default is post
        
        @return: result as json containing rows, page, records, total
    """
    
    params = request.POST if methodType == 'POST' else 'GET'
    
    qset = ModelObj.objects
    
    if baseFilter:
        qset = qset.filter(baseFilter)
    
    recs = qset.count()
    
    log.debug("Query to jqgrid: %s", qset.query)
    
    data = [model_to_dict(d) for d in qset]
    
    result = data
    
    return result