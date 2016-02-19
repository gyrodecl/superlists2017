from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.utils.html import escape
from django.contrib.auth import get_user_model
User = get_user_model()

from lists.views import home_page, new_list, new_list2
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, EMPTY_ITEM_ERROR

import unittest
from unittest.mock import Mock, patch

class ListViewTest(TestCase):
    
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            '/lists/%d' % (list_.id,),
            data={'text': ''}
        )
    
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

    #adding new item to an existing List
    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()
        
        self.client.post(
            reverse('lists:view_list', args=(correct_list.id,)),
            data={'text': 'A new item for an existing list'}
        )
        
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
    
    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            reverse('lists:view_list', args=(correct_list.id,)),
            data={'text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, reverse('lists:view_list', args=(correct_list.id,)))

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d' % (list_.id,))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
    
    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_validation_errors_end_up_on_lists_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))
        
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            '/lists/%d' % (list1.id,),
            data={'text': 'textey'}
        )

        expected_error = escape("You've already got this in your list")
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.all().count(), 1)



class NewListViewIntegratedTest(TestCase):
    
    def test_saving_a_POST_request(self):
        response = self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )        
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
    
    
    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data = {'text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lists:view_list', args=(new_list.id,)))
        '''
        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'lists/home.html',
            {'text':  'A new list item'}
        )
        self.assertEqual(response.content.decode(), expected_html)
        '''
        
    #ch.10
    def test_invalid_input_does_not_create_list_or_items(self):
        response = self.client.post(reverse('lists:new_list'),
                                    data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)
        
        
    #ch.10
    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new',
                                        data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
    
    
    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new',
                                        data={'text':''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))
    
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new',
                                        data={'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)
    
    #Ch.19 this was mocked version---we're going to make things more isolated next
    #ch.19--now with mocks
    # mockList is a mock of the List class, while mock_list is an instance of the
    # mocked list class, a fake list object.
    '''
    @patch('lists.views.List')
    def test_list_owner_is_saved_if_user_is_authenticated(self, mockList):
        mock_list = List.objects.create()
        mock_list.save = Mock()
        mockList.return_value = mock_list
        request = HttpRequest()
        #request.user = User.objects.create()
        request.user = Mock()
        request.user.is_authenticated.return_value = True
        request.POST['text'] = 'new list item'
        
        def check_owner_assigned():
            self.assertEqual(mock_list.owner, request.user)
        mock_list.save.side_effect = check_owner_assigned  
            
        new_list(request)
        
        mock_list.save.assert_called_once_with()
    '''   
    
    '''
    #ch18 want to make sure that owner is associated with list
    def test_list_owner_is_saved_if_user_is_authenticated(self):
        request = HttpRequest()
        request.user = User.objects.create(email='a@b.com')
        request.POST['text'] = 'new list item'
        new_list(request)
        list_ = List.objects.first()
        self.assertEqual(list_.owner, request.user)
    '''
    
    # CH19 our old intgrated test is a sanity check
    #@unittest.skip
    def test_list_owner_is_saved_if_user_is_authenticated(self):
        request = HttpRequest()
        request.user = User.objects.create(email='a@b.com')
        request.POST['text'] = 'new list item'
        new_list2(request)
        list_ = List.objects.first()
        self.assertEqual(list_.owner, request.user)


# CH.19--now using the updated NewListForm
@patch('lists.views.NewListForm')  #1 mock out the form since we'll use it in all the tests
class NewListViewUnitTest(unittest.TestCase):  #2

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'  #3set up basic POST by hand rather than the overly integrated Django Test Client
        self.request.user = Mock()

    # First test, make sure view creates NewListForm with the correct constructor
    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        new_list2(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list2(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)    
    
    # when form is valid we want the view to redirect to the view
    # for that list, so we mock out the redirect function
    @patch('lists.views.redirect')  #1
    def test_redirects_to_form_returned_object_if_form_valid(
        self, mock_redirect, mockNewListForm  #2 patch decorators are innermost first, so method mocked before mockNewListForm
    ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True  #3

        response = new_list2(self.request)

        self.assertEqual(response, mock_redirect.return_value)  #4check that the response from the view is the result of the redirect function
        mock_redirect.assert_called_once_with(mock_form.save.return_value)  #
    
    # when form is invalid, want to make sure it renders the home page template
    @patch('lists.views.render')
    def test_renders_home_template_with_form_if_form_invalid(
        self, mock_render, mockNewListForm
    ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        
        response = new_list2(self.request)
        
        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'lists/home.html', {"form": mock_form}
        )
    
    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list2(self.request)
        self.assertFalse(mock_form.save.called)

#ch18
class MyListsTest(TestCase):
    
    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'lists/my_lists.html')
    
    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)
    


   
        
class HomePageTest(TestCase):
    maxDiff = None
    
    def test_home_page_renders_home_template(self):
        response = self.client.get(reverse('lists:home'))
        self.assertTemplateUsed(response, 'lists/home.html')
        
    def test_home_page_uses_item_form(self):
        response = self.client.get(reverse('lists:home'))
        self.assertIsInstance(response.context['form'], ItemForm)


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