from django.db import models

class List(models.Model):
    pass

class Item(models.Model):
    text = models.CharField(max_length=200, default='')
    list = models.ForeignKey(List, default=None)



