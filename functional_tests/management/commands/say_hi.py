from django.core.management.base import BaseCommand

'''
Call this method with:
$ python manage.py say_hi "name here"  OR
$ python manage.py say_hi name=namehere 
'''

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('name')
    
    def handle(self, *args, **options):
        name_to_send = options['name']
        self.stdout.write("hi there everyone and especially %s" % name_to_send)
    
