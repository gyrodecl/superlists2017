from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
import unittest

class ItemFormTest(TestCase):
    
    @unittest.skip
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.fail(form.as_p())
        
    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
    
    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )
    
        
    
    
    
