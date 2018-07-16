'''
Created on Jun 15, 2012

@author: Shadi Moodad
'''
from django.template.defaultfilters import register
from django.contrib.auth.models import User
import logging

log = logging.getLogger(__name__)

@register.filter
def readableUsername(user):
    '''
     Expect django.contrib.auth.models.User object
     if user.first_name + last_name isn't empty then it returns it else it returns user.username
    '''
    if user != None and isinstance(user, User):
        username = (user.first_name + " " + user.last_name).strip()
        if username != "":
            return username
        else:
            return user.username
    else:
        return user

@register.filter
def hasRole(user, role_name):
    log.debug("Checking role:%s for user: %s", role_name, readableUsername(user))
    if user != None and isinstance(user, User) and user.has_role(role_name):
        return True
    else:
        return False
    