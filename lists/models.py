from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

class List(models.Model):

    def get_absolute_url(self):
        return reverse('lists:view_list', args=[self.id])
    

class Item(models.Model):
    text = models.TextField(default='',blank=False)
    list = models.ForeignKey(List, default=None)
    
    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ('id', )
        unique_together = ('list','text')