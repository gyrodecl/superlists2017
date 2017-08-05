from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import unittest
import sys
import time

#ch17
from .server_tools import reset_database

# Ch. 20
import os
from datetime import datetime

SCREEN_DUMP_LOCATION = os.path.join (
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)
DEFAULT_WAIT = 5

#ch.10 Refactor Functional Tests into Many Files
class FunctionalTest(StaticLiveServerTestCase):
    
    #NOTE: notice the use of the 'return' inside the for loop
    # return, unlike a break, means that if 'liveserver' is in arg
    # it immediately exits the whole FUNCTION setUpClass.  whereas
    # break just exits the for loop and would continue the rest of the
    # function.  so this means if 'liveserver' is in arg, then
    # the normal super().setUpClass() is not run andthe
    # cls.server_url = cls.live_server_url is never run!
    # we call the liveserver approach with
    # $ python manage.py test functional_tests --liveserver=ec2-53-153.computer.amazonaws.com
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:  
            if 'liveserver' in arg:
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                # this line below is necessary again because we're using ec2 as our url
                # but the folder structure on the server has /tdd-lists-staging/
                # we don't want the full ec2 url using in our directory structure
                # the management commands like reset_database that our fabfile.py calls
                # need to know what the base directory is so it can locate manage.py,
                # and the base directory uses cls.server_host to find
                cls.server_host = 'tdd-lists-staging'  
                cls.against_staging = True
                return  
        super().setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url
    
    @classmethod
    def tearDownClass(cls):
        if not cls.against_staging:
        #if cls.server_url == cls.live_server_url:
            super().tearDownClass()
    
    def setUp(self):
        if self.against_staging:
            reset_database(self.server_host)
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()
    
    # helper function 1
    def _test_has_failed(self):
        # for 3.4. In 3.3, can just use self._outcomeForDoCleanups.success:
        for method, error in self._outcome.errors:
            if error:
                return True
        return False
    
    # helper function 2
    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)
    
    # helper function 3
    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)
    
    # helper function 3a.--generate unique filename identifier
    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )
     
    #helper method
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    
    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
    
    
    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was:\n{}'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
            )
        )
        
    # ch. 20
    def wait_for(self, function_with_assertion, timeout=DEFAULT_WAIT):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return function_with_assertion()
            except (AssertionError, WebDriverException):
                time.sleep(0.1)
        # one more try, which will raise any errors if they are outstanding
        return function_with_assertion()
    
    def wait_to_be_logged_in(self, email):
        self.wait_for_element_with_id('id_logout')  #4
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)
    
    def wait_to_be_logged_out(self, email):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
    


'''
#don't need this anymore since using django test runner
if __name__ == '__main__':
    unittest.main(warnings='ignore')
'''