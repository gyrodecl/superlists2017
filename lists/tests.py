from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest

from lists.views import home_page

class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/lists/')
        self.assertEqual(found.func, home_page)
    
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
