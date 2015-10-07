from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List

class ListViewTest(TestCase):
    def test_displays_only_items_for_that_list(self):
        correct_list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list_)
        Item.objects.create(text='itemey 2', list=correct_list_)
        other_list_ = List.objects.create()
        Item.objects.create(text='other list item 1',list=other_list_)
        Item.objects.create(text='other list item 2', list=other_list_)
    
        response = self.client.get(reverse('lists:view_list', args=(correct_list_.id,)))
        
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_uses_list_template(self):
        new_list = List.objects.create()
        response = self.client.get(reverse('lists:view_list', args=(new_list.id,)))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_passes_correct_list_to_template(self):
        correct_list_ = List.objects.create()
        other_list_ = List.objects.create()
        
        response = self.client.get(reverse('lists:view_list', args=(correct_list_.id,)))
        
        self.assertEqual(response.context['list'], correct_list_)

class NewListTest(TestCase):
    
    def test_saving_a_POST_request(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )        
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
    
    
    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data = {'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lists:view_list', args=(new_list.id,)))
        '''
        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'lists/home.html',
            {'new_item_text':  'A new list item'}
        )
        self.assertEqual(response.content.decode(), expected_html)
        '''
        
    #ch.10
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new',
                                        data={'item_text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
        
    #ch.10
    def test_invalid_input_does_not_create_list_or_items(self):
        response = self.client.post(reverse('lists:new_list'),
                                    data={'item_text':''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)
    
        
    
#adding new item to an existing test
class NewItemTest(TestCase):
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()
        
        self.client.post(
            reverse('lists:add_item_to_list', args=(correct_list.id,)),
            data={'item_text': 'A new item for an existing list'}
        )
        
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
    
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            reverse('lists:add_item_to_list', args=(correct_list.id,)),
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, reverse('lists:view_list', args=(correct_list.id,)))


class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/lists/')
        self.assertEqual(found.func, home_page)
    
    #this we should just check if use the right template
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('lists/home.html')
        self.assertEqual(response.content.decode(), expected_html)
        '''
        self.assertIn(b'<html>', response.content)
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertIn(b'</html>', response.content)
        '''

    '''
    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(),0)
    '''
    
    '''
    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
    
        request = HttpRequest()
        response = home_page(request)
        
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())
    '''