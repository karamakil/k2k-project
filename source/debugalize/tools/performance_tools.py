'''
Created on Feb 26, 2015

@author: Shadi Moodad

Misc performance tools and decorators
'''
import time
import logging
from functools import wraps
from django import db

log = logging.getLogger(__name__)

    
def log_time(func):
    """
     Decotrator that logs the execution time of the given function as log.info
     
    """
    
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        before = time.time()
        
        fn_result = func(*args, **kwargs)
        
        log.info("Elapsed time to execute %s is %0.3fs", func.__name__, time.time() - before)
        
        return fn_result
    
    return func_wrapper
        

def log_time_queries(func):
    """
     Decorator that logs the time and total queries for the given function
    """
    
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        before = time.time()
        queriesBefore = len(db.connection.queries)
        
        fn_result = func(*args, **kwargs)
        
        log.info("Elapsed time to execute %s is %0.3fs using %s queries", func.__name__, time.time() - before, len(db.connection.queries) - queriesBefore)
        
        return fn_result
    
    return func_wrapper