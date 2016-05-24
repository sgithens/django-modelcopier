import datetime
from collections import defaultdict
from django.db.models import get_apps, get_models
from django.db.utils import IntegrityError, OperationalError, DatabaseError
from django.db.models.fields import TextField, CharField, DateField, DateTimeField
from django.db import connections
from django.db import models

class ModelCopier(object):
    """
    Utility to copy django items from one database to another.  The initial use
    case for this was to copy items from an Oracle Schema to a MySQL Schema.
    """
    def __init__(self, readdb, writedb):
        self.readdb = readdb
        self.writedb = writedb

    def out(self, text):
        print(text)

    def get_all_models(self):
        """
        Fetches all the models for all the apps in the currently active Django
        context we're in.
        """
        all_models = []
        for app in get_apps():
            all_models.extend(get_models(app))
        return all_models
        
    def turnoff_mysql_checks(self):
        print("Turning off mysql checks")
        write_cursor = connections[self.writedb].cursor()
        write_cursor.execute('SET autocommit=0')
        write_cursor.execute('SET unique_checks=0')
        write_cursor.execute('SET foreign_key_checks=0')
        write_cursor.execute('COMMIT')
        
    def copy_tables(self):
        self.turnoff_mysql_checks()
        tables = self.get_all_models()
        for table in tables:
            self.out("doing model:" + table.__name__)
            items = table.objects.using(self.readdb).all()
            self.out("%s : Need to convert %s items" % (table.__name__, items.count(),))
            for item in items:
                # self.scrub_model_instance(item)
                try:#
                    item.save(using=self.writedb)
                except IntegrityError as e:
                    print "Error copying %s %s" % (table.__name__, item.pk,)
                    raise e

    def scrub_model_instance(self, item):
        "TODO: Put in a utility module."
        phi_safe_fields = self.phi_safe[item._meta.model_name]
        for f in item._meta.fields:
            if f.name in phi_safe_fields:
                continue
            if isinstance(f, TextField) or isinstance(f, CharField):
                setattr(item, f.name, '')
            elif isinstance(f, DateField):
                year_value = getattr(item, f.name)
                if year_value != None: 
                    year_value = datetime.date(year_value.year, 1, 1)
                setattr(item, f.name, year_value)
            elif isinstance(f, DateTimeField):
                year_value = getattr(item, f.name)
                if year_value != None: 
                    year_value = datetime.datetime(year_value.year, 1, 1)
                setattr(item, f.name, year_value)
            else:
                pass
