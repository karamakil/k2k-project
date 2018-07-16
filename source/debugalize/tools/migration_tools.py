'''
Created on Feb 3, 2015

@author: Shadi Moodad
'''

from django.db import migrations
from django.core.management import call_command

def LoadFixture(fixture_name):
    def load_fixture_data(apps, schema_editor):
        call_command("loaddata", fixture_name)
        
    migrations.RunPython(load_fixture_data)    